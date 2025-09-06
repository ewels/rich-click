import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.help.fixtures.wildcard_groups")
    return cmd


def test_wildcard_groups_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
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
╭─ Basic usage ────────────────────────────────────────────────────────────────────────────────────╮
│ *  --type  TEXT  Type of file to sync [default: files] [required]                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Advanced options ───────────────────────────────────────────────────────────────────────────────╮
│ --help              -h     Show this message and exit.                                           │
│ --version                  Show the version and exit.                                            │
│ --debug/--no-debug  -d/-n  Show the debug log messages [default: no-debug]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Main usage ─────────────────────────────────────────────────────────────────────────────────────╮
│ sync             Synchronise all your files between two places.                                  │
│ download         Pretend to download some files from somewhere.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Configuration ──────────────────────────────────────────────────────────────────────────────────╮
│ config                Set up the configuration.                                                  │
│ auth                  Authenticate the app.                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_wildcard_groups_help_subcommand_sync(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "sync --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Usage: cli sync [OPTIONS]                                                                          \n\
                                                                                                    \n\
 Synchronise all your files between two places.                                                     \n\
                                                                                                    \n\
╭─ Advanced usage ─────────────────────────────────────────────────────────────────────────────────╮
│ --overwrite      Overwrite local files                                                           │
│ --all            Sync all the things?                                                            │
│ --help       -h  Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Inputs and outputs ─────────────────────────────────────────────────────────────────────────────╮
│ *  --input   -i  TEXT  Input path [required]                                                     │
│    --output  -o  TEXT  Output path                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
