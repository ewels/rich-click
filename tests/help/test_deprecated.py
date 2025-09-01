import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
import rich_click.rich_click as rc
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_82
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.deprecated")
    return cmd


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_82, reason="Renders differently in click <8.2.")
def test_deprecated_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
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
│ --type             TEXT                Type of file to sync [deprecated: All files will be       │
│                                        synced] [default: files]                                  │
│ --debug        -d                      Enable debug mode [deprecated]                            │
│ --environment  -e  [dev|staging|prod]  Sync to what environment [env var: MY_ENV] [default:      │
│                                        (current)]                                                │
│ --help                                 Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ download  Pretend to download some files from _somewhere_. [deprecated]                          │
│ sync      Synchronise all your files between two places. Example command that doesn't do much    │
│           except print to the terminal. [deprecated: Removing in later version]                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_82, reason="Renders differently in click <8.2.")
def test_deprecated_help_subcommand_bool(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "download --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli download [OPTIONS]                                                                      \n\
                                                                                                    \n\
 [deprecated]                                                                                       \n\
 Pretend to download some files from _somewhere_.                                                   \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --all   Get everything                                                                           │
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_82, reason="Renders differently in click <8.2.")
def test_deprecated_help_subcommand_string(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "sync --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli sync [OPTIONS]                                                                          \n\
                                                                                                    \n\
 [deprecated: Removing in later version]                                                            \n\
 Synchronise all your files between two places. Example command that doesn't do much except print   \n\
 to the terminal.                                                                                   \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --all                                                                                            │
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_82, reason="Renders differently in click <8.2.")
def test_deprecated_help_with_markdown(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.TEXT_MARKUP = "markdown"
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
                                                                                                    \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --type             TEXT                Type of file to sync                                      │
│                                        [deprecated: All files will be synced]                    │
│                                        [default: files]                                          │
│ --debug        -d                      Enable debug mode                                         │
│                                        [deprecated]                                              │
│ --environment  -e  [dev|staging|prod]  Sync to what environment                                  │
│                                        [env var: MY_ENV]                                         │
│                                        [default: (current)]                                      │
│ --help                                 Show this message and exit.                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ download  Pretend to download some files from somewhere.                                         │
│           [deprecated]                                                                           │
│ sync      Synchronise all your files between two places. Example command that doesn't do much    │
│           except print to the terminal.                                                          │
│           [deprecated: Removing in later version]                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_82, reason="Renders differently in click <8.2.")
def test_deprecated_help_subcommand_bool_with_markdown(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.TEXT_MARKUP = "markdown"
    result = cli_runner.invoke(cli, "download --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli download [OPTIONS]                                                                      \n\
                                                                                                    \n\
 [deprecated]                                                                                       \n\
 Pretend to download some files from somewhere.                                                     \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --all   Get everything                                                                           │
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_82, reason="Renders differently in click <8.2.")
def test_deprecated_help_subcommand_string_with_markdown(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.TEXT_MARKUP = "markdown"
    result = cli_runner.invoke(cli, "sync --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli sync [OPTIONS]                                                                          \n\
                                                                                                    \n\
 [deprecated: Removing in later version]                                                            \n\
 Synchronise all your files between two places. Example command that doesn't do much except print   \n\
 to the terminal.                                                                                   \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --all                                                                                            │
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
