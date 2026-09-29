import builtins
import os
import select
import subprocess
import sys
from collections.abc import Generator
from typing import Any

import pytest
from click.testing import CliRunner

import rich_click as click
import rich_click.terminal_background as tb
from rich_click.rich_click_theme import (
    COLORS,
    FORMATS,
    RichClickThemeNotFound,
    get_theme,
    parse_background_theme,
    resolve_background_theme,
)
from rich_click.rich_help_configuration import FromTheme, RichHelpConfiguration


_detect_background = tb.detect_background


@pytest.fixture(autouse=True)
def clean_background_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    monkeypatch.delenv("RICH_CLICK_BACKGROUND", raising=False)
    monkeypatch.delenv("COLORFGBG", raising=False)
    _detect_background.cache_clear()
    yield
    _detect_background.cache_clear()


@pytest.mark.parametrize(
    ("value", "expected"),
    [("dark", "dark"), ("LIGHT", "light"), (" light ", "light"), ("nope", None), ("", None)],
)
def test_env_override(monkeypatch: pytest.MonkeyPatch, value: str, expected: str | None) -> None:
    monkeypatch.setenv("RICH_CLICK_BACKGROUND", value)
    monkeypatch.setenv("COLORFGBG", "0;15")
    assert tb._from_env_override() == expected
    if expected:
        assert tb.detect_background() == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("0;15", "light"),  # black on white
        ("15;0", "dark"),  # white on black
        ("0;default;15", "light"),
        ("15;default;0", "dark"),
        ("12;8", "dark"),
        ("0;7", "light"),
        ("15;default", None),
        ("", None),
    ],
)
def test_colorfgbg(monkeypatch: pytest.MonkeyPatch, value: str, expected: str | None) -> None:
    monkeypatch.setenv("COLORFGBG", value)
    assert tb._from_colorfgbg() == expected


@pytest.mark.parametrize(
    ("reply", "expected"),
    [
        (b"\x1b]11;rgb:ffff/ffff/ffff\x1b\\", "light"),
        (b"\x1b]11;rgb:0000/0000/0000\x07", "dark"),
        (b"\x1b]11;rgb:1e1e/1e1e/2e2e\x1b\\\x1b[?62;22c", "dark"),
        (b"\x1b]11;rgb:fdfd/f6f6/e3e3\x1b\\", "light"),  # Solarized light
        (b"\x1b]11;rgb:ff/ff/ff\x07", "light"),
        (b"\x1b]11;rgba:0000/2b2b/3636/ffff\x07", "dark"),  # Solarized dark
        (b"\x1b[?62;22c", None),
        (b"", None),
    ],
)
def test_parse_osc11_reply(reply: bytes, expected: str | None) -> None:
    assert tb.parse_osc11_reply(reply) == expected


def test_no_query_without_tty() -> None:
    # Under pytest, stdin is not a terminal.
    assert tb._query_terminal() == b""
    assert tb.detect_background() is None


@pytest.mark.skipif(os.name != "posix", reason="needs a pty")
@pytest.mark.parametrize(
    ("reply", "expected"),
    [(b"\x1b]11;rgb:ffff/ffff/ffff\x1b\\", "light"), (b"\x1b]11;rgb:1e1e/1e1e/2e2e\x07", "dark"), (b"", "None")],
)
def test_query_terminal_in_pty(reply: bytes, expected: str) -> None:
    import pty

    code = "from rich_click.terminal_background import detect_background; print('RESULT', detect_background())"
    env = {k: v for k, v in os.environ.items() if k not in ("COLORFGBG", "RICH_CLICK_BACKGROUND")}
    env["TERM"] = "xterm-256color"
    pid, fd = pty.fork()
    if pid == 0:  # pragma: no cover
        os.execvpe(sys.executable, [sys.executable, "-c", code], env)

    output = b""
    answered = False
    try:
        while True:
            ready, _, _ = select.select([fd], [], [], 5)
            if not ready:
                break
            try:
                chunk = os.read(fd, 1024)
            except OSError:
                break
            if not chunk:
                break
            output += chunk
            if not answered and b"\x1b[c" in output:
                assert b"\x1b]11;?" in output
                os.write(fd, reply + b"\x1b[?62;22c")
                answered = True
    finally:
        os.waitpid(pid, 0)
    assert answered
    assert f"RESULT {expected}".encode() in output


