from __future__ import annotations

import json
from collections.abc import Iterator
from importlib.metadata import EntryPoint
from typing import Any

import pytest
from click.testing import CliRunner

import rich_click.help_formats as help_formats
from rich_click import RichHelpConfiguration, command, rich_config


def render_html(command: Any, ctx: Any) -> str:
    """Test renderer loaded through a real EntryPoint object."""
    return f"<h1>{command.name}</h1>"


@pytest.fixture(autouse=True)
def clear_plugin_caches() -> Iterator[None]:
    help_formats._help_format_plugins.cache_clear()
    help_formats.get_help_format_plugin_names.cache_clear()
    help_formats.load_help_format_plugin.cache_clear()
    yield
    help_formats._help_format_plugins.cache_clear()
    help_formats.get_help_format_plugin_names.cache_clear()
    help_formats.load_help_format_plugin.cache_clear()


def test_installed_help_format_is_discovered_and_dispatched(monkeypatch: pytest.MonkeyPatch) -> None:
    plugin = EntryPoint(
        name="html",
        value="tests.test_help_format_plugins:render_html",
        group=help_formats.HELP_FORMAT_ENTRY_POINT_GROUP,
    )
    monkeypatch.setattr(help_formats, "entry_points", lambda **kwargs: [plugin])

    # No `help_formats` override: a CLI author who never heard of this plugin still exposes it, because
    # rich-click appends installed plugin formats automatically.
    @command()
    def cli() -> None:
        """A command."""

    runner = CliRunner()
    assert runner.invoke(cli, ["--help", "html"]).output.strip() == "<h1>cli</h1>"
    schema = json.loads(runner.invoke(cli, ["--help", "json"]).output)
    help_param = next(param for param in schema["params"] if param["name"] == "help")
    assert help_param["choices"] == ["compact", "markdown", "json", "html"]
    assert "[compact|markdown|json|html]" in runner.invoke(cli, ["--help"], terminal_width=120).output


def test_empty_help_formats_still_exposes_plugins(monkeypatch: pytest.MonkeyPatch) -> None:
    plugin = EntryPoint(
        name="html",
        value="tests.test_help_format_plugins:render_html",
        group=help_formats.HELP_FORMAT_ENTRY_POINT_GROUP,
    )
    monkeypatch.setattr(help_formats, "entry_points", lambda **kwargs: [plugin])

    # `[]` turns off the built-in formats but is not a full opt-out: installed plugins still apply.
    @command()
    @rich_config(help_config=RichHelpConfiguration(help_formats=[]))
    def cli() -> None:
        """A command."""

    runner = CliRunner()
    assert runner.invoke(cli, ["--help", "html"]).output.strip() == "<h1>cli</h1>"
    assert "[html]" in runner.invoke(cli, ["--help"], terminal_width=120).output


def test_help_formats_false_disables_plugins_too(monkeypatch: pytest.MonkeyPatch) -> None:
    plugin = EntryPoint(
        name="html",
        value="tests.test_help_format_plugins:render_html",
        group=help_formats.HELP_FORMAT_ENTRY_POINT_GROUP,
    )
    monkeypatch.setattr(help_formats, "entry_points", lambda **kwargs: [plugin])

    # `False` is the real full opt-out: it restores the legacy Boolean `--help` flag, plugins included.
    @command()
    @rich_config(help_config=RichHelpConfiguration(help_formats=False))
    def cli() -> None:
        """A command."""

    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert "html" not in result.output
    assert runner.invoke(cli, ["--help", "html"]).output.lstrip().startswith("Usage:")


def test_plugin_renderer_loads_only_when_selected(monkeypatch: pytest.MonkeyPatch) -> None:
    class Plugin:
        name = "html"
        value = "example:render"

        def load(self) -> Any:
            raise AssertionError("The renderer loaded during metadata discovery")

    monkeypatch.setattr(help_formats, "entry_points", lambda **kwargs: [Plugin()])
    assert help_formats.get_help_format_plugin_names() == ("html",)


def test_duplicate_plugin_names_only_break_the_conflicting_format(monkeypatch: pytest.MonkeyPatch) -> None:
    plugins = [
        EntryPoint(name="html", value="package_a:render", group=help_formats.HELP_FORMAT_ENTRY_POINT_GROUP),
        EntryPoint(name="HTML", value="package_b:render", group=help_formats.HELP_FORMAT_ENTRY_POINT_GROUP),
    ]
    monkeypatch.setattr(help_formats, "entry_points", lambda **kwargs: plugins)

    @command()
    @rich_config(help_config=RichHelpConfiguration(help_formats=["compact", "markdown", "json", "html"]))
    def cli() -> None:
        """A command."""

    runner = CliRunner()
    assert help_formats.get_help_format_plugin_names() == ("html",)
    assert runner.invoke(cli, ["--help"]).exit_code == 0
    assert runner.invoke(cli, ["--help", "json"]).exit_code == 0
    result = runner.invoke(cli, ["--help", "html"])
    assert result.exit_code == 1
    assert isinstance(result.exception, RuntimeError)
    assert "Multiple installed packages" in str(result.exception)
    assert "package_a" in str(result.exception)
    assert "package_b" in str(result.exception)
