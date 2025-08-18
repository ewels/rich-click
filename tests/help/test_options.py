import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
import rich_click.rich_click as rc
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_82
from tests.conftest import load_command_from_module


pytestmark = pytest.mark.skipif(
    CLICK_IS_BEFORE_VERSION_82, reason="options.py uses features not available prior to Click 8.2"
)


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.options")
    return cmd


def test_options_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --number              INTEGER RANGE [1<=x<=6]  Pick a number [default: 4] [required]          │
│    --name                TEXT                     Provide a name                                 │
│    --location            LOCATION                 Provide a name [deprecated]                    │
│    --flag/--no-flag                               Set the flag (or not!).                        │
│    --password            TEXT                     Password to login with                         │
│ *  --loaded          -l  INTEGER RANGE [x>=0]     This option is loaded with everything (assert  │
│                                                   preservation of order)                         │
│                                                   [env var: IS_LOADED]                           │
│                                                   [default: (Random number)]                     │
│                                                   [required]                                     │
│    --help            -h                           Show help.                                     │
│    --version         -v                           Show version.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_options_help_envvar_first(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.OPTION_ENVVAR_FIRST = True
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --number              INTEGER RANGE [1<=x<=6]  Pick a number [default: 4] [required]          │
│    --name                TEXT                     Provide a name                                 │
│    --location            LOCATION                 Provide a name [deprecated]                    │
│    --flag/--no-flag                               Set the flag (or not!).                        │
│    --password            TEXT                     Password to login with                         │
│ *  --loaded          -l  INTEGER RANGE [x>=0]     [env var: IS_LOADED]                           │
│                                                   This option is loaded with everything (assert  │
│                                                   preservation of order)                         │
│                                                   [default: (Random number)]                     │
│                                                   [required]                                     │
│    --help            -h                           Show help.                                     │
│    --version         -v                           Show version.                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_options_help_dont_show_metavars(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.SHOW_METAVARS_COLUMN = False
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --number              Pick a number [default: 4] [required]                                   │
│    --name                Provide a name                                                          │
│    --location            Provide a name [deprecated]                                             │
│    --flag/--no-flag      Set the flag (or not!).                                                 │
│    --password            Password to login with                                                  │
│ *  --loaded          -l  This option is loaded with everything (assert preservation of order)    │
│                          [env var: IS_LOADED]                                                    │
│                          [default: (Random number)]                                              │
│                          [required]                                                              │
│    --help            -h  Show help.                                                              │
│    --version         -v  Show version.                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
