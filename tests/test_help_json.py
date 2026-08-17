import json
from typing import Any, cast

import click
import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click.rich_click as rc
from rich_click import RichCommand, RichHelpConfiguration, argument, command, group, option, rich_config
from rich_click.help_json import command_markdown, compact_command
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
# `--help=json`: complete structured help. Available on every rich-click CLI without config -- the
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

    # JSON includes the complete tree. Each child has its params and usage.
    assert schema["subcommands"]["hello"]["path"] == "cli hello"
    assert schema["subcommands"]["hello"]["params"]
    assert schema["subcommands"]["things"]["aliases"] == ["sub"]
    assert schema["subcommands"]["things"]["subcommands"]["list"]["path"] == "cli things list"


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


def test_help_to_stderr_covers_the_machine_readable_formats(cli_runner: CliRunner) -> None:
    # `help_to_stderr` exists to keep stdout clean for piping. It has to hold for every help document,
    # not just the human one -- otherwise a machine-readable help leaks into the pipe it was set to
    # protect. Covers an explicit format and the bare `--help` an agent environment redirects.
    @group(context_settings={"help_to_stderr": True})
    def cli() -> None:
        """Hi."""

    for args in (["--help"], ["--help=json"], ["--help=markdown"], ["--help=compact"]):
        result = cli_runner.invoke(cli, args)
        assert result.exit_code == 0
        assert result.stdout == "", args
        assert result.stderr.strip(), args


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


def test_help_json_reports_a_flag_that_defaults_on(cli_runner: CliRunner) -> None:
    # A flag defaulting to False is the implied case and is dropped; one defaulting to True is real
    # signal a consumer cannot infer, so the two must not serialize identically.
    @command()
    @option("--debug/--no-debug", default=True, help="Debug mode.")
    @option("--quiet/--no-quiet", default=False, help="Quiet mode.")
    def cli(debug: bool, quiet: bool) -> None:
        """Hi."""

    by_name = {param["name"]: param for param in json.loads(cli_runner.invoke(cli, ["--help=json"]).output)["params"]}
    assert by_name["debug"]["default"] is True
    assert "default" not in by_name["quiet"]


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
        pair: tuple[str, ...],
        shout: bool,
        files: tuple[str, ...],
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
    assert schema["subcommands"]["list"]["path"] == "cli things list"
    assert "params" in schema["subcommands"]["list"]

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
        def to_info_dict(self) -> "dict[str, Any]":
            info = super().to_info_dict()
            info["sensitive"] = True
            return info

    class DocumentedCommand(RichCommand):
        def to_info_dict(self, ctx: "click.Context") -> "dict[str, Any]":
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
        def format_help_json(self, ctx: Any, formatter: Any) -> dict[str, Any]:
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

    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
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


def test_custom_help_format_registered_via_config(cli_runner: CliRunner) -> None:
    # A new `--help <name>` format can be added process-wide via the `help_formats` config option,
    # without subclassing RichCommand. The renderer is `(command, ctx) -> str`.
    rc.HELP_FORMATS = {"yaml": lambda cmd, ctx: f"yaml-for: {cmd.name}"}

    @command()
    @option("--name", help="A name.")
    def cli(name: str) -> None:
        """Hi."""

    # 1. The custom format dispatches.
    result = cli_runner.invoke(cli, ["--help=yaml"])
    assert result.exit_code == 0
    assert result.output.strip() == "yaml-for: cli"
    # 2. It is discoverable: listed in the --help option's choices and in the metavar.
    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
    help_param = next(param for param in schema["params"] if param["name"] == "help")
    assert "yaml" in help_param["choices"]
    assert "[markdown|json|compact|yaml]" in cli_runner.invoke(cli, ["--help"]).output
    # 3. An unknown format still falls back to the normal human-readable help.
    fallback = cli_runner.invoke(cli, ["--help=bogus"])
    assert fallback.exit_code == 0
    assert fallback.output.lstrip().startswith("Usage:")


# --------------------------------------------------------------------------------------------------
# `--help=json` (recursive).
# --------------------------------------------------------------------------------------------------


def test_help_json_is_recursive(cli_runner: CliRunner) -> None:
    # JSON expands every descendant to its full schema in one call.
    cli = _build_cli()
    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)

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


