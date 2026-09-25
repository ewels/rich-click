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
import errno
import os
import subprocess
import sys
from inspect import cleandoc
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from unittest.mock import Mock

import pytest
from inline_snapshot import snapshot


asyncclick = pytest.importorskip("asyncclick")
asyncclick_testing = pytest.importorskip("asyncclick.testing")

from rich_click._click_types_cache import get_command_decorator, is_argument, is_group, is_option  # noqa: E402
from rich_click.patch import _patch_async_module, patch  # noqa: E402
from rich_click.rich_async_command import (  # noqa: E402
    RichAsyncCommand,
    RichAsyncCommandCollection,
    RichAsyncContext,
    RichAsyncGroup,
)


_ORIGINAL_ASYNCCLICK_COMMAND = asyncclick.command


def _build_cli() -> tuple[Any, Any, dict[str, Any]]:
    seen: dict[str, Any] = {}

    @asyncclick.group(cls=RichAsyncGroup)
    @asyncclick.option("--token", help="Shared token.")
    @asyncclick.pass_context
    async def cli(ctx: Any, token: Any) -> None:
        # Async group callback that builds shared state under a single loop.
        await asyncio.sleep(0)
        ctx.obj = {"token": token, "loop": id(asyncio.get_running_loop())}

    @asyncclick.command(cls=RichAsyncCommand)
    @asyncclick.argument("name")
    @asyncclick.option("--count", default=1, help="How many greetings.")
    @asyncclick.pass_context
    async def greet(ctx: Any, name: str, count: int) -> None:
        await asyncio.sleep(0)
        seen["obj"] = ctx.obj
        seen["loop"] = id(asyncio.get_running_loop())
        for _ in range(count):
            asyncclick.echo(f"Hello {name}")

    cli.add_command(greet)
    return cli, greet, seen


def _invoke(cli: Any, args: list[str]) -> Any:
    runner = asyncclick_testing.CliRunner()
    return asyncio.run(runner.invoke(cli, args))


def _module_proxy(command_cls: type[Any] = asyncclick.Command) -> SimpleNamespace:
    return SimpleNamespace(
        __name__="asyncclick_proxy",
        Argument=asyncclick.Argument,
        Command=command_cls,
        CommandCollection=asyncclick.CommandCollection,
        Context=asyncclick.Context,
        Group=asyncclick.Group,
        Option=asyncclick.Option,
        Parameter=asyncclick.Parameter,
        command=asyncclick.command,
        core=SimpleNamespace(
            Command=command_cls,
            CommandCollection=asyncclick.CommandCollection,
            Group=asyncclick.Group,
        ),
        group=asyncclick.group,
    )


def _set_make_context_error(
    monkeypatch: pytest.MonkeyPatch,
    command: RichAsyncCommand,
    error: BaseException,
) -> None:
    async def make_context(*args: Any, **kwargs: Any) -> Any:
        raise error

    monkeypatch.setattr(command, "make_context", make_context)


def test_async_classes_have_expected_mro() -> None:
    # The async classes are mixin-built and an asyncclick subclass, with an async main.
    assert issubclass(RichAsyncGroup, asyncclick.Group)
    assert issubclass(RichAsyncCommand, asyncclick.Command)
    assert issubclass(RichAsyncContext, asyncclick.Context)
    assert asyncio.iscoroutinefunction(RichAsyncCommand.main)


def test_async_classes_are_available_from_top_level_package() -> None:
    import rich_click

    assert rich_click.RichAsyncCommand is RichAsyncCommand
    assert rich_click.RichAsyncCommandCollection is RichAsyncCommandCollection
    assert rich_click.RichAsyncContext is RichAsyncContext
    assert rich_click.RichAsyncGroup is RichAsyncGroup


def test_async_classes_use_asyncclick_command_decorator() -> None:
    assert get_command_decorator(RichAsyncCommand) is _ORIGINAL_ASYNCCLICK_COMMAND
    assert get_command_decorator(RichAsyncGroup) is _ORIGINAL_ASYNCCLICK_COMMAND


def test_top_level_package_does_not_eagerly_import_asyncclick() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys; import rich_click; assert 'asyncclick' not in sys.modules",
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_async_group_subclasses_create_matching_subgroups() -> None:
    class CustomAsyncGroup(RichAsyncGroup):
        pass

    @asyncclick.group(cls=CustomAsyncGroup)
    async def cli() -> None:
        pass

    @cli.group
    async def nested() -> None:
        pass

    assert type(nested) is CustomAsyncGroup


