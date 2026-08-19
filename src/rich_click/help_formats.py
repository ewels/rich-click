"""Discover help format renderers supplied by installed Python packages."""

from __future__ import annotations

from collections.abc import Callable
from functools import cache
from importlib.metadata import EntryPoint, entry_points
from typing import Literal, cast

import click


HELP_FORMAT_ENTRY_POINT_GROUP = "rich_click.help_formats"
"""Entry-point group for third-party help format renderers."""

DEFAULT_HELP_FORMATS = ("compact", "markdown", "json")
"""Machine-readable formats enabled by default, in display order."""

HelpFormatRenderer = Callable[[click.Command, click.Context], str]
"""A callable that renders a command and its context as a string."""


def _normalize_format_name(name: str) -> str:
    """Return one format name normalized for lookup and comparison (stripped, lowercased)."""
    return name.strip().lower()


def normalize_help_formats(value: list[str] | tuple[str, ...] | Literal[False]) -> tuple[str, ...]:
    """Return the enabled format names in normalized, duplicate-free order."""
    if value is False:
        return ()
    if not isinstance(value, (list, tuple)):
        raise TypeError("help_formats must be a list of format names or False.")

    names: list[str] = []
    for value_name in value:
        if not isinstance(value_name, str):
            raise TypeError("Each help_formats item must be a string.")
        name = _normalize_format_name(value_name)
        if name and name not in names:
            names.append(name)
    return tuple(names)


@cache
def _help_format_plugins() -> dict[str, tuple[EntryPoint, ...]]:
    """Return installed help format entry points, grouped by normalized name."""
    plugins: dict[str, list[EntryPoint]] = {}
    for entry_point in entry_points(group=HELP_FORMAT_ENTRY_POINT_GROUP):
        name = _normalize_format_name(entry_point.name)
        if not name:
            continue
        plugins.setdefault(name, []).append(entry_point)
    return {name: tuple(providers) for name, providers in plugins.items()}


@cache
def get_help_format_plugin_names() -> tuple[str, ...]:
    """Return the names of all help formats provided by installed plugins, alphabetically sorted."""
    return tuple(sorted(_help_format_plugins()))


@cache
def load_help_format_plugin(name: str) -> HelpFormatRenderer | None:
    """Load one installed help format renderer, or return ``None`` if it does not exist."""
    normalized = _normalize_format_name(name)
    providers = _help_format_plugins().get(normalized)
    if providers is None:
        return None
    if len(providers) > 1:
        values = ", ".join(repr(provider.value) for provider in providers)
        raise RuntimeError(f"Multiple installed packages provide the rich-click help format {normalized!r}: {values}.")
    entry_point = providers[0]
    renderer = entry_point.load()
    if not callable(renderer):
        raise TypeError(
            f"The rich-click help format entry point {entry_point.name!r} must load a callable; "
            f"it loaded {type(renderer).__name__}."
        )
    return cast(HelpFormatRenderer, renderer)
