# ruff: noqa: D103,E501
"""The Click API re-exported by `rich_click` resolves lazily (#353).

Importing `rich_click` used to import every re-exported Click name eagerly. Click
moves and deprecates names between minor releases, so that made a
`DeprecationWarning` fire at import time for downstreams that never touched the
deprecated name -- which broke CI for projects asserting no warnings
(litestar-org/litestar#5020).

Six primary `click.core` names stay eager; the rest resolve through the module
`__getattr__` on first access.
"""

import subprocess
import sys
from pathlib import Path

import click
import pytest

import rich_click


REPO_ROOT = Path(__file__).resolve().parents[1]
INIT = REPO_ROOT / "src" / "rich_click" / "__init__.py"

#: The primary Click API. Every rich-click subclass derives from one of these,
#: and Click is not going to move them, so they are imported eagerly.
EAGER_NAMES = ("Argument", "Command", "Context", "Group", "Option", "Parameter")


def _declared_click_reexports() -> list[str]:
    """Every `from click...` name in `__init__.py`, eager and lazy alike."""
    return [
        line.split(" as ")[-1].strip()
        for line in open(INIT, encoding="utf-8")
        if line.strip().startswith("from click.")
    ]


def test_the_parser_finds_the_reexports() -> None:
    """Guard the helper: an empty list would make the parametrized tests vacuous."""
    assert len(_declared_click_reexports()) > 40


@pytest.mark.parametrize("name", _declared_click_reexports())
def test_every_reexport_is_the_click_object(name: str) -> None:
    """Lazy resolution must not change what a name means."""
    assert getattr(rich_click, name) is getattr(click, name)


@pytest.mark.parametrize("name", EAGER_NAMES)
def test_the_primary_click_api_is_eager(name: str) -> None:
    assert name in rich_click.__dict__


@pytest.mark.parametrize("name", [n for n in _declared_click_reexports() if n not in EAGER_NAMES])
def test_the_secondary_click_api_is_lazy(name: str) -> None:
    """Not in `__dict__` means `__getattr__` is what served it."""
    assert name not in rich_click.__dict__


def test_dir_lists_the_lazy_names() -> None:
    """Module `__dir__` defaults to `__dict__`, which the lazy names are not in."""
    listing = dir(rich_click)
    assert listing == sorted(listing)
    for name in _declared_click_reexports():
        assert name in listing
    assert "RichMultiCommand" in listing


def test_importing_rich_click_raises_no_deprecation_warning() -> None:
    """The point of #353, in a fresh interpreter.

    A subprocess rather than `warnings.catch_warnings`, because the module is
    already imported by the time this file runs and the warning would have
    fired long ago.
    """
    result = subprocess.run(
        [sys.executable, "-W", "error::DeprecationWarning", "-c", "import rich_click"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_a_deprecated_name_still_warns_where_it_is_used() -> None:
    """Lazy resolution moves the warning; it must not swallow it."""
    result = subprocess.run(
        [
            sys.executable,
            "-W",
            "error::DeprecationWarning",
            "-c",
            "import rich_click; rich_click.RichMultiCommand",
        ],
        capture_output=True,
        text=True,
    )
    from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_9X

    if CLICK_IS_BEFORE_VERSION_9X:
        assert result.returncode != 0
        assert "RichMultiCommand" in result.stderr
