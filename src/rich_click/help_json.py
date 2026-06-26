"""
Machine-readable help formats for rich-click CLIs.

These power the format values on the existing ``--help`` flag -- ``--help=json``,
``--help=json-full`` and ``--help=carapace`` -- so tooling and LLM agents can discover
a CLI's structure as data instead of scraping the rendered ``--help`` screen. No new
flag is added; the capability lives on ``--help`` and bare ``--help`` is unchanged.

``--help=json`` uses progressive disclosure: it reports the *current* command's help,
usage and full parameter detail, plus a name-only index of subcommands, so agents land
on a command, read its parameters as data, and drill into subcommands by name as needed.
``--help=json-full`` expands every descendant to full detail in one call; ``--help=carapace``
maps the tree onto the carapace completion spec.

Composability: the schema is built from each command's ``to_info_dict()`` -- the
same Click method that powers introspection elsewhere -- so anything a developer
adds there flows through automatically. Custom command-level fields appear at the
top level; custom parameter fields appear on the parameter.

The serialization mirrors Click's own ``get_help``/``format_help`` split:
``RichCommand.get_help_json()`` serializes whatever ``RichCommand.format_help_json()``
returns, and the latter delegates to :func:`command_schema` here. Subclass and
override ``format_help_json`` for full control, or use the lighter-touch
``help_json_transform`` config option to post-process the schema without subclassing.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Tuple

import click


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

# Keys from a type's ``to_info_dict()`` already represented elsewhere on the parameter, so they are not
# repeated inside ``type_info``: ``param_type`` becomes the top-level ``type`` string, ``choices`` is
# lifted to the top level, and ``name`` is a redundant human label (e.g. "integer range").
_REDUNDANT_TYPE_KEYS = frozenset({"param_type", "name", "choices"})

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


def _is_unset(value: Any) -> bool:
    """
    Report whether a value is genuinely absent (None or an empty string/list/dict). A literal
    ``False`` or ``0`` is *kept* -- it carries meaning in type config (e.g. ``dir_okay: false``).
    """
    return value is None or value == "" or value == [] or value == {}


def _is_empty(value: Any) -> bool:
    """Report whether a value is worth dropping from the output (None/False/empty), to keep it lean."""
    return value is False or _is_unset(value)


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
    kind = info.get("param_type_name")  # "option" or "argument"
    nargs = info.get("nargs")
    is_flag = info.get("is_flag")
    fields = {
        "name": info.get("name"),
        "kind": kind,
        # An argument's opts just repeat its name, so only options carry opts (the actual flags).
        "opts": info.get("opts") if kind == "option" else None,
        # Secondary opts are an option's negation flags, e.g. ``--no-debug`` for ``--debug/--no-debug``.
        "secondary_opts": info.get("secondary_opts") if kind == "option" else None,
        "type": type_info.get("param_type"),  # e.g. "Bool", "Int", "String", "Path"
        "choices": type_info.get("choices"),
        "required": info.get("required") or None,
        "is_flag": is_flag or None,
        # ``-v/-vv/-vvv`` style counters; distinct from a plain boolean flag.
        "count": info.get("count") or None,
        "multiple": info.get("multiple") or None,
        # nargs == 1 is the default and implied; surface variadic (-1) and fixed multi-value (N) params.
        "nargs": nargs if nargs not in (None, 1) else None,
        "envvar": info.get("envvar") or None,
        # The prompt string shown when the option is requested interactively (None if it never prompts).
        "prompt": info.get("prompt"),
        # Hidden params are kept (parity with to_info_dict) but flagged so consumers can skip them.
        "hidden": info.get("hidden") or None,
        "help": _strip_markup(info.get("help")),
    }
    result = {key: value for key, value in fields.items() if not _is_empty(value)}
    # Remaining type constraints (range min/max, DateTime formats, Path flags, Choice case-sensitivity)
    # nest under ``type_info``. This is a straight passthrough -- minus the redundant keys above -- so it
    # stays correct across Click versions and forwards any keys a future ``ParamType`` adds, without this
    # module needing to know them. ``_is_unset`` (not ``_is_empty``) is the filter: a ``False`` in type
    # config is real signal (e.g. ``dir_okay: false`` = "must not be a directory"), so it must survive.
    type_detail = {
        key: value for key, value in type_info.items() if key not in _REDUNDANT_TYPE_KEYS and not _is_unset(value)
    }
    if type_detail:
        result["type_info"] = type_detail
    # A flag's False default is implied; keep a real default for everything else (including 0 or "").
    default = info.get("default")
    if default is not None and not is_flag:
        result["default"] = default
    # ``flag_value`` is the value a flag sets; only meaningful for value-flags (``--upper``/``--lower``
    # sharing a destination). For plain boolean flags it is just ``True``, which is noise, so skip it.
    flag_value = info.get("flag_value")
    if is_flag and not isinstance(flag_value, bool) and not _is_unset(flag_value):
        result["flag_value"] = flag_value
    # Passthrough: developer-supplied custom keys (e.g. a RichOption subclass adding ``sensitive``).
    for key, value in _passthrough_extensions(info, _STANDARD_PARAM_KEYS).items():
        result.setdefault(key, value)
    return result


def _subcommand_index(commands: Dict[str, Any], parent: Optional[click.Command]) -> Dict[str, Any]:
    """
    Index ``to_info_dict()``'s recursive ``commands`` block by name.

    Each entry carries a one-line ``help`` (so an agent can pick where to drill without a round-trip),
    plus ``aliases`` and a nested ``subcommands`` index where present. This mirrors the entry shape
    used by sibling tools (e.g. Nextflow's ``-help-json``) so a single consumer can parse both.
    Reusing the already-computed tree avoids a second full walk of the command hierarchy.

    The summary comes from each command's ``get_short_help_str(limit=120)`` -- Click collapses the
    docstring to its first sentence and truncates on a word boundary with an ellipsis, so summaries
    never cut off mid-word. ``parent`` is the owning group, used to resolve each child command object
    (which carries that method); we fall back to the info dict's first help line if it can't be found.
    """
    index: Dict[str, Any] = {}
    parent_commands = getattr(parent, "commands", {})
    for name, info in commands.items():
        entry: Dict[str, Any] = {}
        child = parent_commands.get(name)
        if child is not None:
            help_text = _strip_markup(child.get_short_help_str(limit=120))
        else:  # custom MultiCommand without a ``commands`` mapping: best-effort first line
            full_help = _strip_markup(info.get("help"))
            help_text = full_help.split("\n", 1)[0].strip() if full_help else None
        if help_text:
            entry["help"] = help_text
        aliases = info.get("aliases")
        if aliases:
            entry["aliases"] = list(aliases)
        children = info.get("commands")
        if children:
            entry["subcommands"] = _subcommand_index(children, child)
        index[name] = entry
    return index


def _meta_option_ids(cmd: click.Command, ctx: click.Context) -> "set[int]":
    """
    Object id of the ``--help`` option, to keep it out of a command's reported params.

    Resolved by identity (not name) so a customized help flag name (e.g. ``-h``) still matches, and so
    recursive walks exclude it at every node without the caller having to thread the option down the tree.
    """
    ids: "set[int]" = set()
    get_help_option = getattr(cmd, "get_help_option", None)
    if get_help_option is not None:
        try:
            option = get_help_option(ctx)
        except Exception:  # pragma: no cover - defensive: a custom command may not support this off-cycle
            option = None
        if option is not None:
            ids.add(id(option))
    return ids


def _iter_child_contexts(cmd: click.Command, ctx: click.Context) -> Iterator[Tuple[str, click.Command, click.Context]]:
    """
    Yield ``(name, child, child_ctx)`` for each subcommand, building a fresh context per child.

    A child that cannot be contextualized (e.g. a custom loader that needs real args) is skipped rather
    than aborting the whole dump. Yields nothing for a leaf command. Powers the recursive
    ``--help=json-full`` and ``--help=carapace`` walks, where every node is described by the same
    machinery a direct ``--help`` on that node would use.
    """
    list_commands = getattr(cmd, "list_commands", None)
    if list_commands is None:
        return
    for name in list_commands(ctx):
        child = cmd.get_command(ctx, name)  # type: ignore[attr-defined]
        if child is None:
            continue
        try:
            child_ctx = child.make_context(name, [], parent=ctx, resilient_parsing=True)
        except click.ClickException:
            # Skip a child that can't be contextualized with no args (a usage/parameter error). A real
            # bug in the child (TypeError, etc.) is NOT swallowed -- it propagates so it isn't masked.
            continue
        yield name, child, child_ctx


def _subcommand_index_full(cmd: click.Command, ctx: click.Context, child_infos: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively expand every descendant to its full schema (params, usage, nested subcommands)."""
    return {
        name: command_schema(child, child_ctx, recursive=True, info=child_infos.get(name))
        for name, child, child_ctx in _iter_child_contexts(cmd, ctx)
    }


def command_schema(
    cmd: click.Command, ctx: click.Context, recursive: bool = False, info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Build the machine-readable JSON for a single command level.

    Includes the command's own help, usage and full parameter detail (the ``--help`` meta-option is
    always excluded). For groups, a ``subcommands`` key holds either a name-only index of descendants
    (the default, progressive disclosure) or -- when ``recursive`` is set -- the full schema of every
    descendant (powering ``--help=json-full``).

    The command's ``to_info_dict()`` is the single source of truth, so subclass overrides and
    custom fields flow through: unrecognized command-level keys are merged onto the top-level object
    and unrecognized parameter-level keys onto the parameter (never overwriting a derived key).

    ``info`` carries a precomputed ``to_info_dict()`` for ``cmd``. Click's ``Group.to_info_dict()``
    already serializes the whole subtree, so the recursive walk reuses those child entries instead of
    re-serializing each subtree -- one ``to_info_dict()`` call for the tree rather than one per node.
    """
    if info is None:
        info = cmd.to_info_dict(ctx)

    exclude_ids = _meta_option_ids(cmd, ctx)

    params = [_param_to_dict(param.to_info_dict()) for param in cmd.get_params(ctx) if id(param) not in exclude_ids]

    schema: Dict[str, Any] = {"name": info.get("name"), "path": ctx.command_path}
    help_text = _strip_markup(info.get("help"))
    if help_text:  # omit rather than emit a null help for undocumented commands
        schema["help"] = help_text
    schema["usage"] = " ".join([ctx.command_path, *cmd.collect_usage_pieces(ctx)])
    schema["params"] = params
    if "commands" in info:
        if recursive:
            schema["subcommands"] = _subcommand_index_full(cmd, ctx, info["commands"])
        else:
            schema["subcommands"] = _subcommand_index(info["commands"], cmd)

    # Passthrough: rich-click extras (aliases) + any developer-supplied command metadata.
    for key, value in _passthrough_extensions(info, _CONSUMED_CMD_KEYS).items():
        schema.setdefault(key, value)
    return schema


def _carapace_flag_name(opts: Sequence[str]) -> str:
    """Return the bare flag name carapace keys completion by (long name preferred, dashes stripped)."""
    longs = [opt for opt in opts if opt.startswith("--")]
    chosen = longs[0] if longs else opts[0]
    return chosen.lstrip("-")


def _carapace_params(
    cmd: click.Command, ctx: click.Context, exclude_ids: "set[int]"
) -> "tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]":
    """
    Split a command's params into the carapace ``flags`` / ``completion`` / ``documentation`` blocks.

    Flag keys use carapace's string syntax: a trailing ``=`` marks a value-taking flag and ``*`` a
    repeatable one. Positional arguments have no first-class carapace object, so they contribute only
    their help (``documentation``) and any ``Choice`` candidates (``completion``).
    """
    flags: Dict[str, Any] = {}
    completion: Dict[str, Any] = {}
    documentation: Dict[str, Any] = {}
    completion_flag: Dict[str, Any] = {}
    positional: List[Any] = []
    positional_doc: List[Any] = []

    for param in cmd.get_params(ctx):
        if id(param) in exclude_ids:
            continue
        info = param.to_info_dict()
        kind = info.get("param_type_name")
        type_info = info.get("type") or {}
        choices = type_info.get("choices")
        help_text = _strip_markup(info.get("help")) or ""

        if kind == "option":
            opts = info.get("opts") or []
            if not opts:
                continue
            is_flag = bool(info.get("is_flag"))
            multiple = bool(info.get("multiple"))
            nargs = info.get("nargs") or 1
            key = ", ".join(opts)
            if not is_flag:
                key += "="
            if multiple:
                key += "*"
            if not is_flag and isinstance(nargs, int) and nargs > 1:
                flags[key] = {"description": help_text, "nargs": nargs}
            else:
                flags[key] = help_text
            # Boolean negation flags (``--no-foo``) become their own bool entries.
            for secondary in info.get("secondary_opts") or []:
                flags[secondary] = help_text
            if choices:
                completion_flag[_carapace_flag_name(opts)] = list(choices)

        elif kind == "argument":
            nargs = info.get("nargs")
            candidates = list(choices) if choices else []
            if nargs == -1:
                if candidates:
                    completion["positionalany"] = candidates
                if help_text:
                    documentation["positionalany"] = help_text
            else:
                positional.append(candidates)
                positional_doc.append(help_text)

    if completion_flag:
        completion["flag"] = completion_flag
    # Only emit the positional completion list if at least one slot actually has candidates.
    if any(positional):
        completion["positional"] = positional
    if any(positional_doc):
        documentation["positional"] = positional_doc
    return flags, completion, documentation


def carapace_command(cmd: click.Command, ctx: click.Context, info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Describe a command (recursively) as a carapace ``Command`` object.

    Conforms to the carapace completion spec (https://carapace.sh/schemas/command.json) so a rich-click
    CLI can act as a producer for carapace's consumer ecosystem. Carapace is a structure + completion
    spec, not a type/validation one, so some rich-click detail is intentionally dropped: parameter
    *types* (Int/Path/...), *defaults*, *envvars* and per-flag *required* have no home in the schema.

    ``info`` is a precomputed ``to_info_dict()`` for ``cmd``; the recursive walk passes each child's
    entry so the whole tree is serialized once rather than re-serialized per node (see
    :func:`command_schema`).
    """
    if info is None:
        info = cmd.to_info_dict(ctx)
    exclude_ids = _meta_option_ids(cmd, ctx)

    result: Dict[str, Any] = {"name": info.get("name") or ctx.info_name or ""}

    get_short_help = getattr(cmd, "get_short_help_str", None)
    description = _strip_markup(get_short_help(limit=120)) if get_short_help is not None else None
    if description:
        result["description"] = description

    aliases = info.get("aliases")
    if aliases:
        result["aliases"] = list(aliases)
    if info.get("hidden"):
        result["hidden"] = True

    # Click groups parse flags strictly before the subcommand; leaves allow them interspersed.
    if getattr(cmd, "list_commands", None) is not None:
        result["parsing"] = "non-interspersed"

    flags, completion, documentation = _carapace_params(cmd, ctx, exclude_ids)
    if flags:
        result["flags"] = flags
    if completion:
        result["completion"] = completion
    if documentation:
        result["documentation"] = documentation

    children = _carapace_subcommands(cmd, ctx, info.get("commands") or {})
    if children:
        result["commands"] = children
    return result


def _carapace_subcommands(cmd: click.Command, ctx: click.Context, child_infos: Dict[str, Any]) -> List[Any]:
    """Recursively build the carapace ``commands`` array."""
    return [
        carapace_command(child, child_ctx, info=child_infos.get(name))
        for name, child, child_ctx in _iter_child_contexts(cmd, ctx)
    ]


# --------------------------------------------------------------------------------------------------
# Markdown (``--help=md`` / ``--help=md-full``).
#
# A presentation layer over the same :func:`command_schema` data, so all the extraction (and the
# serialize-the-tree-once optimisation) is shared with the JSON formats. The output is tuned for LLM
# consumption: headings give hierarchy, every section is titled by the command's full invocation path
# (so it is unambiguous out of context), and parameters are compact pipe tables an LLM parses reliably.
# --------------------------------------------------------------------------------------------------


def _md_escape(value: Any) -> str:
    """Make a value safe for a Markdown table cell: single line, pipes escaped."""
    return str(value).replace("\n", " ").replace("|", "\\|").strip()


def _md_param_type(param: Dict[str, Any]) -> str:
    """Human-readable type label for a parameter, e.g. ``flag``, ``choice: a / b``, ``Int (repeatable)``."""
    if param.get("count"):
        label = "counter"
    elif param.get("is_flag"):
        label = "flag"
    elif param.get("choices"):
        label = "choice: " + " / ".join(str(choice) for choice in param["choices"])
    else:
        label = param.get("type") or "text"
    extras = []
    if param.get("multiple"):
        extras.append("repeatable")
    nargs = param.get("nargs")
    if nargs == -1:
        extras.append("variadic")
    elif isinstance(nargs, int) and nargs > 1:
        extras.append(f"{nargs} values")
    if extras:
        label = f"{label} ({', '.join(extras)})"
    return _md_escape(label)


def _md_param_description(param: Dict[str, Any]) -> str:
    """Help text plus inline env-var / prompt annotations, for a parameter's table cell."""
    parts = []
    if param.get("help"):
        parts.append(param["help"])
    if param.get("envvar"):
        parts.append(f"[env: {param['envvar']}]")
    if param.get("prompt"):
        parts.append(f"[prompt: {param['prompt']}]")
    return _md_escape(" ".join(parts))


def _md_param_table(params: List[Dict[str, Any]], *, is_option: bool) -> List[str]:
    """Render a list of option/argument dicts as a Markdown table."""
    if is_option:
        rows = ["| Option | Type | Required | Default | Description |", "| --- | --- | --- | --- | --- |"]
    else:
        rows = ["| Argument | Type | Required | Description |", "| --- | --- | --- | --- |"]
    for param in params:
        required = "yes" if param.get("required") else ""
        if is_option:
            names = ", ".join(f"`{opt}`" for opt in [*(param.get("opts") or []), *(param.get("secondary_opts") or [])])
            default = f"`{_md_escape(param['default'])}`" if "default" in param else ""
            rows.append(
                f"| {names} | {_md_param_type(param)} | {required} | {default} | {_md_param_description(param)} |"
            )
        else:
            rows.append(
                f"| `{param.get('name', '')}` | {_md_param_type(param)} | {required} | {_md_param_description(param)} |"
            )
    return rows


def _md_subcommand_index(index: Dict[str, Any], lines: List[str], indent: int) -> None:
    """Render the progressive (name-only) subcommand index as a nested bullet list."""
    for name, entry in index.items():
        bullet = "  " * indent + f"- `{name}`"
        if entry.get("aliases"):
            bullet += f" (aliases: {', '.join(entry['aliases'])})"
        if entry.get("help"):
            bullet += f" — {_md_escape(entry['help'])}"
        lines.append(bullet)
        nested = entry.get("subcommands")
        if nested:
            _md_subcommand_index(nested, lines, indent + 1)


def _render_command_markdown(schema: Dict[str, Any], lines: List[str], recursive: bool) -> None:
    """
    Append one command's Markdown section.

    Every command is a top-level (``#``) section titled by its full invocation path, so each is
    self-describing and the document stays flat and uniform -- easier for an LLM to parse than deeply
    nested headings whose level would otherwise collide with the per-command sub-sections. When
    ``recursive``, subcommands are full schemas rendered as their own sections; otherwise they are the
    progressive name index rendered as a bullet list.
    """
    lines += [f"# `{schema.get('path') or schema.get('name') or ''}`", ""]
    if schema.get("help"):
        lines += [schema["help"], ""]
    if schema.get("aliases"):
        lines += [f"**Aliases:** {', '.join(f'`{alias}`' for alias in schema['aliases'])}", ""]
    if schema.get("usage"):
        lines += [f"**Usage:** `{schema['usage']}`", ""]

    params = schema.get("params", [])
    arguments = [p for p in params if p.get("kind") == "argument" and not p.get("hidden")]
    options = [p for p in params if p.get("kind") == "option" and not p.get("hidden")]
    if arguments:
        lines += ["## Arguments", "", *_md_param_table(arguments, is_option=False), ""]
    if options:
        lines += ["## Options", "", *_md_param_table(options, is_option=True), ""]

    subcommands = schema.get("subcommands")
    if subcommands:
        if recursive:
            for entry in subcommands.values():
                _render_command_markdown(entry, lines, recursive=True)
        else:
            lines += ["## Subcommands", ""]
            _md_subcommand_index(subcommands, lines, indent=0)
            lines.append("")


def command_markdown(cmd: click.Command, ctx: click.Context, recursive: bool = False) -> str:
    """
    Render a command as Markdown, tuned for LLM consumption.

    ``recursive=False`` (``--help=md``) documents the current command in full and lists its subcommands
    as a name index; ``recursive=True`` (``--help=md-full``) documents every descendant in full. Built
    from :func:`command_schema`, so it shares the JSON formats' extraction and single ``to_info_dict()``
    walk.
    """
    lines: List[str] = []
    _render_command_markdown(command_schema(cmd, ctx, recursive=recursive), lines, recursive)
    return "\n".join(lines).strip() + "\n"
