from io import StringIO
from typing import IO, Optional

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
    return Console(
        theme=rich.theme.Theme(
            {
                "option": config.style_option,
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
        width=config.max_width,
        file=file,
        legacy_windows=config.legacy_windows,
    )


def get_module_config() -> RichHelpConfiguration:
    """Get the module-level help configuration.

    A function-level import is used to avoid a circular dependency
    between the formatter and formatter operations.
    """
    from rich_click.rich_click import get_module_help_configuration  # type: ignore

    return get_module_help_configuration()


class RichHelpFormatter(click.HelpFormatter):
    """Rich Help Formatter.

    This class is a container for the help configuration and Rich Console that
    are used internally by the help and error printing methods.
    """

    def __init__(
        self,
        *args,
        config: Optional[RichHelpConfiguration] = None,
        **kwargs,
    ) -> None:
        """Create Rich Help Formatter.

        Args:
            config: Configuration.
                Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self._rich_buffer = StringIO()
        self._config = config or get_module_config()
        self._console = create_console(self._config, self._rich_buffer)

    @property
    def config(self) -> RichHelpConfiguration:
        """Rich Help Configuration."""
        return self._config

    @property
    def console(self) -> Console:
        """Rich Console created from the help configuration.

        This console is meant only for use with the formatter and should
        not be created directly
        """
        return self._console

    def getvalue(self) -> str:
        """Get Console output.

        This maintains compatibility with the current Click interface
        """
        result = super().getvalue()
        if result:
            self._console.print(result)
        return self._rich_buffer.getvalue()
