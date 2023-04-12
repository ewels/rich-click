"""
rich-click is a minimal Python module to combine the efforts of the excellent packages 'rich' and 'click'.

The intention is to provide attractive help output from click, formatted with rich, with minimal
customisation required.
"""

__version__ = "1.6.1"

from typing import Any, Callable, cast, Optional, overload, TYPE_CHECKING, Union

from click import *  # noqa: F401, F403
from click import Command
from click import command as click_command
from click import Group
from click import group as click_group
from rich.console import Console

from . import rich_click  # noqa: F401

from rich_click.rich_command import RichCommand
from rich_click.rich_context import RichContext
from rich_click.rich_group import RichGroup
from rich_click.rich_help_configuration import RichHelpConfiguration

# MyPy does not like star imports. Therefore when we are type checking, we import each individual module
# from click here. This way MyPy will recognize the import and not throw any errors. Furthermore, because of
# the TYPE_CHECKING check, it does not influence the start routine at all.
if TYPE_CHECKING:
    from click import argument, Choice, option, Path, version_option  # noqa: F401

    __all__ = [
        "argument",
        "Choice",
        "option",
        "Path",
        "version_option",
        "group",
        "command",
        "rich_config",
        "RichContext",
        "RichHelpConfiguration",
    ]


def group(name=None, cls=RichGroup, **attrs) -> Callable[..., RichGroup]:
    """
    Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default.
    """

    def wrapper(fn):
        if hasattr(fn, "__rich_context_settings__"):
            rich_context_settings = getattr(fn, "__rich_context_settings__", {})
            console = rich_context_settings.get("rich_console", None)
            help_config = rich_context_settings.get("help_config", None)
            context_settings = attrs.get("context_settings", {})
            context_settings.update(rich_console=console, rich_help_config=help_config)
            attrs.update(context_settings=context_settings)
            del fn.__rich_context_settings__
        if callable(name) and cls:
            group = click_group(cls=cls, **attrs)(name)
        else:
            group = click_group(name, cls=cls, **attrs)
        cmd = cast(RichGroup, group(fn))
        return cmd

    return wrapper


def command(name=None, cls=RichCommand, **attrs) -> Callable[..., RichCommand]:
    """
    Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
    """

    def wrapper(fn):
        if hasattr(fn, "__rich_context_settings__"):
            rich_context_settings = getattr(fn, "__rich_context_settings__", {})
            console = rich_context_settings.get("rich_console", None)
            help_config = rich_context_settings.get("help_config", None)
            context_settings = attrs.get("context_settings", {})
            context_settings.update(rich_console=console, rich_help_config=help_config)
            attrs.update(context_settings=context_settings)
            del fn.__rich_context_settings__
        if callable(name) and cls:
            command = click_command(cls=cls, **attrs)(name)
        else:
            command = click_command(name, cls=cls, **attrs)
        cmd = cast(RichCommand, command(fn))
        return cmd

    return wrapper


class NotSupportedError(Exception):
    """Not Supported Error."""

    pass


def rich_config(console: Optional[Console] = None, help_config: Optional[RichHelpConfiguration] = None):
    """Use decorator to configure Rich Click settings.

    Args:
        console: A Rich Console that will be accessible from the `RichContext`, `RichCommand`, and `RichGroup` instances
            Defaults to None.
        help_config: Rich help configuration that is used internally to format help messages and exceptions
            Defaults to None.
    """

    @overload
    def decorator(obj: Union[RichCommand, RichGroup]) -> Union[RichCommand, RichGroup]:
        ...

    @overload
    def decorator(obj: Callable[..., Any]) -> Callable[..., Any]:
        ...

    def decorator(obj):
        if isinstance(obj, (RichCommand, RichGroup)):
            obj.context_settings.update({"rich_console": console, "rich_help_config": help_config})
        elif callable(obj) and not isinstance(obj, (Command, Group)):
            setattr(obj, "__rich_context_settings__", {"rich_console": console, "rich_help_config": help_config})
        else:
            raise NotSupportedError("`rich_config` requires a `RichCommand` or `RichGroup`. Try using the cls keyword")

        decorator.__doc__ = obj.__doc__
        return obj

    return decorator
