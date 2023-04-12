import sys
from typing import ClassVar, Optional, Type

import click

from rich_click.rich_click import rich_abort_error, rich_format_error, rich_format_help
from rich_click.rich_context import RichContext
from rich_click.rich_help_formatter import RichHelpFormatter


class RichCommand(click.Command):
    """Richly formatted click Command.

    Inherits click.Command and overrides help and error methods
    to print richly formatted output.
    """

    standalone_mode = False
    context_class: ClassVar[Type[RichContext]] = RichContext

    def __init__(self, *args, **kwargs):
        """Create Rich Command.

        Accepts same arguments as Click Command.

        Docs reference: https://click.palletsprojects.com/
        """
        super().__init__(*args, **kwargs)
        self._formatter: Optional[RichHelpFormatter] = None

    @property
    def console(self):
        """Rich Console.

        This is a separate instance from the help formatter that allows full control of the
        console configuration.

        See `rich_config` decorator for how to apply the settings.
        """
        return self.context_settings.get("rich_console")

    @property
    def help_config(self):
        """Rich Help Configuration."""
        return self.context_settings.get("rich_help_config")

    @property
    def formatter(self):
        """Rich Help Formatter.

        This is separate instance from the formatter used to display help,
        but is created from the same `RichHelpConfiguration`. Currently only used
        for error reporting.
        """
        return self._formatter

    def main(self, *args, standalone_mode: bool = True, **kwargs):
        formatter = self._formatter = RichHelpFormatter(config=self.help_config)
        try:
            rv = super().main(*args, standalone_mode=False, **kwargs)
            if not standalone_mode:
                return rv
        except click.ClickException as e:
            rich_format_error(e, formatter)
            if not standalone_mode:
                raise
            sys.stderr.write(formatter.getvalue())
            sys.exit(e.exit_code)
        except click.exceptions.Abort:
            rich_abort_error(formatter)
            if not standalone_mode:
                raise
            sys.stderr.write(formatter.getvalue())
            sys.exit(1)

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter):
        rich_format_help(self, ctx, formatter)
