"""Test helpers for CLIs that use Rich for output and prompts."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from contextlib import contextmanager
from typing import IO, Any, TextIO

import click.testing
import rich
from click import termui
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
      replaced by a fresh one that follows the runner's ``color`` setting.
    """

    @contextmanager
    def isolation(
        self,
        input: str | bytes | IO[Any] | None = None,
        env: Mapping[str, str | None] | None = None,
        color: bool = False,
    ) -> Iterator[Any]:
        """Set up Click's isolation, then route Rich's console and prompts through it."""
        original_input = Console.input
        original_console = rich._console

        def runner_input(
            console: Console,
            prompt: TextType = "",
            *,
            markup: bool = True,
            emoji: bool = True,
            password: bool = False,
            stream: TextIO | None = None,
        ) -> str:
            if stream is not None:
                return original_input(console, prompt, markup=markup, emoji=emoji, password=password, stream=stream)
            if prompt:
                console.print(prompt, markup=markup, emoji=emoji, end="")
            # Inside isolation these are Click's stand-ins that read the runner's input.
            read = termui.hidden_prompt_func if password else termui.visible_prompt_func
            return read("")

        with super().isolation(input=input, env=env, color=color) as streams:
            rich._console = Console(force_terminal=color)
            Console.input = runner_input  # type: ignore[method-assign,assignment]
            try:
                yield streams
            finally:
                Console.input = original_input  # type: ignore[method-assign]
                rich._console = original_console
