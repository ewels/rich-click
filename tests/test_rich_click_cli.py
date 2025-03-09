# ruff: noqa: D101,D103,D401
import os
import subprocess
import sys
from inspect import cleandoc
from pathlib import Path
from typing import Callable, List

import pytest
from click.testing import CliRunner
from pytest import MonkeyPatch
from typing_extensions import Protocol

import rich_click.rich_click as rc
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_8X
from rich_click.cli import main
from rich_click.rich_context import RichContext
from tests.conftest import AssertStr


@pytest.fixture(autouse=True)
def default_config(initialize_rich_click: None) -> None:
    # Default config settings from https://github.com/Textualize/rich/blob/master/tests/render.py
    rc.WIDTH = 100
    rc.COLOR_SYSTEM = None
    rc.FORCE_TERMINAL = True


class WriteScript(Protocol):
    def __call__(self, script: str, module_name: str = "mymodule.py") -> Path:
        """Write a script to a directory."""
        ...


@pytest.fixture
def mock_script_writer(tmp_path: Path, monkeypatch: MonkeyPatch) -> WriteScript:
    def write_script(script: str, module_name: str = "mymodule.py") -> Path:
        path = tmp_path / "scripts"
        path.mkdir()
        py_script = path / module_name
        py_script.write_text(cleandoc(script))

        monkeypatch.setattr(sys, "path", [path.as_posix(), *sys.path.copy()])
        monkeypatch.setitem(os.environ, "PYTHONPATH", path.as_posix())
        monkeypatch.setattr(RichContext, "command_path", "mymodule")
        return path

    return write_script


@pytest.fixture
def simple_script(mock_script_writer: WriteScript) -> Path:
    return mock_script_writer(
        '''
        import click

        # Test if robust to subclassing
        class CustomClickCommand(click.Command):
            pass

        @click.command(cls=CustomClickCommand)
        def cli():
            """My help text"""
            print('Hello, world!')
        '''
    )


@pytest.mark.parametrize(
    "command",
    [
        ["mymodule:cli", "--help"],
        ["--", "mymodule:cli", "--help"],
    ],
)
def test_simple_rich_click_cli(simple_script: Path, assert_str: AssertStr, command: List[str]) -> None:
    res = subprocess.run(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "False"},
    )
    assert res.returncode == 0

    if CLICK_IS_BEFORE_VERSION_8X:
        usage = "mymodule"
    else:
        usage = "python -m src.rich_click.mymodule"

    expected_output = f"""
 Usage: {usage} [OPTIONS]

 My help text

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""

    assert_str(actual=res.stdout.decode(), expectation=expected_output)


@pytest.mark.parametrize(
    "command",
    [
        ["mymodule:cli"],
        ["--", "mymodule:cli"],
        ["mymodule:cli", "--"],
    ],
)
def test_simple_rich_click_cli_execute_command(
    simple_script: Path, cli_runner: CliRunner, assert_str: AssertStr, command: List[str]
) -> None:
    res = cli_runner.invoke(main, command)

    assert res.exit_code == 0
    assert res.stdout == "Hello, world!\n"

    # Throughout the rest of this test module,
    # to avoid side effects and to test and uncover potential issues with lazy-loading,
    # we need to use subprocess.run() instead of cli_runner.invoke().

    subprocess_res = subprocess.run(
        [sys.executable, "-m", "src.rich_click", *command],
        stdout=subprocess.PIPE,
        env={**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "False"},
    )
    assert subprocess_res.returncode == 0

    assert subprocess_res.stdout.decode() == "Hello, world!\n"


def test_custom_config_rich_click_cli(simple_script: Path, assert_str: AssertStr) -> None:
    res = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.rich_click",
            "--rich-config",
            '{"options_panel_title": "Custom Name"}',
            "mymodule:cli",
            "--help",
        ],
        stdout=subprocess.PIPE,
        env={**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "False"},
    )
    assert res.returncode == 0

    if CLICK_IS_BEFORE_VERSION_8X:
        usage = "mymodule"
    else:
        usage = "python -m src.rich_click.mymodule"

    expected_output = f"""
 Usage: {usage} [OPTIONS]

 My help text

╭─ Custom Name ────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""

    assert_str(actual=res.stdout.decode(), expectation=expected_output)


def test_override_click_command(mock_script_writer: Callable[[str], Path], assert_str: AssertStr) -> None:
    mock_script_writer(
        '''
        import click

        class OverrideCommand(click.Command):
            def format_usage(self, ctx, formatter):
                print('I am overriding Command!')
            def format_help_text(self, ctx, formatter):
                print('I am overriding Command!')
            def format_options(self, ctx, formatter):
                print('I am overriding Command!')
            def format_epilog(self, ctx, formatter):
                print('I am overriding Command!')

        @click.command(cls=OverrideCommand)
        def cli():
            """My help text"""
            print('Hello, world!')
        ''',
    )

    res = subprocess.run(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
        stdout=subprocess.PIPE,
        env={**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "False"},
    )
    assert res.returncode == 0

    if CLICK_IS_BEFORE_VERSION_8X:
        usage = "mymodule"
    else:
        usage = "python -m src.rich_click.mymodule"

    expected_output = f"""
 Usage: {usage} [OPTIONS]

 My help text

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
    """

    assert_str(actual=res.stdout.decode(), expectation=expected_output)


