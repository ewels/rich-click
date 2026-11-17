import getpass

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
