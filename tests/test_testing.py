import getpass
import io
from importlib.metadata import version

import click
import pytest
import rich
from rich.console import Console
from rich.prompt import Confirm, Prompt

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
    terminal_console = Console(force_terminal=True)
    monkeypatch.setattr(rich, "_console", terminal_console)

    @click.command()
    def cli() -> None:
        terminal_console.print("[bold]hi[/]")

    assert CliRunner().invoke(cli).output == "hi\n"
    assert CliRunner().invoke(cli, color=True).output == "\x1b[1mhi\x1b[0m\n"
    assert rich.get_console() is terminal_console
    assert terminal_console.is_terminal


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


@pytest.mark.skipif(int(version("click").split(".")[1]) < 2, reason="result.stderr needs click >= 8.2")
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


def test_global_console_created_by_runner_is_discarded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rich, "_console", None)

    CliRunner().invoke(click.Command("cli"))

    assert rich._console is None
