import json
from typing import Any, Dict

import click
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
    # Output is a JSON Schema document.
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["type"] == "object"
    assert schema["title"] == "cli"
    assert schema["description"] == "Root help text."
    assert schema["x-usage"].startswith("cli")

    # Regular options become JSON Schema properties; meta-options are hidden.
    assert "verbose" in schema["properties"]
    all_opts = [opt for prop in schema["properties"].values() for opt in prop["x-cli"]["opts"]]
    assert "--verbose" in all_opts
    assert "--help" not in all_opts
    assert "--help-json" not in all_opts

    # Subcommands are indexed recursively by name, groups nesting their children.
    assert schema["x-subcommands"] == {"hello": {}, "things": {"list": {}}}


def test_help_json_leaf(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["hello", "--help-json"])
    assert result.exit_code == 0

    schema = json.loads(result.output)
    assert schema["title"] == "cli hello"
    assert "x-subcommands" not in schema

    props = schema["properties"]
    assert props["count"]["type"] == "integer"
    assert props["count"]["default"] == 3
    assert props["count"]["description"] == "How many times."
    # The positional argument is reported as an argument and is required (at the schema level).
    assert props["name"]["x-cli"]["kind"] == "argument"
    assert schema["required"] == ["name"]


def test_help_json_choice_becomes_enum(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True

    from click import Choice

    @command()
    @option("--fmt", type=Choice(["json", "yaml"]), default="json", help="Output format.")
    def cli(fmt: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    assert schema["properties"]["fmt"]["enum"] == ["json", "yaml"]
    assert schema["properties"]["fmt"]["default"] == "json"


def test_help_json_group_reports_aliases(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["things", "--help-json"])
    assert result.exit_code == 0

    schema = json.loads(result.output)
    # rich-click's `aliases` flows through to_info_dict() as an x- extension.
    assert schema["x-aliases"] == ["sub"]
    assert schema["x-subcommands"] == {"list": {}}

    # The same command is reachable via the alias; the title reflects how it was invoked.
    via_alias = json.loads(cli_runner.invoke(cli, ["sub", "--help-json"]).output)
    assert via_alias["title"] == "cli sub"
    assert via_alias["description"] == schema["description"]
    assert via_alias["x-subcommands"] == schema["x-subcommands"]


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


def test_help_json_excludes_customized_help_option(cli_runner: CliRunner) -> None:
    # The help/meta options are excluded by object identity, so a non-default help
    # option name (here `-h`) must still be kept out of the reported params.
    rc.HELP_JSON = True

    @command(context_settings={"help_option_names": ["-h", "--help"]})
    @option("--real", help="A real option.")
    def cli(real: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    all_opts = [opt for prop in schema["properties"].values() for opt in prop["x-cli"]["opts"]]
    assert all_opts == ["--real"]


def test_help_json_via_rich_config(cli_runner: CliRunner) -> None:
    @command()
    @rich_config(help_config=RichHelpConfiguration(help_json=True))
    def cli() -> None:
        """Hi."""

    result = cli_runner.invoke(cli, ["--help-json"])
    assert result.exit_code == 0
    assert json.loads(result.output)["title"] == "cli"


def test_help_json_passthrough_of_custom_fields(cli_runner: CliRunner) -> None:
    # Anything a developer adds to to_info_dict() flows through: custom command-level keys
    # become x-<key>, and custom parameter-level keys land in that parameter's x-cli object.
    rc.HELP_JSON = True

    from rich_click import RichCommand, RichOption

    class SecretOption(RichOption):
        def to_info_dict(self) -> "Dict[str, Any]":
            info = super().to_info_dict()
            info["sensitive"] = True
            return info

    class DocumentedCommand(RichCommand):
        def to_info_dict(self, ctx: "click.Context") -> "Dict[str, Any]":
            info = super().to_info_dict(ctx)
            info["examples"] = ["cli --token=XXX"]
            return info

    @command(cls=DocumentedCommand)
    @option("--token", cls=SecretOption, help="API token.")
    def cli(token: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    assert schema["x-examples"] == ["cli --token=XXX"]
    assert schema["properties"]["token"]["x-cli"]["sensitive"] is True


def test_help_json_hidden_param_is_kept_and_flagged(cli_runner: CliRunner) -> None:
    # Hidden params are kept (parity with to_info_dict) but marked hidden so consumers can skip them.
    rc.HELP_JSON = True

    @command()
    @option("--secret", hidden=True, help="Internal.")
    @option("--shown", help="Public.")
    def cli(secret: str, shown: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    assert schema["properties"]["secret"]["x-cli"]["hidden"] is True
    assert "hidden" not in schema["properties"]["shown"]["x-cli"]


def test_help_json_transform_hook(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    rc.HELP_JSON_TRANSFORM = lambda schema, cmd, ctx: {**schema, "x-version": "1.2.3"}

    @command()
    def cli() -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    assert schema["x-version"] == "1.2.3"
