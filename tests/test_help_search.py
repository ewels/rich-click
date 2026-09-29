from __future__ import annotations

import json
from typing import Any

import click
import pytest
from click.testing import CliRunner

from rich_click import RichHelpConfiguration, argument, command, group, option, rich_config, search_help_option
from rich_click.help_search import SearchSettings, search_schemas
from tests.conftest import ConfigureAgentEnv


def make_cli(search: bool = True, **config: Any) -> Any:
    @group()
    def cli() -> None:
        """Manage records and stores."""

    if search:
        cli = search_help_option()(cli)
    if config:
        cli = rich_config(help_config=RichHelpConfiguration(**config))(cli)

    @cli.group()
    def plarv() -> None:
        """Work with records."""

    @plarv.command(aliases=["cl"], examples=[("Create a record", "cli plarv crell --crull 'north ledger'")])
    @option("--crull", required=True, help="Annotation text for the record.")
    @option("--wover", type=int, default=7, help="Weight of the record.")
    def crell(crull: str, wover: int) -> None:
        """Create a record."""

    @plarv.command()
    @argument("record_id")
    def drop(record_id: str) -> None:
        """Delete a record permanently."""

    @cli.group()
    @search_help_option()
    def stores() -> None:
        """Manage stores."""

    @stores.command()
    @option("--path", help="Where to create the store.")
    def init(path: str) -> None:
        """Initialise an empty store."""

    return cli


def test_search_help_is_opt_in() -> None:
    runner = CliRunner()
    cli = make_cli(search=False)
    assert "--search-help" not in runner.invoke(cli, ["--help"]).output
    result = runner.invoke(cli, ["--search-help", "record"])
    assert result.exit_code == 2
    assert "No such option" in result.output


def test_search_help_is_listed_like_any_other_option() -> None:
    runner = CliRunner()
    cli = make_cli()
    output = runner.invoke(cli, ["--help"]).output
    assert "--search-help" in output
    # Like --version, only on the command it decorates.
    assert "--search-help" not in runner.invoke(cli, ["plarv", "--help"]).output
    compact = runner.invoke(cli, ["--help", "compact"]).output
    assert "--search-help QUERY  Search all subcommands" in compact


def test_custom_option_names() -> None:
    @group()
    @search_help_option("--find", "-f", help="Find a command.")
    def cli() -> None:
        """Root."""

    @cli.command()
    def weigh() -> None:
        """Weigh something."""

    runner = CliRunner()
    assert "Find a command." in runner.invoke(cli, ["--help"]).output
    assert runner.invoke(cli, ["-f", "weigh", "--help", "compact"]).output.startswith("# weigh — Weigh something.")


def test_plain_click_group() -> None:
    @click.group()
    @search_help_option()
    def cli() -> None:
        """Root."""

    @cli.command()
    def weigh() -> None:
        """Weigh something."""

    result = CliRunner().invoke(cli, ["--search-help", "weigh"])
    assert result.exit_code == 0
    assert result.output.startswith("# weigh — Weigh something.")


def test_search_help_ranks_the_best_match_first() -> None:
    result = CliRunner().invoke(make_cli(), ["--search-help", "delete a record", "--help", "compact"])
    assert result.exit_code == 0
    assert result.output.startswith("# plarv drop — Delete a record permanently.")


def test_search_help_matches_option_help() -> None:
    result = CliRunner().invoke(make_cli(), ["--search-help", "weight", "--help", "compact"])
    lines = result.output.splitlines()
    assert lines[0] == "# plarv crell [aliases: cl] — Create a record."
    # The matching option comes first; the rest follow in their declared order.
    assert lines[1] == "--wover INTEGER  Weight of the record."
    assert lines[2] == "*--crull TEXT  Annotation text for the record."


@pytest.mark.parametrize(
    "args", [["--search-help", "store", "--help", "json"], ["--help", "json", "--search-help", "store"]]
)
def test_help_picks_the_format_in_either_order(args: list[str]) -> None:
    result = CliRunner().invoke(make_cli(), args)
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert data["query"] == "store"
    paths = [item["path"] for item in data["results"]]
    assert set(paths) == {"cli stores", "cli stores init"}
    stores = next(item for item in data["results"] if item["path"] == "cli stores")
    assert stores["subcommands"] == ["init"]
    assert not any("is_help_option" in param for item in data["results"] for param in item["params"])