def test_async_command_collection_renders_rich_help() -> None:
    @asyncclick.group(cls=RichAsyncGroup)
    async def source() -> None:
        pass

    @source.command
    async def status() -> None:
        """Show the current status."""

    cli = RichAsyncCommandCollection(name="cli", sources=[source])
    result = _invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ status                Show the current status.                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")
    assert result.stderr == ""


def test_async_types_are_detected() -> None:
    cli, greet, _ = _build_cli()
    assert is_group(cli)
    assert is_option(greet.params[1])  # --count
    assert is_argument(greet.params[0])  # NAME


def test_group_help_renders_rich_panels() -> None:
    cli, _, _ = _build_cli()
    result = _invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --token  TEXT  Shared token.                                                                     │
│ --help         Show this message and exit.                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ greet                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")
    assert result.stderr == snapshot("")


def test_subcommand_help_classifies_arguments_and_options(monkeypatch: pytest.MonkeyPatch) -> None:
    cli, _, _ = _build_cli()

    # Argument appears as a positional in the usage metavar, never as an option.
    result = _invoke(cli, ["greet", "--help"])
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli greet [OPTIONS] NAME                                                                    \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --count  INTEGER  How many greetings.                                                            │
│ --help            Show this message and exit.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")
    assert result.stderr == snapshot("")

    # When arguments are shown in their own panel, the positional is classified as
    # an argument (proving is_argument()/is_option() work on asyncclick's types).
    import rich_click.rich_click as rc

    monkeypatch.setattr(rc, "SHOW_ARGUMENTS", True)
    cli2, _, _ = _build_cli()
    result2 = _invoke(cli2, ["greet", "--help"])
    assert result2.exit_code == 0
    assert result2.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli greet [OPTIONS] NAME                                                                    \n\
                                                                                                    \n\
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────╮
│ *  NAME  TEXT  [required]                                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --count  INTEGER  How many greetings.                                                            │
│ --help            Show this message and exit.                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")
    assert result2.stderr == snapshot("")


def test_async_execution_shares_ctx_obj_under_one_loop() -> None:
    cli, _, seen = _build_cli()
    result = _invoke(cli, ["--token", "abc", "greet", "world", "--count", "2"])
    assert result.exit_code == 0
    assert result.output.count("Hello world") == 2
    # Shared async state built in the group callback is visible to the subcommand,
    # and both ran under the same event loop.
    assert seen["obj"]["token"] == "abc"
    assert seen["obj"]["loop"] == seen["loop"]


def test_async_main_expands_windows_args_and_returns_value(monkeypatch: pytest.MonkeyPatch) -> None:
    async def callback() -> int:
        return 7

    command = RichAsyncCommand("cli", callback=callback)
    expand_args = Mock(return_value=[])
    detect_program_name = Mock(return_value="detected-cli")
    monkeypatch.setattr(os, "name", "nt")
    monkeypatch.setattr(sys, "argv", ["cli", "*.txt"])
    monkeypatch.setattr(asyncclick.utils, "_expand_args", expand_args)
    monkeypatch.setattr(asyncclick.utils, "_detect_program_name", detect_program_name)

    assert asyncio.run(command.main(standalone_mode=False)) == 7
    expand_args.assert_called_once_with(["*.txt"])
    detect_program_name.assert_called_once_with()


def test_async_main_success_exits_in_standalone_mode() -> None:
    async def callback() -> None:
        pass

    command = RichAsyncCommand("cli", callback=callback)

    with pytest.raises(SystemExit) as exc_info:
        asyncio.run(command.main([], prog_name="cli"))

    assert exc_info.value.code == 0


def test_async_to_info_dict_includes_rich_metadata() -> None:
    command = RichAsyncCommand("cli", aliases=["c"])
    panel = Mock()
    panel.to_info_dict.return_value = {"name": "Panel"}
    command.panels = [panel]
    ctx = RichAsyncContext(command)

    info = asyncio.run(command.to_info_dict(ctx))

    assert info["panels"] == [{"name": "Panel"}]
    assert info["aliases"] == ["c"]
    panel.to_info_dict.assert_called_once_with(ctx)


