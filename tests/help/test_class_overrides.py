import click
import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.class_overrides")
    return cmd


def test_class_overrides_command_panel(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 Test that command is assigned to panel even if it's not a RichCommand.                             \n\
 (Also test that callback name identifies a command, not just the name of the command.)             \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Rich Click Panel ───────────────────────────────────────────────────────────────────────────────╮
│ click_command  Test that RichParameters can be used with base click Commands.                    │
│ click_options  Test that options+arguments are assigned to the panel even if they're not         │
│                RichParameters.                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_class_overrides_click_command(cli_runner: CliRunner, cli: rich_click.RichGroup) -> None:
    cmd = cli.commands["click-command"]

    assert isinstance(cmd, click.Command)
    assert not isinstance(cmd, rich_click.RichCommand)

    for param in cmd.params:
        assert isinstance(param, rich_click.RichParameter)

    result = cli_runner.invoke(cmd, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Usage: click-command [OPTIONS] RICH_CLICK_ARG

  Test that RichParameters can be used with base click Commands.

Options:
  --rich-click-option TEXT
  --help                    Show this message and exit.
"""
    )
    assert result.stderr == snapshot("")


def test_class_overrides_click_parameters(cli_runner: CliRunner, cli: rich_click.RichGroup) -> None:
    cmd = cli.commands["click-options"]

    for param in cmd.params:
        assert isinstance(param, click.Parameter)
        assert not isinstance(param, rich_click.RichParameter)

    result = cli_runner.invoke(cmd, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: click-options [OPTIONS] CLICK_ARG                                                           \n\
                                                                                                    \n\
 Test that options+arguments are assigned to the panel even if they're not RichParameters.          \n\
                                                                                                    \n\
╭─ Rich Click Panel ───────────────────────────────────────────────────────────────────────────────╮
│ *  CLICK-ARG         TEXT  [required]                                                            │
│ *  --click-option    TEXT  This is help text for a click.Option(). [env var: CLICK_OPTION]       │
│                            [default: foo]                          [required]                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
