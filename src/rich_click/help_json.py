"""
Machine-readable ``--help-json`` schema for rich-click CLIs.

Setting the ``help_json`` config option to ``True`` adds a global ``--help-json``
flag to every command and group. The flag prints the *current* command's help,
usage and full parameter detail as JSON, together with a recursive index of all
subcommand names.

This lets tooling and LLMs discover a CLI one level at a time, without scraping
the rendered ``--help`` text or pulling the whole command tree into context at
once. Agents land on a command, read its parameters as data, and drill into
subcommands by name as needed.

A distinct ``--help-json`` name is used (rather than ``--json``) because many
CLIs already define their own ``--json`` data-output flag; the option name can
be customized via the ``help_json_option_name`` config option.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Dict, Iterable, Optional

import click


if TYPE_CHECKING:  # pragma: no cover
    from rich_click.rich_parameter import RichOption


DEFAULT_HELP_JSON_OPTION_NAME = "--help-json"
DEFAULT_HELP_JSON_HELP = "Print this command's help/usage as JSON, with a recursive index of subcommand names."


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


def _param_to_dict(param: click.Parameter, ctx: click.Context) -> Dict[str, Any]:
    """Convert a Click Option/Argument into a compact, JSON-friendly dict."""
    info = param.to_info_dict()
    type_info = info.get("type") or {}
    fields = {
        "name": info.get("name"),
        "kind": info.get("param_type_name"),  # "option" or "argument"
        "opts": info.get("opts"),
        "type": type_info.get("param_type"),
        "choices": type_info.get("choices"),
        "required": info.get("required") or None,
        "is_flag": info.get("is_flag") or None,
        "multiple": info.get("multiple") or None,
        "help": _strip_markup(info.get("help")),
    }
    # Drop None/False/empty values to keep the output lean. Use identity for None/False so a
    # legitimate falsy value (e.g. a numeric 0, which equals False) is never silently dropped.
    result = {
        key: value
        for key, value in fields.items()
        if value is not None and value is not False and value != "" and value != []
    }
    # Keep a real default (including 0 or "") for non-flag params; a flag's False default is implied.
    default = info.get("default")
    if default is not None and not info.get("is_flag"):
        result["default"] = default
    return result


def _subcommand_name_tree(group: click.Group, ctx: click.Context) -> Dict[str, Any]:
    """
    Recursively map subcommand names to nested children (names only, no help text).

    Leaf commands map to an empty dict; groups map to a dict of their children.
    """
    tree: Dict[str, Any] = {}
    for name in group.list_commands(ctx):
        sub = group.get_command(ctx, name)
        if sub is None:
            continue
        if isinstance(sub, click.Group):
            # A child context is needed only so list_commands/get_command can resolve the next level.
            sub_ctx = click.Context(sub, info_name=name, parent=ctx)
            tree[name] = _subcommand_name_tree(sub, sub_ctx)
        else:
            tree[name] = {}
    return tree


def command_schema(
    cmd: click.Command,
    ctx: click.Context,
    exclude: Iterable[click.Parameter] = (),
) -> Dict[str, Any]:
    """
    Build the JSON schema for a single command level.

    Includes the command's own help, usage and full parameter detail. For groups,
    a ``subcommands`` key holds a recursive name-only index of all descendants.

    Args:
    ----
        cmd: The command or group to describe.
        ctx: The Click context for ``cmd``.
        exclude: Parameters to omit (e.g. the ``--help-json`` meta-option). The
            ``--help`` option is always excluded. Matched by object identity so a
            renamed help option still resolves correctly.

    """
    # Exclude meta-options by identity rather than by name, since the help option's
    # name/flags can be customized via help_option_names.
    exclude_ids = {id(p) for p in exclude}
    get_help_option = getattr(cmd, "get_help_option", None)
    if get_help_option is not None:
        help_option = get_help_option(ctx)
        if help_option is not None:
            exclude_ids.add(id(help_option))
    schema: Dict[str, Any] = {
        "name": cmd.name,
        "path": ctx.command_path,
        "help": _strip_markup(cmd.help),
        "usage": " ".join([ctx.command_path, *cmd.collect_usage_pieces(ctx)]),
        "params": [_param_to_dict(p, ctx) for p in cmd.get_params(ctx) if id(p) not in exclude_ids],
    }
    aliases = getattr(cmd, "aliases", None)
    if aliases:
        schema["aliases"] = list(aliases)
    if isinstance(cmd, click.Group):
        schema["subcommands"] = _subcommand_name_tree(cmd, ctx)
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
