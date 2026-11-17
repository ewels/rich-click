import getpass
import io

import click
import pytest
import rich
from rich.console import Console
from rich.errors import MissingStyle
from rich.prompt import Confirm, Prompt
from rich.theme import Theme

from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_82
from rich_click.testing import CliRunner


@click.command()
def greet() -> None:
    name = Prompt.ask("Name")
    sure = Confirm.ask("Sure?", console=Console())
    secret = Prompt.ask("Password", password=True)
    rich.print(f"[bold]Hello {name}[/] {sure} {secret}")


def test_rich_prompts_read_runner_input(monkeypatch: pytest.MonkeyPatch) -> None:
    def no_getpass(*args: object, **kwargs: object) -> str:
        raise AssertionError("getpass reads the terminal, not the runner input")

    monkeypatch.setattr(getpass, "getpass", no_getpass)
    original_input = Console.input

    result = CliRunner().invoke(greet, input="Jane\ny\nhunter2\n")

    assert result.exception is None
    assert result.output == "Name: Jane\nSure? [y/n]: y\nPassword: \nHello Jane True hunter2\n"
    assert Console.input is original_input


def test_global_console_follows_runner_color(monkeypatch: pytest.MonkeyPatch) -> None:
    # A global console first created in a real terminal keeps emitting ANSI codes.
    monkeypatch.setenv("NO_COLOR", "1")
    monkeypatch.setenv("COLORTERM", "truecolor")
    terminal_console = Console(force_terminal=True)
    monkeypatch.setattr(rich, "_console", terminal_console)

    @click.command()
    def cli() -> None:
        terminal_console.print("[#ff8800]hi[/]")

    assert CliRunner().invoke(cli).output == "hi\n"
    assert CliRunner().invoke(cli, color=True).output == "\x1b[91mhi\x1b[0m\n"
    assert CliRunner().invoke(cli, color=True, env={"NO_COLOR": "1"}).output == "hi\n"
    assert rich.get_console() is terminal_console
    assert terminal_console.is_terminal


def test_outer_environment_does_not_leak(monkeypatch: pytest.MonkeyPatch) -> None:
    for name, value in {"FORCE_COLOR": "1", "TTY_COMPATIBLE": "1", "COLUMNS": "200"}.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setattr(rich, "_console", None)

    @click.command()
    def cli() -> None:
        rich.print(f"[bold]{rich.get_console().is_interactive}[/] " + "word " * 20)

    lines = CliRunner().invoke(cli).output.splitlines()

    assert lines[0].startswith("False word")
    assert max(map(len, lines)) <= 80


def test_password_is_not_echoed_from_stdin(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(getpass, "getpass", lambda *args, **kwargs: "from terminal")

    @click.command()
    def cli() -> None:
        Prompt.ask("Name")
        Prompt.ask("Password", password=True)

    result = CliRunner(echo_stdin=True).invoke(cli, input="Jane\nhunter2\n")

    assert result.output == "Name: Jane\nPassword: \n"


def test_existing_console_input_patch_is_kept(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Console, "input", lambda *args, **kwargs: "y")

    @click.command()
    def cli() -> None:
        click.echo(Confirm.ask("Sure?"))

    assert CliRunner().invoke(cli).output == "True\n"


def test_prompt_aborts_when_input_runs_out() -> None:
    @click.command()
    def cli() -> None:
        Confirm.ask("Sure?")

    result = CliRunner().invoke(cli, input="")

    assert result.exit_code == 1
    assert "Aborted" in result.output


def test_password_prompt_with_stream_reads_runner_input(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(getpass, "getpass", lambda *args, **kwargs: "from terminal")

    @click.command()
    def cli() -> None:
        click.echo(Prompt.ask("Password", password=True, stream=io.StringIO()))

    assert CliRunner().invoke(cli, input="hunter2\n").output == "Password: \nhunter2\n"


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_82, reason="result.stderr needs click >= 8.2")
def test_prompt_echo_goes_to_console_stream() -> None:
    @click.command()
    def cli() -> None:
        Prompt.ask("Name", console=Console(stderr=True))

    result = CliRunner().invoke(cli, input="Jane\n")

    assert result.stdout == ""
    assert result.stderr == "Name: Jane\n"


def test_global_console_keeps_app_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rich, "_console", Console(width=5))

    @click.command()
    def cli() -> None:
        rich.print("hello world")

    assert CliRunner().invoke(cli).output == "hello\nworld\n"


def test_global_console_honours_force_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rich, "_console", Console())

    @click.command()
    def cli() -> None:
        rich.print("[bold]hi[/]")

    assert CliRunner().invoke(cli, env={"FORCE_COLOR": "1"}).output == "\x1b[1mhi\x1b[0m\n"


def test_cached_global_console_follows_later_invocations(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rich, "_console", None)
    cached: list[Console] = []

    @click.command()
    def cli() -> None:
        if not cached:
            cached.append(rich.get_console())
        cached[0].print("[bold]hi[/]")

    assert CliRunner().invoke(cli, color=True).output == "\x1b[1mhi\x1b[0m\n"
    assert CliRunner().invoke(cli, color=True).output == "\x1b[1mhi\x1b[0m\n"
    assert rich.get_console() is cached[0]


def test_changes_to_global_console_are_undone(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rich, "_console", Console())

    @click.command()
    def cli() -> None:
        rich.get_console().push_theme(Theme({"warn": "red"}))

    CliRunner().invoke(cli)

    with pytest.raises(MissingStyle):
        rich.get_console().get_style("warn")
