"""
rich-click is a minimal Python module to combine the efforts of the excellent packages 'rich' and 'click'.

The intention is to provide attractive help output from Click, formatted with Rich, with minimal
customization required.
"""

from __future__ import annotations

import typing as _t


__version__ = "1.9.9"

# The primary Click API, imported eagerly.
# We name these individually rather than `from click import *` to force mypy to
# recognize a few type annotation overrides for the rich_click decorators.
#
# These six are the load-bearing names -- every rich-click subclass derives from
# one -- and Click is not going to move or deprecate them, so importing them
# costs nothing and keeps `rich_click.Command` resolvable without a __getattr__
# hop on the hottest path.
from click.core import Argument as Argument
from click.core import Command as Command
from click.core import Context as Context
from click.core import Group as Group
from click.core import Option as Option
from click.core import Parameter as Parameter


# The rest of the Click API, re-exported but resolved lazily by `__getattr__`.
#
# Click has been moving and deprecating names between minor releases, and
# importing these eagerly meant the DeprecationWarning fired the moment anything
# imported rich_click -- breaking CI for downstreams that assert no warnings
# (litestar-org/litestar#5020) over names most of them never touch. Resolving on
# first access moves the warning to the code that actually uses the name.
#
# Type checkers still see real `from click...` imports, so the annotation
# overrides are unaffected, and a name Click removes outright still fails under
# TYPE_CHECKING -- which is correct. That is a real breakage; it just should not
# land at import time on a CLI that never used the name.
if _t.TYPE_CHECKING:
    from click.core import CommandCollection as CommandCollection
    from click.decorators import make_pass_decorator as make_pass_decorator
    from click.decorators import pass_obj as pass_obj
    from click.exceptions import Abort as Abort
    from click.exceptions import BadArgumentUsage as BadArgumentUsage
    from click.exceptions import BadOptionUsage as BadOptionUsage
    from click.exceptions import BadParameter as BadParameter
    from click.exceptions import ClickException as ClickException
    from click.exceptions import FileError as FileError
    from click.exceptions import MissingParameter as MissingParameter
    from click.exceptions import NoSuchOption as NoSuchOption
    from click.exceptions import UsageError as UsageError
    from click.formatting import HelpFormatter as HelpFormatter
    from click.formatting import wrap_text as wrap_text
    from click.termui import clear as clear
    from click.termui import confirm as confirm
    from click.termui import echo_via_pager as echo_via_pager
    from click.termui import edit as edit
    from click.termui import getchar as getchar
    from click.termui import launch as launch
    from click.termui import pause as pause
    from click.termui import progressbar as progressbar
    from click.termui import prompt as prompt
    from click.termui import secho as secho
    from click.termui import style as style
    from click.termui import unstyle as unstyle
    from click.types import BOOL as BOOL
    from click.types import FLOAT as FLOAT
    from click.types import INT as INT
    from click.types import STRING as STRING
    from click.types import UNPROCESSED as UNPROCESSED
    from click.types import UUID as UUID
    from click.types import Choice as Choice
    from click.types import DateTime as DateTime
    from click.types import File as File
    from click.types import FloatRange as FloatRange
    from click.types import IntRange as IntRange
    from click.types import ParamType as ParamType
    from click.types import Path as Path
    from click.types import Tuple as Tuple
    from click.utils import echo as echo
    from click.utils import format_filename as format_filename
    from click.utils import get_app_dir as get_app_dir
    from click.utils import open_file as open_file

from rich_click.decorators import argument as argument
from rich_click.decorators import command as command
from rich_click.decorators import command_panel as command_panel
from rich_click.decorators import confirmation_option as confirmation_option
from rich_click.decorators import group as group
from rich_click.decorators import help_option as help_option
from rich_click.decorators import option as option
from rich_click.decorators import option_panel as option_panel
from rich_click.decorators import pass_context as pass_context
from rich_click.decorators import password_option as password_option
from rich_click.decorators import rich_config as rich_config
from rich_click.decorators import version_option as version_option
from rich_click.rich_command import RichCommand as RichCommand
from rich_click.rich_command import RichCommandCollection as RichCommandCollection
from rich_click.rich_command import RichGroup as RichGroup
from rich_click.rich_context import RichContext as RichContext
from rich_click.rich_context import get_current_context as get_current_context
from rich_click.rich_help_configuration import RichHelpConfiguration as RichHelpConfiguration
from rich_click.rich_help_formatter import RichHelpFormatter as RichHelpFormatter
from rich_click.rich_panel import RichCommandPanel as RichCommandPanel
from rich_click.rich_panel import RichOptionPanel as RichOptionPanel
from rich_click.rich_panel import RichPanel as RichPanel
from rich_click.rich_parameter import RichArgument as RichArgument
from rich_click.rich_parameter import RichOption as RichOption
from rich_click.rich_parameter import RichParameter as RichParameter

from . import rich_click as rich_click


#: Click names re-exported by rich-click but resolved on first access, so that
#: importing rich_click does not import them. Listed explicitly rather than
#: derived from `dir(click)`, so the public surface stays a decision made in
#: this file rather than whatever the installed Click happens to carry.
_LAZY_CLICK_EXPORTS: _t.Final[tuple[str, ...]] = (
    "Abort",
    "BOOL",
    "BadArgumentUsage",
    "BadOptionUsage",
    "BadParameter",
    "Choice",
    "ClickException",
    "CommandCollection",
    "DateTime",
    "FLOAT",
    "File",
    "FileError",
    "FloatRange",
    "HelpFormatter",
    "INT",
    "IntRange",
    "MissingParameter",
    "NoSuchOption",
    "ParamType",
    "Path",
    "STRING",
    "Tuple",
    "UNPROCESSED",
    "UUID",
    "UsageError",
    "clear",
    "confirm",
    "echo",
    "echo_via_pager",
    "edit",
    "format_filename",
    "get_app_dir",
    "getchar",
    "launch",
    "make_pass_decorator",
    "open_file",
    "pass_obj",
    "pause",
    "progressbar",
    "prompt",
    "secho",
    "style",
    "unstyle",
    "wrap_text",
)


def __dir__() -> list[str]:
    """
    Include the lazily-resolved Click names in `dir(rich_click)`.

    Module `__dir__` defaults to `__dict__`, and these names are not in it until
    something asks for one -- so without this they would be invisible to
    tab-completion and `help()` on a fresh import.
    """
    return sorted({*globals(), *_LAZY_CLICK_EXPORTS, "RichMultiCommand"})


def __getattr__(name: str) -> object:
    from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_9X

    if name == "RichMultiCommand" and CLICK_IS_BEFORE_VERSION_9X:
        import warnings

        warnings.warn(
            "'RichMultiCommand' is deprecated and will be removed in Click 9.0. Use 'RichGroup' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from rich_click.rich_command import RichMultiCommand

        return RichMultiCommand

    else:
        import click

        return getattr(click, name)
