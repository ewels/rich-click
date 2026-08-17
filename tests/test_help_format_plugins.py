from __future__ import annotations

import json
from collections.abc import Iterator
from importlib.metadata import EntryPoint
from typing import Any

import pytest
from click.testing import CliRunner

import rich_click.help_formats as help_formats
from rich_click import command


def render_html(command: Any, ctx: Any) -> str:
    """Test renderer loaded through a real EntryPoint object."""
    return f"<h1>{command.name}</h1>"


@pytest.fixture(autouse=True)
def clear_plugin_caches() -> Iterator[None]:
    help_formats._help_format_plugins.cache_clear()
    help_formats.load_help_format_plugin.cache_clear()
    yield
    help_formats._help_format_plugins.cache_clear()
    help_formats.load_help_format_plugin.cache_clear()


def test_installed_help_format_is_discovered_and_dispatched(monkeypatch: pytest.MonkeyPatch) -> None:
    plugin = EntryPoint(
        name="html",
        value="tests.test_help_format_plugins:render_html",
        group=help_formats.HELP_FORMAT_ENTRY_POINT_GROUP,
    )
    monkeypatch.setattr(help_formats, "entry_points", lambda **kwargs: [plugin])

    @command()
    def cli() -> None:
        """A command."""

    runner = CliRunner()
    assert runner.invoke(cli, ["--help", "html"]).output.strip() == "<h1>cli</h1>"
    schema = json.loads(runner.invoke(cli, ["--help", "json"]).output)
    help_param = next(param for param in schema["params"] if param["name"] == "help")
    assert help_param["choices"] == ["markdown", "json", "compact", "html"]


def test_plugin_renderer_loads_only_when_selected(monkeypatch: pytest.MonkeyPatch) -> None:
    class Plugin:
        name = "html"
        value = "example:render"

        def load(self) -> Any:
            raise AssertionError("The renderer loaded during metadata discovery")

    monkeypatch.setattr(help_formats, "entry_points", lambda **kwargs: [Plugin()])
    assert help_formats.get_help_format_plugin_names() == ("html",)


def test_duplicate_plugin_names_raise_a_clear_error(monkeypatch: pytest.MonkeyPatch) -> None:
    plugins = [
        EntryPoint(name="html", value="package_a:render", group=help_formats.HELP_FORMAT_ENTRY_POINT_GROUP),
        EntryPoint(name="HTML", value="package_b:render", group=help_formats.HELP_FORMAT_ENTRY_POINT_GROUP),
    ]
    monkeypatch.setattr(help_formats, "entry_points", lambda **kwargs: plugins)

    with pytest.raises(RuntimeError, match="Multiple installed packages.*'html'.*package_a.*package_b"):
        help_formats.get_help_format_plugin_names()
