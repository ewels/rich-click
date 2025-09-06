import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.help.fixtures.groups_sorting")
    return cmd


def test_groups_sorting_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
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
│ --version                  Show the version and exit.                                            │
│ --debug/--no-debug  -d/-n  Show the debug log messages [default: no-debug]                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Help ───────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h  Show this message and exit.                                                          │
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


def test_groups_sorting_help_subcommand_sync(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
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
╭─ Inputs and outputs ─────────────────────────────────────────────────────────────────────────────╮
│ *  --input   -i  TEXT  Input path [required]                                                     │
│    --output  -o  TEXT  Output path                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Subcommand help ────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h  Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --all        Sync all the things?                                                                │
│ --overwrite  Overwrite local files                                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_groups_sorting_help_subcommand_download(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "download --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Usage: cli download [OPTIONS]                                                                      \n\
                                                                                                    \n\
 Pretend to download some files from somewhere.                                                     \n\
                                                                                                    \n\
╭─ Subcommand help ────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h  Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --all  Get everything                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_groups_sorting_help_subcommand_config(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "config --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Usage: cli config [OPTIONS]                                                                        \n\
                                                                                                    \n\
 Set up the configuration.                                                                          \n\
                                                                                                    \n\
╭─ Subcommand help ────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h  Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_groups_sorting_help_subcommand_auth(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "auth --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Usage: cli auth [OPTIONS]                                                                          \n\
                                                                                                    \n\
 Authenticate the app.                                                                              \n\
                                                                                                    \n\
╭─ Required ───────────────────────────────────────────────────────────────────────────────────────╮
│ *  --user      -u  TEXT  User [required]                                                         │
│ *  --password  -p  TEXT  Password [required]                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Misc. ──────────────────────────────────────────────────────────────────────────────────────────╮
│ --email  -e  TEXT  Email                                                                         │
│ --role   -r  TEXT  Role                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Auth help ──────────────────────────────────────────────────────────────────────────────────────╮
│ --help  -h  Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
