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


def test_wrap_long_options_off_for_boxed_tables(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    """A box is drawn around every table, and taking a row out of the columns makes more of them."""
    box = {"style_options_table_box": "DOUBLE", "style_commands_table_box": "DOUBLE"}
    cli.context_settings["rich_help_config"] = {**box, "wrap_long_options": 0}
    baseline = cli_runner.invoke(cli, "--help").stdout
    cli.context_settings["rich_help_config"] = box
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == baseline


def test_wrap_long_options_true_from_the_theme_env_var(
    cli_runner: CliRunner, cli: rich_click.RichCommand, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A theme assigns fields directly, so `True` has to be read as the default there too."""
    cli.context_settings["rich_help_config"] = {"wrap_long_options": 40}
    baseline = cli_runner.invoke(cli, "--help").stdout
    cli.context_settings["rich_help_config"] = {}
    monkeypatch.setenv("RICH_CLICK_THEME", '{"wrap_long_options": true}')
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == baseline


def test_wrap_long_options_off_for_a_box_set_on_the_panel(cli_runner: CliRunner) -> None:
    """A panel's own `table_styles` carry the box just as the config does."""
    long_option = "--reject-output-outside-source/--no-reject-output-outside-source"

    @rich_click.command()
    @rich_click.option(long_option, default=True, help="Refuse to write output outside the source tree.")
    @rich_click.option("--format", "-f", type=rich_click.Choice(["svg", "png"]), help="Output format.")
    @rich_click.option_panel(
        "Options", options=["reject_output_outside_source", "format"], table_styles={"box": "DOUBLE"}
    )
    def cli() -> None:
        """CLI help text"""

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout.count("╔") == 1


def test_wrap_long_options_indents_the_next_line_head_like_the_rows(
    cli_runner: CliRunner, cli: rich_click.RichCommand
) -> None:
    """The entry sits above the table, so it has to carry the table's own edge padding itself."""
    cli.context_settings["rich_help_config"] = {"style_options_table_pad_edge": True}
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    head, below = (line for line in result.stdout.splitlines() if "--reject-output" in line or "--format" in line)
    assert head.index("--reject-output") == below.index("--format")
