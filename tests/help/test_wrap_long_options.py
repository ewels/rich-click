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


def _help_is_inline(stdout: str, entry: str, help_text: str) -> bool:
    line = next(line for line in stdout.splitlines() if entry in line)
    return help_text in line


def test_wrap_long_options_fraction_scales_with_the_terminal(
    cli_runner: CliRunner, cli: rich_click.RichCommand
) -> None:
    """A float is a share of the panel, so a wide terminal keeps inline what a narrow one wraps."""
    entry, help_text = "--reject-output-outside-source", "Refuse to write output"

    cli.context_settings["rich_help_config"] = {"wrap_long_options": 0.5, "width": 200}
    wide = cli_runner.invoke(cli, "--help")
    cli.context_settings["rich_help_config"] = {"wrap_long_options": 0.5, "width": 100}
    narrow = cli_runner.invoke(cli, "--help")

    assert _help_is_inline(wide.stdout, entry, help_text)
    assert not _help_is_inline(narrow.stdout, entry, help_text)


def test_wrap_long_options_int_ignores_the_terminal_width(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    """An int is a count of characters, so the same entry wraps however wide the terminal is."""
    entry, help_text = "--reject-output-outside-source", "Refuse to write output"

    for width in (100, 200):
        cli.context_settings["rich_help_config"] = {"wrap_long_options": 24, "width": width}
        result = cli_runner.invoke(cli, "--help")
        assert not _help_is_inline(result.stdout, entry, help_text)


def test_wrap_long_options_callable_is_given_the_panel_width(
    cli_runner: CliRunner, cli: rich_click.RichCommand
) -> None:
    widths: list[int] = []

    def threshold(width: int) -> int:
        widths.append(width)
        return 10_000

    cli.context_settings["rich_help_config"] = {"wrap_long_options": threshold, "width": 100}
    result = cli_runner.invoke(cli, "--help")

    assert result.exit_code == 0
    assert widths and all(0 < width < 100 for width in widths)
    assert _help_is_inline(result.stdout, "--reject-output-outside-source", "Refuse to write output")


def test_wrap_long_options_keeps_row_styles_in_step_across_a_split(
    cli_runner: CliRunner, cli: rich_click.RichCommand
) -> None:
    """Each block of a split panel is its own table, so its row styles have to carry on from the last."""
    cli.context_settings["rich_help_config"] = {
        "style_options_table_row_styles": ["", "on grey19"],
        "color_system": "standard",
    }
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0

    def is_styled(entry: str) -> bool:
        line = next(line for line in result.stdout.splitlines() if entry in line)
        return "\x1b[100m" in line

    # The long entry is row 0 of the panel, so the three rows below it carry on alternating from it.
    assert [is_styled("--format"), is_styled("--out"), is_styled("--help")] == [True, False, True]


def test_wrap_long_options_indents_the_next_line_head_past_the_empty_columns(cli_runner: CliRunner) -> None:
    """A row leaving the required column empty still has to clear it, as every other row does."""

    @rich_click.command()
    @rich_click.option("--needed", required=True, help="Required, so the group keeps a marker column.")
    @rich_click.option("--short", "-s", help="Short enough to stay inline.")
    @rich_click.option(
        "--an-option-with-a-name-long-enough-to-wrap",
        "-a",
        metavar="A|LONG|CHOICE|METAVAR",
        help="Long enough to lose its help to the line below.",
    )
    @rich_click.option_panel("Required", options=["needed"])
    @rich_click.option_panel("Other", options=["short", "an_option_with_a_name_long_enough_to_wrap"])
    def cli() -> None:
        """CLI help text"""

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    lines = result.stdout.splitlines()
    head = next(line for line in lines if "--an-option-with-a-name" in line)
    assert head.index("--an-option-with-a-name") == next(line for line in lines if "--short" in line).index("--short")
    # The marker column is only there because a sibling panel has a required option.
    assert head.index("--an-option-with-a-name") > next(line for line in lines if "--needed" in line).index("*") + 1


def test_wrap_long_options_keeps_the_next_line_head_in_its_columns(cli_runner: CliRunner) -> None:
    """Only the over-wide cell leaves its column; the cells that fit stay lined up with the rows."""

    @rich_click.command()
    @rich_click.option("--comment", "-b", metavar="TEXT", help="Short enough to stay inline.")
    # Widens the name column past --template, so that only the metavar is over-wide.
    @rich_click.option("--sample-filters", "-s", metavar="PATH", help="Also inline.")
    @rich_click.option(
        "--template",
        "-t",
        type=rich_click.Choice(["default", "disco", "gathered", "geo", "original", "sections"]),
        help="A choice metavar too wide for its column.",
    )
    def cli() -> None:
        """CLI help text"""

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    lines = result.stdout.splitlines()
    comment = next(line for line in lines if "--comment" in line)
    template = next(line for line in lines if "--template" in line)

    def short_at(line: str, name: str, short: str) -> int:
        return line.index(short, line.index(name) + len(name))

    # The head sits on its own line, so its help is on the next one.
    assert "A choice metavar" not in template
    assert template.index("--template") == comment.index("--comment")
    assert short_at(template, "--template", "-t") == short_at(comment, "--comment", "-b")
