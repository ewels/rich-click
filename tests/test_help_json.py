import json
from typing import Any, Dict, Tuple, cast

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


def test_help_json_reports_secondary_opts_envvar_and_nargs(cli_runner: CliRunner) -> None:
    # secondary_opts (negation flags), envvar, count and variadic/multi nargs must all be surfaced;
    # a plain boolean flag must NOT leak a noisy flag_value=True.
    rc.HELP_JSON = True

    @command()
    @option("--debug/--no-debug", help="Toggle debug.")
    @option("--token", envvar="MY_TOKEN", help="Auth token.")
    @option("-v", "--verbose", count=True, help="Verbosity.")
    @option("--upper", "transform", flag_value="upper")
    @option("--lower", "transform", flag_value="lower")
    @option("--pair", nargs=2, type=str)
    @option("--shout", is_flag=True)
    @argument("files", nargs=-1)
    def cli(
        debug: bool,
        token: str,
        verbose: int,
        transform: str,
        pair: Tuple[str, ...],
        shout: bool,
        files: Tuple[str, ...],
    ) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    by_name = {param["name"]: param for param in schema["params"]}

    assert by_name["debug"]["secondary_opts"] == ["--no-debug"]
    assert by_name["token"]["envvar"] == "MY_TOKEN"
    assert by_name["verbose"]["count"] is True
    assert by_name["files"]["nargs"] == -1
    assert by_name["pair"]["nargs"] == 2
    # Two value-flags share the "transform" destination; each carries its own flag_value.
    flag_values = {param["flag_value"] for param in schema["params"] if param["name"] == "transform"}
    assert flag_values == {"upper", "lower"}
    # Plain boolean flag: no flag_value noise, and nargs==1 stays implied.
    assert "flag_value" not in by_name["shout"]
    assert "nargs" not in by_name["shout"]


def test_help_json_reports_prompt(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True

    @command()
    @option("--name", prompt="Your name", help="Who.")
    def cli(name: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    name = next(param for param in schema["params"] if param["name"] == "name")
    assert name["prompt"] == "Your name"


def test_help_json_type_info_passthrough(cli_runner: CliRunner) -> None:
    # type_info is a straight passthrough of the type's to_info_dict (minus redundant keys), so it stays
    # correct across Click versions. Crucially, a meaningful False (dir_okay) must survive -- it is not
    # treated as "empty" the way other dropped fields are.
    rc.HELP_JSON = True

    from click import IntRange, Path

    @command()
    @option("--level", type=IntRange(0, 10))
    @option("--dest", type=Path(exists=True, dir_okay=False))
    def cli(level: int, dest: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help-json"]).output)
    by_name = {param["name"]: param for param in schema["params"]}

    assert by_name["level"]["type"] == "IntRange"
    assert by_name["level"]["type_info"]["min"] == 0
    assert by_name["level"]["type_info"]["max"] == 10

    assert by_name["dest"]["type"] == "Path"
    assert by_name["dest"]["type_info"]["exists"] is True
    # A False that carries meaning ("must not be a directory") must not be dropped.
    assert by_name["dest"]["type_info"]["dir_okay"] is False


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


def test_help_json_tip_in_regular_help(cli_runner: CliRunner) -> None:
    # When --help-json is enabled, --help advertises it with a footer tip by default.
    rc.HELP_JSON = True
    cli = _build_cli()
    assert "Tip: add --help-json to any command for machine-readable help." in cli_runner.invoke(cli, ["--help"]).output


def test_help_json_tip_absent_when_disabled(cli_runner: CliRunner) -> None:
    # No tip when --help-json itself is not enabled.
    cli = _build_cli()
    assert "machine-readable" not in cli_runner.invoke(cli, ["--help"]).output


def test_help_json_tip_can_be_suppressed(cli_runner: CliRunner) -> None:
    rc.HELP_JSON = True
    rc.HELP_JSON_SHOW_TIP = False
    cli = _build_cli()
    assert "machine-readable" not in cli_runner.invoke(cli, ["--help"]).output


def test_help_json_tip_uses_custom_option_name_and_text(cli_runner: CliRunner) -> None:
    # The tip reflects the actual flag name and a customizable message.
    rc.HELP_JSON = True
    rc.HELP_JSON_OPTION_NAME = "--schema"
    rc.HELP_JSON_TIP_TEXT = "Run {} for JSON."

    @command()
    def cli() -> None:
        """Hi."""

    assert "Run --schema for JSON." in cli_runner.invoke(cli, ["--help"]).output


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