def test_async_main_reraises_click_exception_when_not_standalone(monkeypatch: pytest.MonkeyPatch) -> None:
    command = RichAsyncCommand("cli")
    error = asyncclick.UsageError("bad input")
    _set_make_context_error(monkeypatch, command, error)

    with pytest.raises(asyncclick.UsageError, match="bad input"):
        asyncio.run(command.main([], prog_name="cli", standalone_mode=False))


def test_async_no_args_help_uses_plain_message(capsys: pytest.CaptureFixture[str]) -> None:
    command = RichAsyncGroup("cli", no_args_is_help=True)

    with pytest.raises(SystemExit) as exc_info:
        asyncio.run(command.main([], prog_name="cli"))

    assert exc_info.value.code == 2
    assert "Usage: cli [OPTIONS] COMMAND [ARGS]..." in capsys.readouterr().out


def test_async_main_handles_broken_pipe(monkeypatch: pytest.MonkeyPatch) -> None:
    command = RichAsyncCommand("cli")
    _set_make_context_error(monkeypatch, command, OSError(errno.EPIPE, "broken pipe"))
    monkeypatch.setattr(asyncclick.utils, "PacifyFlushWrapper", lambda stream: stream)

    with pytest.raises(SystemExit) as exc_info:
        asyncio.run(command.main([], prog_name="cli"))

    assert exc_info.value.code == 1


def test_async_main_reraises_other_os_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    command = RichAsyncCommand("cli")
    _set_make_context_error(monkeypatch, command, OSError(errno.EACCES, "denied"))

    with pytest.raises(OSError, match="denied"):
        asyncio.run(command.main([], prog_name="cli"))


def test_async_main_handles_explicit_exit(monkeypatch: pytest.MonkeyPatch) -> None:
    command = RichAsyncCommand("cli")
    _set_make_context_error(monkeypatch, command, asyncclick.exceptions.Exit(7))

    assert asyncio.run(command.main([], prog_name="cli", standalone_mode=False)) == 7

    with pytest.raises(SystemExit) as exc_info:
        asyncio.run(command.main([], prog_name="cli"))

    assert exc_info.value.code == 7


