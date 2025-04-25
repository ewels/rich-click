import os
import sys
from functools import cached_property
from typing import IO, TYPE_CHECKING, Any, Dict, Optional

import click
from typing_extensions import Literal

from rich_click.rich_help_configuration import RichHelpConfiguration


if TYPE_CHECKING:
    from rich.console import Console
    from rich.highlighter import Highlighter


def create_console(config: RichHelpConfiguration, file: Optional[IO[str]] = None) -> "Console":
    """
    Create a Rich Console configured from Rich Help Configuration.

    Args:
    ----
        config: Rich Help Configuration instance
        file: Optional IO stream to write Rich Console output
            Defaults to None.

    """
    from rich.console import Console
    from rich.theme import Theme

    if file is not None:
        import warnings

        warnings.warn(
            "The file kwarg to `create_console()` is deprecated" " and will be removed in a future release.",
            DeprecationWarning,
            stacklevel=2,
        )

    console = Console(
        theme=Theme(
            {
                "option": config.style_option,
                "command": config.style_command,
                "argument": config.style_argument,
                "switch": config.style_switch,
                "metavar": config.style_metavar,
                "metavar_sep": config.style_metavar_separator,
                "usage": config.style_usage,
            }
        ),
        color_system=config.color_system,
        force_terminal=config.force_terminal,
        file=file or open(os.devnull, "w"),
        width=config.width,
        record=True if file is None else False,
        legacy_windows=config.legacy_windows,
    )
    if isinstance(config.max_width, int):
        console.width = min(config.max_width, console.size.width)
    return console


class RichHelpFormatter(click.HelpFormatter):
    """
    Rich Help Formatter.

    This class is a container for the help configuration and Rich Console that
    are used internally by the help and error printing methods.
    """

    console: "Console"
    """Rich Console created from the help configuration.

    This console is meant only for use with the formatter and should
    not be created directly
    """

    export_console_as: Literal[None, "html", "svg", "text"] = None

    def __init__(
        self,
        indent_increment: int = 2,
        width: Optional[int] = None,
        max_width: Optional[int] = None,
        *args: Any,
        console: Optional["Console"] = None,
        config: Optional[RichHelpConfiguration] = None,
        export_console_as: Literal[None, "html", "svg", "text"] = None,
        export_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Create Rich Help Formatter.

        Args:
        ----
            indent_increment: Passed to click.HelpFormatter.
            width: Passed to click.HelpFormatter. Overrides config.width if not None.
            max_width: Passed to click.HelpFormatter. Overrides config.max_width if not None.
            *args: Args passed to click.HelpFormatter.
            console: Use an external console.
            config: RichHelpConfiguration. If None, then build config from globals.
            file: Stream to output to in the Rich Console. If None, use stdout.
            export_console_as: How output is rendered by getvalue(). Default of None renders output normally.
            export_kwargs: Any kwargs passed to the export method of the Console in getvalue().
            **kwargs: Kwargs passed to click.HelpFormatter.

        """
        if config is not None:
            self.config = config
            # Rich config overrides width and max width if set.
        else:
            self.config = RichHelpConfiguration.load_from_globals()

        file = kwargs.pop("file", None)
        if file is not None:
            import warnings

            warnings.warn(
                "The file kwarg to `RichHelpFormatter()` is deprecated" " and will be removed in a future release.",
                DeprecationWarning,
                stacklevel=2,
            )

        if console:
            self.console = console
        else:
            self.console = create_console(self.config)

        if file is not None:
            self.console.file = file

        # TODO: Revisit this. I don't think this does anything.
        if width is None:
            width = self.config.width
        if max_width is None:
            max_width = self.config.max_width

        self.export_console_as = export_console_as
        self.export_kwargs = export_kwargs or {}

        super().__init__(indent_increment, width, max_width, *args, **kwargs)

    @cached_property
    def highlighter(self) -> "Highlighter":
        if self.config.highlighter is not None:
            return self.config.highlighter
        else:
            from rich.highlighter import RegexHighlighter

            class HighlighterClass(RegexHighlighter):
                highlights = self.config.highlighter_patterns

            return HighlighterClass()

    def write(self, *objects: Any, **kwargs: Any) -> None:
        self.console.print(*objects, **kwargs)

    def write_usage(self, prog: str, args: str = "", prefix: Optional[str] = None) -> None:
        from rich_click.rich_help_rendering import get_rich_usage

        get_rich_usage(formatter=self, prog=prog, args=args, prefix=prefix)

    def write_error(self, e: click.ClickException) -> None:
        from rich_click.rich_help_rendering import rich_format_error

        rich_format_error(self=e, formatter=self)

    def write_abort(self) -> None:
        """Print richly formatted abort error."""
        self.console.print(self.config.aborted_text, style=self.config.style_aborted)

    def getvalue(self) -> str:
        if self.console.record:
            kw = self.export_kwargs.copy()
            kw.setdefault("clear", False)
            if self.export_console_as is None:
                kw.setdefault("styles", True)
                res = self.console.export_text(**kw)
            elif self.export_console_as == "text":
                res = self.console.export_text(**kw)
            elif self.export_console_as == "html":
                res = self.console.export_html(**kw)
            elif self.export_console_as == "svg":
                kw.setdefault("title", " ".join(sys.argv))
                res = self.console.export_svg(**kw)
            else:
                raise ValueError(
                    "Invalid value for `export_console_as`." " Must be one of 'text', 'html', 'svg', or None."
                )
            return res
        else:
            return super().getvalue()
