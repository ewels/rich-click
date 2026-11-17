"""reStructuredText rendering support. Only imported when `text_markup="rst"` is used."""

from __future__ import annotations

import re
from copy import copy
from typing import TYPE_CHECKING, Any

from rich.segment import Segment
from rich.theme import Theme


try:
    from rich_rst import RestructuredText
except ModuleNotFoundError as e:
    if e.name != "rich_rst":
        raise
    raise ImportError(
        "text_markup='rst' requires the rich-rst package. Install it with: pip install 'rich-click[rst]'"
    ) from e


if TYPE_CHECKING:  # pragma: no cover
    from rich.console import Console, ConsoleOptions, RenderResult
    from rich.style import Style, StyleType


_FOOTNOTE_REF = re.compile(r" ?\[[^\]\s]+\]_")
_DEFINITION = re.compile(r"^\.\. [_|].*(?:\n[ \t]+\S.*)*", re.MULTILINE)


def _line_block(paragraph: str) -> str:
    # Non-breaking spaces stop docutils turning indentation into nested blocks; they become spaces again on output.
    lines = [re.sub("^ +", lambda m: "\u00a0" * len(m[0]), line) for line in paragraph[1:].strip("\n").split("\n")]
    # rich-rst ends a line block without a newline, so two empty lines separate it from what follows.
    return "\n".join(f"| {line}" for line in [*lines, "", ""])


def _line_blocks(text: str) -> str:
    r"""Turn Click's `\b` no-rewrap paragraphs into rST line blocks."""
    return "\n\n".join(_line_block(p) if p.startswith("\b") else p for p in text.split("\n\n"))


def first_paragraph(text: str) -> str:
    """Return the first paragraph of an rST document, keeping the link targets and substitutions it can use."""
    first, _, rest = text.partition("\n\n")
    return "\n\n".join([_FOOTNOTE_REF.sub("", first), *_DEFINITION.findall(rest)])


def _is_block_end(text: str) -> bool:
    stripped = text.strip()
    return not stripped or "\u2500" <= stripped[0] <= "\u257f"


class RichClickRST:
    """Render reStructuredText with a base style applied, optionally styling the first block differently."""

    def __init__(
        self, text: str, style: StyleType = "", first_block_style: StyleType | None = None, **kwargs: Any
    ) -> None:
        kwargs.setdefault("admonition_style", "compact")
        kwargs.setdefault("default_lexer", "console")
        self.renderable = RestructuredText(_line_blocks(text), **kwargs)
        self.style = style
        self.first_block_style = first_block_style

    def _render_lines(self, console: Console, options: ConsoleOptions, style: Style) -> list[list[Segment]]:
        # rich-rst gives plain text an explicit reset style, which would override a base style applied afterwards.
        text_style = console.get_style("restructuredtext.text", default="default not bold not italic not underline")
        with console.use_theme(Theme({"restructuredtext.text": text_style + style})):
            lines = console.render_lines(self.renderable, options, pad=False)
        return [
            [Segment(s.text.replace("\u00a0", " "), s.style, s.control) for s in Segment.apply_style(line, style)]
            for line in lines
        ]

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        # rich-rst renders footnote and citation panels at console width, ignoring options.
        console = copy(console)
        console.width = options.max_width
        # rich-rst drops enumerated list item text when justify="left" (e.g. inside table columns).
        options = options.update(justify="default")
        style = console.get_style(self.style)
        lines = self._render_lines(console, options, style)
        # ponytail: a second render for the first block, as rich-rst exposes no block boundaries to restyle.
        first_lines = None
        if self.first_block_style is not None:
            first_lines = self._render_lines(console, options, console.get_style(self.first_block_style))
        new_line = Segment.line()
        previous_blank = False
        for i, line in enumerate(lines):
            text = "".join(s.text for s in line)
            blank = not text.strip()
            # The line-block separator lines double up when a list or block follows.
            if blank and previous_blank:
                continue
            previous_blank = blank
            if first_lines is not None and _is_block_end(text):
                first_lines = None
            yield from line if first_lines is None else first_lines[i]
            yield new_line
