from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, TypedDict


if sys.version_info < (3, 11):
    from typing_extensions import NotRequired
else:
    from typing import NotRequired

if TYPE_CHECKING:
    from rich.style import StyleType

    from rich_click.rich_help_configuration import CommandColumnType, OptionColumnType


notset: Any = object()


def truthy(o: Any) -> bool | None:
    """Check if string or other obj is truthy."""
    if isinstance(o, str):
        if o.lower() in {"y", "yes", "t", "true", "1"}:
            return True
        elif o.lower() in {"n", "no", "f", "false", "0"}:
            return False
        else:
            return None
    elif o is None:
        return None
    else:
        return bool(o)


def method_is_from_subclass_of(cls: type[object], base_cls: type[object], method_name: str) -> bool:
    """
    Check to see whether a class's method comes from a subclass of some base class.

    This is used under the hood to see whether we would expect a patched RichCommand's help text
    methods to be compatible or incompatible with rich-click or not.
    """
    method = getattr(cls, method_name, None)
    if method is None:
        return False
    return any(getattr(c, method_name, None) == method for c in cls.__mro__ if base_cls in c.__mro__)


class CommandGroupDict(TypedDict):
    """Specification for command groups."""

    name: NotRequired[str]
    commands: NotRequired[list[str]]
    help: NotRequired[str | None]
    help_style: NotRequired[StyleType | None]
    table_styles: NotRequired[dict[str, Any] | None]
    panel_styles: NotRequired[dict[str, Any] | None]
    column_types: NotRequired[list[CommandColumnType] | None]
    inline_help_in_title: NotRequired[bool | None]
    title_style: NotRequired[StyleType | None]

    deduplicate: NotRequired[bool]


class OptionGroupDict(TypedDict):
    """Specification for option groups."""

    name: NotRequired[str]
    options: NotRequired[list[str]]
    help: NotRequired[str | None]
    help_style: NotRequired[StyleType | None]
    table_styles: NotRequired[dict[str, Any] | None]
    panel_styles: NotRequired[dict[str, Any] | None]
    column_types: NotRequired[list[OptionColumnType] | None]
    inline_help_in_title: NotRequired[bool | None]
    title_style: NotRequired[StyleType | None]

    deduplicate: NotRequired[bool]
