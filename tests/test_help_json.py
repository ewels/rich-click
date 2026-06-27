import json
from typing import Any, Dict, Set, Tuple, cast

import click
import pytest
from click.testing import CliRunner

import rich_click.rich_click as rc
from rich_click import RichCommand, argument, command, group, option
from rich_click.rich_context import RichContext


def _build_cli() -> RichCommand:
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

    return cast(RichCommand, cli)


# --------------------------------------------------------------------------------------------------
# `--help=json`: progressive disclosure. Available on every rich-click CLI without any config -- the
# capability lives on the always-present `--help` flag, so there is no new flag and bare `--help` is
# unchanged. Only the attached (`=`) form is documented.
# --------------------------------------------------------------------------------------------------


def test_help_json_root(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["--help=json"])
    assert result.exit_code == 0

    schema = json.loads(result.output)
    assert schema["name"] == "cli"
    assert schema["help"] == "Root help text."
    assert schema["usage"].startswith("cli")

    # Regular options are reported, and so is the --help meta-option (like the rendered help screen),
    # carrying the machine-readable formats it accepts as its choices.
    param_opts = [opt for param in schema["params"] for opt in param["opts"]]
    assert "--verbose" in param_opts
    help_param = next(param for param in schema["params"] if param["name"] == "help")
    assert help_param["opts"] == ["--help"]
    assert "markdown" in help_param["choices"] and "json" in help_param["choices"]

    # Subcommands are indexed recursively by name, each entry carrying a one-line help (and
    # aliases / nested subcommands where present), so an agent can navigate without round-trips.
    assert schema["subcommands"] == {
        "hello": {"help": "Say hello."},
        "things": {"help": "Manage things.", "aliases": ["sub"], "subcommands": {"list": {"help": "List things."}}},
    }


def test_help_json_works_without_any_config(cli_runner: CliRunner) -> None:
    # No config is set anywhere: `--help=json` still works, because the format capability hangs off the
    # always-present `--help` flag rather than an opt-in flag.
    @command()
    @option("--name", help="A name.")
    def cli(name: str) -> None:
        """Hi."""

    result = cli_runner.invoke(cli, ["--help=json"])
    assert result.exit_code == 0
    assert json.loads(result.output)["name"] == "cli"


def test_no_new_flag_is_added(cli_runner: CliRunner) -> None:
    # The feature adds no `--help-json` (or similar) flag: only `--help` is modified.
    cli = _build_cli()
    assert cli_runner.invoke(cli, ["--help-json"]).exit_code == 2  # no such option
    assert "--help-json" not in cli_runner.invoke(cli, ["--help"]).output


def test_bare_help_is_unchanged_and_eager(cli_runner: CliRunner) -> None:
    # The format machinery only engages with an attached value; bare `--help` is the normal help, exits
    # 0, carries no `--help TEXT` metavar, and -- being eager -- works with a required argument missing.
    cli = _build_cli()
    plain = cli_runner.invoke(cli, ["--help"])
    assert plain.exit_code == 0
    assert plain.output.lstrip().startswith("Usage:")
    assert "{" not in plain.output.split("Options")[0]  # no JSON leaked into the help body
    help_row = next(line for line in plain.output.splitlines() if "--help " in line or line.strip().endswith("--help"))
    assert "TEXT" not in help_row
    # Eager even with a required argument absent.
    eager = cli_runner.invoke(cli, ["hello", "--help=json"])
    assert eager.exit_code == 0
    assert json.loads(eager.output)["name"] == "hello"


