"""
Search a command tree for the commands and options that match a free-text query (``--search-help``).

Opt-in with :func:`rich_click.search_help_option`. The search runs over the same display schema the
compact and Markdown formats render from, so it sees exactly what an agent reading the whole tree
would: command names, aliases, help text, option names, option help, choice values and examples.
Scoring is plain token overlap weighted by field and by rarity, with no dependencies, so the same
query always returns the same results.

Nothing is filtered out of a result. Matching options are ranked first and, for people, highlighted:
a filtered list invites an agent to guess at what it cannot see, so every option is still listed.
"""

from __future__ import annotations

import math
import re
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

import click


if TYPE_CHECKING:
    from rich.console import Console, ConsoleOptions, RenderableType
    from rich.measure import Measurement
    from rich.segment import Segment
    from rich.style import StyleType

    from rich_click.rich_context import RichContext
    from rich_click.rich_panel import RichPanel


@dataclass(frozen=True)
class SearchSettings:
    """What ``--search-help`` does. Set through :func:`rich_click.search_help_option`'s keyword arguments."""

    max_results: int = 5
    """How many matching commands to return, best first."""
    options: Literal["rank", "filter"] | None = "rank"
    """What to do with each result's options. ``"rank"`` lists the matching ones first, keeping the rest;
    ``"filter"`` lists only the matching ones (plus required ones and arguments), with a count of the
    rest; ``None`` leaves options in their declared order."""
    single_match_help: bool = True
    """Show a single clear match as its full help, rather than as one row of the results panel."""
    highlight: bool = True
    """Highlight the matched words in terminal output, with the ``style_search_match`` style."""


#: How many of a command's best-matching options the multi-command results panel lists under it.
_OPTIONS_PER_RESULT = 3

#: A command is dropped when it scores below this fraction of the best match, so a query that matches
#: one command well is not padded out with commands that only share a common word.
_MIN_RELATIVE_SCORE = 0.3

#: The top result is shown as its full help, rather than as one row of a results panel, when it
#: scores at least this many times the runner-up.
_CLEAR_WINNER = 2.0

#: The formats search results can be rendered in. Plugin formats render a single command, so a search
#: that asks for one falls back to the human-readable results, as an unknown ``--help`` format does.
SEARCH_FORMATS = ("compact", "markdown", "json")

_STOPWORDS = frozenset(
    "a an and are as at be by can do does for from how i in into is it its me my of on or so that the "
    "then this to use using want what when which with".split()
)

# Where a query word matched, and how much that is worth. A word in the command's own name says far
# more about what it does than the same word in one option's help text.
_WEIGHT_NAME = 4.0
_WEIGHT_PARENT = 2.0
_WEIGHT_HELP = 2.0
_WEIGHT_OPTION = 1.5
_WEIGHT_DETAIL = 1.0

# The same idea one level down, for ranking a command's options against each other.
_WEIGHT_OPTION_NAME = 4.0
_WEIGHT_OPTION_HELP = 2.0
_WEIGHT_OPTION_CHOICES = 1.5

_SUFFIXES = ("ing", "ed", "es", "s")


def _stem(word: str) -> str:
    """Strip a common English suffix so ``records`` / ``recorded`` / ``recording`` meet ``record``."""
    for suffix in _SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def _tokens(text: Any) -> set[str]:
    """Return the stemmed, lower-case words in ``text``, stopwords removed."""
    words = re.findall(r"[a-z0-9]+", str(text or "").lower())
    return {_stem(word) for word in words if word not in _STOPWORDS}


def _matches(query_token: str, tokens: set[str]) -> bool:
    """Match a query word exactly, or as a prefix either way once both are long enough to be specific."""
    if query_token in tokens:
        return True
    if len(query_token) < 4:
        return False
    return any(len(token) >= 4 and (token.startswith(query_token) or query_token.startswith(token)) for token in tokens)


