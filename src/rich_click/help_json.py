"""
Machine-readable ``--help-json`` schema for rich-click CLIs.

Setting the ``help_json`` config option to ``True`` adds a global ``--help-json``
flag to every command and group. The flag prints the *current* command's help,
usage and full parameter detail as a `JSON Schema <https://json-schema.org>`_
document, together with a recursive index of all subcommand names.

This lets tooling and LLMs discover a CLI one level at a time, without scraping
the rendered ``--help`` text or pulling the whole command tree into context at
once. Agents land on a command, read its parameters as data, and drill into
subcommands by name as needed.

Why JSON Schema? It is a widely understood standard that validators, function-
calling frameworks and LLMs already speak, so the ``type``/``enum``/``required``/
``default`` parts are meaningful without rich-click-specific knowledge. A CLI is
not a JSON document, though, so everything JSON Schema has no vocabulary for
(the actual ``--flag`` spellings, option-vs-argument, usage line, subcommand
tree) lives under ``x-`` extension keys, which validators ignore by spec.

Composability: the schema is built from each command's ``to_info_dict()`` -- the
same Click method that powers introspection elsewhere -- so anything a developer
adds there flows through automatically. Custom command-level fields appear as
``x-<field>`` at the top level; custom parameter fields appear inside the
parameter's ``x-cli`` object. The ``help_json_transform`` config option offers a
last-mile hook for developers who would rather not subclass.

A distinct ``--help-json`` name is used (rather than ``--json``) because many
CLIs already define their own ``--json`` data-output flag; the option name can
be customized via the ``help_json_option_name`` config option.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

import click


if TYPE_CHECKING:  # pragma: no cover
    from rich_click.rich_parameter import RichOption


DEFAULT_HELP_JSON_OPTION_NAME = "--help-json"
DEFAULT_HELP_JSON_HELP = "Print this command's help/usage as JSON."

JSON_SCHEMA_URI = "https://json-schema.org/draft/2020-12/schema"

#: Type of the optional ``help_json_transform`` hook: ``(schema, command, ctx) -> schema``.
HelpJSONTransform = Callable[[Dict[str, Any], click.Command, click.Context], Dict[str, Any]]

# Click param_type names (from ``to_info_dict``) that map cleanly onto a JSON Schema type.
_PARAM_TYPE_TO_JSON_TYPE = {"Int": "integer", "Float": "number", "Bool": "boolean", "String": "string"}

# Keys Click/rich-click put in a *parameter's* ``to_info_dict()``. We map these onto JSON Schema
# or ``x-cli`` deliberately; any key NOT listed here is treated as developer-supplied metadata and
# passed through into ``x-cli`` verbatim.
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

# Command-level keys we consume directly. ``commands`` becomes the lean ``x-subcommands`` name tree;
# ``short_help`` is dropped as redundant with ``help``/``description``. Everything else not listed here
# -- including rich-click's ``panels``/``aliases`` and any developer-supplied fields -- passes through as ``x-``.
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
    Collect developer-supplied / non-standard keys from a ``to_info_dict()`` for ``x-`` passthrough.

    Keys we map deliberately (``consumed``) and empty values are skipped; Rich markup is stripped from
    string values so the output stays plain text.
    """
    return {
        key: _strip_markup(value) if isinstance(value, str) else value
        for key, value in info.items()
        if key not in consumed and not _is_empty(value)
    }


