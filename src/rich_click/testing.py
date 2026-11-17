"""Test helpers for CLIs that use Rich for output and prompts."""

from __future__ import annotations

import sys
from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import IO, Any, TextIO

import click.testing
import rich
from rich.console import Console
from rich.text import TextType


class CliRunner(click.testing.CliRunner):
    """
    A drop-in replacement for :class:`click.testing.CliRunner` that also isolates Rich.

    While a command runs:

    - Rich prompts (:class:`rich.prompt.Prompt`, :class:`rich.prompt.Confirm`, and ``Console.input()``)
      read from the runner's ``input``, including password prompts, which would otherwise call
      :func:`getpass.getpass` and read from the terminal.
    - Rich's global console (used by ``rich.print()`` and prompts without an explicit console) is
      reset in place to follow the runner's ``color`` setting.
    """

    @contextmanager
    def isolation(
        self,
        input: str | bytes | IO[Any] | None = None,
        env: Mapping[str, str | None] | None = None,
        color: bool = False,
    ) -> Iterator[Any]:
        original_input = Console.input
        echo_stdin = self.echo_stdin

        def runner_input(
            console: Console,
            prompt: TextType = "",
            *,
            markup: bool = True,
            emoji: bool = True,
            password: bool = False,
            stream: TextIO | None = None,
            **kwargs: Any,
        ) -> str:
            # getpass ignores `stream` for reading, so passwords always come from the runner.
            if stream is not None and not password:
                return original_input(console, prompt, markup=markup, emoji=emoji, stream=stream, **kwargs)
            if prompt:
                console.print(prompt, markup=markup, emoji=emoji, end="")
            # Read stdin directly: Click < 8.2's prompt stand-ins return "" at EOF, so Rich prompts would loop forever.
            line = sys.stdin.readline()
            if not line:
                raise EOFError
            value = line.rstrip("\r\n")
            if not echo_stdin:
                console.out("" if password else value, highlight=False)
            return value

        with super().isolation(input=input, env=env, color=color) as streams:
            had_console = rich._console is not None
            global_console = rich.get_console()
            original_state = global_console.__dict__.copy()
            # A fresh Console applies Rich's own FORCE_COLOR / TTY checks against the isolated env and streams.
            probe = Console(force_terminal=True if color else None)
            global_console._force_terminal = probe._force_terminal
            global_console._color_system = probe._color_system
            Console.input = runner_input  # type: ignore[method-assign,assignment]
            try:
                yield streams
            finally:
                Console.input = original_input  # type: ignore[method-assign]
                global_console.__dict__ = original_state
                if not had_console:
                    rich._console = None
