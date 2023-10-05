# flake8: noqa: F401
"""
rich-click is a minimal Python module to combine the efforts of the excellent packages 'rich' and 'click'.

The intention is to provide attractive help output from click, formatted with rich, with minimal
customisation required.
"""

__version__ = "1.7.0dev"

from click import *

from . import rich_click as rich_click

from rich_click.decorators import command as command
from rich_click.decorators import group as group
from rich_click.decorators import rich_config as rich_config
from rich_click.rich_command import RichBaseCommand as RichBaseCommand
from rich_click.rich_command import RichCommand as RichCommand
from rich_click.rich_command import RichGroup as RichGroup
from rich_click.rich_command import RichMultiCommand as RichMultiCommand
from rich_click.rich_context import RichContext as RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration as RichHelpConfiguration
