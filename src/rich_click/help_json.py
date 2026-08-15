"""
Machine-readable help formats for rich-click CLIs.

These power the format values on the existing ``--help`` flag -- ``--help markdown``,
``--help json``, ``--help json-full`` and ``--help carapace`` -- so tooling and LLM agents can
discover a CLI's structure as data instead of scraping the rendered ``--help`` screen. No new
flag is added; the capability lives on ``--help`` and bare ``--help`` is unchanged.

``--help markdown`` renders the structure as LLM-friendly Markdown; like ``--help json`` it uses
progressive disclosure, reporting the *current* command's help, usage and full parameter detail,
plus a name-only index of subcommands, so agents land on a command, read its parameters as data,
and drill into subcommands by name as needed. The ``-full`` variants (``--help markdown-full`` /
``--help json-full``) expand every descendant to full detail in one call; ``--help carapace``
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

from collections.abc import Callable, Iterator, Sequence
from typing import Any

import click


#: Type of the optional ``help_json_transform`` hook: ``(schema, command, ctx) -> schema``.
HelpJSONTransform = Callable[[dict[str, Any], click.Command, click.Context], dict[str, Any]]

#: Type of a custom ``--help`` format renderer registered via the ``help_formats`` config option:
#: ``(command, ctx) -> str``. Lets a new ``--help <name>`` format be added without subclassing.
HelpFormatRenderer = Callable[[click.Command, click.Context], str]

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
# ``short_help`` is dropped as redundant with ``help``; ``examples`` is emitted explicitly. Everything
# else not listed here -- including rich-click's ``aliases`` and any developer-supplied fields -- is
# merged onto the top-level object.
_CONSUMED_CMD_KEYS = frozenset({"name", "help", "params", "commands", "short_help", "examples"})


def _strip_markup(text: str | None) -> str | None:
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


def _passthrough_extensions(info: dict[str, Any], consumed: frozenset[str]) -> dict[str, Any]:
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


def _coerce_examples(value: Any) -> list[dict[str, str]]:
    """
    Coerce a command's ``examples`` into a list of ``{"description", "command"}`` dicts.

    The normal ``examples=`` path already stores this shape (see ``RichCommand._normalize_examples``),
    but ``examples`` can also reach us via a ``to_info_dict()`` override -- the documented extension
    point -- where it may instead be raw ``(description, command)`` pairs, bare command strings, or
    dicts. Normalizing at this single chokepoint means every output format (JSON, carapace, Markdown)
    sees one consistent shape rather than each defending against the others' assumptions. Items that
    can't be coerced are skipped rather than crashing the dump.
    """
    examples: list[dict[str, str]] = []
    for item in value or []:
        if isinstance(item, dict):
            command = item.get("command")
            if command is None:
                continue
            examples.append({"description": str(item.get("description") or ""), "command": str(command)})
        elif isinstance(item, str):
            examples.append({"description": "", "command": item})
        else:
            # A (description, command) pair, like the constructor accepts.
            try:
                description, command = item
            except (TypeError, ValueError):
                continue
            examples.append({"description": str(description), "command": str(command)})
    return examples


def _param_to_dict(info: dict[str, Any]) -> dict[str, Any]:
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


def _subcommand_index(commands: dict[str, Any], parent: click.Command | None) -> dict[str, Any]:
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
    index: dict[str, Any] = {}
    parent_commands = getattr(parent, "commands", {})
    for name, info in commands.items():
        entry: dict[str, Any] = {}
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


def _help_option_ids(cmd: click.Command, ctx: click.Context) -> set[int]:
    """
    Object id of the ``--help`` option, used to recognise it among a command's params.

    The ``--help`` option *is* reported (like the rendered help screen), but it is recognised here so we
    can enrich it with the machine-readable formats it accepts (see :func:`_help_format_names`).
    Resolved by identity (not name) so a customized help flag name (e.g. ``-h``) still matches, and so
    recursive walks find it at every node without the caller having to thread the option down the tree.
    """
    ids: set[int] = set()
    get_help_option = getattr(cmd, "get_help_option", None)
    if get_help_option is not None:
        try:
            option = get_help_option(ctx)
        except Exception:  # pragma: no cover - defensive: a custom command may not support this off-cycle
            option = None
        if option is not None:
            ids.add(id(option))
    return ids


def _help_format_names(cmd: click.Command, ctx: click.Context | None = None) -> list[str]:
    """
    Return the machine-readable format values ``--help`` accepts (``markdown``, ``json``, ...).

    Built-ins come from the command's ``help_formats`` registry, de-duplicated by target so an alias
    (``md``) is not listed next to its canonical name (``markdown``). Any process-wide custom formats
    registered on the config (``help_formats``) are appended. Surfaced as the ``--help`` option's
    ``choices`` and in its metavar, so both a human and an agent can discover the formats exist.
    """
    names: list[str] = []
    seen_targets: set[str] = set()
    for name, target in (getattr(cmd, "help_formats", None) or {}).items():
        if target not in seen_targets:
            seen_targets.add(target)
            names.append(name)
    config = getattr(ctx, "help_config", None)
    for name in getattr(config, "help_formats", None) or {}:
        if name not in names:
            names.append(name)
    return names


def _iter_child_contexts(cmd: click.Command, ctx: click.Context) -> Iterator[tuple[str, click.Command, click.Context]]:
    """
    Yield ``(name, child, child_ctx)`` for each subcommand, building a fresh context per child.

    A child that cannot be contextualized (e.g. a custom loader that needs real args) is skipped rather
    than aborting the whole dump. Yields nothing for a leaf command. Powers the recursive
    ``--help json-full`` and ``--help carapace`` walks, where every node is described by the same
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
            # ``resilient_parsing=True`` suppresses the usual missing-required-argument / bad-value
            # errors, so this only fires for a child that raises a ClickException *even under resilient
            # parsing* -- e.g. a custom command that validates eagerly in ``make_context``/``parse_args``.
            # Such a child can't be entered, so it's skipped here. Callers that need set-equality with the
            # lean index recover it: ``_subcommand_index_full`` falls back to a degraded node so it still
            # appears (carapace, a completion spec, simply omits what it can't introspect). A real bug in
            # the child (TypeError, etc.) is NOT swallowed -- it propagates so it isn't masked.
            continue
        yield name, child, child_ctx