def _param_to_property(info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map a parameter's ``to_info_dict()`` onto a JSON Schema property.

    Standard validation facts (type, enum, default, description) use JSON Schema keywords.
    CLI-specific facts (flag spellings, option-vs-argument, …) and any developer-supplied custom
    keys live under an ``x-cli`` extension object.
    """
    type_info = info.get("type") or {}
    param_type = type_info.get("param_type")

    prop: Dict[str, Any]
    if type_info.get("choices"):
        prop = {"enum": list(type_info["choices"])}
    elif param_type in _PARAM_TYPE_TO_JSON_TYPE:
        prop = {"type": _PARAM_TYPE_TO_JSON_TYPE[param_type]}
    else:
        # CLI input is ultimately text; fall back to "string" and keep the original Click type in x-cli.
        prop = {"type": "string"}

    if info.get("multiple"):
        prop = {"type": "array", "items": prop}

    help_text = _strip_markup(info.get("help"))
    if help_text:
        prop["description"] = help_text

    # A flag's False default is implied; keep a real default for everything else (including 0 or "").
    default = info.get("default")
    if default is not None and not info.get("is_flag"):
        prop["default"] = default

    x_cli: Dict[str, Any] = {"opts": info.get("opts"), "kind": info.get("param_type_name")}
    if info.get("is_flag"):
        x_cli["is_flag"] = True
    if info.get("hidden"):
        # Hidden params are kept (parity with to_info_dict) but flagged so consumers can skip them.
        x_cli["hidden"] = True
    if info.get("secondary_opts"):
        x_cli["secondary_opts"] = info["secondary_opts"]
    if info.get("count"):
        x_cli["count"] = True
    if info.get("nargs") not in (None, 1):
        x_cli["nargs"] = info["nargs"]
    if info.get("envvar"):
        x_cli["envvar"] = info["envvar"]
    if param_type and param_type not in _PARAM_TYPE_TO_JSON_TYPE and not type_info.get("choices"):
        # Preserve the precise Click type (e.g. "Path", "DateTime", "UUID") that JSON Schema flattened to "string".
        x_cli["type"] = param_type
    # Passthrough: developer-supplied custom keys (e.g. a RichOption subclass adding ``sensitive``).
    x_cli.update(_passthrough_extensions(info, _STANDARD_PARAM_KEYS))
    prop["x-cli"] = x_cli
    return prop


def _subcommand_name_tree(commands: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reduce ``to_info_dict()``'s recursive ``commands`` block to a names-only index.

    Leaf commands have no ``commands`` key and map to an empty dict; groups map to a dict of their
    children. Reusing the already-computed tree avoids a second full walk of the command hierarchy.
    """
    return {name: _subcommand_name_tree(info.get("commands", {})) for name, info in commands.items()}


def command_schema(
    cmd: click.Command,
    ctx: click.Context,
    exclude: "tuple[click.Parameter, ...]" = (),
) -> Dict[str, Any]:
    """
    Build the JSON Schema document for a single command level.

    Includes the command's own help, usage and full parameter detail. For groups, an
    ``x-subcommands`` key holds a recursive name-only index of all descendants.

    The command's ``to_info_dict()`` is the single source of truth, so subclass overrides and
    custom fields flow through: unrecognized command-level keys become ``x-<key>`` and unrecognized
    parameter-level keys land in that parameter's ``x-cli`` object.

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

    properties: Dict[str, Any] = {}
    required: List[str] = []
    for param in cmd.get_params(ctx):
        if id(param) in exclude_ids:
            continue
        param_info = param.to_info_dict()
        properties[param_info["name"]] = _param_to_property(param_info)
        if param_info.get("required"):
            required.append(param_info["name"])

    schema: Dict[str, Any] = {"$schema": JSON_SCHEMA_URI, "title": ctx.command_path}
    description = _strip_markup(info.get("help"))
    if description:
        schema["description"] = description
    schema["x-usage"] = " ".join([ctx.command_path, *cmd.collect_usage_pieces(ctx)])
    schema["type"] = "object"
    schema["properties"] = properties
    if required:
        schema["required"] = required
    if "commands" in info:
        schema["x-subcommands"] = _subcommand_name_tree(info["commands"])

    # Passthrough: rich-click extras (panels, aliases) + any developer-supplied command metadata.
    for key, value in _passthrough_extensions(info, _CONSUMED_CMD_KEYS).items():
        schema[f"x-{key}"] = value
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