def test_help_json_leaf(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["hello", "--help=json"])
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
    from click import Choice

    @command()
    @option("--fmt", type=Choice(["json", "yaml"]), default="json", help="Output format.")
    def cli(fmt: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    fmt = next(param for param in schema["params"] if param["name"] == "fmt")
    assert fmt["type"] == "Choice"
    assert fmt["choices"] == ["json", "yaml"]
    assert fmt["default"] == "json"


def test_help_json_reports_secondary_opts_envvar_and_nargs(cli_runner: CliRunner) -> None:
    # secondary_opts (negation flags), envvar, count and variadic/multi nargs must all be surfaced;
    # a plain boolean flag must NOT leak a noisy flag_value=True.
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

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
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
    @command()
    @option("--name", prompt="Your name", help="Who.")
    def cli(name: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    name = next(param for param in schema["params"] if param["name"] == "name")
    assert name["prompt"] == "Your name"


def test_help_json_type_info_passthrough(cli_runner: CliRunner) -> None:
    # type_info is a straight passthrough of the type's to_info_dict (minus redundant keys), so it stays
    # correct across Click versions. Crucially, a meaningful False (dir_okay) must survive -- it is not
    # treated as "empty" the way other dropped fields are.
    from click import IntRange, Path

    @command()
    @option("--level", type=IntRange(0, 10))
    @option("--dest", type=Path(exists=True, dir_okay=False))
    def cli(level: int, dest: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    by_name = {param["name"]: param for param in schema["params"]}

    assert by_name["level"]["type"] == "IntRange"
    assert by_name["level"]["type_info"]["min"] == 0
    assert by_name["level"]["type_info"]["max"] == 10

    assert by_name["dest"]["type"] == "Path"
    assert by_name["dest"]["type_info"]["exists"] is True
    # A False that carries meaning ("must not be a directory") must not be dropped.
    assert by_name["dest"]["type_info"]["dir_okay"] is False


def test_help_json_group_reports_aliases(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["things", "--help=json"])
    assert result.exit_code == 0

    schema = json.loads(result.output)
    # rich-click's `aliases` flows through to_info_dict() as a passthrough field.
    assert schema["aliases"] == ["sub"]
    assert schema["subcommands"] == {"list": {"help": "List things."}}

    # The same command is reachable via the alias.
    via_alias = json.loads(cli_runner.invoke(cli, ["sub", "--help=json"]).output)
    assert via_alias["name"] == "things"


def test_help_json_enriches_customized_help_option(cli_runner: CliRunner) -> None:
    # The help meta-option is recognised by object identity, so a non-default help option name (here
    # `-h`) is still found and enriched with its formats, rather than mistaken for a regular option.
    @command(context_settings={"help_option_names": ["-h", "--help"]})
    @option("--real", help="A real option.")
    def cli(real: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    by_name = {param["name"]: param for param in schema["params"]}
    assert by_name["real"]["opts"] == ["--real"]
    assert set(by_name["help"]["opts"]) == {"-h", "--help"}
    assert "markdown" in by_name["help"]["choices"]


def test_help_json_passthrough_of_custom_fields(cli_runner: CliRunner) -> None:
    # Anything a developer adds to to_info_dict() flows through: custom command-level keys are
    # merged onto the top-level object, and custom parameter-level keys onto the parameter.
    from rich_click import RichOption

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

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    # `examples` injected via a to_info_dict override is normalized to the canonical {description,
    # command} shape, so every format (json/carapace/markdown) sees the same thing -- a bare command
    # string becomes an example with an empty description.
    assert schema["examples"] == [{"description": "", "command": "cli --token=XXX"}]
    token = next(param for param in schema["params"] if param["name"] == "token")
    assert token["sensitive"] is True


def test_help_json_hidden_param_is_kept_and_flagged(cli_runner: CliRunner) -> None:
    # Hidden params are kept (parity with to_info_dict) but marked hidden so consumers can skip them.
    @command()
    @option("--secret", hidden=True, help="Internal.")
    @option("--shown", help="Public.")
    def cli(secret: str, shown: str) -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    by_name = {param["name"]: param for param in schema["params"]}
    assert by_name["secret"]["hidden"] is True
    assert "hidden" not in by_name["shown"]


def test_help_json_omits_help_when_undocumented(cli_runner: CliRunner) -> None:
    # An undocumented command omits `help` entirely rather than emitting a null.
    @command()
    def cli() -> None:
        pass

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    assert "help" not in schema


def test_help_json_format_help_json_override(cli_runner: CliRunner) -> None:
    # `--help=json` serializes whatever `format_help_json` returns, mirroring click's
    # get_help/format_help split, so subclasses can customize the schema by overriding it.
    class MyCommand(RichCommand):
        def format_help_json(self, ctx: Any, formatter: Any) -> Dict[str, Any]:
            data = super().format_help_json(ctx, formatter)
            data["custom"] = "yes"
            return data

    @command(cls=MyCommand)
    def cli() -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    assert schema["custom"] == "yes"
    assert schema["name"] == "cli"


def test_help_json_get_help_json_direct(cli_runner: CliRunner) -> None:
    # get_help_json() can be called directly (e.g. by alternative output paths) and returns
    # the same JSON string the `--help=json` flag prints.
    @command()
    @option("--count", type=int, default=1, help="How many.")
    def cli(count: int) -> None:
        """Hi."""

    with cli.make_context("cli", []) as ctx:
        direct = json.loads(cli.get_help_json(cast(RichContext, ctx)))

    via_flag = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    assert direct == via_flag
    assert direct["name"] == "cli"


def test_help_json_transform_hook(cli_runner: CliRunner) -> None:
    rc.HELP_JSON_TRANSFORM = lambda schema, cmd, ctx: {**schema, "version": "1.2.3"}

    @command()
    def cli() -> None:
        """Hi."""

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    assert schema["version"] == "1.2.3"


# --------------------------------------------------------------------------------------------------
# `--help=json-full` (recursive) and `--help=carapace`.
# --------------------------------------------------------------------------------------------------


def test_help_json_full_is_recursive(cli_runner: CliRunner) -> None:
    # json-full expands every descendant to its full schema (params + usage + nested subcommands) in a
    # single call, unlike the progressive json format.
    cli = _build_cli()
    schema = json.loads(cli_runner.invoke(cli, ["--help=json-full"]).output)

    things = schema["subcommands"]["things"]
    assert things["path"] == "cli things"
    assert "params" in things  # full detail at the child level, not just a name
    # Nested grandchild is also fully expanded.
    list_cmd = things["subcommands"]["list"]
    assert list_cmd["path"] == "cli things list"
    assert list_cmd["name"] == "list"

    # A leaf's params carry the same detail a direct `--help=json` on it would, including the --help
    # meta-option (with its formats) at every node.
    hello = schema["subcommands"]["hello"]
    by_name = {p["name"]: p for p in hello["params"]}
    assert by_name["count"]["default"] == 3
    assert by_name["name"]["kind"] == "argument"
    assert "markdown" in by_name["help"]["choices"]


def test_help_carapace_structure(cli_runner: CliRunner) -> None:
    # Carapace mapping: flag-string keys, value/repeatable suffixes, negation pairs, choices as
    # completion candidates, multi-value nargs, hidden commands, parsing mode and recursion.
    @group()
    @option("--debug/--no-debug", help="Toggle debug.")
    @option("--tag", multiple=True, help="Tags.")
    def cli(debug: bool, tag: Tuple[str, ...]) -> None:
        """Root."""

    @cli.command(aliases=["rm"], hidden=True)
    @option("--coords", type=int, nargs=2, help="Two ints.")
    @option("--fmt", type=click.Choice(["json", "yaml"]), help="Format.")
    @argument("kind", type=click.Choice(["a", "b"]))
    def remove(coords: Tuple[int, ...], fmt: str, kind: str) -> None:
        """Remove."""

    doc = json.loads(cli_runner.invoke(cli, ["--help=carapace"]).output)

    assert doc["name"] == "cli"
    assert doc["description"] == "Root."
    # Groups parse flags strictly before the subcommand.
    assert doc["parsing"] == "non-interspersed"
    # Bool flag with a negation -> two entries; repeatable value flag -> trailing `=*`.
    assert doc["flags"]["--debug"] == "Toggle debug."
    assert doc["flags"]["--no-debug"] == "Toggle debug."
    assert doc["flags"]["--tag=*"] == "Tags."
    # The --help meta-option is emitted as a value-taking flag, completing to the available formats.
    assert doc["flags"]["--help="] == "Show this message and exit."
    assert "markdown" in doc["completion"]["flag"]["help"]

    remove_cmd = next(c for c in doc["commands"] if c["name"] == "remove")
    assert remove_cmd["hidden"] is True
    assert remove_cmd["aliases"] == ["rm"]
    # Multi-value flag uses the object form with nargs.
    assert remove_cmd["flags"]["--coords="] == {"description": "Two ints.", "nargs": 2}
    # Choice option -> completion candidates keyed by flag name; choice argument -> positional.
    assert remove_cmd["completion"]["flag"]["fmt"] == ["json", "yaml"]
    assert remove_cmd["completion"]["positional"] == [["a", "b"]]


def test_help_equals_unknown_format_falls_back_to_plain_help(cli_runner: CliRunner) -> None:
    # An unrecognized format never errors: it falls back to the normal human-readable help. This keeps
    # e.g. `mytool --help install` (a mistaken attempt to get help for a subcommand) friendly.
    cli = _build_cli()
    result = cli_runner.invoke(cli, ["--help=bogus"])
    assert result.exit_code == 0
    assert result.output.lstrip().startswith("Usage:")
    assert "{" not in result.output.split("Options")[0]


def test_help_equals_empty_value_shows_plain_help(cli_runner: CliRunner) -> None:
    # `--help=` (empty value) is still a request for help: it shows the normal help and exits 0, rather
    # than silently doing nothing (leaf) or erroring as a missing command (group).
    cli = _build_cli()
    for args in (["--help="], ["hello", "--help="]):
        result = cli_runner.invoke(cli, args)
        assert result.exit_code == 0, args
        assert result.output.lstrip().startswith("Usage:"), args


def test_help_format_registry_is_extensible(cli_runner: CliRunner) -> None:
    # A subclass can add a format by extending `help_formats` and supplying the rendering method, without
    # overriding the dispatch. Built-in formats keep working.
    class MyCommand(RichCommand):
        help_formats = {**RichCommand.help_formats, "upper": "get_help_upper"}

        def get_help_upper(self, ctx: Any) -> str:
            return "UPPER-HELP"

    @command(cls=MyCommand)
    def cli() -> None:
        """Hi."""

    assert cli_runner.invoke(cli, ["--help=upper"]).output.strip() == "UPPER-HELP"
    assert json.loads(cli_runner.invoke(cli, ["--help=json"]).output)["name"] == "cli"


def test_help_space_form_works_like_the_attached_form(cli_runner: CliRunner) -> None:
    # `--help json` (space) is equivalent to `--help=json`: the optional value consumes the next token,
    # on both groups and leaves.
    cli = _build_cli()

    assert json.loads(cli_runner.invoke(cli, ["--help", "json"]).output)["name"] == "cli"
    assert json.loads(cli_runner.invoke(cli, ["hello", "--help", "json"]).output)["name"] == "hello"

    # A token that is not a format falls back to plain help -- exactly as a plain `--help` always ignored
    # anything that followed it. (To get a subcommand's help, put `--help` after it: `cli things --help`.)
    non_format = cli_runner.invoke(cli, ["--help", "things"])
    assert non_format.exit_code == 0
    assert non_format.output.lstrip().startswith("Usage:")


def test_help_full_and_carapace_direct_methods(cli_runner: CliRunner) -> None:
    # The get_help_* methods can be called directly and match what the flag prints.
    cli = _build_cli()
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        rctx = cast(RichContext, ctx)
        full_direct = json.loads(cli.get_help_json_full(rctx))
        carapace_direct = json.loads(cli.get_help_carapace(rctx))

    assert full_direct == json.loads(cli_runner.invoke(cli, ["--help=json-full"]).output)
    assert carapace_direct == json.loads(cli_runner.invoke(cli, ["--help=carapace"]).output)


def test_help_carapace_override(cli_runner: CliRunner) -> None:
    # format_help_carapace is overridable for full control of the carapace output.
    from rich_click import RichGroup

    class MyGroup(RichGroup):
        def format_help_carapace(self, ctx: Any, formatter: Any) -> Dict[str, Any]:
            data = super().format_help_carapace(ctx, formatter)
            data["group"] = "custom"
            return data

    @group(cls=MyGroup)
    def cli() -> None:
        """Hi."""

    doc = json.loads(cli_runner.invoke(cli, ["--help=carapace"]).output)
    assert doc["group"] == "custom"


# --------------------------------------------------------------------------------------------------
# Markdown: `--help=md` / `--help=md-full` (aliases `markdown` / `markdown-full`).
# --------------------------------------------------------------------------------------------------


def test_help_markdown_progressive(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    out = cli_runner.invoke(cli, ["--help=md"]).output

    # Command titled by its full path; help, usage, and a subcommand index (not full subcommand bodies).
    assert "# `cli`" in out
    assert "Root help text." in out
    assert "**Usage:** `cli [OPTIONS] COMMAND [ARGS]...`" in out
    assert "## Options" in out
    assert "`-v`, `--verbose`" in out  # both flag names rendered
    assert "## Subcommands" in out
    assert "- `hello` — Say hello." in out
    # Nested name index, with aliases; progressive mode does NOT emit the subcommand's own option tables.
    assert "- `things` (aliases: sub) — Manage things." in out
    assert "  - `list` — List things." in out


def test_help_markdown_aliases_match(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    assert cli_runner.invoke(cli, ["--help=markdown"]).output == cli_runner.invoke(cli, ["--help=md"]).output
    assert cli_runner.invoke(cli, ["--help=markdown-full"]).output == cli_runner.invoke(cli, ["--help=md-full"]).output


def test_help_markdown_leaf_tables(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    out = cli_runner.invoke(cli, ["hello", "--help=md"]).output

    assert "# `cli hello`" in out
    # Positional argument rendered in its own table, marked required.
    assert "## Arguments" in out
    assert "| `name` |" in out
    # Option with a default.
    assert "## Options" in out
    assert "`--count`" in out
    assert "`3`" in out  # default surfaced in the table


def test_help_markdown_full_is_recursive_and_flat(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    out = cli_runner.invoke(cli, ["--help=md-full"]).output

    # Every command is its own top-level (`#`) section titled by full path; no deeper heading nesting.
    assert "# `cli`" in out
    assert "# `cli hello`" in out
    assert "# `cli things`" in out
    assert "# `cli things list`" in out
    # Full mode documents each leaf's params inline (unlike the progressive index).
    assert "| `name` |" in out
    # Flat: command sections never go past `#`; only sub-sections use `##`.
    assert "### " not in out


def test_help_markdown_escapes_pipes_in_cells(cli_runner: CliRunner) -> None:
    # A pipe in help text must be escaped so it doesn't break the Markdown table.
    @command()
    @option("--mode", help="Pick a | b.")
    def cli(mode: str) -> None:
        """Hi."""

    out = cli_runner.invoke(cli, ["--help=md"]).output
    assert "Pick a \\| b." in out


def test_help_markdown_override(cli_runner: CliRunner) -> None:
    # format_help_markdown is overridable for full control of the output.
    class MyCommand(RichCommand):
        def format_help_markdown(self, ctx: Any) -> str:
            return "CUSTOM MD"

    @command(cls=MyCommand)
    def cli() -> None:
        """Hi."""

    assert cli_runner.invoke(cli, ["--help=md"]).output.strip() == "CUSTOM MD"


# --------------------------------------------------------------------------------------------------
# Developer-supplied examples, surfaced in every output (rendered help, md, json, carapace).
# --------------------------------------------------------------------------------------------------


def test_examples_require_description_tuples(cli_runner: CliRunner) -> None:
    # Every example is a (description, command) tuple -- description first, command second -- so an
    # example is never shown without explaining what it does.
    @command(examples=[("Run quickly", "tool run fast"), ("Run slowly", "tool run --slow x")])
    def cli() -> None:
        """Hi."""

    examples = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)["examples"]
    assert examples == [
        {"description": "Run quickly", "command": "tool run fast"},
        {"description": "Run slowly", "command": "tool run --slow x"},
    ]


def test_examples_reject_bare_string(cli_runner: CliRunner) -> None:
    # A bare command string is rejected -- callers must supply a description.
    with pytest.raises(TypeError):

        @command(examples=["tool run fast"])
        def cli() -> None:
            """Hi."""


def test_examples_in_rendered_help(cli_runner: CliRunner) -> None:
    # The rendered (human) --help shows an Examples panel; commands without examples do not.
    @command(examples=[("Do the thing", "tool do thing")])
    def cli() -> None:
        """Hi."""

    out = cli_runner.invoke(cli, ["--help"]).output
    assert "Examples" in out
    assert "Do the thing" in out
    assert "tool do thing" in out

    @command()
    def plain() -> None:
        """Hi."""

    assert "Examples" not in cli_runner.invoke(plain, ["--help"]).output


def test_examples_in_markdown(cli_runner: CliRunner) -> None:
    @command(examples=[("Do a thing", "tool do thing"), ("Do the other thing", "tool do other")])
    def cli() -> None:
        """Hi."""

    out = cli_runner.invoke(cli, ["--help=md"]).output
    assert "## Examples" in out
    assert "- Do a thing: `tool do thing`" in out
    assert "- Do the other thing: `tool do other`" in out


def test_examples_in_carapace(cli_runner: CliRunner) -> None:
    @command(examples=[("Do a thing", "tool do thing"), ("Do the other thing", "tool do other")])
    def cli() -> None:
        """Hi."""

    doc = json.loads(cli_runner.invoke(cli, ["--help=carapace"]).output)
    assert doc["examples"] == {"tool do thing": "Do a thing", "tool do other": "Do the other thing"}


def test_examples_non_dict_shape_via_to_info_dict_does_not_crash(cli_runner: CliRunner) -> None:
    # `examples` can arrive via a to_info_dict override as raw strings or (description, command) pairs
    # rather than the normalized dicts. Every format coerces to one shape rather than crashing.
    class CustomCommand(RichCommand):
        def to_info_dict(self, ctx: "click.Context") -> "Dict[str, Any]":
            info = super().to_info_dict(ctx)
            info["examples"] = ["tool raw", ("Greet", "tool hello")]  # str + tuple, not dicts
            return info

    @command(cls=CustomCommand)
    def cli() -> None:
        """Hi."""

    expected = [{"description": "", "command": "tool raw"}, {"description": "Greet", "command": "tool hello"}]
    assert json.loads(cli_runner.invoke(cli, ["--help=json"]).output)["examples"] == expected
    carapace = json.loads(cli_runner.invoke(cli, ["--help=carapace"]).output)
    assert carapace["examples"] == {"tool raw": "", "tool hello": "Greet"}
    md = cli_runner.invoke(cli, ["--help=md"]).output
    assert "`tool raw`" in md and "Greet: `tool hello`" in md


def test_json_full_lists_uncontextualizable_subcommand(cli_runner: CliRunner) -> None:
    # A child that raises a ClickException even under resilient parsing can't be entered, but the
    # recursive dump still lists it (as a degraded node) so json-full matches the lean json index
    # rather than silently dropping it.
    class Eager(RichCommand):
        def make_context(self, *args: Any, **kwargs: Any) -> Any:
            raise click.UsageError("cannot enter")

    @group()
    def cli() -> None:
        """Root."""

    @cli.command()
    def normal() -> None:
        """Normal."""

    cli.add_command(Eager(name="eager", help="Eager command."))

    lean = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)["subcommands"]
    full = json.loads(cli_runner.invoke(cli, ["--help=json-full"]).output)["subcommands"]
    assert set(lean) == set(full) == {"normal", "eager"}
    # The degraded node carries name/path/help but not the params/usage of a fully-walked command.
    assert full["eager"] == {"name": "eager", "path": "cli eager", "help": "Eager command."}
    # markdown-full renders the degraded node as a section rather than breaking on a missing path.
    assert "# `cli eager`" in cli_runner.invoke(cli, ["--help=markdown-full"]).output


def test_examples_recursive_json_full(cli_runner: CliRunner) -> None:
    # Examples on a subcommand appear at that node in the recursive dump.
    @group()
    def cli() -> None:
        """Root."""

    @cli.command(examples=[("Run now", "cli sub --now")])
    def sub() -> None:
        """Sub."""

    schema = json.loads(cli_runner.invoke(cli, ["--help=json-full"]).output)
    assert schema["subcommands"]["sub"]["examples"] == [{"description": "Run now", "command": "cli sub --now"}]


def test_examples_absent_when_not_provided(cli_runner: CliRunner) -> None:
    # No examples key is emitted for a command that defines none.
    cli = _build_cli()
    assert "examples" not in json.loads(cli_runner.invoke(cli, ["--help=json"]).output)


def test_examples_placeholder_detection(cli_runner: CliRunner) -> None:
    # The rendered help colours placeholders inferred from the command's structure: a value after a
    # value-taking flag, an attached `=value`, and a bare positional are all metavar-styled; a boolean
    # flag consumes nothing; the command path and flags get their own styles.

    from rich_click.rich_help_rendering import _styled_example_command

    @command(name="i")
    @option("--dir", "-d", type=click.Path())
    @option("--force", "-f", is_flag=True)
    @argument("tool")
    def inst(dir: str, force: bool, tool: str) -> None:
        """Install."""

    with inst.make_context("nf-core m i", [], resilient_parsing=True) as ctx:
        rctx = cast(RichContext, ctx)
        formatter = rctx.make_formatter()
        styled = _styled_example_command("nf-core m i --dir foo/ -f fastqc", inst, rctx, formatter)

        def style_of(token: str) -> object:
            start = styled.plain.index(token)
            return next((s.style for s in styled.spans if s.start == start), None)

        placeholder = formatter.config.style_examples_placeholder
        # Value after a value-taking flag, and the bare positional, are placeholders.
        assert style_of("foo/") == placeholder
        assert style_of("fastqc") == placeholder
        # The boolean flag does NOT turn the following token into a placeholder (here, end of line).
        assert style_of("--dir") == formatter.config.style_examples_flag_long
        assert style_of("-f") == formatter.config.style_examples_flag_short
        # Command path is not styled as a placeholder (it carries the plain command style).
        assert style_of("nf-core") != placeholder


def test_examples_placeholder_detection_handles_aliases(cli_runner: CliRunner) -> None:
    # When help is invoked via an alias (`foo b`), an example written with the canonical name
    # (`foo bar ...`) must still recognise `bar` as the command path, not a placeholder -- and vice
    # versa. The command path is matched by name OR alias at each level.
    from rich_click.rich_help_rendering import _styled_example_command

    @group()
    def foo() -> None:
        """Root."""

    @foo.command(name="bar", aliases=["b"])
    @option("--now", is_flag=True)
    @argument("target")
    def bar(now: bool, target: str) -> None:
        """Do bar."""

    with foo.make_context("foo", ["b"], resilient_parsing=True) as gctx:
        sub = cast(RichCommand, foo.get_command(gctx, "b"))  # invoked via alias
        with sub.make_context("b", [], parent=gctx, resilient_parsing=True) as sctx:
            rctx = cast(RichContext, sctx)
            formatter = rctx.make_formatter()
            assert sctx.command_path == "foo b"  # help was reached via the alias

            def placeholder_tokens(example: str) -> Set[str]:
                styled = _styled_example_command(example, sub, rctx, formatter)
                ph = formatter.config.style_examples_placeholder
                return {styled.plain[s.start : s.end] for s in styled.spans if s.style == ph}

            # Either spelling of the subcommand is recognised as command path (NOT a placeholder); only
            # the positional `x` is a placeholder.
            assert placeholder_tokens("foo bar --now x") == {"x"}
            assert placeholder_tokens("foo b --now x") == {"x"}
