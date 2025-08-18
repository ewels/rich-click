# fmt: off
from typing import Union

import rich.box
from rich.box import Box


HORIZONTALS_TOP: Box = Box(
    " ── \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
)

HORIZONTALS_DOUBLE_TOP: Box = Box(
    " ══ \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
)

BLANK: Box = Box(
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
    "    \n"
)

BLANK.top = ""
BLANK.top_left = ""
BLANK.top_right = "\t" * 20  # Reasonably ensure padding
BLANK.top_divider = ""

def get_box(name: Union[str, Box]) -> Box:
    """Retrieve a Rich Box by name."""
    if isinstance(name, Box):
        return name
    if name == name.upper() and name in globals():
        return globals()[name]  # type: ignore[no-any-return]
    return getattr(rich.box, name)  # type: ignore[no-any-return]
