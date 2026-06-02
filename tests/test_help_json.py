import json

from click.testing import CliRunner

import rich_click.rich_click as rc
from rich_click import RichHelpConfiguration, argument, command, group, option, rich_config


def _build_cli() -> "group":  # type: ignore[valid-type]
    @group()
    @option("-v", "--verbose", is_flag=True, help="Be loud.")
    def cli(verbose: bool) -> None:
        """Root help text."""

    @cli.command()
    @option("--count", type=int, default=3, help="How many times.")
    @argument("name")
    def hello(count: int, name: str) -> None:
        """Say hello."""

    @cli.group(aliases=["sub"])
    def things() -> None:
        """Manage things."""

    @things.command(name="list")
    def list_things() -> None:
        """List things."""

    return cli


def test_help_json_disabled_by_default(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["--help-json"])
    # No such option -> click usage error.
    assert result.exit_code == 2
    assert "--help-json" not in cli_runner.invoke(cli, ["--help"]).output


def test_help_json_root(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["--help-json"])
    assert result.exit_code == 0

    schema = json.loads(result.output)
    assert schema["name"] == "cli"
    assert schema["help"] == "Root help text."
    assert schema["usage"].startswith("cli")

    # Regular options are reported; meta-options are hidden.
    param_opts = [opt for param in schema["params"] for opt in param["opts"]]
    assert "--verbose" in param_opts
    assert "--help" not in param_opts
    assert "--help-json" not in param_opts

    # Subcommands are indexed recursively by name, groups nesting their children.
    assert schema["subcommands"] == {"hello": {}, "things": {"list": {}}}


def test_help_json_leaf(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["hello", "--help-json"])
    assert result.exit_code == 0

    schema = json.loads(result.output)
    assert schema["name"] == "hello"
    assert schema["path"] == "cli hello"
    assert "subcommands" not in schema

    by_name = {param["name"]: param for param in schema["params"]}
    assert by_name["count"]["default"] == 3
    assert by_name["count"]["help"] == "How many times."
    # The positional argument is reported as an argument and is required.
    assert by_name["name"]["kind"] == "argument"
    assert by_name["name"]["required"] is True


def test_help_json_group_reports_aliases(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["things", "--help-json"])
    assert result.exit_code == 0

    schema = json.loads(result.output)
    assert schema["aliases"] == ["sub"]
    assert schema["subcommands"] == {"list": {}}

    # The same schema is reachable via the alias.
    via_alias = json.loads(cli_runner.invoke(cli, ["sub", "--help-json"]).output)
    assert via_alias["name"] == "things"


def test_help_json_appears_in_regular_help(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    cli = _build_cli()
    assert "--help-json" in cli_runner.invoke(cli, ["--help"]).output


def test_help_json_custom_option_name(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    rc.HELP_JSON_OPTION_NAME = "--schema"

    @command()
    def cli() -> None:
        """Hi."""

    assert cli_runner.invoke(cli, ["--schema"]).exit_code == 0
    assert cli_runner.invoke(cli, ["--help-json"]).exit_code == 2
    assert "--schema" in cli_runner.invoke(cli, ["--help"]).output


def test_help_json_via_rich_config(cli_runner: CliRunner) -> None:
    @command()
    @rich_config(help_config=RichHelpConfiguration(help_json=True))
    def cli() -> None:
        """Hi."""

    result = cli_runner.invoke(cli, ["--help-json"])
    assert result.exit_code == 0
    assert json.loads(result.output)["name"] == "cli"
