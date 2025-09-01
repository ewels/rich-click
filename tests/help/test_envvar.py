import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
import rich_click.rich_click as rc
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.envvar")
    return cmd


def test_envvar_greet_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "greet --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Usage: cli greet [OPTIONS]                                                                         \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --username      TEXT  This can be set via env var GREETER_GREET_USERNAME [env var:               │
│                       GREETER_GREET_USERNAME]                                                    │
│ --nickname      TEXT  This can be set via env var NICKNAME [env var: NICKNAME]                   │
│ --email         TEXT  This can be set via env var EMAIL or EMAIL_ADDRESS [env var: EMAIL,        │
│                       EMAIL_ADDRESS] [default: foo@bar.com]                                      │
│ --token     -t  TEXT  [env var: GREETER_GREET_TOKEN]                                             │
│ --help                Show this message and exit.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_envvar_greet_help_with_envvar_string(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.ENVVAR_STRING = "(ENV: {})"
    result = cli_runner.invoke(cli, "greet --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Usage: cli greet [OPTIONS]                                                                         \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --username      TEXT  This can be set via env var GREETER_GREET_USERNAME (ENV:                   │
│                       GREETER_GREET_USERNAME)                                                    │
│ --nickname      TEXT  This can be set via env var NICKNAME (ENV: NICKNAME)                       │
│ --email         TEXT  This can be set via env var EMAIL or EMAIL_ADDRESS (ENV: EMAIL,            │
│                       EMAIL_ADDRESS) [default: foo@bar.com]                                      │
│ --token     -t  TEXT  (ENV: GREETER_GREET_TOKEN)                                                 │
│ --help                Show this message and exit.                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