def test_async_main_handles_abort(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    command = RichAsyncCommand("cli")
    _set_make_context_error(monkeypatch, command, asyncclick.Abort())

    with pytest.raises(asyncclick.Abort):
        asyncio.run(command.main([], prog_name="cli", standalone_mode=False))

    with pytest.raises(SystemExit) as exc_info:
        asyncio.run(command.main([], prog_name="cli"))

    assert exc_info.value.code == 1
    assert "Aborted" in capsys.readouterr().err


def test_async_main_abort_falls_back_to_echo(monkeypatch: pytest.MonkeyPatch) -> None:
    command = RichAsyncCommand("cli")
    _set_make_context_error(monkeypatch, command, asyncclick.Abort())
    echo = Mock()
    monkeypatch.setattr(command, "_error_formatter", Mock(side_effect=RuntimeError))
    monkeypatch.setattr(asyncclick, "echo", echo)

    with pytest.raises(SystemExit) as exc_info:
        asyncio.run(command.main([], prog_name="cli"))

    assert exc_info.value.code == 1
    echo.assert_called_once_with("Aborted!", file=sys.stderr)


def test_async_main_converts_eof_to_abort(monkeypatch: pytest.MonkeyPatch) -> None:
    command = RichAsyncCommand("cli")
    _set_make_context_error(monkeypatch, command, EOFError())

    with pytest.raises(SystemExit) as exc_info:
        asyncio.run(command.main([], prog_name="cli"))

    assert exc_info.value.code == 1


def test_async_usage_error_renders_rich_panel() -> None:
    cli, _, _ = _build_cli()
    # Missing required argument is a usage error; the async main must route it
    # through rich-click's formatter rather than asyncclick's plain output.
    result = _invoke(cli, ["greet"])
    assert result.exit_code == 2
    assert result.stdout == snapshot("")
    assert result.stderr == snapshot("""\
                                                                                                    \n\
 Usage: cli greet [OPTIONS] NAME                                                                    \n\
                                                                                                    \n\
 Try 'cli greet --help' for help                                                                    \n\
╭─ Error ──────────────────────────────────────────────────────────────────────────────────────────╮
│ Missing argument 'NAME'.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
""")


def test_async_command_row_override_is_used() -> None:
    class CustomRowCommand(RichAsyncCommand):
        def get_rich_table_row(self, *args: Any, **kwargs: Any) -> list[Any | None]:
            return ["custom-row", None, "Rendered by the override."]

    @asyncclick.group(cls=RichAsyncGroup)
    async def cli() -> None:
        pass

    @cli.command(cls=CustomRowCommand)
    async def original_name() -> None:
        """This help should be replaced."""

    result = _invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ custom-row                    Rendered by the override.                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")
    assert result.stderr == snapshot("")


# The patch() test runs in a subprocess because patch(module=asyncclick) mutates the
# asyncclick module globally and is not reversible. A subprocess keeps that mutation
# out of the rest of the suite.
PATCH_SCRIPT = '''
import asyncclick
from rich_click import command_panel, option_panel, rich_config
from rich_click.patch import patch
from rich_click.rich_help_configuration import RichHelpConfiguration

patch(module=asyncclick)

@asyncclick.group
@rich_config(help_config=RichHelpConfiguration(options_panel_title="MY OPTIONS"))
@option_panel("Credentials", options=["--token"])
@command_panel("Utilities", commands=["status"])
@asyncclick.option("--token", help="Shared token.")
async def cli(token):
    """A vanilla async CLI patched by rich-click."""

@cli.command
async def status():
    """Show status."""

@cli.command(panel="Custom Panel", aliases=["g"])
@asyncclick.argument("name")
async def greet(name):
    """Greet NAME asynchronously."""
    asyncclick.echo("Hello " + name)

if __name__ == "__main__":
    cli()
'''

OUTER_METADATA_SCRIPT = '''
import asyncclick
from rich_click import command_panel, option_panel, rich_config
from rich_click.patch import patch
from rich_click.rich_help_configuration import RichHelpConfiguration

patch(module=asyncclick)

@rich_config(help_config=RichHelpConfiguration(options_panel_title="OUTER OPTIONS"))
@option_panel("Outer Credentials", options=["--token"])
@command_panel("Outer Commands", commands=["status"])
@asyncclick.group
@asyncclick.option("--token", help="Shared token.")
async def cli(token):
    """Metadata decorators applied above the patched group."""

@cli.command
async def status():
    """Show status."""

if __name__ == "__main__":
    cli()
'''


def _run_script(
    tmp_path: Path,
    source: str,
    args: list[str],
    filename: str = "patched_cli.py",
) -> subprocess.CompletedProcess[bytes]:
    script = tmp_path / filename
    script.write_text(cleandoc(source))
    env = {**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "0", "NO_COLOR": "1"}
    return subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True,
        env=env,
    )


