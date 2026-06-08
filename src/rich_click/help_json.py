"""
Machine-readable ``--help-json`` schema for rich-click CLIs.

Setting the ``help_json`` config option to ``True`` adds a global ``--help-json``
flag to every command and group. The flag prints the *current* command's help,
usage and full parameter detail as a compact JSON object, together with a
recursive index of all subcommand names.

This lets tooling and LLMs discover a CLI one level at a time, without scraping
the rendered ``--help`` text or pulling the whole command tree into context at
once. Agents land on a command, read its parameters as data, and drill into
subcommands by name as needed.

Composability: the schema is built from each command's ``to_info_dict()`` -- the
same Click method that powers introspection elsewhere -- so anything a developer
adds there flows through automatically. Custom command-level fields appear at the
top level; custom parameter fields appear on the parameter. The
``help_json_transform`` config option offers a last-mile hook for developers who
would rather not subclass.

A distinct ``--help-json`` name is used (rather than ``--json``) because many
CLIs already define their own ``--json`` data-output flag; the option name can
be customized via the ``help_json_option_name`` config option.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional

import click


if TYPE_CHECKING:  # pragma: no cover
    from rich_click.rich_parameter import RichOption


DEFAULT_HELP_JSON_OPTION_NAME = "--help-json"
DEFAULT_HELP_JSON_HELP = "Print this command's help/usage as JSON."

#: Type of the optional ``help_json_transform`` hook: ``(schema, command, ctx) -> schema``.
HelpJSONTransform = Callable[[Dict[str, Any], click.Command, click.Context], Dict[str, Any]]

# Keys Click/rich-click put in a *parameter's* ``to_info_dict()``. We map the useful ones onto a
# compact representation deliberately; any key NOT listed here is treated as developer-supplied
# metadata and merged onto the parameter verbatim.
_STANDARD_PARAM_KEYS = frozenset(
    {
        "name",
        "param_type_name",
        "opts",
        "secondary_opts",
        "type",
        "required",
        "nargs",
        "multiple",
        "default",
        "envvar",
        "help",
        "prompt",
        "is_flag",
        "flag_value",
        "count",
        "hidden",
    }
)

# Command-level keys we consume directly. ``commands`` becomes the lean ``subcommands`` name tree;
# ``short_help`` is dropped as redundant with ``help``. Everything else not listed here -- including
# rich-click's ``aliases`` and any developer-supplied fields -- is merged onto the top-level object.
_CONSUMED_CMD_KEYS = frozenset({"name", "help", "params", "commands", "short_help"})


def _strip_markup(text: Optional[str]) -> Optional[str]:
    r"""Render Rich console markup (``[dim]``, ``\[default: …]``, …) to plain text."""
    if not text:
        return text
    from rich.errors import MarkupError
    from rich.text import Text

    try:
        return Text.from_markup(text).plain.strip()
    except MarkupError:
        return text.strip()


def _is_empty(value: Any) -> bool:
    """Report whether a value is worth dropping from the output (None/False/empty), to keep it lean."""
    return value is None or value is False or value == "" or value == [] or value == {}


def _passthrough_extensions(info: Dict[str, Any], consumed: "frozenset[str]") -> Dict[str, Any]:
    """
    Collect developer-supplied / non-standard keys from a ``to_info_dict()`` to pass through.

    Keys we map deliberately (``consumed``) and empty values are skipped; Rich markup is stripped from
    string values so the output stays plain text.
    """
    return {
        key: _strip_markup(value) if isinstance(value, str) else value
        for key, value in info.items()
        if key not in consumed and not _is_empty(value)
    }


def _param_to_dict(info: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a parameter's ``to_info_dict()`` into a compact, JSON-friendly dict."""
    type_info = info.get("type") or {}
    fields = {
        "name": info.get("name"),
        "kind": info.get("param_type_name"),  # "option" or "argument"
        "opts": info.get("opts"),
        "type": type_info.get("param_type"),  # e.g. "Bool", "Int", "String", "Path"
        "choices": type_info.get("choices"),
        "required": info.get("required") or None,
        "is_flag": info.get("is_flag") or None,
        "multiple": info.get("multiple") or None,
        # Hidden params are kept (parity with to_info_dict) but flagged so consumers can skip them.
        "hidden": info.get("hidden") or None,
        "help": _strip_markup(info.get("help")),
    }
    result = {key: value for key, value in fields.items() if not _is_empty(value)}
    # A flag's False default is implied; keep a real default for everything else (including 0 or "").
    default = info.get("default")
    if default is not None and not info.get("is_flag"):
        result["default"] = default
    # Passthrough: developer-supplied custom keys (e.g. a RichOption subclass adding ``sensitive``).
    for key, value in _passthrough_extensions(info, _STANDARD_PARAM_KEYS).items():
        result.setdefault(key, value)
    return result


