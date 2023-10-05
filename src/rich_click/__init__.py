# flake8: noqa: F401
"""
rich-click is a minimal Python module to combine the efforts of the excellent packages 'rich' and 'click'.

The intention is to provide attractive help output from click, formatted with rich, with minimal
customisation required.
"""

__version__ = "1.7.0dev"

from click import *

from . import rich_click as rich_click

from rich_click.decorators import command as command  # type: ignore[no-redef]
from rich_click.decorators import group as group  # type: ignore[no-redef]
from rich_click.decorators import pass_context as pass_context  # type: ignore[no-redef,assignment]
from rich_click.decorators import rich_config as rich_config
from rich_click.rich_command import RichCommand as RichCommand
from rich_click.rich_command import RichGroup as RichGroup
from rich_click.rich_command import RichMultiCommand as RichMultiCommand
from rich_click.rich_context import RichContext as RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration as RichHelpConfiguration


def __getattr__(name: str) -> object:
    import click

    from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_9X

    if name == "RichMultiCommand" and CLICK_IS_BEFORE_VERSION_9X:
        import warnings

        warnings.warn(
            "'RichMultiCommand' is deprecated and will be removed in Click 9.0. Use" " 'RichGroup' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from rich_click.rich_command import RichMultiCommand

        return RichMultiCommand

    # Support for potentially deprecated objects in newer versions of click:
    elif name in {"BaseCommand", "OptionParser", "MultiCommand"}:
        return getattr(click, name)

    else:
        raise AttributeError(name)
