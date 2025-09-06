# ruff: noqa: D101,D103,D401,E501
import json
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Callable, List

import packaging.version
import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

from rich_click.cli import main
from tests.conftest import WriteScript, run_as_subprocess


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
def test_simple_rich_click_cli(simple_script: Path, command: List[str]) -> None:
    res = run_as_subprocess([sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"])
    assert res.returncode == 0
    assert res.stdout.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click.mymodule [OPTIONS]                                                 \n\
                                                                                                    \n\
 My help text                                                                                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )


@pytest.mark.parametrize(
    "command",
    [
        ["mymodule:cli"],
        ["--", "mymodule:cli"],
        ["mymodule:cli", "--"],
    ],
)
def test_simple_rich_click_cli_execute_command(simple_script: Path, cli_runner: CliRunner, command: List[str]) -> None:
    res = cli_runner.invoke(main, command)

    assert res.exit_code == 0
    assert res.stdout == "Hello, world!\n"

    subprocess_res = run_as_subprocess([sys.executable, "-m", "src.rich_click", *command])
    assert subprocess_res.returncode == 0

    assert subprocess_res.stdout.decode() == "Hello, world!\n"


def test_rich_click_cli_help() -> None:
    res = run_as_subprocess([sys.executable, "-m", "src.rich_click", "--help"])
    assert res.returncode == 0


def test_rich_click_cli_help_with_rich_config() -> None:
    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "--rich-config", '{"style_option": "bold red"}', "--help"]
    )
    assert res.returncode == 0


def test_rich_click_cli_help_with_rich_config_from_file(tmp_path: Path) -> None:
    config_data = {"options_panel_title": "Custom Name"}
    config_file = tmp_path / "myconfig.json"
    config_file.write_text(json.dumps(config_data))

    res = run_as_subprocess([sys.executable, "-m", "src.rich_click", "--rich-config", f"@{config_file}", "--help"])
    assert res.returncode == 0
    assert res.stdout.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click [OPTIONS] SCRIPT | MODULE[:CLICK_COMMAND] ...                      \n\
                                                                                                    \n\
 The rich-click CLI provides richly formatted help output from any tool using click, formatted with \n\
 rich.                                                                                              \n\
 Full docs here: https://ewels.github.io/rich-click/latest/documentation/rich_click_cli/            \n\
 The rich-click command line tool can be prepended before any Python package using native click to  \n\
 provide attractive richified click help output.                                                    \n\
 For example, if you have a package called my_package that uses click, you can run:                 \n\
 >>> rich-click my_package --help                                                                   \n\
 When not rendering help text, the provided command will run normally, so it is safe to replace     \n\
 calls to the tool with rich-click in front, e.g.:                                                  \n\
 >>> rich-click my_package cmd --foo 3                                                              \n\
                                                                                                    \n\
╭─ Advanced Options ───────────────────────────────────────────────────────────────────────────────╮
│ --errors-in-output-format                       If set, forces the CLI to render CLI error       │
│                                                 messages in the format specified by the --output │
│                                                 option. By default, error messages render        │
│                                                 normally, i.e. they are not converted to html or │
│                                                 svg.                                             │
│ --suppress-warnings/--do-not-suppress-warnings  Suppress warnings when there are conflicting     │
│                                                 entry_points. This situation is extremely rare.  │
│                                                 [env var: RICH_CLICK_CLI_SUPPRESS_WARNINGS]      │
│ --patch-rich-click/--no-patch-rich-click        If set, patch rich_click.Command, not just       │
│                                                 click.Command.                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Extra ──────────────────────────────────────────────────────────────────────────────────────────╮
│ --themes       List all available themes and exit.                                               │
│ --version      Show the version and exit.                                                        │
│ --help     -h  Show this message and exit.                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom Name ────────────────────────────────────────────────────────────────────────────────────╮
│ --theme        -t  THEME            Set the theme to render the CLI with.                        │
│ --rich-config  -c  JSON             Keyword arguments to pass into the RichHelpConfiguration()   │
│                                     used to render the help text of the command. You can pass    │
│                                     either a JSON directly, or a file prefixed with `@` (for     │
│                                     example: '@rich_config.json'). Note that the --rich-config   │
│                                     option is also used to render this help text you're reading  │
│                                     right now!                                                   │
│ --output       -o  [html|svg|text]  Optionally render help text as HTML or SVG or plain text. By │
│                                     default, help text is rendered normally.                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )


def test_rich_click_cli_help_with_bad_rich_config() -> None:
    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "--rich-config", '{"bad", "json"}', "--help"],
    )
    assert res.returncode == 0


def test_rich_click_cli_help_with_bad_rich_config_v2() -> None:
    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "--rich-config", "[]", "--help"],
    )
    assert res.returncode == 0


def test_custom_config_rich_click_cli(simple_script: Path) -> None:
    res = run_as_subprocess(
        [
            sys.executable,
            "-m",
            "src.rich_click",
            "--rich-config",
            '{"options_panel_title": "Custom Name"}',
            "mymodule:cli",
            "--help",
        ]
    )
    assert res.returncode == 0
    assert res.stdout.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click.mymodule [OPTIONS]                                                 \n\
                                                                                                    \n\
 My help text                                                                                       \n\
                                                                                                    \n\
╭─ Custom Name ────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )


def test_override_click_command(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import click

        class OverrideCommand(click.Command):
            def format_usage(self, ctx, formatter):
                formatter.write('I am overriding Command!')
            def format_help_text(self, ctx, formatter):
                formatter.write('I am overriding Command!')
            def format_options(self, ctx, formatter):
                formatter.write('I am overriding Command!')
            def format_epilog(self, ctx, formatter):
                formatter.write('I am overriding Command!')

        @click.command(cls=OverrideCommand)
        def cli():
            """My help text"""
            print('Hello, world!')
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click.mymodule [OPTIONS]                                                 \n\
                                                                                                    \n\
 My help text                                                                                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )


def test_override_click_group(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import click

        class OverrideCommand(click.Command):
            def format_usage(self, ctx, formatter):
                formatter.write('I am overriding Command!')
            def format_help_text(self, ctx, formatter):
                formatter.write('I am overriding Command!')
            def format_options(self, ctx, formatter):
                formatter.write('I am overriding Command!')
            def format_epilog(self, ctx, formatter):
                formatter.write('I am overriding Command!')

        class OverrideGroup(OverrideCommand, click.Group):
            command_class = OverrideCommand
            def format_commands(self, ctx, formatter):
                formatter.write('I am overriding Command!')

        @click.group(cls=OverrideGroup)
        def cli():
            """My help text"""

        @cli.command("subcommand")
        def subcommand():
            """Subcommand help text"""
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click.mymodule [OPTIONS] COMMAND [ARGS]...                               \n\
                                                                                                    \n\
 My help text                                                                                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ subcommand                        Subcommand help text                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )


def test_override_rich_click_command(mock_script_writer: WriteScript) -> None:
    mock_script_writer(
        '''
        import rich_click as click

        # Test if robust to subclassing
        class OverrideRichCommand(click.RichCommand):
            def format_usage(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (usage)')
            def format_help_text(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (help_text)')
            def format_options(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (options)')
            def format_epilog(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (epilog)')

        @click.command(cls=OverrideRichCommand)
        def cli():
            """My help text"""
            print('Hello, world!')
        '''
    )

    res = run_as_subprocess([sys.executable, "-m", "rich_click", "mymodule:cli", "--help"])
    assert res.returncode == 0

    assert res.returncode == 0
    assert res.stdout.decode() == snapshot(
        """\
I am overriding RichCommand! (usage)
I am overriding RichCommand! (help_text)
I am overriding RichCommand! (options)
I am overriding RichCommand! (epilog)
"""
    )