def _degraded_schema(name: str, info: dict[str, Any], parent_ctx: click.Context) -> dict[str, Any]:
    """
    Minimal schema node for a child that couldn't be contextualized (raised a ClickException even under
    resilient parsing), so it can't be fully expanded.

    Built from its ``to_info_dict()`` alone -- no context -- so the recursive formats still list it
    (matching the lean ``--help json`` index) instead of silently dropping it. Its own descendants are
    not walked, since we couldn't enter it; consumers can re-run ``--help`` on that command directly.
    """
    schema: dict[str, Any] = {"name": info.get("name") or name, "path": f"{parent_ctx.command_path} {name}".strip()}
    help_text = _strip_markup(info.get("help"))
    if help_text:
        schema["help"] = help_text
    for key, value in _passthrough_extensions(info, _CONSUMED_CMD_KEYS).items():
        schema.setdefault(key, value)
    return schema


def _subcommand_index_full(cmd: click.Command, ctx: click.Context, child_infos: dict[str, Any]) -> dict[str, Any]:
    """
    Recursively expand every descendant to its full schema (params, usage, nested subcommands).

    Iterates ``child_infos`` -- the same ``to_info_dict()``-derived source the lean index uses -- so the
    full walk lists exactly the same subcommands as ``--help json`` (a child that can't be entered gets a
    degraded node rather than vanishing), and the ordering stays stable.
    """
    full = {
        name: command_schema(child, child_ctx, recursive=True, info=child_infos.get(name))
        for name, child, child_ctx in _iter_child_contexts(cmd, ctx)
    }
    return {
        name: full[name] if name in full else _degraded_schema(name, info, ctx) for name, info in child_infos.items()
    }


