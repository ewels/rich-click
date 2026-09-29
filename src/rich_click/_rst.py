"""reStructuredText rendering support. Only imported when `text_markup="rst"` is used."""

from __future__ import annotations

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


class RichClickRST:
    """Render reStructuredText with a base style applied."""

    def __init__(self, text: str, style: StyleType = "", **kwargs: Any) -> None:
        kwargs.setdefault("admonition_style", "compact")
        self.renderable = RestructuredText(text, **kwargs)
        self.style = style

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        # rich-rst drops enumerated list item text when justify="left" (e.g. inside table columns).
        options = options.update(justify="default")
        style = console.get_style(self.style)
        lines = console.render_lines(self.renderable, options, style=style)
        new_line = Segment.line()
        for line in lines:
            yield from line
            yield new_line

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        return Measurement.get(console, options, self.renderable)
