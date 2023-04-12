from typing import ClassVar, Optional, Type

import click
from rich.console import Console

from rich_click.rich_help_configuration import RichHelpConfiguration
from rich_click.rich_help_formatter import RichHelpFormatter


class RichContext(click.Context):
    """Click Context class endowed with Rich superpowers."""

    formatter_class: ClassVar[Type[RichHelpFormatter]] = RichHelpFormatter

    def __init__(
        self,
        *args,
        rich_console: Optional[Console] = None,
        rich_help_config: Optional[RichHelpConfiguration] = None,
        **kwargs,
    ) -> None:
        """Create Rich Context instance.

        Args:
            rich_console: Rich Console.
                Defaults to None.
            rich_help_config: Rich help configuration.
                Defaults to None.
        """
        super().__init__(*args, **kwargs)
        self._console = rich_console
        self._help_config = rich_help_config

    @property
    def console(self) -> Optional[Console]:
        """Rich Console instance for displaying beautfil application output in the terminal.

        NOTE: This is a separate instance from the one used by the help formatter, and allows full control of the
        console configuration.

        See `rich_config` decorator for how to apply the settings.
        """
        return self._console

    @property
    def help_config(self) -> Optional[RichHelpConfiguration]:
        """Rich help configuration."""
        return self._help_config

    def make_formatter(self):
        """Create the Rich Help Formatter."""
        return self.formatter_class(config=self.help_config)