def command_schema(
    cmd: click.Command, ctx: click.Context, recursive: bool = False, info: dict[str, Any] | None = None
) -> dict[str, Any]:
    """
    Build the machine-readable JSON for a single command level.

    Includes the command's own help, usage and full parameter detail -- including the ``--help``
    option, just as the rendered help screen lists it, enriched with the machine-readable formats it
    accepts (its ``choices``). For groups, a ``subcommands`` key holds either a name-only index of
    descendants (the default, progressive disclosure) or -- when ``recursive`` is set -- the full schema
    of every descendant (powering ``--help json-full``).

    The command's ``to_info_dict()`` is the single source of truth, so subclass overrides and
    custom fields flow through: unrecognized command-level keys are merged onto the top-level object
    and unrecognized parameter-level keys onto the parameter (never overwriting a derived key).

    ``info`` carries a precomputed ``to_info_dict()`` for ``cmd``. Click's ``Group.to_info_dict()``
    already serializes the whole subtree, so the recursive walk reuses those child entries instead of
    re-serializing each subtree -- one ``to_info_dict()`` call for the tree rather than one per node.
    """
    if info is None:
        info = cmd.to_info_dict(ctx)

    help_ids = _help_option_ids(cmd, ctx)

    params = []
    for param in cmd.get_params(ctx):
        param_dict = _param_to_dict(param.to_info_dict())
        # Surface the formats ``--help`` accepts as its choices, so an agent discovers them in the data.
        if id(param) in help_ids and not param_dict.get("choices"):
            formats = _help_format_names(cmd, ctx)
            if formats:
                param_dict["choices"] = formats
        params.append(param_dict)

    schema: dict[str, Any] = {"name": info.get("name"), "path": ctx.command_path}
    help_text = _strip_markup(info.get("help"))
    if help_text:  # omit rather than emit a null help for undocumented commands
        schema["help"] = help_text
    schema["usage"] = " ".join([ctx.command_path, *cmd.collect_usage_pieces(ctx)])
    schema["params"] = params
    examples = _coerce_examples(info.get("examples"))
    if examples:
        schema["examples"] = examples
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
    cmd: click.Command, ctx: click.Context, help_ids: set[int]
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """
    Split a command's params into the carapace ``flags`` / ``completion`` / ``documentation`` blocks.

    Flag keys use carapace's string syntax: a trailing ``=`` marks a value-taking flag and ``*`` a
    repeatable one. Positional arguments have no first-class carapace object, so they contribute only
    their help (``documentation``) and any ``Choice`` candidates (``completion``). The ``--help`` option
    (in ``help_ids``) is included like any other, with the formats it accepts as its completions.
    """
    flags: dict[str, Any] = {}
    completion: dict[str, Any] = {}
    documentation: dict[str, Any] = {}
    completion_flag: dict[str, Any] = {}
    positional: list[Any] = []
    positional_doc: list[Any] = []

    for param in cmd.get_params(ctx):
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
            elif id(param) in help_ids:
                # ``--help`` is not a Choice type, but it accepts the machine-readable format values;
                # offer those as completions so `--help <TAB>` suggests markdown/json/...
                formats = _help_format_names(cmd, ctx)
                if formats:
                    completion_flag[_carapace_flag_name(opts)] = formats

        elif kind == "argument":
            nargs = info.get("nargs")
            candidates = list(choices) if choices else []
            if nargs == -1:
                if candidates:
                    completion["positionalany"] = candidates
                if help_text:
                    documentation["positionalany"] = help_text
            else:
                # A fixed-arity argument occupies ``nargs`` positional slots (nargs defaults to 1).
                # Carapace's positional arrays hold one entry per slot, so repeat this argument's
                # candidates/help once per slot it consumes -- otherwise an ``nargs=2`` argument would
                # shift every later positional one slot to the left and mis-target its completions.
                slots = nargs if isinstance(nargs, int) and nargs > 0 else 1
                for _ in range(slots):
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


