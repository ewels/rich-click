# This file exists to keep around original copies of all the Click types.
# This is needed for rich_help_rendering, which is lazy-loaded after `rich-click` patching occurs.
# However, this file needs to be instantiated _before_ patching occurs.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Tuple, Type

from click import Argument as Argument
from click import Command as Command
from click import CommandCollection as CommandCollection
from click import Group as Group
from click import Option as Option
from click import Parameter as Parameter


if TYPE_CHECKING:  # pragma: no cover
    import sys

    if sys.version_info >= (3, 13):
        from typing import TypeIs
    else:
        from typing_extensions import TypeIs


# Fork-agnostic type detection.
#
# rich-click's renderer needs to recognize commands/groups/parameters by type.
# click-compatible forks (e.g. asyncclick) ship a *parallel* class tree that does
# not subclass click's, so a plain ``isinstance(x, click.Group)`` returns ``False``
# for them. These tuples back the ``is_*`` helpers below; a fork registers its
# classes once via :func:`register_click_impl` and detection then works for both.

_ARGUMENT_TYPES: Tuple[type, ...] = (Argument,)
_COMMAND_TYPES: Tuple[type, ...] = (Command,)
_GROUP_TYPES: Tuple[type, ...] = (Group,)
_OPTION_TYPES: Tuple[type, ...] = (Option,)
_PARAMETER_TYPES: Tuple[type, ...] = (Parameter,)


def register_click_impl(module: Any) -> None:
    """
    Register a click-compatible fork's classes so rich-click can detect them.

    Allows forks such as ``asyncclick`` to opt in to rich-click's type detection
    without rich-click taking a hard dependency on them. Calling this more than
    once with the same module is a no-op (idempotent).

    Args:
    ----
        module: A module exposing ``Argument``, ``Command``, ``Group``,
            ``Option`` and ``Parameter`` (e.g. ``asyncclick``).

    """
    global _ARGUMENT_TYPES, _COMMAND_TYPES, _GROUP_TYPES, _OPTION_TYPES, _PARAMETER_TYPES

    for tuple_name, attr in (
        ("_ARGUMENT_TYPES", "Argument"),
        ("_COMMAND_TYPES", "Command"),
        ("_GROUP_TYPES", "Group"),
        ("_OPTION_TYPES", "Option"),
        ("_PARAMETER_TYPES", "Parameter"),
    ):
        cls: Type[Any] = getattr(module, attr)
        existing: Tuple[type, ...] = globals()[tuple_name]
        if cls not in existing:
            globals()[tuple_name] = existing + (cls,)


def is_argument(obj: Any) -> "TypeIs[Argument]":
    """Return whether ``obj`` is a click (or registered fork) Argument."""
    return isinstance(obj, _ARGUMENT_TYPES)


def is_command(obj: Any) -> "TypeIs[Command]":
    """Return whether ``obj`` is a click (or registered fork) Command."""
    return isinstance(obj, _COMMAND_TYPES)


def is_group(obj: Any) -> "TypeIs[Group]":
    """Return whether ``obj`` is a click (or registered fork) Group."""
    return isinstance(obj, _GROUP_TYPES)


def is_option(obj: Any) -> "TypeIs[Option]":
    """Return whether ``obj`` is a click (or registered fork) Option."""
    return isinstance(obj, _OPTION_TYPES)


def is_parameter(obj: Any) -> "TypeIs[Parameter]":
    """Return whether ``obj`` is a click (or registered fork) Parameter."""
    return isinstance(obj, _PARAMETER_TYPES)
