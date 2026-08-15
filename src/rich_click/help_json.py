"""
Machine-readable help formats for rich-click CLIs.

These power the format values on the existing ``--help`` flag -- ``--help markdown``,
``--help json``, ``--help json-full``, ``--help carapace`` and ``--help compact`` -- so tooling and
LLM agents can discover a CLI's structure as data instead of scraping the rendered ``--help``
screen. No new flag is added; the capability lives on ``--help`` and bare ``--help`` is unchanged.

``--help json`` uses progressive disclosure, reporting the *current* command's help, usage and full
parameter detail plus a name-only index of subcommands, so agents land on a command, read its
parameters as data, and drill into subcommands by name as needed. ``--help markdown`` renders the
same structure as LLM-friendly Markdown, but with *adaptive* disclosure: the invoked command in full
plus as much of the rest of the tree as fits a character ceiling, nearest hop first (see
:func:`adaptive_command_markdown`). ``--help compact`` renders the whole tree in the leanest form that
keeps it complete -- one line per record, no tables -- which is what a bare ``--help`` renders in a
detected agent environment, there under the same character ceiling (see :func:`compact_command`). The
``-full`` variants (``--help markdown-full`` / ``--help json-full``) expand every descendant to full
detail in one call, and ``--help carapace`` maps the tree onto the carapace completion spec.

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
from typing import Any, NamedTuple

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
    if "[" not in text:
        # No markup is possible without a bracket, and the overwhelming majority of help strings have
        # none. Worth the guard: a whole-tree walk runs this over every help string in the CLI, and
        # ``Text.from_markup`` on markup-free text is two orders of magnitude slower than the check.
        return text.strip()
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
    # A flag defaulting to False is the implied case and says nothing, so it is dropped. Every other
    # default is kept -- including 0 and "", and including a flag that defaults to *True*
    # (``--debug/--no-debug`` starting on), which is real signal a consumer cannot infer.
    default = info.get("default")
    if default is not None and not (is_flag and default is False):
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


def _hidden(info: dict[str, Any] | None) -> bool:
    """Report whether a command's ``to_info_dict()`` marks it hidden."""
    return bool((info or {}).get("hidden"))


def _subcommand_index(commands: dict[str, Any], parent: click.Command | None, display: bool = False) -> dict[str, Any]:
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

    ``display`` drops ``hidden=True`` commands, matching the rendered help screen. The JSON formats
    keep them (like ``to_info_dict`` does, and like hidden *parameters*), but a text rendering meant to
    stand in for the help screen must not show what the help screen hides.
    """
    index: dict[str, Any] = {}
    parent_commands = getattr(parent, "commands", {})
    for name, info in commands.items():
        if display and _hidden(info):
            continue
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
            nested = _subcommand_index(children, child, display)
            if nested:
                entry["subcommands"] = nested
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


def _subcommand_index_full(
    cmd: click.Command, ctx: click.Context, child_infos: dict[str, Any], display: bool = False
) -> dict[str, Any]:
    """
    Recursively expand every descendant to its full schema (params, usage, nested subcommands).

    Iterates ``child_infos`` -- the same ``to_info_dict()``-derived source the lean index uses -- so the
    full walk lists exactly the same subcommands as ``--help json`` (a child that can't be entered gets a
    degraded node rather than vanishing), and the ordering stays stable.
    """
    if display:  # a text rendering must not show what the rendered help screen hides
        child_infos = {name: info for name, info in child_infos.items() if not _hidden(info)}
    full = {
        name: command_schema(child, child_ctx, recursive=True, info=child_infos.get(name), display=display)
        for name, child, child_ctx in _iter_child_contexts(cmd, ctx)
        if name in child_infos
    }
    return {
        name: full[name] if name in full else _degraded_schema(name, info, ctx) for name, info in child_infos.items()
    }


def command_schema(
    cmd: click.Command,
    ctx: click.Context,
    recursive: bool = False,
    info: dict[str, Any] | None = None,
    display: bool = False,
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

    ``display`` adds the fields the *text* renderings need and the JSON formats deliberately omit: each
    parameter's rendered ``metavar``, an ``is_help_option`` marker on the ``--help`` option, and the
    command's one-line ``short_help``. All are computed by Click itself here, where the live command and
    parameter objects are in hand, so the Markdown and compact renderers do not have to reconstruct them
    from the serialized type name further downstream.
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
        if display:
            param_dict["metavar"] = _param_metavar(param, ctx)
            if id(param) in help_ids:
                # Flagged (in the display schema only) so a rendering can drop the ``--help`` row, which
                # is the same boilerplate on every command in the tree. See :func:`compact_command`.
                param_dict["is_help_option"] = True
        params.append(param_dict)

    schema: dict[str, Any] = {"name": info.get("name"), "path": ctx.command_path}
    help_text = _strip_markup(info.get("help"))
    if help_text:  # omit rather than emit a null help for undocumented commands
        schema["help"] = help_text
    if display:
        schema["short_help"] = _strip_markup(cmd.get_short_help_str(limit=120)) or ""
    schema["usage"] = " ".join([ctx.command_path, *cmd.collect_usage_pieces(ctx)])
    schema["params"] = params
    examples = _coerce_examples(info.get("examples"))
    if examples:
        schema["examples"] = examples
    if "commands" in info:
        if recursive:
            schema["subcommands"] = _subcommand_index_full(cmd, ctx, info["commands"], display=display)
        else:
            schema["subcommands"] = _subcommand_index(info["commands"], cmd, display)

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

    Flag keys use carapace's string syntax: a bare name takes no value, a trailing ``=`` marks a
    required value, ``?`` an optional one, and ``*`` a repeatable flag. Positional arguments have no
    first-class carapace object, so they contribute only their help (``documentation``) and any
    ``Choice`` candidates (``completion``). The ``--help`` option (in ``help_ids``) is included like any
    other, with the formats it accepts as its completions.
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
            # A counter (``-v/-vv/-vvv``) is not ``is_flag``, but it takes no value either -- marking it
            # ``=`` would have carapace demand an argument for it. An optional-value option (Click sets a
            # ``flag_value`` on a non-flag, as ``--help`` does) takes ``?``, since a bare ``--help`` is
            # valid too.
            takes_value = not is_flag and not info.get("count")
            key = ", ".join(opts)
            if takes_value:
                key += "?" if info.get("flag_value") is not None else "="
            if multiple:
                key += "*"
            if takes_value and isinstance(nargs, int) and nargs > 1:
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


def _one_line(value: Any) -> str:
    """Collapse a value onto a single line, so one record stays one line."""
    return " ".join(str(value).split())


def _md_escape(value: Any) -> str:
    """Make a value safe for a Markdown table cell: single line, pipes escaped."""
    return _one_line(value).replace("|", "\\|")


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


def _param_envvars(param: dict[str, Any]) -> str:
    """Render a parameter's environment variable(s) as a comma-separated list, or ``""`` when it has none."""
    envvar = param.get("envvar")
    if not envvar:
        return ""
    # Click accepts either a single name or a list of them; a list rendered via ``str()`` would come out
    # as ``['A', 'B']``, which is Python syntax rather than the names the reader has to export.
    return ", ".join(str(name) for name in envvar) if isinstance(envvar, (list, tuple)) else str(envvar)


