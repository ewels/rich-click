"""reStructuredText rendering support. Only imported when `text_markup="rst"` is used."""

from __future__ import annotations

from copy import copy
from typing import TYPE_CHECKING, Any

from rich.measure import Measurement
from rich.segment import Segment


try:
    from rich_rst import RestructuredText
except ImportError as e:
    raise ImportError(
        "text_markup='rst' requires the rich-rst package. Install it with: pip install 'rich-click[rst]'"
    ) from e


if TYPE_CHECKING:  # pragma: no cover
    from rich.console import Console, ConsoleOptions, RenderResult
    from rich.style import StyleType


def _line_blocks(text: str) -> str:
    r"""Turn Click's `\b` no-rewrap paragraphs into rST line blocks."""
    return "\n\n".join(
        "\n".join(f"| {line}" for line in p[1:].strip("\n").split("\n")) if p.startswith("\b") else p
        for p in text.split("\n\n")
    )


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

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        # rich-rst renders footnote and citation panels at console width, ignoring options.
        console = copy(console)
        console.width = options.max_width
        # rich-rst drops enumerated list item text when justify="left" (e.g. inside table columns).
        options = options.update(justify="default")
        style = console.get_style(self.style)
        line_style = style if self.first_block_style is None else console.get_style(self.first_block_style)
        new_line = Segment.line()
        for line in console.render_lines(self.renderable, options):
            if line_style is not style and not "".join(s.text for s in line).strip():
                line_style = style
            yield from Segment.apply_style(line, line_style)
            yield new_line

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        return Measurement.get(console, options, self.renderable)