def test_parse_background_theme() -> None:
    assert parse_background_theme("nord-modern") is None
    assert parse_background_theme("dark:nord-modern, light:solarized-modern") == {
        "dark": "nord-modern",
        "light": "solarized-modern",
    }


@pytest.mark.parametrize(
    "theme",
    ["dark:nord", "dark:nord,dark:forest", "dark:nord,blue:forest", "dark:,light:forest", "dark:nord,light"],
)
def test_parse_background_theme_invalid(theme: str) -> None:
    with pytest.raises(RichClickThemeNotFound):
        parse_background_theme(theme)
    with pytest.raises(RichClickThemeNotFound):
        get_theme(theme)


@pytest.mark.parametrize(
    ("background", "expected"),
    [("dark", "nord-modern"), ("light", "solarized-slim"), (None, "light:solarized-slim")],
)
def test_resolve_background_theme(monkeypatch: pytest.MonkeyPatch, background: str | None, expected: str) -> None:
    monkeypatch.setattr(tb, "detect_background", lambda: background)
    # When undetected, the first theme listed is used.
    theme = "light:solarized-slim,dark:nord-modern" if background is None else "dark:nord-modern,light:solarized-slim"
    expected = "solarized-slim" if background is None else expected
    assert resolve_background_theme(theme) == expected
    assert get_theme(theme).styles == (COLORS[expected.split("-")[0]] + FORMATS[expected.split("-")[1]]).styles


def test_theme_pair_resolved_only_when_rendering(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[None] = []

    def fake_detect() -> str:
        calls.append(None)
        return "light"

    monkeypatch.setattr(tb, "detect_background", fake_detect)
    cfg = RichHelpConfiguration(theme="dark:nord-modern,light:solarized-slim")
    assert calls == []
    assert isinstance(cfg.style_option, FromTheme)

    cfg.apply_theme(force_default=True)
    assert calls == [None]
    assert cfg.style_option == get_theme("solarized-slim").styles["style_option"]


def test_theme_pair_from_env_var(monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner) -> None:
    monkeypatch.setenv("RICH_CLICK_THEME", "dark:nord-modern,light:solarized-slim")
    monkeypatch.setenv("RICH_CLICK_BACKGROUND", "light")

    @click.command()
    def cli() -> None:
        pass

    res = cli_runner.invoke(cli, "--help")
    assert res.exit_code == 0
    # The 'slim' format has no panel boxes.
    assert "╭" not in res.stdout
    assert "Options" in res.stdout


def test_detection_not_imported_during_execution(monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner) -> None:
    monkeypatch.setenv("RICH_CLICK_THEME", "dark:nord-modern,light:solarized-slim")
    modules: list[str] = []
    _import = builtins.__import__

    def noisy_import(name: str, *args: Any, **kwargs: Any) -> Any:
        modules.append(name)
        return _import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", noisy_import)

    @click.command()
    @click.rich_config({"theme": "dark:nord-modern,light:solarized-slim"})
    def cli() -> None:
        print("Hello, world!")

    res = cli_runner.invoke(cli)
    assert res.exit_code == 0
    assert res.stdout == "Hello, world!\n"
    assert "rich_click.terminal_background" not in modules
    assert not any(m in ("termios", "tty", "select") for m in modules)


def test_detection_not_imported_on_startup() -> None:
    code = "import sys, rich_click; print('rich_click.terminal_background' in sys.modules)"
    res = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert res.stdout.strip() == "False"


def test_lazy_public_export() -> None:
    assert click.detect_background is tb.detect_background


def test_invalid_theme_pair_fails_early() -> None:
    with pytest.raises(RichClickThemeNotFound):
        RichHelpConfiguration(theme="dark:nord")