def _md_param_description(param: dict[str, Any]) -> str:
    """Help text plus inline env-var / prompt annotations, for a parameter's table cell."""
    parts = []
    if param.get("help"):
        parts.append(param["help"])
    envvars = _param_envvars(param)
    if envvars:
        parts.append(f"[env: {envvars}]")
    if param.get("prompt"):
        parts.append(f"[prompt: {param['prompt']}]")
    return _md_escape(" ".join(parts))


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
                ", ".join(f"`{opt}`" for opt in _md_param_opts(param)) if is_option else f"`{param.get('name', '')}`",
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


def _param_metavar(param: click.Parameter, ctx: click.Context) -> str:
    """
    Render the value a parameter takes, as it would appear on the command line.

    Defers to Click's own ``make_metavar`` (via rich-click's version-safe wrapper), so an explicit
    ``metavar=``, a ``Path(file_okay=False)``'s ``DIRECTORY``, a ``Tuple``'s ``<INT TEXT>`` and any
    custom ``ParamType`` all come out exactly as they do in the rendered help. Flags and counters are
    blanked: Click reports ``BOOLEAN`` / ``INTEGER RANGE`` for them, but on the command line they take
    no value at all, and these renderings show what you type.
    """
    from rich_click.rich_help_rendering import _make_param_metavar

    if getattr(param, "is_flag", False) or getattr(param, "count", False):
        return ""
    metavar = _make_param_metavar(param, ctx)  # type: ignore[arg-type]
    # Click renders a repeatable option as a plain metavar; the ellipsis is what says "give it again".
    if getattr(param, "multiple", False) and not metavar.endswith("..."):
        metavar += "..."
    return metavar


def _schema_path(schema: dict[str, Any]) -> str:
    """Return a command's full invocation path (program name included), or its bare name as a fallback."""
    return str(schema.get("path") or schema.get("name") or "")


def _md_param_opts(param: dict[str, Any]) -> list[str]:
    """Return an option's flags, negation flags included."""
    return [*(param.get("opts") or []), *(param.get("secondary_opts") or [])]


def _md_param_metavar(param: dict[str, Any], *, brackets: bool = True) -> str:
    """
    Return the metavar to show in a lean rendering, preferring a spelled-out choice list.

    A ``Choice`` renders from the schema's own ``choices`` rather than from Click's metavar, because
    these renderings have no description column to lean on and the choice values *are* the vocabulary
    needed to construct a valid invocation. That also keeps the ``--help`` option's full format list,
    which the rendered help abbreviates to ``[markdown|json|...]`` to fit a terminal. ``brackets=False``
    drops the enclosing brackets (``fast|safe``), which is how the compact format spells the same thing.
    """
    choices = param.get("choices")
    if choices:
        joined = "|".join(str(choice) for choice in choices)
        return f"[{joined}]" if brackets else joined
    return param.get("metavar") or ""


