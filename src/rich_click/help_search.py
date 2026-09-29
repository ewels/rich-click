"""
Search a command tree for the commands that match a free-text query (``--search-help``).

Opt-in with :func:`rich_click.search_help_option`. The search runs over the same display schema the
compact and Markdown formats render from, so it sees exactly what an agent reading the whole tree
would: command names, aliases, help text, option names, option help, choice values and examples.
Scoring is plain token overlap weighted by field and by rarity, with no dependencies, so the same
query always returns the same commands.
"""

from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING, Any

import click


if TYPE_CHECKING:
    from rich_click.rich_context import RichContext


#: How many matching commands to return, best first.
MAX_RESULTS = 5

#: A command is dropped when it scores below this fraction of the best match, so a query that matches
#: one command well is not padded out with commands that only share a common word.
_MIN_RELATIVE_SCORE = 0.3

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


def _stem(word: str) -> str:
    """Strip a common English suffix so ``records`` / ``recorded`` / ``recording`` meet ``record``."""
    for suffix in ("ing", "ed", "es", "s"):
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


def _fields(schema: dict[str, Any], root_path: str) -> list[tuple[float, set[str]]]:
    """Return a command's searchable text as ``(weight, tokens)`` pairs."""
    path = str(schema.get("path") or "")
    parents = path[len(root_path) :].split()[:-1] if path.startswith(root_path) else []
    options: set[str] = set()
    details: set[str] = set()
    for param in schema.get("params", []):
        if param.get("hidden") or param.get("is_help_option"):
            continue
        for opt in (*(param.get("opts") or []), *(param.get("secondary_opts") or [])):
            options |= _tokens(opt.replace("-", " "))
        options |= _tokens(" ".join(str(choice) for choice in param.get("choices") or []))
        details |= _tokens(param.get("help"))
    for example in schema.get("examples") or []:
        details |= _tokens(example.get("description"))
        details |= _tokens(example.get("command"))
    return [
        (_WEIGHT_NAME, _tokens(schema.get("name")) | _tokens(" ".join(schema.get("aliases") or []))),
        (_WEIGHT_PARENT, _tokens(" ".join(parents))),
        (_WEIGHT_HELP, _tokens(schema.get("help"))),
        (_WEIGHT_OPTION, options),
        (_WEIGHT_DETAIL, details),
    ]


def _descendants(schema: dict[str, Any]) -> list[dict[str, Any]]:
    """Return every command below ``schema``, depth-first in declaration order."""
    found: list[dict[str, Any]] = []
    for child in (schema.get("subcommands") or {}).values():
        found.append(child)
        found.extend(_descendants(child))
    return found


def search_schemas(root: dict[str, Any], query: str) -> list[dict[str, Any]]:
    """
    Rank the commands below ``root`` against ``query`` and return the best matches, best first.

    Each query word scores the heaviest field it appears in, scaled by how rare the word is across the
    tree, so a word every command shares ("record" in a CLI of record commands) counts for little and a
    word only one command uses decides the result. Ties keep declaration order.
    """
    query_tokens = _tokens(query)
    candidates = _descendants(root)
    if not query_tokens or not candidates:
        return []

    root_path = str(root.get("path") or "")
    fields = [_fields(schema, root_path) for schema in candidates]
    rarity = {}
    for token in query_tokens:
        count = sum(1 for command in fields if any(_matches(token, tokens) for _, tokens in command))
        if count:
            rarity[token] = math.log(1 + len(candidates) / count)

    scored = []
    for index, (schema, command) in enumerate(zip(candidates, fields)):
        score = 0.0
        for token, weight in rarity.items():
            best = max((field_weight for field_weight, tokens in command if _matches(token, tokens)), default=0.0)
            score += best * weight
        if score:
            scored.append((score, index, schema))
    if not scored:
        return []

    scored.sort(key=lambda item: (-item[0], item[1]))
    threshold = scored[0][0] * _MIN_RELATIVE_SCORE
    return [schema for score, _, schema in scored[:MAX_RESULTS] if score >= threshold]


