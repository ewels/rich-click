from typing import TYPE_CHECKING, Any, Optional, Sequence

import click


if TYPE_CHECKING:
    from rich.columns import Columns

    from rich_click.rich_context import RichContext
    from rich_click.rich_help_formatter import RichHelpFormatter
    from rich_click.rich_help_rendering import RichPanelRow


class RichParameter(click.Parameter):
    r"""
    A parameter to a command comes in two versions: they are either
    :class:`Option`\s or :class:`Argument`\s.  Other subclasses are currently
    not supported by design as some of the internals for parsing are
    intentionally not finalized.
    """

    def __init__(self, *args: Any, panel: Optional[str] = None, **kwargs: Any):
        """Create RichParameter instance."""
        super().__init__(*args, **kwargs)
        self.panel = panel

    def get_rich_help(self, ctx: "RichContext", formatter: "RichHelpFormatter") -> "Columns":
        """Get the rich help text for this parameter."""
        from rich_click.rich_help_rendering import get_help_parameter

        return get_help_parameter(self, ctx, formatter)

    def get_rich_table_row(self, ctx: "RichContext", formatter: "RichHelpFormatter") -> "RichPanelRow":
        """Create a row for the rich table corresponding with this parameter."""
        from rich_click.rich_help_rendering import get_rich_table_row

        return get_rich_table_row(self, ctx, formatter)


class RichArgument(click.Argument, RichParameter):
    """
    Arguments are positional parameters to a command.  They generally
    provide fewer features than options but can have infinite ``nargs``
    and are required by default.

    All parameters are passed onwards to the constructor of :class:`Parameter`.
    """

    param_type_name = "argument"

    def __init__(
        self,
        param_decls: Sequence[str],
        required: Optional[bool] = None,
        help: Optional[str] = None,
        panel: Optional[str] = None,
        **attrs: Any,
    ) -> None:
        """Create RichArgument instance."""
        super().__init__(param_decls, required=required, **attrs)
        self.help = help
        self.panel = panel


class RichOption(click.Option, RichParameter):
    """
    Options are usually optional values on the command line and
    have some extra features that arguments don't have.

    All other parameters are passed onwards to the parameter constructor.
    """

    pass