def carapace_command(cmd: click.Command, ctx: click.Context, info: dict[str, Any] | None = None) -> dict[str, Any]:
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
    help_ids = _help_option_ids(cmd, ctx)

    result: dict[str, Any] = {"name": info.get("name") or ctx.info_name or ""}

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

    flags, completion, documentation = _carapace_params(cmd, ctx, help_ids)
    if flags:
        result["flags"] = flags
    if completion:
        result["completion"] = completion
    if documentation:
        result["documentation"] = documentation

    # Carapace's ``examples`` is a {string: string} map; we key it by the command line. (Two examples
    # that share a command line collapse to one entry -- see the carapace note in the docs.)
    examples = _coerce_examples(info.get("examples"))
    if examples:
        result["examples"] = {ex["command"]: ex["description"] for ex in examples}

    children = _carapace_subcommands(cmd, ctx, info.get("commands") or {})
    if children:
        result["commands"] = children
    return result


def _carapace_subcommands(cmd: click.Command, ctx: click.Context, child_infos: dict[str, Any]) -> list[Any]:
    """Recursively build the carapace ``commands`` array."""
    return [
        carapace_command(child, child_ctx, info=child_infos.get(name))
        for name, child, child_ctx in _iter_child_contexts(cmd, ctx)
    ]


# --------------------------------------------------------------------------------------------------
# Markdown (``--help markdown`` / ``--help markdown-full``).
#
# A presentation layer over the same :func:`command_schema` data, so all the extraction (and the
# serialize-the-tree-once optimisation) is shared with the JSON formats. The output is tuned for LLM
# consumption: headings give hierarchy, every section is titled by the command's full invocation path
# (so it is unambiguous out of context), and parameters are compact pipe tables an LLM parses reliably.
# --------------------------------------------------------------------------------------------------


def _md_escape(value: Any) -> str:
    """Make a value safe for a Markdown table cell: single line, pipes escaped."""
    return str(value).replace("\n", " ").replace("|", "\\|").strip()


def _md_param_type(param: dict[str, Any]) -> str:
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


def _md_param_description(param: dict[str, Any]) -> str:
    """Help text plus inline env-var / prompt annotations, for a parameter's table cell."""
    parts = []
    if param.get("help"):
        parts.append(param["help"])
    if param.get("envvar"):
        parts.append(f"[env: {param['envvar']}]")
    if param.get("prompt"):
        parts.append(f"[prompt: {param['prompt']}]")
    return _md_escape(" ".join(parts))


def _md_param_names(param: dict[str, Any], *, is_option: bool) -> str:
    """Return the identifying cell of a parameter row: an option's flags, or an argument's name."""
    if is_option:
        return ", ".join(f"`{opt}`" for opt in [*(param.get("opts") or []), *(param.get("secondary_opts") or [])])
    return f"`{param.get('name', '')}`"


def _md_param_table(params: list[dict[str, Any]], *, is_option: bool) -> list[str]:
    """
    Render a list of option/argument dicts as a Markdown table.

    Any column that is empty for *every* row -- typically Required and Default -- is dropped rather than
    rendered as a run of empty cells. For an agent reading the help, an all-empty column is pure token
    padding, and dropping it costs no information. The name column is always kept, since it is what
    identifies the row.
    """
    headers = ["Option" if is_option else "Argument", "Type", "Required", "Default", "Description"]
    rows: list[list[str]] = []
    for param in params:
        rows.append(
            [
                _md_param_names(param, is_option=is_option),
                _md_param_type(param),
                "yes" if param.get("required") else "",
                # An argument with a default carries it in the schema just like an option does, so render
                # a Default column for both -- otherwise a positional's default silently disappears.
                f"`{_md_escape(param['default'])}`" if "default" in param else "",
                _md_param_description(param),
            ]
        )
    keep = [0, *(index for index in range(1, len(headers)) if any(row[index] for row in rows))]
    return [
        "| " + " | ".join(headers[index] for index in keep) + " |",
        "| " + " | ".join("---" for _ in keep) + " |",
        *("| " + " | ".join(row[index] for index in keep) + " |" for row in rows),
    ]


