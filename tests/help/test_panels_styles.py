import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.panels_styles")
    return cmd


def test_styles_command_panel(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 Test basic styles for command panel.                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
   Custom Panel                                                                                     \n\
  This is help text for the command panel.                                                          \n\
  subcommand              Test basic styles for option panel.                                       \n\
                                        Additional Commands                                         \n\
                                                                                                    \n\
"""
    )
    assert result.stderr == snapshot("")


def test_styles_options_panel(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "subcommand --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli subcommand [OPTIONS]                                                                    \n\
                                                                                                    \n\
 Test basic styles for option panel.                                                                \n\
                                                                                                    \n\
   Custom Panel                                                                                     \n\
  This is help text for the option panel.                                                           \n\
  --a  -a  TEXT  Help text for A                                                                    \n\
  --b  -b  TEXT  Help text for B                                                                    \n\
  --c  -c  TEXT  Help text for C                                                                    \n\
                                         Additional Options                                         \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