def _run_patch_script(tmp_path: Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return _run_script(tmp_path, PATCH_SCRIPT, args)


def test_patch_module_renders_rich_help(tmp_path: Path) -> None:
    res = _run_patch_script(tmp_path, ["--help"])
    assert res.returncode == 0
    assert res.stdout.decode() == snapshot("""\
                                                                                                    \n\
 Usage: patched_cli.py [OPTIONS] COMMAND [ARGS]...                                                  \n\
                                                                                                    \n\
 A vanilla async CLI patched by rich-click.                                                         \n\
                                                                                                    \n\
╭─ Credentials ────────────────────────────────────────────────────────────────────────────────────╮
│ --token  TEXT  Shared token.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Utilities ──────────────────────────────────────────────────────────────────────────────────────╮
│ status                             Show status.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom Panel ───────────────────────────────────────────────────────────────────────────────────╮
│ greet            g       Greet NAME asynchronously.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ MY OPTIONS ─────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")
    assert res.stderr.decode() == snapshot("")


def test_patch_module_applies_metadata_above_group(tmp_path: Path) -> None:
    res = _run_script(tmp_path, OUTER_METADATA_SCRIPT, ["--help"], "outer_metadata.py")
    assert res.returncode == 0
    assert res.stdout.decode() == snapshot("""\
                                                                                                    \n\
 Usage: outer_metadata.py [OPTIONS] COMMAND [ARGS]...                                               \n\
                                                                                                    \n\
 Metadata decorators applied above the patched group.                                               \n\
                                                                                                    \n\
╭─ Outer Commands ─────────────────────────────────────────────────────────────────────────────────╮
│ status                             Show status.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Outer Credentials ──────────────────────────────────────────────────────────────────────────────╮
│ --token  TEXT  Shared token.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ OUTER OPTIONS ──────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")
    assert res.stderr.decode() == snapshot("")


def test_patch_module_renders_rich_error_panel(tmp_path: Path) -> None:
    res = _run_patch_script(tmp_path, ["greet"])
    assert res.returncode == 2
    assert res.stdout.decode() == snapshot("")
    assert res.stderr.decode() == snapshot("""\
                                                                                                    \n\
 Usage: patched_cli.py greet [OPTIONS] NAME                                                         \n\
                                                                                                    \n\
 Try 'patched_cli.py greet --help' for help                                                         \n\
╭─ Error ──────────────────────────────────────────────────────────────────────────────────────────╮
│ Missing argument 'NAME'.                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
""")


def test_patch_module_executes_async_command(tmp_path: Path) -> None:
    res = _run_patch_script(tmp_path, ["greet", "world"])
    assert res.returncode == 0
    assert res.stdout.decode() == snapshot("Hello world\n")
    assert res.stderr.decode() == snapshot("")


def test_patch_module_supports_bare_command(tmp_path: Path) -> None:
    script = '''
import asyncclick
from rich_click.patch import patch

patch(module=asyncclick)

@asyncclick.command
async def cli():
    """A bare patched command."""

if __name__ == "__main__":
    cli()
'''
    path = tmp_path / "bare_command.py"
    path.write_text(cleandoc(script))
    res = subprocess.run(
        [sys.executable, str(path), "--help"],
        capture_output=True,
        env={**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "0", "NO_COLOR": "1"},
    )
    assert res.returncode == 0
    assert res.stdout.decode() == snapshot("""\
                                                                                                    \n\
 Usage: bare_command.py [OPTIONS]                                                                   \n\
                                                                                                    \n\
 A bare patched command.                                                                            \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")
    assert res.stderr.decode() == snapshot("")


def test_async_help_to_stderr() -> None:
    @asyncclick.command(cls=RichAsyncCommand, context_settings={"help_to_stderr": True})
    async def cli() -> None:
        """An async command with help on stderr."""

    result = _invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert result.stdout == snapshot("")
    assert result.stderr == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 An async command with help on stderr.                                                              \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


def test_patch_async_module_rejects_sync_command() -> None:
    import click

    with pytest.raises(TypeError, match="only supports asynchronous click forks"):
        _patch_async_module(_module_proxy(click.Command))


@pytest.mark.parametrize("module", ["asyncclick", SimpleNamespace(__name__="incomplete")])
def test_patch_rejects_invalid_async_modules(module: Any) -> None:
    with pytest.raises(TypeError, match="only supports asynchronous click forks"):
        patch(module=module)


def test_patch_rejects_sync_module_without_patching_click() -> None:
    import click

    original_command = click.command

    with pytest.raises(TypeError, match="For synchronous click, call patch\\(\\)"):
        patch(module=click)

    assert click.command is original_command


def test_patch_async_module_in_process() -> None:
    import rich_click.rich_command

    module = _module_proxy()
    rich_config = Mock()
    original_overrides_guard = rich_click.rich_command.OVERRIDES_GUARD

    patch(module=module, rich_config=rich_config)

    assert module.Command is RichAsyncCommand
    assert module.Group is RichAsyncGroup
    assert module.CommandCollection is RichAsyncCommandCollection
    assert module.core.Command is RichAsyncCommand
    assert module.core.Group is RichAsyncGroup
    assert module.core.CommandCollection is RichAsyncCommandCollection

    @module.command
    async def command() -> None:
        pass

    @module.group
    async def group() -> None:
        pass

    assert isinstance(command, RichAsyncCommand)
    assert isinstance(group, RichAsyncGroup)
    assert rich_click.rich_command.OVERRIDES_GUARD is original_overrides_guard
    rich_config.dump_to_globals.assert_called_once_with()


def test_patched_async_decorators_match_asyncclick_naming_and_params() -> None:
    module = _module_proxy()
    patch(module=module)

    @module.group
    async def cli() -> None:
        pass

    @cli.command
    async def status_cmd() -> None:
        pass

    @cli.group
    async def data_group() -> None:
        pass

    @data_group.command
    async def init_data_command() -> None:
        pass

    @cli.command(params=[asyncclick.Option(["--flag"], is_flag=True)])
    async def explicit_params() -> None:
        pass

    @module.command
    async def solo_cmd() -> None:
        pass

    assert sorted(cli.commands) == ["data", "explicit-params", "status"]
    assert sorted(data_group.commands) == ["init-data"]
    assert solo_cmd.name == "solo"