#: Metavars for the parameter types Click ships, keyed by the ``param_type`` in its ``to_info_dict()``.
#: Used by the compact signature renderings, which have no description column to lean on -- the metavar
#: is what tells a reader (or an agent) what an option expects. Mirrors the metavars Click's own
#: ``ParamType.get_metavar()`` produces, so the two renderings agree. An unknown (custom) type falls
#: back to its uppercased name.
_MD_METAVAR_BY_TYPE = {
    "String": "TEXT",
    "Int": "INTEGER",
    "Float": "FLOAT",
    "Bool": "BOOLEAN",
    "UUID": "UUID",
    "File": "FILENAME",
    "Path": "PATH",
    "IntRange": "INTEGER RANGE",
    "FloatRange": "FLOAT RANGE",
    "DateTime": "DATETIME",
    "Tuple": "TEXT",
    "FuncParamType": "TEXT",
    "Unprocessed": "TEXT",
}


def _md_param_metavar(param: dict[str, Any]) -> str:
    """
    Return the value a parameter takes, as it would appear on the command line.

    Choices are spelled out (``[a|b|c]``) rather than named, because the choice values *are* the
    vocabulary an agent needs to construct a valid invocation. Flags take no value, so they get none.
    """
    if param.get("is_flag") or param.get("count"):
        return ""
    choices = param.get("choices")
    if choices:
        metavar = "[" + "|".join(str(choice) for choice in choices) + "]"
    else:
        type_name = param.get("type")
        metavar = _MD_METAVAR_BY_TYPE.get(str(type_name), str(type_name).upper() if type_name else "TEXT")
    nargs = param.get("nargs")
    if nargs == -1:
        metavar = f"[{metavar}]..."
    elif isinstance(nargs, int) and nargs > 1:
        metavar = " ".join([metavar] * nargs)
    if param.get("multiple"):
        metavar += "..."
    return metavar


def _md_param_signature(param: dict[str, Any], *, is_option: bool = True) -> str:
    """Return a parameter's names and the value it takes, e.g. ``-c, --count INTEGER`` or ``--mode [a|b]``."""
    if is_option:
        names = ", ".join([*(param.get("opts") or []), *(param.get("secondary_opts") or [])])
    else:
        names = str(param.get("name", ""))
    return f"{names} {_md_param_metavar(param)}".strip()


def _md_short_help(text: str | None, limit: int = 120) -> str:
    """
    Collapse a command's help down to a single summary line.

    Mirrors what Click's ``get_short_help_str`` does with a docstring -- first paragraph, cut at the
    first sentence, truncated on a word boundary -- but works from the schema's already-extracted help
    text, so the recursive walk needs no second pass over the command objects to summarise a node.
    """
    if not text:
        return ""
    summary = " ".join(text.strip().split("\n\n", 1)[0].split())
    sentence, separator, _ = summary.partition(". ")
    if separator:
        summary = f"{sentence}."
    if len(summary) > limit:
        summary = summary[: limit - 3].rsplit(" ", 1)[0] + "..."
    return summary


def _md_subcommand_index(index: dict[str, Any], lines: list[str], indent: int) -> None:
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


def _render_command_body(schema: dict[str, Any], lines: list[str]) -> None:
    """
    Append one command's own Markdown -- everything but its subcommands (level **L2**, "full").

    Every command is a top-level (``#``) section titled by its full invocation path, so each is
    self-describing and the document stays flat and uniform -- easier for an LLM to parse than deeply
    nested headings whose level would otherwise collide with the per-command sub-sections.
    """
    lines += [f"# `{schema.get('path') or schema.get('name') or ''}`", ""]
    if schema.get("help"):
        lines += [schema["help"], ""]
    if schema.get("aliases"):
        lines += [f"**Aliases:** {', '.join(f'`{alias}`' for alias in schema['aliases'])}", ""]
    if schema.get("usage"):
        lines += [f"**Usage:** `{schema['usage']}`", ""]

    if schema.get("examples"):
        lines += ["## Examples", ""]
        for example in schema["examples"]:
            lines.append(f"- {_md_escape(example['description'])}: `{example['command']}`")
        lines.append("")

    params = schema.get("params", [])
    arguments = [p for p in params if p.get("kind") == "argument" and not p.get("hidden")]
    options = [p for p in params if p.get("kind") == "option" and not p.get("hidden")]
    if arguments:
        lines += ["## Arguments", "", *_md_param_table(arguments, is_option=False), ""]
    if options:
        lines += ["## Options", "", *_md_param_table(options, is_option=True), ""]


