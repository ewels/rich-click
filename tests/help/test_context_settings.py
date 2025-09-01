import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from rich_click._compat_click import CLICK_IS_VERSION_80
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.context_settings")
    return cmd


@pytest.mark.skipif(CLICK_IS_VERSION_80, reason="Renders differently in click 8.1+.")
def test_context_settings_help_for_click_8_1_plus(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 Test cases for context_settings.                                                                   \n\
 Note that in click < 8.1, '[default: False]' shows for "--help".                                   \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --a        TEXT  This works in all supported click versions. [default: show me always]           │
│ --b        TEXT  This works in all supported click versions. [default: show me always]           │
│ --c        TEXT  Hide default only in click>=8.1                                                 │
│ --d        TEXT  Show 'default: (show me in c8+)' in click>=8.0. In click 7, no default is       │
│                  shown. [default: (show me in c8+)]                                              │
│ --version        Show the version and exit.                                                      │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


@pytest.mark.skipif(not CLICK_IS_VERSION_80, reason="Renders differently in click 8.0.")
def test_context_settings_help_for_click_8_0(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 Test cases for context_settings.                                                                   \n\
 Note that in click < 8.1, '[default: False]' shows for "--help".                                   \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --a        TEXT  This works in all supported click versions. [default: show me always]           │
│ --b        TEXT  This works in all supported click versions. [default: show me always]           │
│ --c        TEXT  Hide default only in click>=8.1 [default: show me in old versions]              │
│ --d        TEXT  Show 'default: (show me in c8+)' in click>=8.0. In click 7, no default is       │
│                  shown.                                                                          │
│                  [default: (show me in c8+)]                                                     │
│ --version        Show the version and exit. [default: False]                                     │
│ --help           Show this message and exit. [default: False]                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