def _subcommand_index(commands: Dict[str, Any]) -> Dict[str, Any]:
    """
    Index ``to_info_dict()``'s recursive ``commands`` block by name.

    Each entry carries a one-line ``help`` (so an agent can pick where to drill without a round-trip),
    plus ``aliases`` and a nested ``subcommands`` index where present. This mirrors the entry shape
    used by sibling tools (e.g. Nextflow's ``-help-json``) so a single consumer can parse both.
    Reusing the already-computed tree avoids a second full walk of the command hierarchy.
    """
    index: Dict[str, Any] = {}
    for name, info in commands.items():
        entry: Dict[str, Any] = {}
        help_text = _strip_markup(info.get("help"))
        if help_text:
            entry["help"] = help_text.split("\n", 1)[0].strip()  # first line, like a short help
        aliases = info.get("aliases")
        if aliases:
            entry["aliases"] = list(aliases)
        children = info.get("commands")
        if children:
            entry["subcommands"] = _subcommand_index(children)
        index[name] = entry
    return index


def command_schema(
    cmd: click.Command,
    ctx: click.Context,
    exclude: "tuple[click.Parameter, ...]" = (),
) -> Dict[str, Any]:
    """
    Build the machine-readable JSON for a single command level.

    Includes the command's own help, usage and full parameter detail. For groups, a
    ``subcommands`` key holds a recursive name-only index of all descendants.

    The command's ``to_info_dict()`` is the single source of truth, so subclass overrides and
    custom fields flow through: unrecognized command-level keys are merged onto the top-level object
    and unrecognized parameter-level keys onto the parameter (never overwriting a derived key).

    Args:
    ----
        cmd: The command or group to describe.
        ctx: The Click context for ``cmd``.
        exclude: Parameters to omit (e.g. the ``--help-json`` meta-option). The ``--help`` option is
            always excluded. Matched by object identity so a renamed help option still resolves.

    """
    info = cmd.to_info_dict(ctx)

    # Exclude meta-options by identity rather than by name, since the help option's
    # name/flags can be customized via help_option_names.
    exclude_ids = {id(p) for p in exclude}
    get_help_option = getattr(cmd, "get_help_option", None)
    if get_help_option is not None:
        help_option = get_help_option(ctx)
        if help_option is not None:
            exclude_ids.add(id(help_option))

    params = [_param_to_dict(param.to_info_dict()) for param in cmd.get_params(ctx) if id(param) not in exclude_ids]

    schema: Dict[str, Any] = {
        "name": info.get("name"),
        "path": ctx.command_path,
        "help": _strip_markup(info.get("help")),
        "usage": " ".join([ctx.command_path, *cmd.collect_usage_pieces(ctx)]),
        "params": params,
    }
    if "commands" in info:
        schema["subcommands"] = _subcommand_index(info["commands"])

    # Passthrough: rich-click extras (aliases) + any developer-supplied command metadata.
    for key, value in _passthrough_extensions(info, _CONSUMED_CMD_KEYS).items():
        schema.setdefault(key, value)
    return schema


def build_help_json_option(
    option_name: Optional[str] = None,
    help_text: Optional[str] = None,
) -> "RichOption":
    """
    Build the eager ``--help-json`` option that prints the command schema and exits.

    Args:
    ----
        option_name: The flag name to use. Defaults to ``--help-json``.
        help_text: Help text shown for the flag in the regular ``--help`` output.

    """
    from rich_click.rich_parameter import RichOption

    def show_help_json(ctx: click.Context, param: click.Parameter, value: bool) -> None:
        if not value or ctx.resilient_parsing:
            return
        schema = command_schema(ctx.command, ctx, exclude=(param,))
        config = getattr(ctx, "help_config", None)
        transform: Optional[HelpJSONTransform] = getattr(config, "help_json_transform", None)
        if transform is not None:
            schema = transform(schema, ctx.command, ctx)
        click.echo(json.dumps(schema, indent=2, default=str))
        ctx.exit()

    return RichOption(
        [option_name or DEFAULT_HELP_JSON_OPTION_NAME],
        is_flag=True,
        is_eager=True,
        expose_value=False,
        callback=show_help_json,
        help=help_text or DEFAULT_HELP_JSON_HELP,
    )