def _render_command_signature(schema: dict[str, Any], lines: list[str]) -> None:
    """
    Append a command's *signature* section (level **L1**) -- the middle tier of adaptive disclosure.

    Usage line, one-line summary, and the command's options as a bare signature list: names, metavars
    and choice values, with no description column. That is the vocabulary an agent needs to tell whether
    a command is the one it wants and to build a syntactically valid invocation, at a fraction of the
    cost of the full option table. Positional arguments are already spelled out in the usage line, so
    they are not repeated here.
    """
    lines += [f"# `{schema.get('path') or schema.get('name') or ''}`", ""]
    summary = _md_short_help(schema.get("help"))
    if summary:
        lines += [summary, ""]
    if schema.get("aliases"):
        lines += [f"**Aliases:** {', '.join(f'`{alias}`' for alias in schema['aliases'])}", ""]
    if schema.get("usage"):
        lines += [f"**Usage:** `{schema['usage']}`", ""]

    options = [p for p in schema.get("params", []) if p.get("kind") == "option" and not p.get("hidden")]
    if options:
        lines += ["## Options", ""]
        for param in options:
            required = " (required)" if param.get("required") else ""
            lines.append(f"- `{_md_param_signature(param)}`{required}")
        lines.append("")


def _render_command_pointer(schema: dict[str, Any]) -> str:
    """Render a command as a single index bullet (level **L0**) -- name, aliases, one-line summary."""
    bullet = f"- `{schema.get('name') or ''}`"
    if schema.get("aliases"):
        bullet += f" (aliases: {', '.join(schema['aliases'])})"
    summary = _md_short_help(schema.get("help"))
    if summary:
        bullet += f" — {_md_escape(summary)}"
    return bullet


def _render_command_markdown(schema: dict[str, Any], lines: list[str], recursive: bool) -> None:
    """
    Append one command's Markdown section, including its subcommands.

    When ``recursive``, subcommands are full schemas rendered as their own sections; otherwise they are
    the progressive name index rendered as a bullet list.
    """
    _render_command_body(schema, lines)

    subcommands = schema.get("subcommands")
    if subcommands:
        if recursive:
            for entry in subcommands.values():
                _render_command_markdown(entry, lines, recursive=True)
        else:
            lines += ["## Subcommands", ""]
            _md_subcommand_index(subcommands, lines, indent=0)
            lines.append("")


# --------------------------------------------------------------------------------------------------
# Adaptive disclosure for ``--help markdown``.
#
# Plain progressive disclosure -- the invoked command in full, its descendants as name-only rows -- is
# cheap but makes an agent *guess*: the vocabulary that decides which subcommand is the right one lives
# in option help text, which a name-only row does not carry. So the agent descends, reads, backtracks,
# and burns turns. Dumping the whole tree instead (``--help markdown-full``) removes the guessing, but
# does not scale to a large CLI.
#
# Adaptive disclosure is the middle path, and needs no configuration: render the invoked command in
# full, then keep promoting descendants -- nearest hop first -- to richer detail levels for as long as
# the estimated size of the whole response stays under a token ceiling. A small or mid-size CLI (the
# overwhelming majority) therefore emits its *entire* tree in full detail, and only a genuinely large
# one degrades, gracefully and nearest-first.
# --------------------------------------------------------------------------------------------------

#: Characters per token, used to estimate a response's size without a tokenizer dependency.
#:
#: Measured against real rendered Markdown help: the tables, backticks, flag names and punctuation that
#: dominate this output tokenize far more densely than prose (~4 chars/token), landing around 3.3. The
#: constant is deliberately on the pessimistic side -- underestimating the size would let a response
#: overshoot its budget, while overestimating only makes the renderer slightly more conservative.
CHARS_PER_TOKEN = 3.3

