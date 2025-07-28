import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_82
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.simple")
    return cmd


def test_simple_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific subcommands.                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug/--no-debug  -d/-n    Enable debug mode. Newlines are removed by default.                 │
│                              Double newlines are preserved.                                      │
│ --help                       Show this message and exit.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ download  Optionally use short-help for the group help text                                      │
│ sync      Synchronise all your files between two places. Example command that doesn't do much    │
│           except print to the terminal.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_simple_help_no_args_is_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    # when raising NoArgsIsHelpError:
    # - exit code is 2 in Click >=8.2
    # - exit code is 0 in Click <8.2
    # - stdout + stderr should be equivalent to using --help.
    result = cli_runner.invoke(cli)
    if CLICK_IS_BEFORE_VERSION_82:
        assert result.exit_code == 0
    else:
        assert result.exit_code == 2
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific subcommands.                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug/--no-debug  -d/-n    Enable debug mode. Newlines are removed by default.                 │
│                              Double newlines are preserved.                                      │
│ --help                       Show this message and exit.                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ download  Optionally use short-help for the group help text                                      │
│ sync      Synchronise all your files between two places. Example command that doesn't do much    │
│           except print to the terminal.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")

    result_with_help = cli_runner.invoke(cli, "--help")
    assert result.stdout == result_with_help.stdout
    assert result.stderr == result_with_help.stderr