def test_help_json_direct_method(cli_runner: CliRunner) -> None:
    # The get_help_json method can be called directly and matches what the flag prints.
    cli = _build_cli()
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        rctx = cast(RichContext, ctx)
        direct = json.loads(cli.get_help_json(rctx))

    assert direct == json.loads(cli_runner.invoke(cli, ["--help=json"]).output)


# --------------------------------------------------------------------------------------------------
# Markdown.
# --------------------------------------------------------------------------------------------------


def test_help_markdown_nonrecursive_helper(cli_runner: CliRunner) -> None:
    # `max_chars=None` opts out of adaptive disclosure: the invoked command in full, descendants as a
    # name index. This tests the lower-level nonrecursive rendering mode.
    cli = _build_cli()
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        out = command_markdown(cli, ctx, recursive=False, max_chars=None)

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
    assert "# `cli hello`" not in out


def test_removed_formats_fall_back_to_plain_help(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    assert list(RichCommand.help_formats) == ["markdown", "json", "compact"]
    for removed in ("md", "md-full", "markdown-full", "json-full", "carapace"):
        output = cli_runner.invoke(cli, [f"--help={removed}"]).output
        assert output.lstrip().startswith("Usage:")


def test_help_markdown_leaf_tables(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    out = cli_runner.invoke(cli, ["hello", "--help=markdown"]).output

    assert "# `cli hello`" in out
    # Positional argument rendered in its own table, marked required.
    assert "## Arguments" in out
    assert "| `name` |" in out
    # Option with a default.
    assert "## Options" in out
    assert "`--count`" in out
    assert "`3`" in out  # default surfaced in the table


def test_help_markdown_is_recursive_and_flat(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    out = cli_runner.invoke(cli, ["--help=markdown"]).output

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

    out = cli_runner.invoke(cli, ["--help=markdown"]).output
    assert "Pick a \\| b." in out


def test_help_markdown_snapshot(cli_runner: CliRunner) -> None:
    # Markdown renders the complete tree and drops a column that is empty for every row
    # of a table (here Required and Default) is dropped rather than padded out.
    cli = _build_cli()
    assert cli_runner.invoke(cli, ["--help=markdown"]).output == snapshot(
        """\
# `cli`

Root help text.

**Usage:** `cli [OPTIONS] COMMAND [ARGS]...`

## Options

| Option | Type | Description |
| --- | --- | --- |
| `-v`, `--verbose` | flag | Be loud. |
| `--help` | choice: markdown / json / compact | Show this message and exit. |

# `cli hello`

Say hello.

**Usage:** `cli hello [OPTIONS] NAME`

## Arguments

| Argument | Type | Required |
| --- | --- | --- |
| `name` | String | yes |

## Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `--count` | Int | `3` | How many times. |
| `--help` | choice: markdown / json / compact |  | Show this message and exit. |

# `cli things`

Manage things.

**Aliases:** `sub`

**Usage:** `cli things [OPTIONS] COMMAND [ARGS]...`

## Options

| Option | Type | Description |
| --- | --- | --- |
| `--help` | choice: markdown / json / compact | Show this message and exit. |

# `cli things list`

List things.

**Usage:** `cli things list [OPTIONS]`

## Options

| Option | Type | Description |
| --- | --- | --- |
| `--help` | choice: markdown / json / compact | Show this message and exit. |

"""
    )


def test_text_renderings_omit_hidden_commands(cli_runner: CliRunner) -> None:
    # A text rendering stands in for the help screen, so it must not show what the help screen hides --
    # and adaptive disclosure would otherwise document a hidden command's whole option table, not just
    # name it. The JSON formats still report it, like `to_info_dict` and like hidden *parameters* do.
    @group()
    def cli() -> None:
        """A tool."""

    @cli.command(hidden=True)
    @option("--secret", help="A secret option.")
    def internal(secret: str) -> None:
        """An internal command."""

    @cli.command()
    def visible() -> None:
        """A visible command."""

    for fmt in ("markdown", "compact"):
        out = cli_runner.invoke(cli, [f"--help={fmt}"]).output
        assert "visible" in out, fmt
        assert "internal" not in out, fmt
        assert "secret" not in out, fmt

    assert "internal" in cli_runner.invoke(cli, ["--help=json"]).output


def test_markdown_table_keeps_columns_that_any_row_uses(cli_runner: CliRunner) -> None:
    # A column is dropped only when *every* row leaves it empty: one row using it keeps it for all.
    @command()
    @option("--count", type=int, default=3, help="How many.")
    @option("--name", required=True, help="Who.")
    def cli(count: int, name: str) -> None:
        """Hi."""

    out = cli_runner.invoke(cli, ["--help=markdown"]).output
    assert "| Option | Type | Required | Default | Description |" in out
    assert "| `--name` | String | yes |  | Who. |" in out


def test_markdown_table_drops_the_columns_no_row_uses(cli_runner: CliRunner) -> None:
    # Nothing is required and nothing has a default, so both columns are pure padding and are dropped.
    @command()
    @option("--name", help="Who.")
    def cli(name: str) -> None:
        """Hi."""

    out = cli_runner.invoke(cli, ["--help=markdown"]).output
    assert "| Option | Type | Description |" in out
    assert "Required" not in out
    assert "Default" not in out


# --------------------------------------------------------------------------------------------------
# Adaptive disclosure helpers remain available for the agent-facing compact format.
# --------------------------------------------------------------------------------------------------


def _big_cli(groups: int = 15, commands: int = 20) -> RichCommand:
    """A synthetic tree far too large to render in full: `groups * commands` leaves plus the groups."""

    @group()
    def cli() -> None:
        """A very large CLI."""

    for group_index in range(groups):

        @cli.group(name=f"grp{group_index:02d}")
        def subgroup() -> None:
            """A group of related commands."""

        for command_index in range(commands):

            @subgroup.command(name=f"cmd{command_index:02d}")
            @option("--target", type=click.Choice(["alpha", "beta"]), help="Which target to act on.")
            @option("--seed", type=int, help="Seed for deterministic behaviour.")
            def leaf(target: str, seed: int) -> None:
                """Do a thing to the target."""

    return cast(RichCommand, cli)


def test_explicit_markdown_renders_the_whole_tree(cli_runner: CliRunner) -> None:
    cli = _build_cli()
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        expected = command_markdown(cli, ctx, recursive=True)
    assert cli_runner.invoke(cli, ["--help=markdown"]).output.rstrip() == expected.rstrip()


def test_explicit_markdown_does_not_apply_the_agent_character_limit(cli_runner: CliRunner) -> None:
    out = cli_runner.invoke(_big_cli(), ["--help=markdown"]).output

    assert len(out) > RichHelpConfiguration().agent_help_max_chars  # type: ignore[operator]
    assert "# `cli`" in out
    assert "| Option | Type | Description |" in out
    assert "# `cli grp00`" in out
    assert "# `cli grp14 cmd19`" in out


@pytest.mark.parametrize("fmt", ["markdown", "compact"])
def test_adaptive_output_is_deterministic(cli_runner: CliRunner, fmt: str) -> None:
    cli = _big_cli()
    outputs = {cli_runner.invoke(cli, [f"--help={fmt}"]).output for _ in range(3)}
    assert len(outputs) == 1


@pytest.fixture
def mixed_level_cli() -> RichCommand:
    """
    A CLI whose tree does not fit `_MIXED_LEVEL_TOKENS`, so it renders at more than one detail level.

    Six sibling commands, each with enough option help to be expensive at full detail: the nearest are
    promoted all the way, the furthest only as far as a signature.
    """

    @group()
    def cli() -> None:
        """Root."""

    for index in range(6):

        @cli.command(name=f"run{index}", examples=[("Run it", f"cli run{index} thing")])
        @option("--mode", type=click.Choice(["fast", "safe"]), help="How to run the operation end to end.")
        @option("--count", type=int, required=True, help="How many iterations to perform in total.")
        @argument("target")
        def run(mode: str, count: int, target: str) -> None:
            """Run the thing against a target."""

    return cast(RichCommand, cli)


#: A ceiling that fits every `mixed_level_cli` command's signature, but only the nearest few in full.
_MIXED_LEVEL_CHARS = 3300


def _render_mixed_levels(cli: RichCommand) -> tuple[str, str]:
    """Render `mixed_level_cli` at its mixed-level ceiling, as `(whole document, last command's section)`."""
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        out = command_markdown(cli, ctx, max_chars=_MIXED_LEVEL_CHARS)
    return out, out.split("# `cli run5`")[1]


def test_signature_level_carries_metavars_and_choices(mixed_level_cli: RichCommand) -> None:
    # The point of the middle tier: an agent sees what each option *takes* -- metavars and choice
    # values -- without paying for a description column.
    out, last = _render_mixed_levels(mixed_level_cli)

    # The first command was promoted all the way to a full option table...
    assert "| `--mode` | choice: fast / safe |" in out.split("# `cli run1`")[0]
    # ...the last only to a signature: names, metavars, choice values, required marker -- no
    # descriptions, and no table.
    assert "**Usage:** `cli run5 [OPTIONS] TARGET`" in last  # the argument lives in the usage line
    assert "- `--mode [fast|safe]`" in last
    assert "- `--count INTEGER` (required)" in last
    assert "How to run the operation end to end." not in last
    assert "| --- |" not in last  # a signature list, not a table


def test_adaptive_disclosure_can_be_tuned_and_disabled(cli_runner: CliRunner) -> None:
    cli = _build_cli()

    @group()
    @rich_config(help_config=RichHelpConfiguration(agent_help_max_chars=None))
    def off() -> None:
        """Root help text."""

    @off.command()
    def hello() -> None:
        """Say hello."""

    # Explicit Markdown ignores the agent limit and returns the full tree.
    out = cli_runner.invoke(off, ["--help=markdown"]).output
    assert "# `off hello`" in out

    # The lower-level adaptive renderer can still limit agent-facing output.
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        assert "# `cli things list`" not in command_markdown(cli, ctx, max_chars=700)


@pytest.mark.parametrize("max_chars", [15_000, 20_000, 25_000])
def test_the_character_budget_is_exact_not_estimated(max_chars: int) -> None:
    # The whole reason the ceiling is in characters: `len()` is exact, so the rendered document can be
    # asserted against the configured number rather than against an estimate of it. A token ceiling
    # needed a chars-per-token divisor, and an agent harness truncates by characters anyway.
    cli = _big_cli()
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        for render in (command_markdown, compact_command):
            out = render(cli, ctx, max_chars=max_chars)
            assert len(out) <= max_chars, (render.__name__, len(out))
            # And the budget is actually spent, not left mostly unused: adaptive disclosure that stops
            # far short of the ceiling would be silently withholding detail that fits.
            assert len(out) > max_chars * 0.9, (render.__name__, len(out))


def test_the_budget_never_hides_a_commands_existence() -> None:
    # The one thing a ceiling does not buy: a floor of the invoked command's own block plus a name for
    # every descendant is always emitted, however small the ceiling. Truncating that would leave an
    # agent unable to discover a command at all, which is worse than a long response.
    cli = _big_cli(groups=4, commands=4)
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        out = compact_command(cli, ctx, max_chars=10)

    assert out.startswith("# cli — A very large CLI.")
    for group_index in range(4):
        for command_index in range(4):
            assert f"grp{group_index:02d} cmd{command_index:02d}  Do a thing to the target." in out


def test_help_markdown_override(cli_runner: CliRunner) -> None:
    # format_help_markdown is overridable for full control of the output.
    class MyCommand(RichCommand):
        def format_help_markdown(self, ctx: Any) -> str:
            return "CUSTOM MD"

    @command(cls=MyCommand)
    def cli() -> None:
        """Hi."""

    assert cli_runner.invoke(cli, ["--help=markdown"]).output.strip() == "CUSTOM MD"


# --------------------------------------------------------------------------------------------------
# `--help compact`: the character-lean rendering, and what a bare `--help` gives a detected agent.
#
# The format is designed against one constraint: agent harnesses truncate a tool's output by
# *characters* (Claude Code at ~30,000), and a help page that gets cut costs the agent turns re-reading
# it. So every rule below buys characters back -- and spends none on anything a model cannot already
# read without being taught a new notation.
# --------------------------------------------------------------------------------------------------


def _record_cli() -> RichCommand:
    """The reference command from the format's design: five options, an alias, two examples."""

    @group()
    def quorv() -> None:
        """A demo CLI."""

    @quorv.group()
    def plarv() -> None:
        """Manage records."""

    @plarv.command(
        aliases=["cl"],
        examples=[
            ("Create a record", "quorv plarv crell --crull 'north ledger'"),
            ("Pick a mode and weight", "quorv plarv crell --crull 'north ledger' --kolm crox --wover 12"),
        ],
    )
    @option("--crull", required=True, help="Annotation text for the record.")
    @option("--kolm", type=click.Choice(["pelm", "crox", "zeff"]), default="pelm", help="Mode of the record.")
    @option("--wover", type=int, metavar="INT", default=7, help="Weight of the record.")
    @option("--torv", multiple=True, help="Label to attach; repeat for several.")
    @option("--murd", default="veld", envvar="QUORV_MURD", help="Steward name.")
    def crell(**kwargs: Any) -> None:
        """Create a record."""

    return cast(RichCommand, quorv)


def test_compact_block_is_exactly_this(cli_runner: CliRunner) -> None:
    # The format, pinned byte-for-byte. Every element of the design is visible in these ten lines: the
    # `#` anchor that makes a block greppable, the two-space signature/description boundary, `*` for
    # required, choices inline in place of the metavar, `...` for repeatable, Click's own `[default: ]`
    # and `[env: ]` tags, no `--help` row, no usage line (nothing positional to order), and examples as
    # bare command lines.
    out = cli_runner.invoke(_record_cli(), ["plarv", "crell", "--help=compact"]).output

    assert out == snapshot(
        """\
# plarv crell [aliases: cl] — Create a record.
*--crull TEXT  Annotation text for the record.
--kolm pelm|crox|zeff  Mode of the record. [default: pelm]
--wover INT  Weight of the record. [default: 7]
--torv TEXT ...  Label to attach; repeat for several.
--murd TEXT  Steward name. [default: veld] [env: QUORV_MURD]
examples:
- quorv plarv crell --crull 'north ledger'
- quorv plarv crell --crull 'north ledger' --kolm crox --wover 12

"""
    )
    # The size target this format exists to hit: the same command renders at ~2,000 characters of
    # Markdown, which is what put a mid-size CLI past a harness's truncation point.
    assert len(out) <= 520


def test_compact_never_pads_or_trails(cli_runner: CliRunner) -> None:
    # The two-space separator is the whole layout: one space would be ambiguous with the spaces inside a
    # signature, and padding to a column would make the boundary depend on the widest row in the block.
    # Asserted over a whole large tree, at every detail level, since that is where a stray pad would
    # hide -- the block above is already pinned byte-for-byte by the snapshot.
    cli = _big_cli(groups=3, commands=3)
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        out = compact_command(cli, ctx, recursive=True) + compact_command(cli, ctx, max_chars=1_200)

    for line in out.splitlines():
        assert line == line.rstrip(), repr(line)  # no trailing whitespace, anywhere
        assert "   " not in line, repr(line)  # no column padding: two spaces is always the separator
        signature, separator, description = line.partition("  ")
        if separator:  # a line without one is a bare signature, which is a whole line by itself
            assert signature and description, repr(line)


def test_compact_usage_line_only_when_there_are_positionals(cli_runner: CliRunner) -> None:
    # A usage line for an option-only command repeats the anchor line and nothing else. With positional
    # arguments it carries something no other line can: their *order*.
    @group()
    def cli() -> None:
        """A tool."""

    @cli.command()
    @option("--force", is_flag=True, help="Overwrite.")
    @argument("src")
    @argument("dest", required=False)
    def move(force: bool, src: str, dest: str) -> None:
        """Move a record."""

    @cli.command()
    @option("--force", is_flag=True, help="Overwrite.")
    def sweep(force: bool) -> None:
        """Sweep the records."""

    out = cli_runner.invoke(cli, ["--help=compact"]).output

    assert "usage: cli move SRC [DEST]" in out  # positionals in order, and `[OPTIONS]` left out
    assert "# move — Move a record.\nusage:" in out  # directly under the anchor line
    assert "# sweep — Sweep the records.\n--force" in out  # no usage line at all


def test_compact_usage_keeps_every_positional_slot(cli_runner: CliRunner) -> None:
    # An explicit `metavar=""` leaves an argument with nothing to render. Dropping it from the usage line
    # would shift every later positional one slot left, making the line say the opposite of the truth --
    # so it falls back to the name, as Click does when no metavar is given at all.
    @command()
    @argument("what", metavar="")
    @argument("dest")
    def cli(what: str, dest: str) -> None:
        """Do a thing."""

    assert "usage: cli WHAT DEST" in cli_runner.invoke(cli, ["--help=compact"]).output


def test_compact_documents_arguments_that_carry_their_own_help(cli_runner: CliRunner) -> None:
    # A bare positional is fully described by the usage line, so it gets no line of its own; one with
    # help text or a default does, keyed by the same metavar the usage line uses.
    @command()
    @argument("src")
    @argument("mode", type=click.Choice(["fast", "safe"]), required=False, help="How to run.")
    def cli(src: str, mode: str) -> None:
        """Hi."""

    out = cli_runner.invoke(cli, ["--help=compact"]).output

    assert "usage: cli SRC [fast|safe]" in out
    assert "[fast|safe]  How to run." in out
    assert "\nSRC" not in out


def test_compact_preserves_explicit_nested_bracket_metavar() -> None:
    from rich_click.help_json import _param_metavar
    from rich_click.rich_help_rendering import _make_param_metavar

    param = click.Argument(["value"], required=False, metavar="[[VALUE]]")
    ctx = RichContext(RichCommand(name="cli"))

    assert _param_metavar(param, ctx) == _make_param_metavar(param, ctx)


def test_compact_omits_the_help_option(cli_runner: CliRunner) -> None:
    # The one row that is identical on every command of every CLI, and the largest block of pure
    # repetition in a whole-tree rendering. The other formats still report it.
    cli = _build_cli()

    assert "--help" not in cli_runner.invoke(cli, ["--help=compact"]).output
    assert "--help" in cli_runner.invoke(cli, ["--help=markdown"]).output
    assert "--help" in cli_runner.invoke(cli, ["--help=json"]).output


def test_compact_uses_clicks_own_metavars(cli_runner: CliRunner) -> None:
    # The signature is what tells the reader what to type, and it comes from Click itself: an explicit
    # `metavar=`, a `Path(file_okay=False)`'s DIRECTORY and any custom ParamType survive as they are.
    @command()
    @option("--pkg", metavar="PKG_NAME", help="Which package.")
    @option("--out", type=click.Path(file_okay=False), help="Where to write.")
    @option("--tag", multiple=True, help="Repeatable.")
    @option("--shout", is_flag=True, help="Be loud.")
    @option("--debug/--no-debug", default=True, help="Toggle.")
    def cli(pkg: str, out: str, tag: tuple[str, ...], shout: bool, debug: bool) -> None:
        """Hi."""

    out = cli_runner.invoke(cli, ["--help=compact"]).output

    assert "--pkg PKG_NAME  Which package." in out
    assert "--out DIRECTORY  Where to write." in out
    assert "--tag TEXT ...  Repeatable." in out  # repeatable, which Click's own metavar does not mark
    assert "--shout  Be loud." in out  # a flag takes no value, so it shows none
    assert "--debug, --no-debug  Toggle. [default: True]" in out  # negation flag included

    # The metavars are a rendering concern only: the JSON formats are untouched by them.
    assert "metavar" not in cli_runner.invoke(cli, ["--help=json"]).output


def test_compact_marks_required_with_a_star_not_a_word(cli_runner: CliRunner) -> None:
    # `*` is the marker rich-click's rendered help already uses, and it costs one character where
    # `[required]` costs ten -- on every required option of every command.
    @command()
    @option("--name", required=True, help="Who.")
    @option("--nick", help="Optional.")
    def cli(name: str, nick: str) -> None:
        """Hi."""

    out = cli_runner.invoke(cli, ["--help=compact"]).output

    assert "*--name TEXT  Who." in out
    assert "--nick TEXT  Optional." in out
    assert "required" not in out


def test_compact_group_lists_its_subcommands(cli_runner: CliRunner) -> None:
    # A group that is *not* rendering its descendants in full lists them instead: one line each, same
    # two-space separator, nested by path rather than indentation so each line is a runnable command.
    cli = _build_cli()
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        out = compact_command(cli, ctx, max_chars=None)

    assert out == snapshot(
        """\
# cli — Root help text.
-v, --verbose  Be loud.
hello  Say hello.
things [aliases: sub]  Manage things.
things list  List things.
"""
    )


def test_compact_renders_the_whole_tree(cli_runner: CliRunner) -> None:
    # What an explicit `--help compact` is for: every command in the tree, depth-first in definition
    # order, one blank line between blocks, no ceiling. A caller who names the format wants everything.
    out = cli_runner.invoke(_build_cli(), ["--help=compact"]).output

    assert out == snapshot(
        """\
# cli — Root help text.
-v, --verbose  Be loud.

# hello — Say hello.
usage: cli hello NAME
--count INTEGER  How many times. [default: 3]

# things [aliases: sub] — Manage things.

# things list — List things.

"""
    )


def test_compact_is_leaner_than_markdown(cli_runner: CliRunner) -> None:
    # The whole point of the format: the same content, a fraction of the characters -- the currency an
    # agent harness truncates in.
    cli = _big_cli()
    compact = cli_runner.invoke(cli, ["--help=compact"]).output
    markdown = cli_runner.invoke(cli, ["--help=markdown"]).output

    assert len(compact) < len(markdown) / 2


def test_compact_adaptive_uses_all_three_tiers(cli_runner: CliRunner) -> None:
    # As the agent default the format adapts like Markdown does: the invoked command in full, the rest
    # promoted breadth-first from a listing line, through a bare signature, to a full block.
    cli = _big_cli()
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        out = compact_command(cli, ctx, max_chars=15_000)

    assert len(out) <= 15_000
    # L2, the invoked command: its own block, in full.
    assert out.startswith("# cli — A very large CLI.")
    # L1, a near command: anchor line and bare signatures, no descriptions.
    assert "# grp00 cmd00 — Do a thing to the target.\n--target alpha|beta\n--seed INTEGER\n" in out
    assert "# grp00 cmd00 — Do a thing to the target.\n--target alpha|beta  Which" not in out
    # L0, a distant one: a listing line under the nearest ancestor with a block, named but not documented.
    assert "cmd19  Do a thing to the target." in out
    assert "# grp14 cmd19" not in out
    # And the reader is told what was abbreviated, and how to get the rest.
    assert out.rstrip().endswith("Run `cli <COMMAND> --help compact` on any command for its full detail.")
    assert "note: size-limited: 1 command(s) shown in full," in out


def test_compact_adaptive_promotes_signatures_before_full_blocks(cli_runner: CliRunner) -> None:
    # Breadth before depth: every command's option *names* are worth more to an agent choosing between
    # commands than an exhaustive treatment of the first few. So no command is documented in full until
    # every command has at least a signature.
    cli = _big_cli(groups=6, commands=6)
    with cli.make_context("cli", [], resilient_parsing=True) as ctx:
        out = compact_command(cli, ctx, max_chars=4_000)

    assert len(out) <= 4_000
    for group_index in range(6):
        for command_index in range(6):
            assert f"# grp{group_index:02d} cmd{command_index:02d} —" in out
    # Signatures everywhere, descriptions only on the commands whose full block also fit.
    assert "--target alpha|beta\n--seed INTEGER\n" in out
    assert 0 < out.count("--target alpha|beta  Which target to act on.") < 36


def test_compact_is_the_agent_default(cli_runner: CliRunner) -> None:
    # The format a bare `--help` renders when an agent is detected: the leanest complete rendering, and
    # the one that keeps a mid-size CLI inside a single tool response.
    assert RichHelpConfiguration().agent_help_format == "compact"
    assert RichHelpConfiguration().agent_help_max_chars == 25_000
    assert "compact" in json.loads(cli_runner.invoke(_build_cli(), ["--help=json"]).output)["params"][-1]["choices"]


def test_help_compact_override(cli_runner: CliRunner) -> None:
    # format_help_compact is overridable for full control of the output.
    class MyCommand(RichCommand):
        def format_help_compact(self, ctx: Any) -> str:
            return "CUSTOM COMPACT"

    @command(cls=MyCommand)
    def cli() -> None:
        """Hi."""

    assert cli_runner.invoke(cli, ["--help=compact"]).output.strip() == "CUSTOM COMPACT"


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

    out = cli_runner.invoke(cli, ["--help=markdown"]).output
    assert "## Examples" in out
    assert "- Do a thing: `tool do thing`" in out
    assert "- Do the other thing: `tool do other`" in out


def test_examples_come_before_the_parameters_in_markdown(cli_runner: CliRunner) -> None:
    # Ordering is not cosmetic: an example is a complete, copyable invocation, so it is the highest-value
    # thing a model can read about a command. Agent-facing formats put it first, right after the usage
    # line, so the answer is already there before the option tables are reached.
    @command(examples=[("Do a thing", "tool do thing")])
    @option("--mode", type=click.Choice(["fast", "safe"]), help="How to run.")
    @argument("name")
    def cli(mode: str, name: str) -> None:
        """Hi."""

    out = cli_runner.invoke(cli, ["--help=markdown"]).output
    assert out.index("**Usage:**") < out.index("## Examples") < out.index("## Arguments") < out.index("## Options")


def test_examples_come_before_the_parameters_at_every_level(
    cli_runner: CliRunner, mixed_level_cli: RichCommand
) -> None:
    # Markdown documents every node; the ordering holds in each section.
    for section in cli_runner.invoke(mixed_level_cli, ["--help=markdown"]).output.split("# `cli run")[1:]:
        assert section.index("**Usage:**") < section.index("## Examples") < section.index("## Options")

    # And at the compact signature level too: examples are short, and a worked invocation earns its
    # tokens against a list of flags the model would still have to assemble.
    _, last = _render_mixed_levels(mixed_level_cli)
    assert "| --- |" not in last  # a signature section, not a full one
    assert last.index("**Usage:**") < last.index("## Examples") < last.index("## Options")


def test_human_help_keeps_examples_after_the_options(cli_runner: CliRunner) -> None:
    # The rendered help is laid out the other way round, and stays that way: a person scanning a
    # terminal wants the reference material first and the worked examples at the end.
    @command(examples=[("Do a thing", "tool do thing")])
    @option("--mode", help="How to run.")
    def cli(mode: str) -> None:
        """Hi."""

    out = cli_runner.invoke(cli, ["--help"]).output
    assert out.index("Options") < out.index("Examples")


def test_examples_non_dict_shape_via_to_info_dict_does_not_crash(cli_runner: CliRunner) -> None:
    # `examples` can arrive via a to_info_dict override as raw strings or (description, command) pairs
    # rather than the normalized dicts. Every format coerces to one shape rather than crashing.
    class CustomCommand(RichCommand):
        def to_info_dict(self, ctx: "click.Context") -> "dict[str, Any]":
            info = super().to_info_dict(ctx)
            info["examples"] = ["tool raw", ("Greet", "tool hello")]  # str + tuple, not dicts
            return info

    @command(cls=CustomCommand)
    def cli() -> None:
        """Hi."""

    expected = [{"description": "", "command": "tool raw"}, {"description": "Greet", "command": "tool hello"}]
    assert json.loads(cli_runner.invoke(cli, ["--help=json"]).output)["examples"] == expected
    md = cli_runner.invoke(cli, ["--help=markdown"]).output
    assert "`tool raw`" in md and "Greet: `tool hello`" in md


def test_json_lists_uncontextualizable_subcommand(cli_runner: CliRunner) -> None:
    # A child that raises a ClickException even under resilient parsing can't be entered, but the
    # recursive dump still lists it as a degraded node rather than silently dropping it.
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

    full = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)["subcommands"]
    assert set(full) == {"normal", "eager"}
    # The degraded node carries name/path/help but not the params/usage of a fully-walked command.
    assert full["eager"] == {"name": "eager", "path": "cli eager", "help": "Eager command."}
    # Markdown renders the degraded node as a section rather than breaking on a missing path.
    assert "# `cli eager`" in cli_runner.invoke(cli, ["--help=markdown"]).output


def test_examples_recursive_json(cli_runner: CliRunner) -> None:
    # Examples on a subcommand appear at that node in the recursive dump.
    @group()
    def cli() -> None:
        """Root."""

    @cli.command(examples=[("Run now", "cli sub --now")])
    def sub() -> None:
        """Sub."""

    schema = json.loads(cli_runner.invoke(cli, ["--help=json"]).output)
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

            def placeholder_tokens(example: str) -> set[str]:
                styled = _styled_example_command(example, sub, rctx, formatter)
                ph = formatter.config.style_examples_placeholder
                return {styled.plain[s.start : s.end] for s in styled.spans if s.style == ph}

            # Either spelling of the subcommand is recognised as command path (NOT a placeholder); only
            # the positional `x` is a placeholder.
            assert placeholder_tokens("foo bar --now x") == {"x"}
            assert placeholder_tokens("foo b --now x") == {"x"}