#: The three per-node detail levels the adaptive renderer promotes between.
DETAIL_POINTER = 0
"""Name + one-line description, as a row in the parent's subcommand index."""
DETAIL_SIGNATURE = 1
"""Usage, one-line description and a compact option signature list (no descriptions)."""
DETAIL_FULL = 2
"""Everything: description, usage, examples and the full option/argument tables."""

#: Tokens held back from the ceiling for the closing note, which is only emitted when the tree did not
#: fit in full and therefore has to tell the reader how to get the rest.
_BUDGET_NOTE_TOKENS = 80


def estimate_tokens(text: str) -> int:
    """
    Estimate how many tokens a string costs, without a tokenizer.

    A deliberate approximation (see :data:`CHARS_PER_TOKEN`): the adaptive renderer only needs to
    compare a response against a ceiling, and a real tokenizer would mean a heavyweight dependency and
    a per-render cost, to decide something a ratio decides just as well.
    """
    return _tokens_from_chars(len(text))


def _tokens_from_chars(chars: int) -> int:
    """Convert a character count to the estimated token count, rounding up."""
    import math

    return math.ceil(chars / CHARS_PER_TOKEN)


class _MarkdownNode:
    """
    One command in the tree the adaptive renderer budgets over.

    Each node caches its rendering at every detail level, along with that rendering's character count,
    so the promotion loop can price a candidate tree by walking node totals instead of re-rendering the
    document on every attempt.
    """

    __slots__ = ("children", "level", "schema", "_pointer", "_sections")

    def __init__(self, schema: dict[str, Any]) -> None:
        self.schema = schema
        self.level = DETAIL_POINTER
        self.children = [_MarkdownNode(child) for child in (schema.get("subcommands") or {}).values()]
        self._sections: dict[int, tuple[list[str], int]] = {}
        self._pointer: tuple[str, int] | None = None

    def section(self, level: int) -> tuple[list[str], int]:
        """Return this node's own section at ``level`` (L1 or L2), as ``(lines, characters)``."""
        cached = self._sections.get(level)
        if cached is None:
            lines: list[str] = []
            if level == DETAIL_FULL:
                _render_command_body(self.schema, lines)
            else:
                _render_command_signature(self.schema, lines)
            cached = (lines, _line_chars(lines))
            self._sections[level] = cached
        return cached

    def pointer(self) -> tuple[str, int]:
        """Return this node's index bullet (L0), as ``(line, characters)``, excluding its indent."""
        if self._pointer is None:
            line = _render_command_pointer(self.schema)
            self._pointer = (line, len(line) + 1)
        return self._pointer


def _line_chars(lines: Sequence[str]) -> int:
    """Count the characters a block of lines occupies once joined with newlines."""
    return sum(len(line) + 1 for line in lines)


def _breadth_first(root: _MarkdownNode) -> list[_MarkdownNode]:
    """Return the tree in breadth-first order: nearest hop first, declaration order within a hop."""
    order = [root]
    index = 0
    while index < len(order):
        order.extend(order[index].children)
        index += 1
    return order


def _emit(node: _MarkdownNode, indent: int, out: list[str] | None) -> int:
    """
    Render (when ``out`` is given) and price one node and its descendants at their current levels.

    Doubling as the renderer and the estimator is deliberate: a separate size model would be free to
    drift from what is actually emitted, and a budget computed from a stale model is worse than no
    budget at all. Sections come out in the same depth-first order ``--help markdown-full`` uses, so a
    tree that is entirely at L2 renders byte-for-byte like ``markdown-full``.
    """
    if node.level == DETAIL_POINTER:
        line, chars = node.pointer()
        prefix = "  " * indent
        if out is not None:
            out.append(prefix + line)
        total = chars + len(prefix)
        for child in node.children:
            total += _emit(child, indent + 1, out)
        return total

    lines, total = node.section(node.level)
    if out is not None:
        out.extend(lines)
    # Children that were not promoted are listed as an index under this node, the nearest ancestor with
    # a section of its own; promoted ones follow as their own sections.
    pointers = [child for child in node.children if child.level == DETAIL_POINTER]
    if pointers:
        if out is not None:
            out += ["## Subcommands", ""]
        total += _line_chars(["## Subcommands", ""])
        for child in pointers:
            total += _emit(child, 0, out)
        if out is not None:
            out.append("")
        total += 1
    for child in node.children:
        if child.level != DETAIL_POINTER:
            total += _emit(child, 0, out)
    return total


