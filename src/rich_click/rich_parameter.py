from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any

import click


if TYPE_CHECKING:
    from rich.columns import Columns
    from rich.style import StyleType

    from rich_click.rich_context import RichContext
    from rich_click.rich_help_formatter import RichHelpFormatter
    from rich_click.rich_help_rendering import RichPanelRow
    from rich_click.rich_panel import RichOptionPanel


class RichParameter(click.Parameter):
    """Base class of `RichOption` and `RichArgument`: a click Parameter that rich-click formats in help."""

    def __init__(
        self,
        *args: Any,
        panel: str | list[str] | None = None,
        help: str | None = None,
        help_style: StyleType | None = None,
        **kwargs: Any,
    ):
        """Create RichParameter instance."""
        super().__init__(*args, **kwargs)
        self.panel = panel

        if help:
            help = inspect.cleandoc(help)

            deprecated = kwargs.get("deprecated")
            if deprecated:
                deprecated_message = f"(DEPRECATED: {deprecated})" if isinstance(deprecated, str) else "(DEPRECATED)"
                help = help + deprecated_message if help is not None else deprecated_message

        self.help = help

        self.help_style = help_style

    def to_info_dict(self) -> dict[str, Any]:
        """
        Gather information that could be useful for a tool generating
        user-facing documentation.

        Use :meth:`click.Context.to_info_dict` to traverse the entire
        CLI structure.
        """
        info = super().to_info_dict()
        info.setdefault("help", self.help)
        return info

    def get_rich_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> Columns:
        """Get the rich help text for this parameter."""
        from rich_click.rich_help_rendering import get_help_parameter

        return get_help_parameter(self, ctx, formatter)

    def get_rich_table_row(
        self,
        ctx: RichContext,
        formatter: RichHelpFormatter,
        panel: RichOptionPanel | None = None,
    ) -> RichPanelRow:
        """Create a row for the rich table corresponding with this parameter."""
        from rich_click.rich_help_rendering import get_parameter_rich_table_row

        return get_parameter_rich_table_row(self, ctx, formatter, panel)


class RichArgument(RichParameter, click.Argument):
    """
    A positional argument of a command, formatted by rich-click. The `argument` decorator creates one.

    Arguments are required by default. With `nargs=-1`, an argument takes any number of values.
    """


class RichOption(RichParameter, click.Option):
    """An option of a command, formatted by rich-click. The `option` decorator creates one."""
