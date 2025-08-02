import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.header")
    return cmd


def test_header_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Welcome to my CLI!                                                                                 \n\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug/--no-debug                                                                               │
│ --help                  Show this message and exit.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ subcommand                        Subcommand help text                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_header_subcommand_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "subcommand --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Welcome to my CLI! (with Text())                                                                   \n\
                                                                                                    \n\
 Usage: cli subcommand [OPTIONS]                                                                    \n\
                                                                                                    \n\
 Subcommand help text                                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_header_help_turn_off_rich_markup(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    cli.context_settings["rich_help_config"]["text_markup"] = None
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 [magenta]Welcome to my CLI![/]                                                                     \n\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug/--no-debug                                                                               │
│ --help                  Show this message and exit.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ subcommand                        Subcommand help text                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