def _visible_params(schema: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the parameters a search looks at: every visible one except ``--help`` and ``--search-help``."""
    return [param for param in schema.get("params", []) if _is_searchable(param)]


def _param_fields(param: dict[str, Any]) -> list[tuple[float, set[str]]]:
    """Return one parameter's searchable text as ``(weight, tokens)`` pairs."""
    names: set[str] = set()
    for opt in (*(param.get("opts") or []), *(param.get("secondary_opts") or [])):
        names |= _tokens(opt.replace("-", " "))
    names |= _tokens(str(param.get("name") or "").replace("_", " "))
    return [
        (_WEIGHT_OPTION_NAME, names),
        (_WEIGHT_OPTION_HELP, _tokens(param.get("help"))),
        (_WEIGHT_OPTION_CHOICES, _tokens(" ".join(str(choice) for choice in param.get("choices") or []))),
    ]


def _fields(schema: dict[str, Any], root_path: str, *, params_only: bool = False) -> list[tuple[float, set[str]]]:
    """
    Return a command's searchable text as ``(weight, tokens)`` pairs.

    ``params_only`` limits it to the command's parameters, for the group a search starts from: its own
    name and help describe the whole tree, so matching them would put it at the top of every search.
    """
    options: set[str] = set()
    details: set[str] = set()
    for param in _visible_params(schema):
        names, help_tokens, choices = (tokens for _, tokens in _param_fields(param))
        options |= names | choices
        details |= help_tokens
    if params_only:
        return [(_WEIGHT_OPTION, options), (_WEIGHT_DETAIL, details)]
    for example in schema.get("examples") or []:
        details |= _tokens(example.get("description"))
        details |= _tokens(example.get("command"))
    path = str(schema.get("path") or "")
    parents = path[len(root_path) :].split()[:-1] if path.startswith(root_path) else []
    return [
        (_WEIGHT_NAME, _tokens(schema.get("name")) | _tokens(" ".join(schema.get("aliases") or []))),
        (_WEIGHT_PARENT, _tokens(" ".join(parents))),
        (_WEIGHT_HELP, _tokens(schema.get("help"))),
        (_WEIGHT_OPTION, options),
        (_WEIGHT_DETAIL, details),
    ]


def _score(fields: list[tuple[float, set[str]]], rarity: dict[str, float]) -> float:
    """Score one record: each query word counts once, at the heaviest field it matches, scaled by rarity."""
    score = 0.0
    for token, weight in rarity.items():
        score += weight * max((field_weight for field_weight, tokens in fields if _matches(token, tokens)), default=0.0)
    return score


def _descendants(schema: dict[str, Any]) -> list[dict[str, Any]]:
    """Return every command below ``schema``, depth-first in declaration order."""
    found: list[dict[str, Any]] = []
    for child in (schema.get("subcommands") or {}).values():
        found.append(child)
        found.extend(_descendants(child))
    return found


def _rank_params(schema: dict[str, Any], rarity: dict[str, float]) -> list[str]:
    """Return the names of a command's parameters that match the query, best first."""
    scored = []
    for index, param in enumerate(_visible_params(schema)):
        score = _score(_param_fields(param), rarity)
        if score:
            scored.append((-score, index, str(param.get("name") or "")))
    return [name for _, _, name in sorted(scored)]


def search_schemas(root: dict[str, Any], query: str, settings: SearchSettings | None = None) -> list[dict[str, Any]]:
    """
    Rank the commands in ``root``'s tree against ``query`` and return the best matches, best first.

    Each query word scores the heaviest field it appears in, scaled by how rare the word is across the
    tree, so a word every command shares ("record" in a CLI of record commands) counts for little and a
    word only one command uses decides the result. Ties keep declaration order.

    ``root`` is a candidate too: on its own parameters for a group, and in full for a single command, so
    a CLI with one command and hundreds of options can still be searched. Each returned schema carries
    ``_score`` and ``_matched_params`` (the names of its matching parameters, best first, or empty when
    the ``options`` setting is ``None``).
    """
    settings = settings or SearchSettings()
    query_tokens = _tokens(query)
    if not query_tokens:
        return []

    root_path = str(root.get("path") or "")
    descendants = _descendants(root)
    candidates = [root, *descendants]
    fields = [_fields(schema, root_path, params_only=schema is root and bool(descendants)) for schema in candidates]

    rarity = {}
    for token in query_tokens:
        count = sum(1 for command in fields if any(_matches(token, tokens) for _, tokens in command))
        if count:
            rarity[token] = math.log(1 + len(candidates) / count)

    scored = []
    for index, (schema, command) in enumerate(zip(candidates, fields)):
        score = _score(command, rarity)
        if score:
            scored.append((score, index, schema))
    if not scored:
        return []

    scored.sort(key=lambda item: (-item[0], item[1]))
    threshold = scored[0][0] * _MIN_RELATIVE_SCORE
    results = []
    for score, _, schema in scored[: settings.max_results]:
        if score < threshold:
            break
        matched = _rank_params(schema, rarity) if settings.options else []
        results.append({**schema, "_score": score, "_matched_params": matched})
    return results


def search_command_tree(
    cmd: click.Command, ctx: click.Context, query: str, settings: SearchSettings | None = None
) -> list[dict[str, Any]]:
    """Return display schemas for the commands in ``cmd``'s tree that best match ``query``, best first."""
    from rich_click.help_json import command_schema

    root = command_schema(
        cmd, ctx, recursive=True, display=True, tolerate_load_errors=True, respect_default_visibility=True
    )
    return search_schemas(root, query, settings)


# --------------------------------------------------------------------------------------------------
# Text formats (compact, Markdown, JSON).
# --------------------------------------------------------------------------------------------------


def _is_searchable(param: dict[str, Any]) -> bool:
    """Report whether a parameter counts towards a search: visible, and not ``--help``/``--search-help``."""
    return not param.get("hidden") and not param.get("is_help_option") and not param.get("is_search_help_option")


def _arranged(schema: dict[str, Any], settings: SearchSettings) -> tuple[dict[str, Any], int]:
    """
    Return ``schema`` with its options ranked or filtered, and how many options filtering left out.

    Ranking moves the matching options to the front, best first, and keeps the rest. Filtering keeps the
    matching and required options only, unless nothing matched (a command found by its name), when every
    option is kept. Arguments are never moved or dropped: the usage line is built from their order.
    """
    order = {name: rank for rank, name in enumerate(schema.get("_matched_params") or [])}
    if not order:
        return schema, 0
    params = schema.get("params", [])
    arguments = [param for param in params if param.get("kind") != "option"]
    options = [param for param in params if param.get("kind") == "option"]
    matched = sorted(
        (param for param in options if str(param.get("name") or "") in order),
        key=lambda param: order[str(param.get("name") or "")],
    )
    rest = [param for param in options if str(param.get("name") or "") not in order]
    omitted = 0
    if settings.options == "filter":
        omitted = sum(1 for param in rest if _is_searchable(param) and not param.get("required"))
        rest = [param for param in rest if param.get("required")]
    return {**schema, "params": arguments + matched + rest}, omitted


def _omitted_note(schema: dict[str, Any], omitted: int) -> str:
    noun = "option" if omitted == 1 else "options"
    return f"{omitted} more {noun}: {_schema_path(schema)} --help"


def _schema_path(schema: dict[str, Any]) -> str:
    return str(schema.get("path") or schema.get("name") or "")


def _no_matches(ctx: click.Context, query: str) -> str:
    return f"No commands under '{ctx.command_path}' match '{query}'."


def _render_markdown(results: list[dict[str, Any]], settings: SearchSettings) -> str:
    """Render each match as its own Markdown section, with a name index for a group's subcommands."""
    from rich_click.help_json import _md_index_entry, _pointer_entry, _render_command_body

    lines: list[str] = []
    for schema in results:
        arranged, omitted = _arranged(schema, settings)
        _render_command_body(arranged, lines)
        if omitted:
            lines += [f"_{_omitted_note(schema, omitted)}_", ""]
        children = (schema.get("subcommands") or {}).values()
        if children:
            lines += ["## Subcommands", "", *(_md_index_entry(*_pointer_entry(child)) for child in children), ""]
    return "\n".join(lines).strip()


def _render_compact(results: list[dict[str, Any]], settings: SearchSettings) -> str:
    """Render each match as a full compact block, with a name listing for a group's subcommands."""
    from rich_click.help_json import _compact_index_entry, _pointer_entry, _render_compact_body

    lines: list[str] = []
    for schema in results:
        arranged, omitted = _arranged(schema, settings)
        _render_compact_body(arranged, lines)
        if omitted:
            lines.append(f"... {_omitted_note(schema, omitted)}")
        lines += [_compact_index_entry(*_pointer_entry(child)) for child in (schema.get("subcommands") or {}).values()]
        lines.append("")
    return "\n".join(lines).strip()


def _json_result(schema: dict[str, Any], settings: SearchSettings) -> dict[str, Any]:
    """
    Strip a display schema back to the public JSON shape, listing subcommands by name only.

    Ranked parameters keep their declared order and the matching ones carry ``match_rank`` (1 is best).
    Filtered ones are only those that matched or are required, with ``omitted_params`` counting the rest.
    """
    ranks = {name: rank for rank, name in enumerate(schema.get("_matched_params") or [], start=1)}
    result = {key: value for key, value in schema.items() if not key.startswith("_") and key != "subcommands"}
    params = []
    omitted = 0
    for param in schema.get("params", []):
        rank = ranks.get(str(param.get("name") or ""))
        keep = rank is not None or not ranks or settings.options != "filter"
        keep = keep or param.get("kind") != "option" or bool(param.get("required"))
        if not keep:
            omitted += _is_searchable(param)
            continue
        entry = {key: value for key, value in param.items() if key not in ("is_help_option", "is_search_help_option")}
        if rank is not None:
            entry["match_rank"] = rank
        params.append(entry)
    result["params"] = params
    if omitted:
        result["omitted_params"] = omitted
    if schema.get("subcommands"):
        result["subcommands"] = list(schema["subcommands"])
    return result


def render_search_results(
    ctx: click.Context,
    query: str,
    results: list[dict[str, Any]],
    fmt: str,
    settings: SearchSettings | None = None,
) -> str:
    """Render search results in one of :data:`SEARCH_FORMATS`."""
    settings = settings or SearchSettings()
    if fmt == "json":
        import json

        data = {
            "query": query,
            "path": ctx.command_path,
            "results": [_json_result(schema, settings) for schema in results],
        }
        return json.dumps(data, indent=2, default=str)
    if not results:
        return _no_matches(ctx, query)
    return _render_markdown(results, settings) if fmt == "markdown" else _render_compact(results, settings)


# --------------------------------------------------------------------------------------------------
# Terminal output.
# --------------------------------------------------------------------------------------------------


def highlight_pattern(query: str) -> re.Pattern[str] | None:
    """
    Return a regex matching the words ``query`` would match, for highlighting them in rendered help.

    Mirrors :func:`_matches`: a long query word also highlights longer words it starts (``format`` in
    ``formats`` and ``--output-format``), a short one only itself plus a common suffix.
    """
    parts = []
    for token in sorted(_tokens(query), key=len, reverse=True):
        suffix = r"[a-z0-9]*" if len(token) >= 4 else r"(?:{})?".format("|".join(_SUFFIXES))
        parts.append(re.escape(token) + suffix)
    if not parts:
        return None
    return re.compile(r"(?<![a-z0-9])(?:{})(?![a-z0-9])".format("|".join(parts)), re.IGNORECASE)


class SearchHighlight:
    """
    Wrap a renderable, adding a style to every word a search matched.

    Works on the rendered segments, so it highlights inside any renderable -- panels, tables, the usage
    line -- without the rendering code knowing a search is going on.
    """

    def __init__(self, renderable: RenderableType, pattern: re.Pattern[str], style: StyleType) -> None:
        """Wrap ``renderable``, highlighting ``pattern``'s matches with ``style``."""
        self.renderable = renderable
        self.pattern = pattern
        self.style = style

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> Iterator[Segment]:
        from rich.segment import Segment

        match_style = console.get_style(self.style)
        for segment in console.render(self.renderable, options):
            text, style, control = segment
            if control or not text:
                yield segment
                continue
            position = 0
            for match in self.pattern.finditer(text):
                if match.start() > position:
                    yield Segment(text[position : match.start()], style)
                yield Segment(match.group(), style + match_style if style else match_style)
                position = match.end()
            if position == 0:
                yield segment
            elif position < len(text):
                yield Segment(text[position:], style)

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        from rich.measure import Measurement

        return Measurement.get(console, options, self.renderable)


def arrange_panels(
    command: click.Command, ctx: RichContext, panels: list[RichPanel[Any, Any]]
) -> tuple[list[RichPanel[Any, Any]], int]:
    """
    Rank or filter the options inside each option panel of a ``--search-help`` result's help.

    The author's panels are kept, in their order: within each, matching options move to the front, best
    first, or with filtering only matching, required and positional parameters stay. Returns the new
    panels (copies -- the command's own panels are never changed) and how many options were left out.
    """
    import copy

    from rich_click.rich_panel import RichOptionPanel
    from rich_click.rich_parameter import RichSearchHelpOption

    order = {name: rank for rank, name in enumerate(ctx.search_matched_params or [])}
    params = command.get_params(ctx)
    help_option = command.get_help_option(ctx)

    def lookup(entry: str) -> click.Parameter | None:
        return next((param for param in params if entry in (*param.opts, param.name)), None)

    def keep(param: click.Parameter | None) -> bool:
        if param is None or param.name in order:
            return True
        return isinstance(param, click.Argument) or bool(param.required)

    arranged: list[RichPanel[Any, Any]] = []
    omitted: set[int] = set()
    for panel in panels:
        if not isinstance(panel, RichOptionPanel):
            arranged.append(panel)
            continue
        entries = [(entry, lookup(entry)) for entry in panel.options]
        if ctx.search_filter:
            for _, param in entries:
                if not keep(param) and param is not help_option and not isinstance(param, RichSearchHelpOption):
                    omitted.add(id(param))
            entries = [(entry, param) for entry, param in entries if keep(param)]
        entries.sort(key=lambda item: order.get(getattr(item[1], "name", None) or "", len(order)))
        new_panel = copy.copy(panel)
        new_panel.options = [entry for entry, _ in entries]
        arranged.append(new_panel)
    return arranged, len(omitted)


def omitted_options_note(ctx: RichContext, omitted: int) -> str:
    """Return the line that follows a filtered result's panels, so the reader knows options were left out."""
    noun = "option" if omitted == 1 else "options"
    return f"{omitted} more {noun} not shown. Run '{ctx.command_path} --help' to see them all."


def _clear_winner(results: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Return the top result when it should be shown as its full help rather than as a list."""
    if len(results) == 1 or (results and results[0]["_score"] >= _CLEAR_WINNER * results[1]["_score"]):
        return results[0]
    return None


def _command_help(
    cmd: click.Command, ctx: click.Context, query: str, schema: dict[str, Any], settings: SearchSettings
) -> str | None:
    """
    Render one result's normal help, with its options ranked or filtered inside their panels.

    Returns ``None`` when the command cannot render rich help (a plain Click command in the tree).
    """
    from rich_click.help_json import _make_child_context
    from rich_click.rich_command import RichCommand
    from rich_click.rich_context import RichContext

    owned: list[click.Context] = []
    try:
        command, command_ctx = cmd, ctx
        for name in str(schema.get("path") or "")[len(ctx.command_path) :].split():
            child = command.get_command(command_ctx, name) if isinstance(command, click.Group) else None
            if child is None:
                return None
            command_ctx = _make_child_context(child, name, command_ctx)
            owned.append(command_ctx)
            command = child
        if not isinstance(command, RichCommand) or not isinstance(command_ctx, RichContext):
            return None
        command_ctx.search_query = query if settings.highlight else None
        command_ctx.search_matched_params = schema.get("_matched_params") or []
        command_ctx.search_filter = settings.options == "filter"
        try:
            return command.get_help(command_ctx)
        finally:
            command_ctx.search_query = None
            command_ctx.search_matched_params = None
            command_ctx.search_filter = False
    finally:
        for child_ctx in reversed(owned):
            child_ctx.close()


def _results_panel(ctx: RichContext, query: str, results: list[dict[str, Any]], settings: SearchSettings) -> str:
    """Render several results as a panel: each command, with its best-matching options underneath."""
    from rich.table import Table
    from rich.text import Text

    from rich_click.help_json import _summary
    from rich_click.rich_box import get_box
    from rich_click.rich_help_rendering import RichClickRichPanel

    formatter = ctx.make_formatter()
    config = formatter.config
    if settings.highlight:
        formatter.search_highlight = highlight_pattern(query)

    table = Table.grid(padding=(0, 2))
    for schema in results:
        table.add_row(
            Text(str(schema.get("path") or ""), style=config.style_command),
            formatter.rich_text(_summary(schema), config.style_commands_panel_help_style),
        )
        params = {str(param.get("name") or ""): param for param in schema.get("params", [])}
        for name in (schema.get("_matched_params") or [])[:_OPTIONS_PER_RESULT]:
            param = params[name]
            opts = [*(param.get("opts") or []), *(param.get("secondary_opts") or [])]
            signature = Text("  ")
            signature.append(", ".join(opts) or name.upper(), style=config.style_option)
            if param.get("metavar") and param.get("kind") == "option":
                signature.append(" ")
                signature.append(str(param["metavar"]), style=config.style_metavar)
            table.add_row(signature, formatter.rich_text(param.get("help") or "", config.style_option_help))
    box = config.style_commands_panel_box
    formatter.write(
        RichClickRichPanel(
            table,
            title=Text(
                config.panel_title_string.format(f"Commands matching '{query}'"),
                style=config.style_commands_panel_title_style,
            ),
            title_align=config.align_commands_panel,
            border_style=config.style_commands_panel_border,
            box=get_box(box if box is not None else "SIMPLE"),
            padding=config.style_commands_panel_padding,
            style=config.style_commands_panel_style,
            title_padding=config.panel_title_padding,
        )
    )
    return formatter.getvalue()


def rich_search_results(
    cmd: click.Command,
    ctx: RichContext,
    query: str,
    results: list[dict[str, Any]],
    settings: SearchSettings | None = None,
) -> str:
    """
    Render search results for a terminal, with every matched word highlighted.

    A single clear match is shown as that command's normal help, with its options ranked or filtered;
    several matches as a panel listing each command and its best-matching options.
    """
    from rich.text import Text

    settings = settings or SearchSettings()
    if not results:
        formatter = ctx.make_formatter()
        formatter.write(Text(_no_matches(ctx, query)))
        return formatter.getvalue()
    winner = _clear_winner(results) if settings.single_match_help else None
    if winner is not None:
        rendered = _command_help(cmd, ctx, query, winner, settings)
        if rendered is not None:
            return rendered
    return _results_panel(ctx, query, results, settings)


def get_search_help(
    cmd: click.Command,
    ctx: click.Context,
    query: str,
    fmt: str | bool | None = None,
    settings: SearchSettings | None = None,
) -> str:
    """
    Search ``cmd``'s tree and render the results. ``fmt`` is the value given to ``--help``, if any.

    A named format renders in that format when search supports it (compact, Markdown or JSON) and it is
    enabled; anything else renders for the terminal, as an unknown ``--help`` format does. With no
    format, a detected AI agent gets ``agent_help_format``, as a bare ``--help`` would.
    """
    from rich_click._agent_detection import is_agent_mode
    from rich_click.decorators import HELP_PLAIN_VALUE
    from rich_click.help_formats import _normalize_format_name
    from rich_click.help_json import _help_format_names
    from rich_click.rich_context import RichContext

    if not isinstance(fmt, str) or not fmt or fmt == HELP_PLAIN_VALUE:
        fmt = getattr(getattr(ctx, "help_config", None), "agent_help_format", None) if is_agent_mode() else None
    fmt = _normalize_format_name(fmt) if fmt else None

    settings = settings or SearchSettings()
    search = getattr(cmd, "search_commands", None)
    results = search(ctx, query, settings) if search is not None else search_command_tree(cmd, ctx, query, settings)
    if fmt in SEARCH_FORMATS and fmt in _help_format_names(cmd, ctx):
        return render_search_results(ctx, query, results, fmt, settings)
    if not isinstance(ctx, RichContext):
        # A plain Click context has no rich formatter to draw the panel with.
        return render_search_results(ctx, query, results, "compact", settings)
    return rich_search_results(cmd, ctx, query, results, settings)
