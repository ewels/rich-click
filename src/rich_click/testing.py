"""Test helpers for CLIs that use Rich for output and prompts."""

from __future__ import annotations

import copy
import os
import sys
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import IO, Any, TextIO

import click.testing
import rich
from rich.console import Console, ConsoleThreadLocals
from rich.text import TextType


_RICH_INPUT = Console.input

# Unset or pinned so that Rich output does not depend on the terminal that runs the tests.
_RICH_ENV: dict[str, str | None] = {
    "COLORTERM": None,
    "FORCE_COLOR": None,
    "NO_COLOR": None,
    "TERM": None,
    "TTY_COMPATIBLE": None,
    "TTY_INTERACTIVE": None,
    "COLUMNS": "80",
    "LINES": "25",
}


class CliRunner(click.testing.CliRunner):
    """
    A drop-in replacement for `click.testing.CliRunner` that also isolates Rich.

    While a command runs:

    - Rich prompts (`rich.prompt.Prompt`, `rich.prompt.Confirm`, and `Console.input()`)
      read from the runner's `input`, including password prompts, which would otherwise call
      `getpass.getpass` and read from the terminal.
    - Rich's global console (used by `rich.print()` and prompts without an explicit console) is
      reset in place to follow the runner's `color` setting, and is not interactive.
    - Environment variables that change Rich output (`FORCE_COLOR`, `NO_COLOR`, `COLUMNS`, ...)
      are unset or pinned, unless given in `env`.
    """

    @contextmanager
    def isolation(
        self,
        input: str | bytes | IO[Any] | None = None,
        env: Mapping[str, str | None] | None = None,
        color: bool = False,
    ) -> Iterator[Any]:
        echo_stdin = self.echo_stdin

        def runner_input(
            console: Console,
            prompt: TextType = "",
            *,
            markup: bool = True,
            emoji: bool = True,
            password: bool = False,
            stream: TextIO | None = None,
        ) -> str:
            # getpass ignores `stream` for reading, so passwords always come from the runner.
            if stream is not None and not password:
                return _RICH_INPUT(console, prompt, markup=markup, emoji=emoji, stream=stream)
            if prompt:
                console.print(prompt, markup=markup, emoji=emoji, end="")
            # Read stdin directly: Click < 8.2's prompt stand-ins return "" at EOF, so Rich prompts would loop forever.
            with click.testing._pause_echo(sys.stdin.buffer if echo_stdin and password else None):  # type: ignore[arg-type]
                line = sys.stdin.readline()
            if not line:
                raise EOFError
            value = line.rstrip("\r\n")
            if password or not echo_stdin:
                console.out("" if password else value, highlight=False)
            return value

        # Created outside isolation to match what Rich would create, and kept for app code that caches it.
        global_console = rich.get_console()
        defaults = Console()
        patch_input = Console.input is _RICH_INPUT

        with super().isolation(input=input, env={**_RICH_ENV, **self.env, **(env or {})}, color=color) as streams:
            original_state = global_console.__dict__.copy()
            for name, value in original_state.items():
                if isinstance(value, list):
                    setattr(global_console, name, value.copy())
            theme_stack = copy.copy(global_console._thread_locals.theme_stack)
            theme_stack._entries = theme_stack._entries.copy()
            global_console._thread_locals = ConsoleThreadLocals(theme_stack=theme_stack)

            probe = Console(
                force_terminal=True if color else None,
                force_interactive=None if "TTY_INTERACTIVE" in os.environ else False,
            )
            for name in ("_force_terminal", "_color_system", "is_interactive", "no_color"):
                setattr(global_console, name, getattr(probe, name))
            # A size equal to a fresh console's came from the terminal or COLUMNS / LINES, not from the app.
            for name in ("_width", "_height"):
                if getattr(global_console, name) == getattr(defaults, name):
                    setattr(global_console, name, getattr(probe, name))

            if patch_input:
                Console.input = runner_input  # type: ignore[method-assign,assignment]
            try:
                yield streams
            finally:
                if patch_input:
                    Console.input = _RICH_INPUT  # type: ignore[method-assign]
                global_console.__dict__ = original_state