def _promote(root: _MarkdownNode, order: Sequence[_MarkdownNode], max_tokens: int) -> None:
    """
    Promote descendants L0 -> L1 -> L2, breadth-first, for as long as the response fits the ceiling.

    Two passes, not one: lifting every node to a signature before lifting any node to full detail
    spends the budget on *breadth* first, so a large CLI still exposes every command's option names --
    the vocabulary that tells an agent which command it wants -- rather than exhaustively documenting
    the first few commands and leaving the rest as bare names.

    Promotion stops entirely at the first step that would not fit, rather than skipping that node and
    trying smaller ones. That keeps what is disclosed a contiguous nearest-first prefix of the tree
    (a node is never richer than its parent) and keeps the result a pure function of the tree and the
    ceiling -- the same command always renders the same help.
    """
    for target in (DETAIL_SIGNATURE, DETAIL_FULL):
        for node in order:
            if node.level >= target:
                continue
            node.level = target
            if _tokens_from_chars(_emit(root, 0, None)) > max_tokens:
                node.level = target - 1
                return


def _budget_note(root: _MarkdownNode, order: Sequence[_MarkdownNode]) -> str:
    """Build the closing note telling the reader what was abbreviated, and how to get the rest."""
    full = sum(1 for node in order if node.level == DETAIL_FULL)
    signature = sum(1 for node in order if node.level == DETAIL_SIGNATURE)
    path = root.schema.get("path") or root.schema.get("name") or ""
    return (
        f"> **Note:** this help was size-limited: {full} command(s) documented in full, {signature} in "
        f"brief, {len(order) - full - signature} listed by name only. Run "
        f"`{path} <COMMAND> --help markdown` on any command for its full detail."
    )


def adaptive_command_markdown(cmd: click.Command, ctx: click.Context, max_tokens: int) -> str:
    """
    Render a command tree as Markdown, disclosing as much detail as ``max_tokens`` allows.

    The invoked command is always rendered in full; its descendants are promoted breadth-first from a
    name-only pointer, through a compact signature, to full detail, until the ceiling is reached. Trees
    that fit entirely are emitted in full -- identical to ``--help markdown-full`` -- and only larger
    ones degrade, nearest hop first.
    """
    root = _MarkdownNode(command_schema(cmd, ctx, recursive=True))
    order = _breadth_first(root)

    for node in order:
        node.level = DETAIL_FULL
    truncated = _tokens_from_chars(_emit(root, 0, None)) > max_tokens
    if truncated:
        for node in order:
            node.level = DETAIL_POINTER
        root.level = DETAIL_FULL  # the invoked command is never abbreviated
        _promote(root, order[1:], max_tokens - _BUDGET_NOTE_TOKENS)

    lines: list[str] = []
    _emit(root, 0, lines)
    if truncated:
        lines += ["", _budget_note(root, order)]
    return "\n".join(lines).strip() + "\n"


def command_markdown(
    cmd: click.Command, ctx: click.Context, recursive: bool = False, max_tokens: int | None = None
) -> str:
    """
    Render a command as Markdown, tuned for LLM consumption.

    ``recursive=True`` (``--help markdown-full``) documents every descendant in full. Otherwise
    (``--help markdown``) the output adapts to ``max_tokens``: see :func:`adaptive_command_markdown`.
    Passing ``max_tokens=None`` opts out of adaptation entirely, documenting the current command and
    listing its descendants as a name index. Built from :func:`command_schema`, so it shares the JSON
    formats' extraction and single ``to_info_dict()`` walk.
    """
    if not recursive and max_tokens is not None:
        return adaptive_command_markdown(cmd, ctx, max_tokens)
    lines: list[str] = []
    _render_command_markdown(command_schema(cmd, ctx, recursive=recursive), lines, recursive)
    return "\n".join(lines).strip() + "\n"
