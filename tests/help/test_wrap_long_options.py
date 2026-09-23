import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.help.fixtures.wrap_long_options")
    return cmd


def test_wrap_long_options(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --reject-output-outside-source/--no-reject-output-outside-source                                 │
│                          Refuse to write output outside the source tree.                         │
│ --format  -f  [svg|png]  Output format.                                                          │
│ --out     -o  PATH       Where to write the rendered diagram.                                    │
│ --help                   Show this message and exit.                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ a-command-with-a-very-long-name                                                                  │
│                          Long enough to trip the threshold too.                                  │
│ render                   Render the thing.                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


def test_wrap_long_options_disabled_by_a_high_threshold(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    cli.context_settings["rich_help_config"] = {"wrap_long_options": 10_000}
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --reject-output-outside-source/--no-reje                 Refuse to write output outside the      │
│ ct-output-outside-source                                 source tree.                            │
│ --format                                  -f  [svg|png]  Output format.                          │
│ --out                                     -o  PATH       Where to write the rendered diagram.    │
│ --help                                                   Show this message and exit.             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ a-command-with-a-very-long-name              Long enough to trip the threshold too.              │
│ render                                       Render the thing.                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


@pytest.mark.parametrize("disabled", [0, -1, False, None])
def test_wrap_long_options_off(cli_runner: CliRunner, cli: rich_click.RichCommand, disabled: object) -> None:
    """Every falsy or non-positive spelling leaves entries in their columns."""
    cli.context_settings["rich_help_config"] = {"wrap_long_options": 10_000}
    baseline = cli_runner.invoke(cli, "--help").stdout
    cli.context_settings["rich_help_config"] = {"wrap_long_options": disabled}
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == baseline


def test_wrap_long_options_true_means_the_default() -> None:
    config = rich_click.RichHelpConfiguration
    assert config(wrap_long_options=True).wrap_long_options == config().wrap_long_options