def _md_param_signature(param: dict[str, Any], metavar: str | None = None) -> str:
    """
    Return an option's flags and the value it takes, e.g. ``-c, --count INTEGER`` or ``--mode [a|b]``.

    ``metavar`` overrides the value part, for a rendering that spells it differently.
    """
    if metavar is None:
        metavar = _md_param_metavar(param)
    return f"{', '.join(_md_param_opts(param))} {metavar}".strip()


def _summary(schema: dict[str, Any]) -> str:
    """
    Return a command's one-line summary.

    Normally Click's own ``get_short_help_str`` result, computed into the schema by ``command_schema``
    so an explicit ``short_help=`` is honoured and the truncation matches the rendered help exactly. The
    fallback covers a node that could not be contextualized at all (see ``_degraded_schema``), which has
    no command object to ask.
    """
    short_help = schema.get("short_help")
    if short_help:
        return str(short_help)
    return _one_line((schema.get("help") or "").split("\n\n", 1)[0])


def _md_child_prefix(prefix: str, name: str) -> str:
    """Nest a Markdown index one level deeper: indentation, as a bullet list is nested."""
    return f"{prefix}  "


def _compact_child_prefix(prefix: str, name: str) -> str:
    """
    Nest a compact index one level deeper: by path, so ``list`` under ``things`` reads ``things list``.

    It costs the same characters as indentation and hands the reader the invocation to type, instead of
    a bare name they would have to assemble from an enclosing line.
    """
    return f"{prefix}{name} "


def _subcommand_index_lines(
    index: dict[str, Any],
    lines: list[str],
    prefix: str,
    entry_line: Callable[[str, dict[str, Any]], str],
    child_prefix: Callable[[str, str], str],
) -> None:
    """
    Walk a name-only subcommand index depth-first, one line per command.

    ``entry_line`` formats a single command and ``child_prefix`` decides how nesting is expressed; the
    Markdown and compact renderings differ only in those two, so they share this walk rather than each
    carrying their own copy of the tree recursion.
    """
    for name, entry in index.items():
        lines.append(prefix + entry_line(name, entry))
        nested = entry.get("subcommands")
        if nested:
            _subcommand_index_lines(nested, lines, child_prefix(prefix, name), entry_line, child_prefix)


def _md_index_entry(name: str, entry: dict[str, Any]) -> str:
    """Format one subcommand as a Markdown bullet."""
    bullet = f"- `{name}`"
    if entry.get("aliases"):
        bullet += f" (aliases: {', '.join(entry['aliases'])})"
    if entry.get("help"):
        bullet += f" — {_md_escape(entry['help'])}"
    return bullet


def _render_examples(schema: dict[str, Any], lines: list[str]) -> None:
    """
    Append a command's Examples section -- always immediately after the usage line.

    Examples come *before* the parameters in every agent-facing format, and the ordering is not
    cosmetic: an example is a complete, copyable invocation, so it is the single highest-value thing a
    model can read about a command, and models demonstrably copy the ones they are shown. Making it the
    first thing after the usage line means the answer is already there before the option tables are
    reached. (The human help is laid out the other way round, with an Examples panel after the options:
    a person scanning a terminal wants the reference material first and the worked examples at the end.)
    """
    if not schema.get("examples"):
        return
    lines += ["## Examples", ""]
    for example in schema["examples"]:
        lines.append(f"- {_md_escape(example['description'])}: `{example['command']}`")
    lines.append("")


