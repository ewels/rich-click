"""Discover help format renderers supplied by installed Python packages."""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from importlib.metadata import EntryPoint, entry_points
from typing import cast

import click


HELP_FORMAT_ENTRY_POINT_GROUP = "rich_click.help_formats"
"""Entry-point group for third-party help format renderers."""

HelpFormatRenderer = Callable[[click.Command, click.Context], str]
"""A callable that renders a command and its context as a string."""


@cache
def _help_format_plugins() -> dict[str, EntryPoint]:
    """Return installed help format entry points, indexed by normalized name."""
    plugins: dict[str, EntryPoint] = {}
    for entry_point in entry_points(group=HELP_FORMAT_ENTRY_POINT_GROUP):
        name = entry_point.name.strip().lower()
        if not name:
            continue
        existing = plugins.get(name)
        if existing is not None:
            raise RuntimeError(
                f"Multiple installed packages provide the rich-click help format {name!r}: "
                f"{existing.value!r} and {entry_point.value!r}."
            )
        plugins[name] = entry_point
    return plugins


def get_help_format_plugin_names() -> tuple[str, ...]:
    """Return the names of all help formats provided by installed plugins."""
    return tuple(_help_format_plugins())


@cache
def load_help_format_plugin(name: str) -> HelpFormatRenderer | None:
    """Load one installed help format renderer, or return ``None`` if it does not exist."""
    entry_point = _help_format_plugins().get(name.strip().lower())
    if entry_point is None:
        return None
    renderer = entry_point.load()
    if not callable(renderer):
        raise TypeError(
            f"The rich-click help format entry point {entry_point.name!r} must load a callable; "
            f"it loaded {type(renderer).__name__}."
        )
    return cast(HelpFormatRenderer, renderer)
