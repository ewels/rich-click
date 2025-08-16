import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_821
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.custom_errors")
    return cmd


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_821, reason="CliRunner's stderr capture doesn't work before 8.2.1.")
def test_custom_errors_bad_input(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "bad_input")
    assert result.exit_code == 2
    assert result.stdout == snapshot("")
    assert result.stderr == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] INPUT                                                                         \n\
                                                                                                    \n\
 Try running the '--help' flag for more information.                                                \n\
╭─ Error ──────────────────────────────────────────────────────────────────────────────────────────╮
│ Invalid usage                                                                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
 To find out more, visit https://mytool.com                                                         \n\
                                                                                                    \n\
"""
    )