def test_search_help_markdown() -> None:
    result = CliRunner().invoke(make_cli(), ["--search-help", "weight", "--help", "markdown"])
    assert result.output.startswith("# `cli plarv crell`")
    assert "| `--wover` |" in result.output


def test_search_help_is_scoped_to_the_group() -> None:
    result = CliRunner().invoke(make_cli(), ["stores", "--search-help", "record", "--help", "compact"])
    assert result.output.strip() == "No commands under 'cli stores' match 'record'."


def test_several_matches_render_a_results_panel() -> None:
    result = CliRunner().invoke(make_cli(), ["--search-help", "record"])
    assert result.exit_code == 0
    assert "Commands matching 'record'" in result.output
    assert "cli plarv crell" in result.output
    assert "Create a record." in result.output
    # The best-matching options are listed under their command.
    assert "--crull" in result.output


def test_one_clear_match_renders_its_help_with_matching_options_first() -> None:
    result = CliRunner().invoke(make_cli(), ["--search-help", "weight"])
    assert result.exit_code == 0
    output = result.output
    assert "Usage: cli plarv crell" in output
    assert "Matching options (1 of 2)" in output
    # Nothing is hidden: the author's own panel still lists every option, --wover included.
    assert output.index("Matching options") < output.index("Options ─")
    assert output.count("--wover") == 2
    assert "--crull" in output


def test_single_command_cli_can_be_searched() -> None:
    @command()
    @search_help_option()
    @option("--alpha", help="First letter.")
    @option("--zulu", help="Last letter of the alphabet.")
    def cli(alpha: str, zulu: str) -> None:
        """One command, many options."""

    runner = CliRunner()
    compact = runner.invoke(cli, ["--search-help", "last letter", "--help", "compact"]).output
    lines = compact.splitlines()
    assert lines[0].startswith("# cli")
    # Ranked, not filtered: --zulu matched best so it comes first, and --alpha is still listed.
    assert lines[1].startswith("--zulu") and lines[2].startswith("--alpha")
    assert "Matching options (2 of 2)" in runner.invoke(cli, ["--search-help", "last letter"]).output


def test_search_help_does_not_match_itself() -> None:
    result = CliRunner().invoke(make_cli(), ["--search-help", "search query", "--help", "compact"])
    assert result.output.strip() == "No commands under 'cli' match 'search query'."


def test_json_marks_matching_params_with_their_rank() -> None:
    result = CliRunner().invoke(make_cli(), ["--search-help", "weight", "--help", "json"])
    crell = json.loads(result.output)["results"][0]
    ranks = {param["name"]: param.get("match_rank") for param in crell["params"]}
    assert ranks["wover"] == 1
    assert ranks["crull"] is None


def test_matched_words_are_highlighted() -> None:
    from rich.console import Console
    from rich.text import Text

    from rich_click.help_search import SearchHighlight, highlight_pattern

    pattern = highlight_pattern("output formats")
    assert pattern is not None
    assert pattern.findall("--output-format sets the Output FORMAT; outputs too, but not reformat") == [
        "output",
        "format",
        "Output",
        "FORMAT",
        "outputs",
    ]
    console = Console(width=60, color_system="truecolor", force_terminal=True)
    segments = list(console.render(SearchHighlight(Text("write output here"), pattern, "underline")))
    underlined = [segment.text for segment in segments if segment.style and segment.style.underline]
    assert underlined == ["output"]


def test_unsupported_format_falls_back_to_terminal_output() -> None:
    result = CliRunner().invoke(make_cli(), ["--search-help", "weight", "--help", "nope"])
    assert "Matching options (1 of 2)" in result.output


def test_disabled_format_falls_back_to_terminal_output() -> None:
    cli = make_cli(help_formats=["compact"])
    result = CliRunner().invoke(cli, ["--search-help", "weight", "--help", "json"])
    assert "Matching options (1 of 2)" in result.output


