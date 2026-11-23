from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, Literal

import click
from click.globals import get_current_context as click_get_current_context

from rich_click.rich_help_configuration import RichHelpConfiguration
from rich_click.rich_help_formatter import RichHelpFormatter


if TYPE_CHECKING:  # pragma: no cover
    from types import TracebackType

    from rich.console import Console

    # At runtime the mixin is baseless (object) so it can be composed with either
    # click's or a fork's Context. For type-checking we give it click.Context as a
    # base so static analysis sees the inherited attributes (terminal_width, etc.).
    _ContextBase = click.Context
else:
    _ContextBase = object


class RichContextMixin(_ContextBase):
    """
    Rich help formatting for a click Context, as a mixin with no click base class.

    `RichContext` combines this mixin with `click.Context`. A click fork combines it
    with its own Context class, such as `asyncclick.Context`. Because the mixin has
    no click base class, it does not add click's synchronous methods to the fork.

    Note:
        To customize the context of a click CLI, subclass `RichContext`, not this mixin.
    """

    formatter_class: type[RichHelpFormatter] = RichHelpFormatter
    console: Console | None = None
    export_console_as: Literal["html", "svg", "text"] | None = None
    errors_in_output_format: bool = False
    help_to_stderr: bool = False

    def __init__(
        self,
        *args: Any,
        rich_console: Console | None = None,
        rich_help_config: Mapping[str, Any] | RichHelpConfiguration | None = None,
        export_console_as: Literal["html", "svg", "text"] | None = None,
        errors_in_output_format: bool | None = None,
        help_to_stderr: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Create a context. An argument that is not set takes its value from the parent context.

        Args:
            *args: Positional arguments for the click Context.
            rich_console: Rich console to print help and errors with.
            rich_help_config: How to format help and errors, as a `RichHelpConfiguration` or a dict of
                its fields. A dict changes only the fields it names.
            export_console_as: Export help as `"html"`, `"svg"` or `"text"`, not as terminal output.
            errors_in_output_format: Export errors in the `export_console_as` format too.
            help_to_stderr: Print help to stderr, not stdout.
            **kwargs: Keyword arguments for the click Context.
        """
        super().__init__(*args, **kwargs)
        parent: RichContextMixin | None = self.parent  # type: ignore[assignment]

        if help_to_stderr is None and hasattr(parent, "help_to_stderr"):
            self.help_to_stderr = parent.help_to_stderr  # type: ignore[union-attr]
        else:
            self.help_to_stderr = help_to_stderr or self.help_to_stderr

        if export_console_as is None and hasattr(parent, "export_console_as"):
            self.export_console_as = parent.export_console_as  # type: ignore[union-attr]
        else:
            self.export_console_as = export_console_as or self.export_console_as

        if errors_in_output_format is None and hasattr(parent, "errors_in_output_format"):
            self.errors_in_output_format = parent.errors_in_output_format  # type: ignore[union-attr]
        else:
            self.errors_in_output_format = errors_in_output_format or self.errors_in_output_format

        if rich_console is None and hasattr(parent, "console"):
            rich_console = parent.console  # type: ignore[union-attr]

        if rich_console is not None:
            self.console = rich_console

        if rich_help_config is None:
            if hasattr(parent, "help_config"):
                self.help_config = parent.help_config  # type: ignore[has-type,union-attr]
            else:
                self.help_config = RichHelpConfiguration.load_from_globals()
        elif isinstance(rich_help_config, Mapping):
            if hasattr(parent, "help_config"):
                if TYPE_CHECKING:  # pragma: no cover
                    assert parent is not None
                kw = parent.help_config.__dict__.copy()
                theme_fields = kw.pop("_theme_fields")
                if "theme" in rich_help_config:
                    for k in theme_fields:
                        del kw[k]
                kw.update(rich_help_config)
                self.help_config = RichHelpConfiguration(**kw)
            else:
                self.help_config = RichHelpConfiguration.load_from_globals(**rich_help_config)
        else:
            self.help_config = rich_help_config

    def make_formatter(self, error_mode: bool = False) -> RichHelpFormatter:
        """Create the Rich Help Formatter."""
        formatter = self.formatter_class(
            width=self.terminal_width,
            max_width=self.max_content_width,
            config=self.help_config,
            console=self.console,
            export_console_as=(self.export_console_as if not error_mode or self.errors_in_output_format else None),
        )
        return formatter


class RichContext(RichContextMixin, click.Context):
    """The context of a rich-click command: a click Context that formats help and errors with Rich."""

    if TYPE_CHECKING:  # pragma: no cover

        def __enter__(self) -> RichContext:
            super().__enter__()
            return self

        def __exit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            tb: TracebackType | None,
        ) -> None:
            super().__exit__(exc_type, exc_value, tb)


def get_current_context(silent: bool = False) -> RichContext | None:
    """
    Return the context of the command that runs now.

    Use it in helper functions that need the context but do not get it from the `pass_context` decorator.

    Args:
        silent: If true, return `None` when no command runs. If false, raise a `RuntimeError`.

    Returns:
        The context, or `None` if no command runs and `silent` is true.
    """
    return click_get_current_context(silent=silent)  # type: ignore[return-value]