def _visible(params: list[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
    """Return a command's non-hidden parameters of one kind."""
    return [param for param in params if param.get("kind") == kind and not param.get("hidden")]


def _render_command_header(schema: dict[str, Any], lines: list[str], *, description: str) -> None:
    """
    Append the part of a command's section that is the same at every detail level.

    Every command is a top-level (``#``) section titled by its full invocation path, so each is
    self-describing and the document stays flat and uniform -- easier for an LLM to parse than deeply
    nested headings whose level would otherwise collide with the per-command sub-sections. Only the
    ``description`` differs between levels: the full help text, or a one-line summary of it.
    """
    lines += [f"# `{_schema_path(schema)}`", ""]
    if description:
        lines += [description, ""]
    if schema.get("aliases"):
        lines += [f"**Aliases:** {', '.join(f'`{alias}`' for alias in schema['aliases'])}", ""]
    if schema.get("usage"):
        lines += [f"**Usage:** `{schema['usage']}`", ""]
    _render_examples(schema, lines)


def _render_command_body(schema: dict[str, Any], lines: list[str]) -> None:
    """Append one command's own Markdown -- everything but its subcommands (level **L2**, "full")."""
    _render_command_header(schema, lines, description=schema.get("help") or "")

    params = schema.get("params", [])
    arguments = _visible(params, "argument")
    options = _visible(params, "option")
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

    Examples are the one thing kept in full at this level. They are short, and a worked invocation
    earns its tokens several times over against a list of flags a model still has to assemble.
    """
    _render_command_header(schema, lines, description=_summary(schema))

    options = _visible(schema.get("params", []), "option")
    if options:
        lines += ["## Options", ""]
        for param in options:
            required = " (required)" if param.get("required") else ""
            lines.append(f"- `{_md_param_signature(param)}`{required}")
        lines.append("")


def _pointer_entry(schema: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Reduce a full schema to the ``(name, entry)`` pair a subcommand-index formatter takes."""
    return str(schema.get("name") or ""), {"aliases": schema.get("aliases"), "help": _summary(schema)}


def _render_command_pointer(schema: dict[str, Any]) -> str:
    """Render a command as a single index bullet (level **L0**) -- name, aliases, one-line summary."""
    return _md_index_entry(*_pointer_entry(schema))


def _render_command_markdown(schema: dict[str, Any], lines: list[str]) -> None:
    """Append one command's Markdown section, followed by a name index of its subcommands."""
    _render_command_body(schema, lines)

    subcommands = schema.get("subcommands")
    if subcommands:
        lines += ["## Subcommands", ""]
        _subcommand_index_lines(subcommands, lines, "", _md_index_entry, _md_child_prefix)
        lines.append("")


# --------------------------------------------------------------------------------------------------
# Compact (``--help compact``).
#
# The same data as the Markdown formats, in the shape a truncating agent harness can actually hold.
# Agent harnesses cut a tool's output at a *character* count (Claude Code at ~30,000), and a help page
# that gets cut is worse than a short one: the agent re-reads it through grep/tail, spending turns. So
# every rule here buys characters back, and spends them only where a model needs them:
#
# * One line per record, with the signature and the description separated by exactly two spaces. No
#   tables, no box drawing, no column padding -- alignment is the single most expensive habit in a help
#   screen and carries no information a separator does not.
# * Only conventions models already know: a leading ``*`` for a required option (rich-click's rendered
#   help marks required options the same way), ``a|b|c`` in place of a choice metavar, ``...`` for a
#   repeatable one, and Click's own ``[default: x]`` / ``[env: NAME]`` tags. No invented sigils, so
#   nothing has to be explained to the reader before the page can be used.
# * Every command block opens with a ``#`` anchor line, which is what makes a multi-command document
#   greppable and gives a model something to navigate by.
# * Boilerplate is dropped: the ``--help`` row (identical on every command) and the ``usage:`` line for
#   commands that have no positional arguments (the anchor line already gives the path, and the options
#   are listed underneath -- only argument *order* is information a heading cannot carry).
# --------------------------------------------------------------------------------------------------

#: The separator between a signature and its description, on every line of every compact block.
#:
#: Exactly two spaces. One space is ambiguous with the spaces inside a signature (``--kolm a|b|c``), and
#: padding to a column would make the boundary depend on the widest row in the block -- costing
#: characters and making the format harder, not easier, to read a line at a time.
_COMPACT_GAP = "  "


def _compact_path(schema: dict[str, Any]) -> str:
    """
    Return a command's invocation path with the program name dropped, for its anchor line.

    ``cli things list`` becomes ``things list``: the program name is a constant repeated on every one of
    a large tree's anchor lines, and it is already spelled out in the usage line and the examples, which
    are the lines a reader copies. A top-level command, whose path *is* the program name, keeps it.
    """
    path = str(schema.get("path") or schema.get("name") or "")
    _, _, rest = path.partition(" ")
    return rest or path


def _compact_aliases(aliases: Any) -> str:
    """
    Render a command's aliases as ``` [aliases: co, cr]```, or nothing at all when it has none.

    Labelled, not just parenthesised: a bare ``(co)`` after a command name is a guess for the reader,
    and aliases are rare enough that the handful of characters costs almost nothing across a whole tree.
    The label is the same one rich-click's rendered help uses, and the bracket tag is the same shape as
    ``[default: x]`` -- plural whatever the count, like every other fixed tag.
    """
    return f" [aliases: {', '.join(str(alias) for alias in aliases)}]" if aliases else ""


def _compact_anchor(schema: dict[str, Any]) -> str:
    """
    Return a command block's opening line: ``# <path> [aliases: …] — <short help>``.

    The ``#`` is the anchor: in a document holding a whole command tree it is what a model greps for and
    what tells it where one command's block ends and the next begins. The summary stays on that line
    rather than moving to the one below, so a single ``grep '^#'`` over a whole-tree rendering returns a
    table of contents that says what each command *does* -- which is what makes the anchor worth
    grepping for in the first place.
    """
    line = f"# {_compact_path(schema)}{_compact_aliases(schema.get('aliases'))}"
    summary = _summary(schema)
    return f"{line} — {_one_line(summary)}" if summary else line


def _is_option(param: dict[str, Any]) -> bool:
    """Report whether a parameter is an option rather than a positional argument."""
    return param.get("kind") == "option"


def _compact_metavar(param: dict[str, Any]) -> str:
    """
    Return the value a parameter takes, as the compact format spells it.

    An option's ``Choice`` is spelled out inline (``pelm|crox|zeff``) in place of Click's bracketed
    metavar: the choice values *are* the vocabulary needed to build a valid invocation, and there is no
    description column here to carry them. Arguments keep Click's own metavar unchanged, so the token in
    an argument's line is the same token the usage line shows -- including the ``{a|b}`` a ``Choice``
    argument already renders as, and the brackets that mark an optional one.
    """
    metavar = _md_param_metavar(param, brackets=False) if _is_option(param) else str(param.get("metavar") or "")
    if param.get("multiple"):
        # ``_param_metavar`` marks a repeatable option by gluing an ellipsis onto the metavar; separating
        # it keeps ``...`` a token of its own, which is how every CLI convention writes "repeat this".
        metavar = metavar.removesuffix("...").rstrip()
        metavar = f"{metavar} ..." if metavar else "..."
    return metavar


def _compact_signature(param: dict[str, Any]) -> str:
    """
    Return a parameter's signature: ``*--crull TEXT``, ``--kolm pelm|crox|zeff``, ``SRC``.

    A required option is marked with a leading ``*`` -- the marker rich-click's rendered help already
    uses -- rather than a trailing ``[required]``, which costs ten times as many characters to say the
    same thing. Arguments carry no marker: Click's metavar already brackets the optional ones.
    """
    metavar = _compact_metavar(param)
    if not _is_option(param):
        return metavar
    required = "*" if param.get("required") else ""
    return f"{required}{_md_param_signature(param, metavar)}"


def _compact_tags(param: dict[str, Any]) -> list[str]:
    """
    Return a parameter's trailing ``[default: x]`` / ``[env: NAME]`` / ``[prompt: …]`` tags.

    Click's own phrasing, verbatim, because a model has read it a thousand times in rendered help
    screens. ``[required]`` is deliberately absent: the signature's ``*`` already says it.
    """
    tags = []
    if "default" in param:
        tags.append(f"[default: {_one_line(param['default'])}]")
    envvars = _param_envvars(param)
    if envvars:
        tags.append(f"[env: {envvars}]")
    if param.get("prompt"):
        tags.append(f"[prompt: {_one_line(param['prompt'])}]")
    return tags


def _compact_param_line(param: dict[str, Any], tags: list[str] | None = None) -> str:
    """
    Render one parameter as ``<signature>  <description> [default: x] [env: NAME]``.

    ``tags`` accepts an already-computed :func:`_compact_tags` result, for a caller that had to look at
    them to decide whether to emit the line at all.
    """
    description = [_one_line(param["help"])] if param.get("help") else []
    description += _compact_tags(param) if tags is None else tags
    signature = _compact_signature(param)
    # No description and no tags means no separator: the format never emits trailing whitespace.
    return f"{signature}{_COMPACT_GAP}{' '.join(description)}" if description else signature


def _compact_options(schema: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Return the options a compact block lists: every visible one except ``--help``.

    ``--help`` is dropped because it is the one row that is identical on every command of every CLI. In
    a whole-tree rendering it is the single largest block of pure repetition, and a model that has read
    one help page already knows the flag exists.
    """
    return [param for param in _visible(schema.get("params", []), "option") if not param.get("is_help_option")]


def _compact_usage(schema: dict[str, Any]) -> str | None:
    """
    Return the ``usage:`` line, or ``None`` for a command that does not need one.

    Only commands with positional arguments get one, and it lists only those positionals: their *order*
    is real information no other line carries. ``[OPTIONS]`` is omitted -- the options are listed
    directly underneath -- and a command with no positionals is fully described by its anchor line and
    its option lines, so a usage line would be pure repetition.
    """
    arguments = _visible(schema.get("params", []), "argument")
    if not arguments:
        return None
    pieces = [metavar for param in arguments if (metavar := _compact_metavar(param))]
    return " ".join(["usage:", _schema_path(schema), *pieces])


def _compact_index_entry(name: str, entry: dict[str, Any]) -> str:
    """Format one listed subcommand as ``<name> [aliases: …]  <short help>``."""
    line = f"{name}{_compact_aliases(entry.get('aliases'))}"
    help_text = entry.get("help")
    return f"{line}{_COMPACT_GAP}{_one_line(help_text)}" if help_text else line


def _compact_head(schema: dict[str, Any], lines: list[str]) -> None:
    """Append the lines every compact block opens with, at any detail level: anchor, then usage."""
    lines.append(_compact_anchor(schema))
    usage = _compact_usage(schema)
    if usage:
        lines.append(usage)


def _render_compact_body(schema: dict[str, Any], lines: list[str]) -> None:
    """
    Append one command's full compact block (level **L2**).

    Order is anchor, usage, arguments, options, examples. Examples come last here -- the opposite of the
    Markdown formats, where they lead -- because a compact block is short enough to read whole, so the
    examples land as the summary of what the option lines just spelled out rather than as an answer
    ahead of the reference material.
    """
    _compact_head(schema, lines)

    for param in _visible(schema.get("params", []), "argument"):
        # A bare positional is already fully described by the usage line; only one that carries a
        # description or a tag has anything left to say.
        tags = _compact_tags(param)
        if param.get("help") or tags:
            lines.append(_compact_param_line(param, tags))
    lines += [_compact_param_line(param) for param in _compact_options(schema)]

    if schema.get("examples"):
        # The command lines alone, without their descriptions: sitting under the option list, a worked
        # invocation describes itself, and the description is the part a model does not copy.
        lines.append("examples:")
        lines += [f"- {_one_line(example['command'])}" for example in schema["examples"]]


def _render_compact_signature(schema: dict[str, Any], lines: list[str]) -> None:
    """
    Append a command's compact *signature* block (level **L1**) -- anchor line plus bare signatures.

    The middle tier of adaptive disclosure: enough for a model to tell whether this is the command it
    wants and to build a syntactically valid invocation, without paying for a word of description. The
    usage line survives when there are positionals, since nothing else at this level would mention them.
    """
    _compact_head(schema, lines)
    lines += [_compact_signature(param) for param in _compact_options(schema)]


def _render_compact_pointer(schema: dict[str, Any]) -> str:
    """Render a command as a single listing line (level **L0**) -- name, aliases, one-line summary."""
    return _compact_index_entry(*_pointer_entry(schema))


# --------------------------------------------------------------------------------------------------
# Adaptive disclosure, shared by ``--help markdown`` and the compact agent default.
#
# Plain progressive disclosure -- the invoked command in full, its descendants as name-only rows -- is
# cheap but makes an agent *guess*: the vocabulary that decides which subcommand is the right one lives
# in option help text, which a name-only row does not carry. So the agent descends, reads, backtracks,
# and burns turns. Dumping the whole tree instead (``--help markdown-full``) removes the guessing, but
# does not scale to a large CLI.
#
# Adaptive disclosure is the middle path, and needs no configuration: render the invoked command in
# full, then keep promoting descendants -- nearest hop first -- to richer detail levels for as long as
# the whole response stays under a character ceiling. A small or mid-size CLI (the overwhelming
# majority) therefore emits its *entire* tree in full detail, and only a genuinely large one degrades,
# gracefully and nearest-first.
#
# The budget is in **characters**, not tokens, because the failure it exists to prevent is an agent
# harness truncating the output -- and every known harness measures its cap in characters (Claude Code
# cuts a tool result at ~30,000). Characters also need no estimator: ``len(text)`` is exact, where a
# token count would need a per-format chars-per-token divisor that drifts from what is actually emitted.
# A character ceiling bounds the token cost implicitly, since help text does not go below ~2.5
# characters per token.
# --------------------------------------------------------------------------------------------------

#: The three per-node detail levels the adaptive renderer promotes between.
DETAIL_POINTER = 0
"""Name + one-line description, as a row in the parent's subcommand listing."""
DETAIL_SIGNATURE = 1
"""One-line description and a bare option signature list (no descriptions)."""
DETAIL_FULL = 2
"""Everything: description, usage, examples and the full option/argument detail."""


def _line_chars(lines: Sequence[str]) -> int:
    """Count the characters a block of lines occupies once joined with newlines."""
    return sum(len(line) + 1 for line in lines)


class _RenderStyle(NamedTuple):
    """
    How one rendering draws the three detail levels, so the budgeting machinery can be shared.

    Markdown and compact differ only in what a node's block looks like at each level, how listed (L0)
    descendants are introduced, and how the closing note is worded -- not in how the tree is priced or
    promoted. Keeping the whole difference in one record means the two formats cannot drift apart in
    their disclosure behaviour, only in their typography, and that a style is never half-defined.
    """

    #: Append a node's block at L2 / L1 to a line buffer.
    full: Callable[[dict[str, Any], list[str]], None]
    signature: Callable[[dict[str, Any], list[str]], None]
    #: Render a node as a single L0 listing line, without its prefix.
    pointer: Callable[[dict[str, Any]], str]
    #: Extend the prefix carried down to a listed node's own children (indentation, or a path).
    child_prefix: Callable[[str, str], str]
    #: Emitted before a block's listed children, with its character count alongside -- the pricing walk
    #: asks for that on every node of every pass, and the answer cannot change. Build a style with
    #: :func:`_style` so the two cannot disagree.
    pointer_heading: tuple[str, ...]
    pointer_heading_chars: int
    #: Closing note when the tree did not fit, as a template over ``path``/``full``/``signature``/``pointer``.
    note: str


def _style(pointer_heading: tuple[str, ...] = (), **fields: Any) -> _RenderStyle:
    """Build a :class:`_RenderStyle`, pricing its pointer heading once so the walk never re-counts it."""
    return _RenderStyle(pointer_heading=pointer_heading, pointer_heading_chars=_line_chars(pointer_heading), **fields)


_MARKDOWN_STYLE = _style(
    full=_render_command_body,
    signature=_render_command_signature,
    pointer=_render_command_pointer,
    child_prefix=_md_child_prefix,
    # The heading opens with a blank line to separate the listing from the block it belongs to.
    pointer_heading=("", "## Subcommands", ""),
    note=(
        "> **Note:** this help was size-limited: {full} command(s) documented in full, {signature} in "
        "brief, {pointer} listed by name only. Run "
        "`{path} <COMMAND> --help markdown` on any command for its full detail."
    ),
)

_COMPACT_STYLE = _style(
    full=_render_compact_body,
    signature=_render_compact_signature,
    pointer=_render_compact_pointer,
    # Compact nests its listing by path, and needs no heading to introduce it: an option line starts
    # with a dash or a star, and a listing line does not.
    child_prefix=_compact_child_prefix,
    note=(
        "note: size-limited: {full} command(s) shown in full, {signature} in brief, {pointer} by name "
        "only. Run `{path} <COMMAND> --help compact` on any command for its full detail."
    ),
)


class _HelpNode:
    """
    One command in the tree the adaptive renderer budgets over.

    Each node caches its rendering at every detail level, along with that rendering's character count,
    so the promotion loop can price a candidate tree by walking node totals instead of re-rendering the
    document on every attempt.
    """

    __slots__ = ("children", "level", "schema", "style", "_pointer", "_sections")

    def __init__(self, schema: dict[str, Any], style: _RenderStyle) -> None:
        self.schema = schema
        self.style = style
        self.level = DETAIL_POINTER
        self.children = [_HelpNode(child, style) for child in (schema.get("subcommands") or {}).values()]
        self._sections: dict[int, tuple[list[str], int]] = {}
        self._pointer: tuple[str, int] | None = None

    def section(self) -> tuple[list[str], int]:
        """
        Return this node's own block at its current level, as ``(lines, characters)``.

        Trailing blank lines are stripped, so that every block ends the same way whatever produced it
        (the Markdown renderers close their last section with one; the compact ones do not) and
        :func:`_emit` can terminate a block with a single rule instead of a per-style knob.
        """
        cached = self._sections.get(self.level)
        if cached is None:
            lines: list[str] = []
            render = self.style.full if self.level == DETAIL_FULL else self.style.signature
            render(self.schema, lines)
            while lines and not lines[-1]:
                lines.pop()
            cached = (lines, _line_chars(lines))
            self._sections[self.level] = cached
        return cached

    def pointer(self) -> tuple[str, int]:
        """Return this node's listing line (L0), as ``(line, characters)``, excluding its prefix."""
        if self._pointer is None:
            line = self.style.pointer(self.schema)
            self._pointer = (line, len(line) + 1)
        return self._pointer


def _breadth_first(root: _HelpNode) -> list[_HelpNode]:
    """Return the tree in breadth-first order: nearest hop first, declaration order within a hop."""
    order = [root]
    index = 0
    while index < len(order):
        order.extend(order[index].children)
        index += 1
    return order


def _emit(node: _HelpNode, prefix: str, out: list[str] | None) -> int:
    """
    Render (when ``out`` is given) and price one node and its descendants at their current levels.

    Doubling as the renderer and the estimator is deliberate: a separate size model would be free to
    drift from what is actually emitted, and a budget computed from a stale model is worse than no
    budget at all. Because the price is a character count of the very lines that get emitted, the
    ceiling is exact rather than approximate. Blocks come out in the same depth-first order the
    whole-tree formats use, so a tree that is entirely at L2 renders byte-for-byte like
    ``--help markdown-full`` / ``--help compact``.
    """
    style = node.style
    if node.level == DETAIL_POINTER:
        line, chars = node.pointer()
        if out is not None:
            out.append(prefix + line)
        total = chars + len(prefix)
        if node.children:  # most nodes are leaves; building a prefix for nobody is the common case
            child_prefix = style.child_prefix(prefix, str(node.schema.get("name") or ""))
            for child in node.children:
                total += _emit(child, child_prefix, out)
        return total

    lines, total = node.section()
    if out is not None:
        out.extend(lines)
    # Children that were not promoted are listed under this node, the nearest ancestor with a block of
    # its own; promoted ones follow as their own blocks. The listing starts a fresh prefix, since it is
    # written relative to the command whose block it sits in.
    pointers = [child for child in node.children if child.level == DETAIL_POINTER]
    if pointers:
        if out is not None:
            out.extend(style.pointer_heading)
        total += style.pointer_heading_chars
        for child in pointers:
            total += _emit(child, "", out)
    if out is not None:
        out.append("")  # one blank line closes every block, and separates it from the next
    total += 1
    for child in node.children:
        if child.level != DETAIL_POINTER:
            total += _emit(child, "", out)
    return total


def _promote(root: _HelpNode, order: Sequence[_HelpNode], max_chars: int) -> None:
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
            if _emit(root, "", None) > max_chars:
                node.level = target - 1
                return


def _note_reserve(root: _HelpNode, order: Sequence[_HelpNode], style: _RenderStyle) -> int:
    """
    Characters to hold back from the ceiling for the closing note, which is only emitted when the tree
    did not fit and therefore has to tell the reader how to get the rest.

    Priced against the widest the note can get -- every count at its maximum, so every number is at its
    maximum number of digits -- plus the blank line before it and its own newline. Reserving the real
    upper bound, rather than a guessed constant, is what makes the ceiling an exact one.
    """
    counts = len(order)
    widest = style.note.format(path=_schema_path(root.schema), full=counts, signature=counts, pointer=counts)
    return len(widest) + 2


def _adaptive_help(cmd: click.Command, ctx: click.Context, max_chars: int, style: _RenderStyle) -> str:
    """
    Render a command tree, disclosing as much detail as ``max_chars`` allows.

    The invoked command is always rendered in full; its descendants are promoted breadth-first from a
    name-only pointer, through a bare signature, to full detail, until the ceiling is reached. Trees
    that fit entirely are emitted in full -- identical to the format's whole-tree variant -- and only
    larger ones degrade, nearest hop first.

    The result never exceeds ``max_chars`` above the format's floor -- the invoked command's own block
    plus a name-only line per descendant, which is what the least-disclosed rendering costs. Neither is
    abbreviated further: a ceiling below that floor is overshot rather than dropping the command that
    was asked about, or hiding a command's existence entirely.
    """
    root = _HelpNode(command_schema(cmd, ctx, recursive=True, display=True), style)
    order = _breadth_first(root)

    for node in order:
        node.level = DETAIL_FULL
    truncated = _emit(root, "", None) > max_chars
    if truncated:
        for node in order:
            node.level = DETAIL_POINTER
        root.level = DETAIL_FULL  # the invoked command is never abbreviated
        _promote(root, order[1:], max_chars - _note_reserve(root, order, style))

    lines: list[str] = []
    _emit(root, "", lines)
    text = "\n".join(lines).strip()
    if truncated:
        full = sum(1 for node in order if node.level == DETAIL_FULL)
        signature = sum(1 for node in order if node.level == DETAIL_SIGNATURE)
        note = style.note.format(
            path=_schema_path(root.schema), full=full, signature=signature, pointer=len(order) - full - signature
        )
        text += f"\n\n{note}"
    return text + "\n"


def _whole_tree_help(cmd: click.Command, ctx: click.Context, style: _RenderStyle) -> str:
    """Render every command in the tree at full detail, depth-first in definition order."""
    root = _HelpNode(command_schema(cmd, ctx, recursive=True, display=True), style)
    for node in _breadth_first(root):
        node.level = DETAIL_FULL
    lines: list[str] = []
    _emit(root, "", lines)
    return "\n".join(lines).strip() + "\n"


def adaptive_command_markdown(cmd: click.Command, ctx: click.Context, max_chars: int) -> str:
    """Render a command tree as Markdown, disclosing as much detail as ``max_chars`` allows."""
    return _adaptive_help(cmd, ctx, max_chars, _MARKDOWN_STYLE)


def adaptive_command_compact(cmd: click.Command, ctx: click.Context, max_chars: int) -> str:
    """Render a command tree in the compact format, disclosing as much detail as ``max_chars`` allows."""
    return _adaptive_help(cmd, ctx, max_chars, _COMPACT_STYLE)


def command_markdown(
    cmd: click.Command, ctx: click.Context, recursive: bool = False, max_chars: int | None = None
) -> str:
    """
    Render a command as Markdown, tuned for LLM consumption.

    ``recursive=True`` (``--help markdown-full``) documents every descendant in full. Otherwise
    (``--help markdown``) the output adapts to ``max_chars``: see :func:`adaptive_command_markdown`.
    Passing ``max_chars=None`` opts out of adaptation entirely, documenting the current command and
    listing its descendants as a name index. Built from :func:`command_schema`, so it shares the JSON
    formats' extraction and single ``to_info_dict()`` walk.
    """
    if recursive:
        return _whole_tree_help(cmd, ctx, _MARKDOWN_STYLE)
    if max_chars is not None:
        return adaptive_command_markdown(cmd, ctx, max_chars)
    lines: list[str] = []
    _render_command_markdown(command_schema(cmd, ctx, recursive=False, display=True), lines)
    return "\n".join(lines).strip() + "\n"


def compact_command(
    cmd: click.Command, ctx: click.Context, recursive: bool = False, max_chars: int | None = None
) -> str:
    """
    Render a command in the compact format: one line per record, no tables, no Markdown scaffolding.

    ``recursive=True`` -- what an explicit ``--help compact`` asks for -- renders the invoked command's
    block followed by every descendant's, depth-first, with no ceiling: the whole tree, in the smallest
    form that keeps it complete. Otherwise the output adapts to ``max_chars`` (see
    :func:`adaptive_command_compact`), which is what a bare ``--help`` uses in a detected agent
    environment. ``max_chars=None`` opts out of adaptation, rendering this command's block plus a
    name listing of its descendants.
    """
    if recursive:
        return _whole_tree_help(cmd, ctx, _COMPACT_STYLE)
    if max_chars is not None:
        return adaptive_command_compact(cmd, ctx, max_chars)
    schema = command_schema(cmd, ctx, recursive=False, display=True)
    lines: list[str] = []
    _render_compact_body(schema, lines)
    if schema.get("subcommands"):
        _subcommand_index_lines(schema["subcommands"], lines, "", _compact_index_entry, _compact_child_prefix)
    return "\n".join(lines).strip() + "\n"
