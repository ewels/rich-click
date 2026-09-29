from __future__ import annotations

import json
from typing import Any

import click
import pytest
from click.testing import CliRunner

from rich_click import RichHelpConfiguration, argument, group, option, rich_config, search_help_option
from rich_click.help_search import MAX_RESULTS, search_schemas
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
    assert result.output.startswith("# plarv crell [aliases: cl] — Create a record.")
    assert "--wover INTEGER  Weight of the record." in result.output


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


def test_search_help_renders_a_panel_for_humans() -> None:
    result = CliRunner().invoke(make_cli(), ["--search-help", "weight"])
    assert result.exit_code == 0
    assert "Commands matching 'weight'" in result.output
    assert "cli plarv crell" in result.output
    assert "Create a record." in result.output


def test_unsupported_format_falls_back_to_the_panel() -> None:
    result = CliRunner().invoke(make_cli(), ["--search-help", "weight", "--help", "nope"])
    assert "Commands matching 'weight'" in result.output


def test_disabled_format_falls_back_to_the_panel() -> None:
    cli = make_cli(help_formats=["compact"])
    result = CliRunner().invoke(cli, ["--search-help", "weight", "--help", "json"])
    assert "Commands matching 'weight'" in result.output


def test_search_help_with_legacy_help_flag() -> None:
    cli = make_cli(help_formats=False)
    result = CliRunner().invoke(cli, ["--help", "--search-help", "weight"])
    assert result.exit_code == 0
    assert "Commands matching 'weight'" in result.output


def test_agent_gets_the_agent_help_format(agent_env: ConfigureAgentEnv) -> None:
    agent_env(override="true")
    result = CliRunner().invoke(make_cli(), ["--search-help", "weight"])
    assert result.output.startswith("# plarv crell [aliases: cl] — Create a record.")


def test_search_schemas_limits_and_filters_results() -> None:
    leaves = {
        f"cmd{i}": {"name": f"cmd{i}", "path": f"cli cmd{i}", "help": "Shared words.", "params": []} for i in range(8)
    }
    root = {"name": "cli", "path": "cli", "params": [], "subcommands": leaves}
    assert len(search_schemas(root, "shared")) == MAX_RESULTS
    assert search_schemas(root, "the and of") == []
    assert search_schemas(root, "nothing") == []