def test_override_click_group(mock_script_writer: Callable[[str], Path], assert_str: AssertStr) -> None:
    mock_script_writer(
        '''
        import click

        class OverrideCommand(click.Command):
            def format_usage(self, ctx, formatter):
                print('I am overriding Command!')
            def format_help_text(self, ctx, formatter):
                print('I am overriding Command!')
            def format_options(self, ctx, formatter):
                print('I am overriding Command!')
            def format_epilog(self, ctx, formatter):
                print('I am overriding Command!')

        class OverrideGroup(OverrideCommand, click.Group):
            command_class = OverrideCommand
            def format_commands(self, ctx, formatter):
                print('I am overriding Command!')

        @click.group(cls=OverrideGroup)
        def cli():
            """My help text"""

        @cli.command("subcommand")
        def subcommand():
            """Subcommand help text"""
        ''',
    )

    res = subprocess.run(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
        stdout=subprocess.PIPE,
        env={**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "False"},
    )
    assert res.returncode == 0

    if CLICK_IS_BEFORE_VERSION_8X:
        usage = "mymodule"
    else:
        usage = "python -m src.rich_click.mymodule"

    expected_output = f"""
 Usage: {usage} [OPTIONS] COMMAND [ARGS]...

 My help text

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ subcommand                        Subcommand help text                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯

"""

    assert_str(actual=res.stdout.decode(), expectation=expected_output)


def test_override_rich_click_command(mock_script_writer: WriteScript) -> None:
    mock_script_writer(
        '''
        import rich_click as click

        # Test if robust to subclassing
        class OverrideRichCommand(click.RichCommand):
            def format_usage(self, ctx, formatter):
                print('I am overriding RichCommand!')
            def format_help_text(self, ctx, formatter):
                print('I am overriding RichCommand!')
            def format_options(self, ctx, formatter):
                print('I am overriding RichCommand!')
            def format_epilog(self, ctx, formatter):
                print('I am overriding RichCommand!')

        class OverrideRichGroup(OverrideRichCommand, click.RichGroup):
            command_class = OverrideRichCommand
            def format_commands(self, ctx, formatter):
                print('I am overriding RichCommand!')

        @click.group(cls=OverrideRichGroup)
        def cli():
            """My help text"""

        @cli.command("subcommand")
        def subcommand():
            """Subcommand help text"""

        @click.command(cls=OverrideRichCommand)
        def cli():
            """My help text"""
            print('Hello, world!')
        '''
    )

    res = subprocess.run(
        [sys.executable, "-m", "rich_click", "mymodule:cli", "--help"], stdout=subprocess.PIPE, env=os.environ
    )
    assert res.returncode == 0

    expected_output = ("I am overriding RichCommand!\n" * 4) + "\n"

    assert res.returncode == 0
    assert res.stdout.decode() == expected_output


def test_override_rich_click_group(mock_script_writer: Callable[[str], Path], assert_str: AssertStr) -> None:
    mock_script_writer(
        '''
        import rich_click as click

        # Test if robust to subclassing
        class OverrideRichCommand(click.RichCommand):
            def format_usage(self, ctx, formatter):
                print('I am overriding RichCommand!')
            def format_help_text(self, ctx, formatter):
                print('I am overriding RichCommand!')
            def format_epilog(self, ctx, formatter):
                print('I am overriding RichCommand!')

        class OverrideRichGroup(OverrideRichCommand, click.RichGroup):
            command_class = OverrideRichCommand
            def format_commands(self, ctx, formatter):
                print('I am overriding RichCommand (format_commands)!')

        @click.group(cls=OverrideRichGroup)
        def cli():
            """My help text"""

        @cli.command("subcommand")
        def subcommand():
            """Subcommand help text"""

        @click.command(cls=OverrideRichCommand)
        def cli():
            """My help text"""
            print('Hello, world!')
        ''',
    )

    res = subprocess.run(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
        stdout=subprocess.PIPE,
        env={**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "False"},
    )
    assert res.returncode == 0

    expected_output = """
I am overriding RichCommand!
I am overriding RichCommand!
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
I am overriding RichCommand!
    """

    assert_str(actual=res.stdout.decode(), expectation=expected_output)


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_8X, reason="Warning message gets in the way.")
def test_error_to_stderr(mock_script_writer: Callable[[str], Path], assert_str: AssertStr) -> None:
    mock_script_writer(
        '''
        import click

        @click.group("foo")
        def foo():
            """foo group"""

        @foo.command("bar")
        def bar():
            """bar command"""
        '''
    )

    res_grp = subprocess.run(
        [sys.executable, "-m", "src.rich_click", "mymodule:foo", "--bad-input"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "False"},
    )
    assert res_grp.returncode == 2

    expected_output_grp = """
     Usage: python -m src.rich_click.mymodule [OPTIONS] COMMAND [ARGS]...

    Try 'python -m src.rich_click.mymodule --help' for help
    ╭─ Error ──────────────────────────────────────────────────────────────────────────────────────────╮
    │ No such option: --bad-input                                                                      │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
    """

    assert_str(actual=res_grp.stdout.decode(), expectation="")
    assert_str(actual=res_grp.stderr.decode(), expectation=expected_output_grp)

    res_cmd = subprocess.run(
        [sys.executable, "-m", "src.rich_click", "mymodule:foo", "bar", "--bad-input"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "False"},
    )
    assert res_cmd.returncode == 2

    expected_output_grp = """
     Usage: python -m src.rich_click.mymodule bar [OPTIONS]

    Try 'python -m src.rich_click.mymodule bar --help' for help
    ╭─ Error ──────────────────────────────────────────────────────────────────────────────────────────╮
    │ No such option: --bad-input                                                                      │
    ╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
    """

    assert_str(actual=res_cmd.stdout.decode(), expectation="")
    assert_str(actual=res_cmd.stderr.decode(), expectation=expected_output_grp)