def test_override_rich_click_group(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import rich_click as click

        # Test if robust to subclassing
        class OverrideRichCommand(click.RichCommand):
            def format_usage(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (usage)')
            def format_help_text(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (help_text)')
            def format_options(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (options)')
            def format_epilog(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (epilog)')

        class OverrideRichGroup(OverrideRichCommand, click.RichGroup):
            command_class = OverrideRichCommand
            def format_commands(self, ctx, formatter):
                formatter.write('I am overriding RichCommand (format_commands)!')

        @click.group(cls=OverrideRichGroup)
        def cli():
            """My help text"""
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        """\
I am overriding RichCommand! (usage)
I am overriding RichCommand! (help_text)
I am overriding RichCommand! (options)
I am overriding RichCommand! (epilog)
"""
    )


def test_override_rich_click_command_collection(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import rich_click as click

        # Test if robust to subclassing
        class OverrideRichCommand(click.RichCommand):
            def format_usage(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (usage)')
            def format_help_text(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (help_text)')
            def format_options(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (options)')
            def format_epilog(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (epilog)')

        class OverrideRichCommandCollection(OverrideRichCommand, click.RichCommandCollection):
            command_class = OverrideRichCommand
            def format_commands(self, ctx, formatter):
                formatter.write('I am overriding RichCommand (format_commands)!')

        @click.group(cls=OverrideRichCommandCollection)
        def cli():
            """My help text"""

        @cli.command("subcommand")
        def subcommand():
            """Subcommand help text"""
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        """\
I am overriding RichCommand! (usage)
I am overriding RichCommand! (help_text)
I am overriding RichCommand! (options)
I am overriding RichCommand! (epilog)
"""
    )


def test_override_guard_click_command(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import click

        # Test if robust to subclassing
        class OverrideCommand(click.Command):
            def format_usage(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (usage)')
            def format_help_text(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (help_text)')
            def format_options(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (options)')
            def format_epilog(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (epilog)')

        @click.group(cls=OverrideCommand)
        def cli():
            """My help text"""
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click.mymodule [OPTIONS]                                                 \n\
                                                                                                    \n\
 My help text                                                                                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )


def test_override_guard_click_group(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import click

        # Test if robust to subclassing
        class OverrideCommand(click.Command):
            def format_usage(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (usage)')
            def format_help_text(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (help_text)')
            def format_options(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (options)')
            def format_epilog(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (epilog)')

        class OverrideGroup(OverrideCommand, click.Group):
            command_class = OverrideCommand
            def format_commands(self, ctx, formatter):
                formatter.write('I am overriding RichCommand (format_commands)!')

        @click.group(cls=OverrideGroup)
        def cli():
            """My help text"""
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click.mymodule [OPTIONS] COMMAND [ARGS]...                               \n\
                                                                                                    \n\
 My help text                                                                                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )


def test_override_guard_disabled_click_from_rich_click(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import rich_click as click

        # Test if robust to subclassing
        class OverrideCommand(click.Command):
            def format_usage(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (usage)')
            def format_help_text(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (help_text)')
            def format_options(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (options)')
            def format_epilog(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (epilog)')

        class OverrideGroup(OverrideCommand, click.Group):
            command_class = OverrideCommand
            def format_commands(self, ctx, formatter):
                formatter.write('I am overriding RichCommand (format_commands)!')

        @click.group(cls=OverrideGroup)
        def cli():
            """My help text"""
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "--no-patch-rich-click", "mymodule:cli", "--help"],
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        "I am overriding RichCommand! (usage)I am overriding RichCommand! (help_text)I am overriding RichCommand! (options)I am overriding RichCommand! (epilog)\n"
    )


def test_override_guard_enabled_click_from_rich_click(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import rich_click as click

        # Test if robust to subclassing
        class OverrideCommand(click.Command):
            def format_usage(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (usage)')
            def format_help_text(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (help_text)')
            def format_options(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (options)')
            def format_epilog(self, ctx, formatter):
                formatter.write('I am overriding RichCommand! (epilog)')

        class OverrideGroup(OverrideCommand, click.Group):
            command_class = OverrideCommand
            def format_commands(self, ctx, formatter):
                formatter.write('I am overriding RichCommand (format_commands)!')

        @click.group(cls=OverrideGroup)
        def cli():
            """My help text"""
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "mymodule:cli", "--help"],
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click.mymodule [OPTIONS] COMMAND [ARGS]...                               \n\
                                                                                                    \n\
 My help text                                                                                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )


def test_error_to_stderr(mock_script_writer: Callable[[str], Path]) -> None:
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

    res_grp = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "mymodule:foo", "--bad-input"],
    )
    assert res_grp.returncode == 2
    assert res_grp.stdout.decode() == ""
    assert res_grp.stderr.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click.mymodule [OPTIONS] COMMAND [ARGS]...                               \n\
                                                                                                    \n\
 Try 'python -m src.rich_click.mymodule --help' for help                                            \n\
╭─ Error ──────────────────────────────────────────────────────────────────────────────────────────╮
│ No such option: --bad-input                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
"""
    )

    res_cmd = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "mymodule:foo", "bar", "--bad-input"],
    )
    assert res_cmd.returncode == 2

    assert res_grp.stdout.decode() == ""
    assert res_grp.stderr.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click.mymodule [OPTIONS] COMMAND [ARGS]...                               \n\
                                                                                                    \n\
 Try 'python -m src.rich_click.mymodule --help' for help                                            \n\
╭─ Error ──────────────────────────────────────────────────────────────────────────────────────────╮
│ No such option: --bad-input                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
"""
    )


rich_version = packaging.version.parse(version("rich"))


@pytest.mark.skipif(rich_version < packaging.version.parse("13.0.0"), reason="Rich <13 renders differently")
def test_cli_output_html(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import rich_click as click

        @click.command()
        def cli():
            """My help text"""
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "--output", "html", "mymodule:cli", "--help"],
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        """\
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>

body {
    color: #000000;
    background-color: #ffffff;
}
</style>
</head>
<body>
    <pre style="font-family:Menlo,'DejaVu Sans Mono',consolas,'Courier New',monospace"><code style="font-family:inherit">                                                                                                    \n\
 <span style="color: #808000; text-decoration-color: #808000">Usage:</span> <span style="font-weight: bold">python -m src.rich_click.mymodule</span> [<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">OPTIONS</span>]                                                 \n\
                                                                                                    \n\
 My help text                                                                                       \n\
                                                                                                    \n\
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--help</span>  Show this message and exit.                                                              <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────────────────────────────────╯</span>
</code></pre>
</body>
</html>
"""
    )


def test_cli_output_svg(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import rich_click as click

        @click.command()
        def cli():
            """My help text"""
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "--output", "svg", "mymodule:cli", "--help"],
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        """\
<svg class="rich-terminal" viewBox="0 0 1238 245.2" xmlns="http://www.w3.org/2000/svg">
    <!-- Generated with Rich https://www.textualize.io -->
    <style>

    @font-face {
        font-family: "Fira Code";
        src: local("FiraCode-Regular"),
                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Regular.woff2") format("woff2"),
                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Regular.woff") format("woff");
        font-style: normal;
        font-weight: 400;
    }
    @font-face {
        font-family: "Fira Code";
        src: local("FiraCode-Bold"),
                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff2/FiraCode-Bold.woff2") format("woff2"),
                url("https://cdnjs.cloudflare.com/ajax/libs/firacode/6.2.0/woff/FiraCode-Bold.woff") format("woff");
        font-style: bold;
        font-weight: 700;
    }

    .terminal-237638219-matrix {
        font-family: Fira Code, monospace;
        font-size: 20px;
        line-height: 24.4px;
        font-variant-east-asian: full-width;
    }

    .terminal-237638219-title {
        font-size: 18px;
        font-weight: bold;
        font-family: arial;
    }

    .terminal-237638219-r1 { fill: #c5c8c6 }
.terminal-237638219-r2 { fill: #d0b344 }
.terminal-237638219-r3 { fill: #c5c8c6;font-weight: bold }
.terminal-237638219-r4 { fill: #68a0b3;font-weight: bold }
.terminal-237638219-r5 { fill: #868887 }
    </style>

    <defs>
    <clipPath id="terminal-237638219-clip-terminal">
      <rect x="0" y="0" width="1219.0" height="194.2" />
    </clipPath>
    <clipPath id="terminal-237638219-line-0">
    <rect x="0" y="1.5" width="1220" height="24.65"/>
            </clipPath>
<clipPath id="terminal-237638219-line-1">
    <rect x="0" y="25.9" width="1220" height="24.65"/>
            </clipPath>
<clipPath id="terminal-237638219-line-2">
    <rect x="0" y="50.3" width="1220" height="24.65"/>
            </clipPath>
<clipPath id="terminal-237638219-line-3">
    <rect x="0" y="74.7" width="1220" height="24.65"/>
            </clipPath>
<clipPath id="terminal-237638219-line-4">
    <rect x="0" y="99.1" width="1220" height="24.65"/>
            </clipPath>
<clipPath id="terminal-237638219-line-5">
    <rect x="0" y="123.5" width="1220" height="24.65"/>
            </clipPath>
<clipPath id="terminal-237638219-line-6">
    <rect x="0" y="147.9" width="1220" height="24.65"/>
            </clipPath>
    </defs>

    <rect fill="#292929" stroke="rgba(255,255,255,0.35)" stroke-width="1" x="1" y="1" width="1236" height="243.2" rx="8"/><text class="terminal-237638219-title" fill="#c5c8c6" text-anchor="middle" x="618" y="27">mymodule&#160;--help</text>
            <g transform="translate(26,22)">
            <circle cx="0" cy="0" r="7" fill="#ff5f57"/>
            <circle cx="22" cy="0" r="7" fill="#febc2e"/>
            <circle cx="44" cy="0" r="7" fill="#28c840"/>
            </g>
        \n\
    <g transform="translate(9, 41)" clip-path="url(#terminal-237638219-clip-terminal)">
    \n\
    <g class="terminal-237638219-matrix">
    <text class="terminal-237638219-r1" x="1220" y="20" textLength="12.2" clip-path="url(#terminal-237638219-line-0)">
</text><text class="terminal-237638219-r2" x="12.2" y="44.4" textLength="73.2" clip-path="url(#terminal-237638219-line-1)">Usage:</text><text class="terminal-237638219-r3" x="97.6" y="44.4" textLength="402.6" clip-path="url(#terminal-237638219-line-1)">python&#160;-m&#160;src.rich_click.mymodule</text><text class="terminal-237638219-r1" x="512.4" y="44.4" textLength="12.2" clip-path="url(#terminal-237638219-line-1)">[</text><text class="terminal-237638219-r4" x="524.6" y="44.4" textLength="85.4" clip-path="url(#terminal-237638219-line-1)">OPTIONS</text><text class="terminal-237638219-r1" x="610" y="44.4" textLength="12.2" clip-path="url(#terminal-237638219-line-1)">]</text><text class="terminal-237638219-r1" x="1220" y="44.4" textLength="12.2" clip-path="url(#terminal-237638219-line-1)">
</text><text class="terminal-237638219-r1" x="1220" y="68.8" textLength="12.2" clip-path="url(#terminal-237638219-line-2)">
</text><text class="terminal-237638219-r1" x="12.2" y="93.2" textLength="146.4" clip-path="url(#terminal-237638219-line-3)">My&#160;help&#160;text</text><text class="terminal-237638219-r1" x="1220" y="93.2" textLength="12.2" clip-path="url(#terminal-237638219-line-3)">
</text><text class="terminal-237638219-r1" x="1220" y="117.6" textLength="12.2" clip-path="url(#terminal-237638219-line-4)">
</text><text class="terminal-237638219-r5" x="0" y="142" textLength="24.4" clip-path="url(#terminal-237638219-line-5)">╭─</text><text class="terminal-237638219-r5" x="24.4" y="142" textLength="109.8" clip-path="url(#terminal-237638219-line-5)">&#160;Options&#160;</text><text class="terminal-237638219-r5" x="134.2" y="142" textLength="1061.4" clip-path="url(#terminal-237638219-line-5)">───────────────────────────────────────────────────────────────────────────────────────</text><text class="terminal-237638219-r5" x="1195.6" y="142" textLength="24.4" clip-path="url(#terminal-237638219-line-5)">─╮</text><text class="terminal-237638219-r1" x="1220" y="142" textLength="12.2" clip-path="url(#terminal-237638219-line-5)">
</text><text class="terminal-237638219-r5" x="0" y="166.4" textLength="12.2" clip-path="url(#terminal-237638219-line-6)">│</text><text class="terminal-237638219-r4" x="24.4" y="166.4" textLength="73.2" clip-path="url(#terminal-237638219-line-6)">--help</text><text class="terminal-237638219-r1" x="122" y="166.4" textLength="329.4" clip-path="url(#terminal-237638219-line-6)">Show&#160;this&#160;message&#160;and&#160;exit.</text><text class="terminal-237638219-r5" x="1207.8" y="166.4" textLength="12.2" clip-path="url(#terminal-237638219-line-6)">│</text><text class="terminal-237638219-r1" x="1220" y="166.4" textLength="12.2" clip-path="url(#terminal-237638219-line-6)">
</text><text class="terminal-237638219-r5" x="0" y="190.8" textLength="1220" clip-path="url(#terminal-237638219-line-7)">╰──────────────────────────────────────────────────────────────────────────────────────────────────╯</text><text class="terminal-237638219-r1" x="1220" y="190.8" textLength="12.2" clip-path="url(#terminal-237638219-line-7)">
</text>
    </g>
    </g>
</svg>
"""
    )


def test_cli_output_text(mock_script_writer: Callable[[str], Path]) -> None:
    mock_script_writer(
        '''
        import rich_click as click

        @click.command()
        def cli():
            """My help text"""
        ''',
    )

    res = run_as_subprocess(
        [sys.executable, "-m", "src.rich_click", "--output", "text", "mymodule:cli", "--help"],
        # Even with FORCE_COLOR=True, no color should render with --output=text
        env={"FORCE_COLOR": "True"},
    )
    assert res.returncode == 0

    assert res.stdout.decode() == snapshot(
        """\
                                                                                                    \n\
 Usage: python -m src.rich_click.mymodule [OPTIONS]                                                 \n\
                                                                                                    \n\
 My help text                                                                                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
