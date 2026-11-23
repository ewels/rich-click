from typing import cast

import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.help.fixtures.aligned_panels")
    return cmd


@pytest.fixture
def wrap_cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.help.fixtures.aligned_panels_wrap")
    return cmd


def test_aligned_panels_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config  -c  PATH  Config file. [required]                                                   │
│    --help              Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Core ───────────────────────────────────────────────────────────────────────────────────────────╮
│ run                    Run the thing.                                                            │
│ a-much-longer-name     Do something else.                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Extras ─────────────────────────────────────────────────────────────────────────────────────────╮
│ tidy                   Tidy up.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Logging ────────────────────────────────────────────────────────────────────────────────────────╮
│    --verbose           Be loud.                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


def test_aligned_panels_wide_entries(cli_runner: CliRunner, wrap_cli: rich_click.RichCommand) -> None:
    """Entries too wide for their own column spill into the empty ones, or fall to the next line."""
    result = cli_runner.invoke(wrap_cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Output ─────────────────────────────────────────────────────────────────────────────────────────╮
│ --output  [svg|html|png|gif|webp|webm]                                                           │
│                                   Output format.                                                 │
│ --reject-output-outside-source/--no-reject-output-outside-source                                 │
│                                   Reject an output path outside the source repository.           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Layout ─────────────────────────────────────────────────────────────────────────────────────────╮
│ --center-ports/--no-center-ports  Centre inter-section ports.                                    │
│ --mode  [light|dark|auto]         Palette to render with.                                        │
│ --compact-offsets/--no-compact-offsets                                                           │
│                                   Size each station for its lines.                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help                            Show this message and exit.                                    │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


def test_aligned_panels_off(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    """Each panel sizes its own columns, so the help text starts in a different place in each."""
    cli.context_settings["rich_help_config"] = {"align_columns_across_panels": False}
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config  -c  PATH  Config file. [required]                                                   │
│    --help              Show this message and exit.                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Core ───────────────────────────────────────────────────────────────────────────────────────────╮
│ run                                              Run the thing.                                  │
│ a-much-longer-name                               Do something else.                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Extras ─────────────────────────────────────────────────────────────────────────────────────────╮
│ tidy                                Tidy up.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Logging ────────────────────────────────────────────────────────────────────────────────────────╮
│ --verbose  Be loud.                                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


def test_aligned_panels_give_up_when_the_columns_would_crowd_out_the_help(
    cli_runner: CliRunner, wrap_cli: rich_click.RichCommand
) -> None:
    """Below the width alignment needs, panels size themselves exactly as if it were switched off."""
    config = {"width": 54, "wrap_long_options": 40}
    wrap_cli.context_settings["rich_help_config"] = {**config, "align_columns_across_panels": False}
    unaligned = cli_runner.invoke(wrap_cli, "--help")
    wrap_cli.context_settings["rich_help_config"] = {**config, "align_columns_across_panels": True}
    result = cli_runner.invoke(wrap_cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == unaligned.stdout


def test_get_table_does_not_reuse_another_renders_rows(cli: rich_click.RichCommand) -> None:
    """The rows the alignment pass keeps belong to that render's formatter, not to the panel."""
    from rich_click.rich_context import RichContext
    from rich_click.rich_panel import construct_panels

    ctx = cast(RichContext, cli.make_context("cli", [], resilient_parsing=True))
    panels = construct_panels(cli, ctx, ctx.make_formatter())
    panel = next(p for p in panels if p.name == "Options")

    cast(rich_click.Option, cli.params[0]).help = "Changed help."
    formatter = ctx.make_formatter()
    with formatter.console.capture() as capture:
        formatter.console.print(panel.get_table(cli, ctx, formatter))
    assert "Changed help." in capture.get()


def test_aligned_panels_with_the_help_column_in_the_middle(cli_runner: CliRunner) -> None:
    """Every column after the help is flexible, so the ones past it must survive the alignment."""

    @rich_click.command()
    @rich_click.option("--alpha", type=rich_click.Choice(["x", "yyyy"]), help="A.")
    @rich_click.option("--beta-with-a-longer-name", type=rich_click.Path(), help="B.")
    @rich_click.option_panel("One", options=["alpha"], table_styles={"show_header": True})
    @rich_click.option_panel("Two", options=["beta_with_a_longer_name", "help"], table_styles={"show_header": True})
    @rich_click.rich_config({"options_table_column_types": ["opt_long", "help", "metavar"]})
    def cli() -> None:
        """CLI help text"""

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ One ────────────────────────────────────────────────────────────────────────────────────────────╮
│ Opt Long                   Help                               Metavar                            │
│ --alpha                    A.                                 [x|yyyy]                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Two ────────────────────────────────────────────────────────────────────────────────────────────╮
│ Opt Long                   Help                               Metavar                            │
│ --beta-with-a-longer-name  B.                                 PATH                               │
│ --help                     Show this message and exit.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


def test_aligned_panels_without_a_help_column(cli_runner: CliRunner) -> None:
    """With no help column there is nothing to line up, and the panels still render."""

    @rich_click.command()
    @rich_click.option("--alpha", help="A.")
    @rich_click.option("--beta", help="B.")
    @rich_click.option_panel("One", options=["alpha"])
    @rich_click.option_panel("Two", options=["beta", "help"])
    @rich_click.rich_config({"options_table_column_types": ["opt_long"]})
    def cli() -> None:
        """CLI help text"""

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ One ────────────────────────────────────────────────────────────────────────────────────────────╮
│ --alpha                                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Two ────────────────────────────────────────────────────────────────────────────────────────────╮
│ --beta                                                                                           │
│ --help                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


def test_aligned_panels_measure_against_the_panel_padding(cli_runner: CliRunner) -> None:
    """Wide panel padding leaves the table less room, so the columns have to be pinned narrower."""

    @rich_click.command()
    @rich_click.option(
        "--reject-output-outside-source/--no-reject-output-outside-source",
        default=True,
        help="Refuse to write output outside the source tree.",
    )
    @rich_click.option("--format", "-f", type=rich_click.Choice(["svg", "png"]), help="Output format.")
    @rich_click.option("--mode", type=rich_click.Choice(["light", "dark"]), help="Palette.", panel="Layout")
    @rich_click.option("--center-ports/--no-center-ports", help="Centre ports.", panel="Layout")
    @rich_click.rich_config({"style_options_panel_padding": (0, 16)})
    def cli() -> None:
        """CLI help text"""

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Layout ─────────────────────────────────────────────────────────────────────────────────────────╮
│                --mode        [light|dark]        Palette.                                        │
│                --center-ports/--no-center-ports  Centre ports.                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│                --reject-output-outside-source/--no-reject-output-outside-source                  │
│                                                  Refuse to write output outside                  │
│                                                  the source tree.                                │
│                --format  -f  [svg|png]           Output format.                                  │
│                --help                            Show this message and exit.                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


def test_aligned_panels_size_a_column_by_the_entries_that_reach_past_it(cli_runner: CliRunner) -> None:
    """An entry with no short form runs on under that column instead of widening the one before."""

    @rich_click.command()
    @rich_click.option("--zeta", "-z", help="Z.")
    @rich_click.option("--a-flag-with-a-long-name/--no-a-flag-with-a-long-name", help="A.")
    @rich_click.option_panel("One", options=["zeta"])
    @rich_click.option_panel("Two", options=["a_flag_with_a_long_name"])
    def cli() -> None:
        """CLI help text"""

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    lines = result.stdout.splitlines()
    zeta = next(line for line in lines if "--zeta" in line)
    flag_help = next(line for line in lines if " A." in line)
    assert zeta.index("-z ") == zeta.index("--zeta") + len("--zeta") + 2
    assert zeta.index("Z.") == flag_help.index("A.")


def test_aligned_panels_leave_command_panels_alone_when_a_ratio_is_set(
    cli_runner: CliRunner, cli: rich_click.RichCommand
) -> None:
    """An explicit ratio is the user sizing those columns, so alignment has nothing left to decide."""
    baseline = cli_runner.invoke(cli, "--help").stdout
    cli.context_settings["rich_help_config"] = {"style_commands_table_column_width_ratio": (1, 2)}
    with pytest.warns(DeprecationWarning, match="style_commands_table_column_width_ratio"):
        result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0

    def column_of(stdout: str, text: str) -> int:
        return next(line for line in stdout.splitlines() if text in line).index(text)

    assert column_of(result.stdout, "Run the thing.") != column_of(baseline, "Run the thing.")
    # Only command panels opt out; the option panels still line up with each other.
    assert column_of(result.stdout, "Show this message") == column_of(baseline, "Show this message")
