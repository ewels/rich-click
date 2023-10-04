import click

from rich_click.rich_mixin import RichMixin


class RichCommand(RichMixin, click.Command):
    """Richly formatted click Command.

    Inherits click.Command and overrides help and error methods
    to print richly formatted output.
    """
