import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
import rich_click.rich_click as rc
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.defaults")
    return cmd


def test_defaults_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug        -d                      Enable debug mode                                         │
│ --environment  -e  [dev|staging|prod]  Sync to what environment [env var: MY_ENV]                │
│ --help                                 Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ download                             Download files                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_defaults_help_subcommand_with_show_default_string(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "download --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Environment: None
Debug mode is off
                                                                                                    \n\
 Usage: cli download [OPTIONS]                                                                      \n\
                                                                                                    \n\
 Download files                                                                                     \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --files    TEXT  What files to download [default: (All files)]                                   │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_defaults_help_subcommand_with_show_default_string_and_markdown(
    cli_runner: CliRunner, cli: rich_click.RichCommand
) -> None:
    rc.TEXT_MARKUP = "markdown"
    result = cli_runner.invoke(cli, "download --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Environment: None
Debug mode is off
                                                                                                    \n\
 Usage: cli download [OPTIONS]                                                                      \n\
                                                                                                    \n\
 Download files                                                                                     \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --files    TEXT  What files to download                                                          │
│                  [default: (All files)]                                                          │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
