import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot
from rich import box

import rich_click
import rich_click.rich_click as rc
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.arguments")
    return cmd


def test_arguments_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] INPUT OUTPUT                                                                  \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────╮
│ *  INPUT   PATH  Input file [required]                                                           │
│ *  OUTPUT  PATH  Output file [required]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --type             TEXT                Type of file to sync [default: files]                     │
│ --debug        -d                      Enable debug mode                                         │
│ --environment  -e  [dev|staging|prod]  Sync to what environment [env var: MY_ENV]                │
│                                        [default: (current)]                                      │
│ --help                                 Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_arguments_help_with_no_show_arguments(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.SHOW_ARGUMENTS = False
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] INPUT OUTPUT                                                                  \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --type             TEXT                Type of file to sync [default: files]                     │
│ --debug        -d                      Enable debug mode                                         │
│ --environment  -e  [dev|staging|prod]  Sync to what environment [env var: MY_ENV]                │
│                                        [default: (current)]                                      │
│ --help                                 Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_arguments_help_with_help_panel_title(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.ARGUMENTS_PANEL_TITLE = "My amazing tool arguments"
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] INPUT OUTPUT                                                                  \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ My amazing tool arguments ──────────────────────────────────────────────────────────────────────╮
│ *  INPUT   PATH  Input file [required]                                                           │
│ *  OUTPUT  PATH  Output file [required]                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --type             TEXT                Type of file to sync [default: files]                     │
│ --debug        -d                      Enable debug mode                                         │
│ --environment  -e  [dev|staging|prod]  Sync to what environment [env var: MY_ENV]                │
│                                        [default: (current)]                                      │
│ --help                                 Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_arguments_help_with_help_panel_config(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.ARGUMENTS_PANEL_TITLE = "My amazing tool arguments"
    rc.OPTION_GROUPS = {"cli": [{"name": "My amazing tool arguments", "panel_styles": {"box": box.DOUBLE_EDGE}}]}
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] INPUT OUTPUT                                                                  \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╔═ My amazing tool arguments ══════════════════════════════════════════════════════════════════════╗
║ *  INPUT   PATH  Input file [required]                                                           ║
║ *  OUTPUT  PATH  Output file [required]                                                          ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --type             TEXT                Type of file to sync [default: files]                     │
│ --debug        -d                      Enable debug mode                                         │
│ --environment  -e  [dev|staging|prod]  Sync to what environment [env var: MY_ENV]                │
│                                        [default: (current)]                                      │
│ --help                                 Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_arguments_help_grouped_with_options(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.GROUP_ARGUMENTS_OPTIONS = True
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] INPUT OUTPUT                                                                  \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ *  INPUT              PATH                Input file [required]                                  │
│ *  OUTPUT             PATH                Output file [required]                                 │
│    --type             TEXT                Type of file to sync [default: files]                  │
│    --debug        -d                      Enable debug mode                                      │
│    --environment  -e  [dev|staging|prod]  Sync to what environment [env var: MY_ENV]             │
│                                           [default: (current)]                                   │
│    --help                                 Show this message and exit.                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
