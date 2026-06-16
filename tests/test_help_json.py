import json
from typing import Any, Dict, cast

import click
from click.testing import CliRunner

import rich_click.rich_click as rc
from rich_click import RichHelpConfiguration, argument, command, group, option, rich_config
from rich_click.rich_context import RichContext


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

    # Subcommands are indexed recursively by name, each entry carrying a one-line help (and
    # aliases / nested subcommands where present), so an agent can navigate without round-trips.
    assert schema["subcommands"] == {
        "hello": {"help": "Say hello."},
        "things": {"help": "Manage things.", "aliases": ["sub"], "subcommands": {"list": {"help": "List things."}}},
    }


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
    # The positional argument is reported as an argument and is required. It carries no `opts`
    # (those would just repeat the name); only options report their flags.
    assert by_name["name"]["kind"] == "argument"
    assert by_name["name"]["required"] is True
    assert "opts" not in by_name["name"]
    assert "opts" in by_name["count"]


def test_help_json_choice(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True

    from click import Choice

    @command()
    @option("--fmt", type=Choice(["json", "yaml"]), default="json", help="Output format.")
    def cli(fmt: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    fmt = next(param for param in schema["params"] if param["name"] == "fmt")
    assert fmt["type"] == "Choice"
    assert fmt["choices"] == ["json", "yaml"]
    assert fmt["default"] == "json"


def test_help_json_group_reports_aliases(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["things", "--help-json"])
    assert result.exit_code == 0

    schema = json.loads(result.output)
    # rich-click's `aliases` flows through to_info_dict() as a passthrough field.
    assert schema["aliases"] == ["sub"]
    assert schema["subcommands"] == {"list": {"help": "List things."}}

    # The same command is reachable via the alias.
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


def test_help_json_excludes_customized_help_option(cli_runner: CliRunner) -> None:
    # The help/meta options are excluded by object identity, so a non-default help
    # option name (here `-h`) must still be kept out of the reported params.
    rc.HELP_JSON = True

    @command(context_settings={"help_option_names": ["-h", "--help"]})
    @option("--real", help="A real option.")
    def cli(real: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    param_opts = [opt for param in schema["params"] for opt in param["opts"]]
    assert param_opts == ["--real"]


def test_help_json_via_rich_config(cli_runner: CliRunner) -> None:
    @command()
    @rich_config(help_config=RichHelpConfiguration(help_json=True))
    def cli() -> None:
        """Hi."""

    result = cli_runner.invoke(cli, ["--help-json"])
    assert result.exit_code == 0
    assert json.loads(result.output)["name"] == "cli"


def test_help_json_passthrough_of_custom_fields(cli_runner: CliRunner) -> None:
    # Anything a developer adds to to_info_dict() flows through: custom command-level keys are
    # merged onto the top-level object, and custom parameter-level keys onto the parameter.
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
    assert schema["examples"] == ["cli --token=XXX"]
    token = next(param for param in schema["params"] if param["name"] == "token")
    assert token["sensitive"] is True


def test_help_json_hidden_param_is_kept_and_flagged(cli_runner: CliRunner) -> None:
    # Hidden params are kept (parity with to_info_dict) but marked hidden so consumers can skip them.
    rc.HELP_JSON = True

    @command()
    @option("--secret", hidden=True, help="Internal.")
    @option("--shown", help="Public.")
    def cli(secret: str, shown: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    by_name = {param["name"]: param for param in schema["params"]}
    assert by_name["secret"]["hidden"] is True
    assert "hidden" not in by_name["shown"]


def test_help_json_omits_help_when_undocumented(cli_runner: CliRunner) -> None:
    # An undocumented command omits `help` entirely rather than emitting a null.
    rc.HELP_JSON = True

    @command()
    def cli() -> None:
        pass

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    assert "help" not in schema


def test_help_json_option_names_via_context_settings(cli_runner: CliRunner) -> None:
    # `help_json_option_names` in context_settings enables --help-json (parallel to click's
    # `help_option_names`), without needing the `help_json` config, and sets custom flag name(s).
    @command(context_settings={"help_json_option_names": ["--schema", "--meta"]})
    @option("--real", help="A real option.")
    def cli(real: str) -> None:
        """Hi."""

    assert cli_runner.invoke(cli, ["--schema"]).exit_code == 0
    assert cli_runner.invoke(cli, ["--meta"]).exit_code == 0
    # The default flag is not added when custom names are supplied.
    assert cli_runner.invoke(cli, ["--help-json"]).exit_code == 2

    schema = json.loads(cli_runner.invoke(cli, ["--schema"]).output)
    assert schema["name"] == "cli"
    # The custom meta-flags are kept out of the reported params.
    param_opts = [opt for param in schema["params"] for opt in param["opts"]]
    assert param_opts == ["--real"]


def test_help_json_option_names_takes_precedence_over_config(cli_runner: CliRunner) -> None:
    # When both are set, the context_settings names win over the rich config name.
    rc.HELP_JSON = True
    rc.HELP_JSON_OPTION_NAME = "--from-config"

    @command(context_settings={"help_json_option_names": ["--from-ctx"]})
    def cli() -> None:
        """Hi."""

    assert cli_runner.invoke(cli, ["--from-ctx"]).exit_code == 0
    assert cli_runner.invoke(cli, ["--from-config"]).exit_code == 2


def test_help_json_format_help_json_override(cli_runner: CliRunner) -> None:
    # `--help-json` serializes whatever `format_help_json` returns, mirroring click's
    # get_help/format_help split, so subclasses can customize the schema by overriding it.
    rc.HELP_JSON = True

    from rich_click import RichCommand

    class MyCommand(RichCommand):
        def format_help_json(self, ctx: Any, formatter: Any) -> Dict[str, Any]:
            data = super().format_help_json(ctx, formatter)
            data["custom"] = "yes"
            return data

    @command(cls=MyCommand)
    def cli() -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    assert schema["custom"] == "yes"
    assert schema["name"] == "cli"


def test_help_json_get_help_json_direct(cli_runner: CliRunner) -> None:
    # get_help_json() can be called directly (e.g. by alternative output paths) and returns
    # the same JSON string the --help-json flag prints.
    rc.HELP_JSON = True

    @command()
    @option("--count", type=int, default=1, help="How many.")
    def cli(count: int) -> None:
        """Hi."""

    with cli.make_context("cli", []) as ctx:
        direct = json.loads(cli.get_help_json(cast(RichContext, ctx)))

    via_flag = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    assert direct == via_flag
    assert direct["name"] == "cli"


def test_help_json_transform_hook(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    rc.HELP_JSON_TRANSFORM = lambda schema, cmd, ctx: {**schema, "version": "1.2.3"}

    @command()
    def cli() -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    assert schema["version"] == "1.2.3"
