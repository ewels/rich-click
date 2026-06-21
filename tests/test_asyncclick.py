"""
Tests proving rich-click supports asyncclick.

asyncclick (https://github.com/python-trio/asyncclick) is a fork of click whose
command machinery (``main``/``invoke``/``make_context``/``scope``) is async. Its
``Command``/``Group``/``Option``/``Argument``/``Context`` are a *parallel* class
tree that does not subclass click's.

Two integration paths are exercised:

1. The ``RichAsync*`` classes in ``rich_click.rich_async_command``, which compose
   the baseless ``Rich*Mixin`` classes onto asyncclick's bases and add an async
   ``main`` that routes errors through rich-click's formatter.
2. ``patch(module=asyncclick)``, which swaps asyncclick's classes for the
   ``RichAsync*`` ones so a plain ``@asyncclick.command`` CLI gets Rich help and
   Rich error panels with no rich-specific code.
"""

import asyncio
import os
import subprocess
import sys
from inspect import cleandoc
from pathlib import Path

import pytest


asyncclick = pytest.importorskip("asyncclick")
asyncclick_testing = pytest.importorskip("asyncclick.testing")

from rich_click._click_types_cache import is_argument, is_group, is_option  # noqa: E402
from rich_click.rich_async_command import RichAsyncCommand, RichAsyncContext, RichAsyncGroup  # noqa: E402


# Horizontal box-drawing character that Rich uses to draw panel borders. Defined as
# an escape so this source file stays ASCII-only.
BOX_BORDER = "\u2500"


def _build_cli():
    seen = {}

    @asyncclick.group(cls=RichAsyncGroup)
    @asyncclick.option("--token", help="Shared token.")
    @asyncclick.pass_context
    async def cli(ctx, token):
        # Async group callback that builds shared state under a single loop.
        await asyncio.sleep(0)
        ctx.obj = {"token": token, "loop": id(asyncio.get_running_loop())}

    @asyncclick.command(cls=RichAsyncCommand)
    @asyncclick.argument("name")
    @asyncclick.option("--count", default=1, help="How many greetings.")
    @asyncclick.pass_context
    async def greet(ctx, name, count):
        await asyncio.sleep(0)
        seen["obj"] = ctx.obj
        seen["loop"] = id(asyncio.get_running_loop())
        for _ in range(count):
            asyncclick.echo(f"Hello {name}")

    cli.add_command(greet)
    return cli, greet, seen


def _invoke(cli, args):
    runner = asyncclick_testing.CliRunner()
    return asyncio.run(runner.invoke(cli, args))


def test_async_classes_have_expected_mro():
    # The async classes are mixin-built and an asyncclick subclass, with an async main.
    assert issubclass(RichAsyncGroup, asyncclick.Group)
    assert issubclass(RichAsyncCommand, asyncclick.Command)
    assert issubclass(RichAsyncContext, asyncclick.Context)
    assert asyncio.iscoroutinefunction(RichAsyncCommand.main)


def test_async_types_are_detected():
    cli, greet, _ = _build_cli()
    assert is_group(cli)
    assert is_option(greet.params[1])  # --count
    assert is_argument(greet.params[0])  # NAME


def test_group_help_renders_rich_panels():
    cli, _, _ = _build_cli()
    result = _invoke(cli, ["--help"])
    assert result.exit_code == 0
    # Rich renders bordered panels (box-drawing chars) rather than click's plain help.
    assert BOX_BORDER in result.output
    assert "Options" in result.output
    assert "Commands" in result.output
    assert "greet" in result.output


def test_subcommand_help_classifies_arguments_and_options():
    cli, _, _ = _build_cli()

    # Argument appears as a positional in the usage metavar, never as an option.
    result = _invoke(cli, ["greet", "--help"])
    assert result.exit_code == 0
    assert BOX_BORDER in result.output
    assert "NAME" in result.output  # positional metavar in the usage line
    assert "Options" in result.output
    assert "--count" in result.output

    # When arguments are shown in their own panel, the positional is classified as
    # an argument (proving is_argument()/is_option() work on asyncclick's types).
    import rich_click.rich_click as rc

    rc.SHOW_ARGUMENTS = True
    rc.GROUP_ARGUMENTS_WITH_OPTIONS = False
    try:
        cli2, _, _ = _build_cli()
        result2 = _invoke(cli2, ["greet", "--help"])
    finally:
        rc.SHOW_ARGUMENTS = False
        rc.GROUP_ARGUMENTS_WITH_OPTIONS = True
    assert result2.exit_code == 0
    assert "Arguments" in result2.output


def test_async_execution_shares_ctx_obj_under_one_loop():
    cli, _, seen = _build_cli()
    result = _invoke(cli, ["--token", "abc", "greet", "world", "--count", "2"])
    assert result.exit_code == 0
    assert result.output.count("Hello world") == 2
    # Shared async state built in the group callback is visible to the subcommand,
    # and both ran under the same event loop.
    assert seen["obj"]["token"] == "abc"
    assert seen["obj"]["loop"] == seen["loop"]


def test_async_usage_error_renders_rich_panel():
    cli, _, _ = _build_cli()
    # Missing required argument is a usage error; the async main must route it
    # through rich-click's formatter rather than asyncclick's plain output.
    result = _invoke(cli, ["greet"])
    assert result.exit_code == 2
    assert BOX_BORDER in result.output
    assert "Error" in result.output
    assert "Missing argument" in result.output


# The patch() test runs in a subprocess because patch(module=asyncclick) mutates the
# asyncclick module globally and is not reversible. A subprocess keeps that mutation
# out of the rest of the suite.
PATCH_SCRIPT = '''
import asyncclick
from rich_click.patch import patch

patch(module=asyncclick)

@asyncclick.group()
@asyncclick.option("--token", help="Shared token.")
async def cli(token):
    """A vanilla async CLI patched by rich-click."""

@cli.command()
@asyncclick.argument("name")
async def greet(name):
    """Greet NAME asynchronously."""
    asyncclick.echo("Hello " + name)

if __name__ == "__main__":
    cli()
'''


def _run_patch_script(tmp_path: Path, args):
    script = tmp_path / "patched_cli.py"
    script.write_text(cleandoc(PATCH_SCRIPT))
    env = {**os.environ, "TERMINAL_WIDTH": "80", "FORCE_COLOR": "0", "NO_COLOR": "1"}
    return subprocess.run(
        [sys.executable, str(script), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )


def test_patch_module_renders_rich_help(tmp_path):
    res = _run_patch_script(tmp_path, ["--help"])
    out = res.stdout.decode()
    assert res.returncode == 0
    assert BOX_BORDER in out  # Rich panels, not plain asyncclick help
    assert "Commands" in out
    assert "greet" in out


def test_patch_module_renders_rich_error_panel(tmp_path):
    res = _run_patch_script(tmp_path, ["greet"])
    out = res.stdout.decode()
    assert res.returncode == 2
    assert BOX_BORDER in out
    assert "Missing argument" in out


def test_patch_module_executes_async_command(tmp_path):
    res = _run_patch_script(tmp_path, ["greet", "world"])
    out = res.stdout.decode()
    assert res.returncode == 0
    assert "Hello world" in out
