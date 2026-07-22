from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Mapping, Optional, Type, Union

import click
from click.core import augment_usage_errors
from click.globals import get_current_context as click_get_current_context

from rich_click.rich_help_configuration import RichHelpConfiguration
from rich_click.rich_help_formatter import RichHelpFormatter


if TYPE_CHECKING:  # pragma: no cover
    from types import TracebackType

    from rich.console import Console


def _click_base_command_type() -> Type["click.Command"]:
    """
    Return the genuine ``click.Command`` class.

    ``rich_click.patch.patch()`` rebinds ``click.Command`` /
    ``click.core.Command`` to a rich-click subclass. Click's own
    ``Context.forward`` / ``Context.invoke`` resolve the bare name ``Command``
    from ``click.core`` at call time and use it in an ``isinstance`` guard, so
    after patching that guard is narrowed to the subclass and rejects genuine
    Click commands that are not that exact subclass (e.g. ``RichCommand``
    instances or commands defined before ``patch()`` ran). Walk the MRO so we
    always recover the real base class even when ``click.Command`` is patched.
    """
    for klass in click.Command.__mro__:
        if klass.__module__ == "click.core" and klass.__name__ == "Command":
            return klass
    return click.Command


class RichContext(click.Context):
    """Click Context class endowed with Rich superpowers."""

    formatter_class: Type[RichHelpFormatter] = RichHelpFormatter
    console: Optional["Console"] = None
    export_console_as: Optional[Literal["html", "svg", "text"]] = None
    errors_in_output_format: bool = False
    help_to_stderr: bool = False

    def __init__(
        self,
        *args: Any,
        rich_console: Optional["Console"] = None,
        rich_help_config: Optional[Union[Mapping[str, Any], RichHelpConfiguration]] = None,
        export_console_as: Optional[Literal["html", "svg", "text"]] = None,
        errors_in_output_format: Optional[bool] = None,
        help_to_stderr: Optional[bool] = None,
        **kwargs: Any,
    ) -> None:
        """
        Create Rich Context instance.

        Args:
        ----
            *args: Args that get passed to click.Context.
            rich_console: Rich Console. Defaults to None.
            rich_help_config: Rich help configuration.  Defaults to None.
            export_console_as: Arg is passed to RichHelpFormatter().
            errors_in_output_format: Arg is passed to RichHelpFormatter().
            help_to_stderr: If set, help is printed to stderr.
            **kwargs: Kwargs that get passed to click.Context.

        """
        super().__init__(*args, **kwargs)
        parent: Optional[RichContext] = kwargs.pop("parent", None)

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

    def forward(self, __cmd: "click.Command", *args: Any, **kwargs: Any) -> Any:
        """
        Forward to another command, tolerant of ``patch()``.

        Mirrors ``click.Context.forward`` but validates against the genuine
        ``click.Command`` base class so forwarding keeps working after
        ``rich_click.patch.patch()`` rebinds ``click.Command`` to a subclass.
        """
        if not isinstance(__cmd, _click_base_command_type()):
            raise TypeError("Callback is not a command.")

        for param in self.params:
            if param not in kwargs:
                kwargs[param] = self.params[param]

        return self.invoke(__cmd, *args, **kwargs)

    def invoke(self, __callback: Any, *args: Any, **kwargs: Any) -> Any:
        """
        Invoke a command/callback, tolerant of ``patch()``.

        ``click.Context.invoke`` decides whether its first argument is a command
        via ``isinstance(arg, click.Command)``. After ``patch()`` narrows
        ``click.Command`` to a subclass, genuine Click commands that are not that
        exact subclass fall through to the raw-callback branch and get called as
        ``cmd(**params)``, which is wrong. Detect that case and run Click's
        command dispatch against the real base class; delegate everything else
        unchanged.
        """
        base_command = _click_base_command_type()
        if isinstance(__callback, base_command) and not isinstance(__callback, click.Command):
            other_cmd = __callback
            if other_cmd.callback is None:
                raise TypeError("The given command does not have a callback that can be invoked.")
            callback = other_cmd.callback

            ctx = self._make_sub_context(other_cmd)

            for param in other_cmd.params:
                if param.name not in kwargs and param.expose_value:
                    kwargs[param.name] = param.type_cast_value(ctx, param.get_default(ctx))

            # Track all kwargs as params, so that forward() will pass
            # them on in subsequent calls.
            ctx.params.update(kwargs)

            with augment_usage_errors(self):
                with ctx:
                    return callback(*args, **kwargs)

        return super().invoke(__callback, *args, **kwargs)

    if TYPE_CHECKING:  # pragma: no cover

        def __enter__(self) -> "RichContext":
            return super().__enter__()  # type: ignore[return-value]

        def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            tb: Optional[TracebackType],
        ) -> None:
            super().__exit__(exc_type, exc_value, tb)


def get_current_context(silent: bool = False) -> Optional[RichContext]:
    """
    Return the current click context.  This can be used as a way to
    access the current context object from anywhere.  This is a more implicit
    alternative to the :func:`pass_context` decorator.  This function is
    primarily useful for helpers such as :func:`echo` which might be
    interested in changing its behavior based on the current context.

    To push the current context, :meth:`Context.scope` can be used.

    .. versionadded:: 5.0

    :param silent: if set to `True` the return value is `None` if no context
                   is available.  The default behavior is to raise a
                   :exc:`RuntimeError`.
    """
    return click_get_current_context(silent=silent)  # type: ignore[return-value]
