from functools import wraps
from typing import Any, IO, Optional

import click
import rich
import rich.highlighter
import rich.markdown
import rich.padding
import rich.text
import rich.theme
from rich.console import Console

from rich_click.rich_help_configuration import RichHelpConfiguration


def create_console(config: RichHelpConfiguration, file: Optional[IO[str]] = None) -> Console:
    """Create a Rich Console configured from Rich Help Configuration.

    Args:
        config: Rich Help Configuration instance
        file: Optional IO stream to write Rich Console output
            Defaults to None.
    """
    console = Console(
        theme=rich.theme.Theme(
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
        highlighter=config.highlighter,
        color_system=config.color_system,
        force_terminal=config.force_terminal,
        file=file,
        width=config.width,
        legacy_windows=config.legacy_windows,
    )
    if isinstance(config.max_width, int):
        console.width = min(config.max_width, console.size.width)
    return console


class RichHelpFormatter(click.HelpFormatter):
    """Rich Help Formatter.

    This class is a container for the help configuration and Rich Console that
    are used internally by the help and error printing methods.
    """

    console: Console
    """Rich Console created from the help configuration.

    This console is meant only for use with the formatter and should
    not be created directly
    """

    def __init__(
        self,
        indent_increment: int = 2,
        width: Optional[int] = None,
        max_width: Optional[int] = None,
        *args: Any,
        config: Optional[RichHelpConfiguration] = None,
        file: Optional[IO[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Create Rich Help Formatter.

        Args:
            config: Configuration.
                Defaults to None.
        """
        if config is not None:
            self.config = config
            # Rich config overrides width and max width if set.
        else:
            self.config = RichHelpConfiguration.build_from_globals()

        self.console = create_console(self.config)

        if width is None:
            width = self.config.width
        if max_width is None:
            max_width = self.config.max_width

        super().__init__(indent_increment, width, max_width, *args, **kwargs)

    @wraps(Console.print)
    def write(self, string: Any, **kwargs: Any) -> None:
        self.console.print(string, **kwargs)

    def write_usage(self, prog: str, args: str = "", prefix: Optional[str] = None) -> None:
        from rich_click.rich_help_rendering import get_rich_usage

        get_rich_usage(formatter=self, prog=prog, args=args, prefix=prefix)

    def write_abort(self) -> None:
        """Print richly formatted abort error."""
        self.console.print(self.config.aborted_text, style=self.config.style_aborted)