def test_search_help_with_legacy_help_flag() -> None:
    cli = make_cli(help_formats=False)
    result = CliRunner().invoke(cli, ["--help", "--search-help", "weight"])
    assert result.exit_code == 0
    assert "Matching options (1 of 2)" in result.output


def test_agent_gets_the_agent_help_format(agent_env: ConfigureAgentEnv) -> None:
    agent_env(override="true")
    result = CliRunner().invoke(make_cli(), ["--search-help", "weight"])
    assert result.output.startswith("# plarv crell [aliases: cl] — Create a record.")


def test_search_schemas_limits_and_filters_results() -> None:
    leaves = {
        f"cmd{i}": {"name": f"cmd{i}", "path": f"cli cmd{i}", "help": "Shared words.", "params": []} for i in range(8)
    }
    root = {"name": "cli", "path": "cli", "params": [], "subcommands": leaves}
    assert len(search_schemas(root, "shared")) == SearchSettings().max_results
    assert len(search_schemas(root, "shared", SearchSettings(max_results=2))) == 2
    assert search_schemas(root, "the and of") == []
    assert search_schemas(root, "nothing") == []


def make_single_command(**settings: Any) -> Any:
    @command()
    @search_help_option(**settings)
    @option("--alpha", help="First letter.")
    @option("--zulu", help="Last letter of the alphabet.")
    def cli(alpha: str, zulu: str) -> None:
        """One command, many options."""

    return cli


def test_rank_options_off_keeps_declared_order() -> None:
    runner = CliRunner()
    cli = make_single_command(rank_options=False)
    output = runner.invoke(cli, ["--search-help", "last letter", "--help", "compact"]).output
    assert output.index("--alpha") < output.index("--zulu")
    assert "Matching options" not in runner.invoke(cli, ["--search-help", "last letter"]).output
    data = json.loads(runner.invoke(cli, ["--search-help", "last letter", "--help", "json"]).output)
    assert not any("match_rank" in param for param in data["results"][0]["params"])


def test_matching_options_zero_drops_the_panel() -> None:
    output = CliRunner().invoke(make_single_command(matching_options=0), ["--search-help", "last letter"]).output
    assert "Usage: cli" in output
    assert "Matching options" not in output


def test_single_match_help_off_always_uses_the_results_panel() -> None:
    output = CliRunner().invoke(make_single_command(single_match_help=False), ["--search-help", "zulu"]).output
    assert "Commands matching 'zulu'" in output
    assert "--zulu" in output


def test_options_per_result_zero_lists_commands_only() -> None:
    output = (
        CliRunner()
        .invoke(make_single_command(single_match_help=False, options_per_result=0), ["--search-help", "zulu"])
        .output
    )
    assert "Commands matching 'zulu'" in output
    assert "--zulu" not in output


def test_highlight_off() -> None:
    from rich_click.rich_help_formatter import RichHelpFormatter

    seen: list[object] = []
    original = RichHelpFormatter.write

    def spy(self: RichHelpFormatter, *objects: Any, **kwargs: Any) -> None:
        seen.append(self.search_highlight)
        original(self, *objects, **kwargs)

    RichHelpFormatter.write = spy  # type: ignore[method-assign]
    try:
        runner = CliRunner()
        runner.invoke(make_single_command(), ["--search-help", "zulu"])
        assert any(pattern is not None for pattern in seen)
        seen.clear()
        runner.invoke(make_single_command(highlight=False), ["--search-help", "zulu"])
        assert seen and all(pattern is None for pattern in seen)
    finally:
        RichHelpFormatter.write = original  # type: ignore[method-assign]


def test_search_own_options_off() -> None:
    @group()
    @search_help_option(search_own_options=False)
    @option("--verbose", is_flag=True, help="Chatty logging.")
    def cli(verbose: bool) -> None:
        """Root."""

    @cli.command()
    def weigh() -> None:
        """Weigh something."""

    output = CliRunner().invoke(cli, ["--search-help", "chatty logging", "--help", "compact"]).output
    assert output.strip() == "No commands under 'cli' match 'chatty logging'."
