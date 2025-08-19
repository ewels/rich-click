import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from rich_click import RichHelpConfiguration
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.metavars")
    return cmd


def test_metavars_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug                                               Enable debug mode.                         │
│ --number    [one|two|three|four|five|six|seven|eight  This click choice has loads of options.    │
│             |nine|ten|eleven|twelve|thirteen|fourtee                                             │
│             n|fifteen|sixteen|seventeen|eighteen|nin                                             │
│             eteen|twenty|twenty-one|twenty-two|twent                                             │
│             y-three|twenty-four|twenty-five|twenty-s                                             │
│             ix|twenty-seven|twenty-eight|twenty-nine                                             │
│             |thirty]                                                                             │
│ --help                                                Show this message and exit.                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_metavars_help_flipped(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    with pytest.warns(PendingDeprecationWarning, match=r"`show_metavars_column=` will be deprecated.*"):
        cfg = RichHelpConfiguration.load_from_globals(show_metavars_column=False, append_metavars_help=True)
    cli = rich_click.rich_config(help_config=cfg)(cli)

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug     Enable debug mode.                                                                   │
│ --number    This click choice has loads of options.                                              │
│             [one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fi │
│             fteen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three| │
│             twenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty]     │
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_metavars_help_flipped_help_string(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    with pytest.warns(PendingDeprecationWarning, match=r"`show_metavars_column=` will be deprecated.*"):
        cfg = RichHelpConfiguration.load_from_globals(
            show_metavars_column=False, append_metavars_help=True, append_metavars_help_string="[choices: {}]"
        )
    cli = rich_click.rich_config(help_config=cfg)(cli)

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug     Enable debug mode.                                                                   │
│ --number    This click choice has loads of options.                                              │
│             [choices:                                                                            │
│             one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fif │
│             teen|sixteen|seventeen|eighteen|nineteen|twenty|twenty-one|twenty-two|twenty-three|t │
│             wenty-four|twenty-five|twenty-six|twenty-seven|twenty-eight|twenty-nine|thirty]      │
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