def search_command_tree(cmd: click.Command, ctx: click.Context, query: str) -> list[dict[str, Any]]:
    """Return display schemas for the commands below ``cmd`` that best match ``query``, best first."""
    from rich_click.help_json import command_schema

    root = command_schema(
        cmd, ctx, recursive=True, display=True, tolerate_load_errors=True, respect_default_visibility=True
    )
    return search_schemas(root, query)


def _no_matches(ctx: click.Context, query: str) -> str:
    return f"No commands under '{ctx.command_path}' match '{query}'."


def _render_markdown(results: list[dict[str, Any]]) -> str:
    """Render each match as its own Markdown section, with a name index for a group's subcommands."""
    from rich_click.help_json import _md_index_entry, _pointer_entry, _render_command_body

    lines: list[str] = []
    for schema in results:
        _render_command_body(schema, lines)
        children = (schema.get("subcommands") or {}).values()
        if children:
            lines += ["## Subcommands", "", *(_md_index_entry(*_pointer_entry(child)) for child in children), ""]
    return "\n".join(lines).strip()


def _render_compact(results: list[dict[str, Any]]) -> str:
    """Render each match as a full compact block, with a name listing for a group's subcommands."""
    from rich_click.help_json import _compact_index_entry, _pointer_entry, _render_compact_body

    lines: list[str] = []
    for schema in results:
        _render_compact_body(schema, lines)
        lines += [_compact_index_entry(*_pointer_entry(child)) for child in (schema.get("subcommands") or {}).values()]
        lines.append("")
    return "\n".join(lines).strip()


def _json_result(schema: dict[str, Any]) -> dict[str, Any]:
    """Strip a display schema back to the public JSON shape, listing subcommands by name only."""
    result = {key: value for key, value in schema.items() if not key.startswith("_") and key != "subcommands"}
    result["params"] = [
        {key: value for key, value in param.items() if key != "is_help_option"} for param in schema.get("params", [])
    ]
    if schema.get("subcommands"):
        result["subcommands"] = list(schema["subcommands"])
    return result


def render_search_results(ctx: click.Context, query: str, results: list[dict[str, Any]], fmt: str) -> str:
    """Render search results in one of :data:`SEARCH_FORMATS`."""
    if fmt == "json":
        import json

        data = {"query": query, "path": ctx.command_path, "results": [_json_result(schema) for schema in results]}
        return json.dumps(data, indent=2, default=str)
    if not results:
        return _no_matches(ctx, query)
    return _render_markdown(results) if fmt == "markdown" else _render_compact(results)


def rich_search_results(ctx: RichContext, query: str, results: list[dict[str, Any]]) -> str:
    """Render search results for a terminal: a panel of matching commands, styled like the commands panel."""
    from rich.table import Table
    from rich.text import Text

    from rich_click.help_json import _summary
    from rich_click.rich_box import get_box
    from rich_click.rich_help_rendering import RichClickRichPanel

    formatter = ctx.make_formatter()
    config = formatter.config
    if not results:
        formatter.write(Text(_no_matches(ctx, query)))
        return formatter.getvalue()

    table = Table.grid(padding=(0, 2))
    for schema in results:
        table.add_row(
            Text(str(schema.get("path") or ""), style=config.style_command),
            formatter.rich_text(_summary(schema), config.style_commands_panel_help_style),
        )
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


def get_search_help(cmd: click.Command, ctx: click.Context, query: str, fmt: str | bool | None = None) -> str:
    """
    Search below ``cmd`` and render the results. ``fmt`` is the value given to ``--help``, if any.

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

    search = getattr(cmd, "search_commands", None)
    results = search(ctx, query) if search is not None else search_command_tree(cmd, ctx, query)
    if fmt in SEARCH_FORMATS and fmt in _help_format_names(cmd, ctx):
        return render_search_results(ctx, query, results, fmt)
    if not isinstance(ctx, RichContext):
        # A plain Click context has no rich formatter to draw the panel with.
        return render_search_results(ctx, query, results, "compact")
    return rich_search_results(ctx, query, results)
