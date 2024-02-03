from typing import Any, Dict, Optional, Sequence

from typing_extensions import NotRequired, TypedDict


def truthy(o: Any) -> Optional[bool]:
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


class CommandGroupDict(TypedDict):
    """Specification for command groups."""

    name: NotRequired[str]
    commands: Sequence[str]
    table_styles: NotRequired[Dict[str, Any]]


class OptionGroupDict(TypedDict):
    """Specification for option groups."""

    name: NotRequired[str]
    options: Sequence[str]
    table_styles: NotRequired[Dict[str, Any]]
