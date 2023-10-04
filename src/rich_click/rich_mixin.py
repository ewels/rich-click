import errno
import os
import sys
from functools import wraps
from typing import Any, cast, ClassVar, Optional, Sequence, TextIO, Type

import click
from click.utils import _detect_program_name, _expand_args, PacifyFlushWrapper

from rich_click.rich_click import rich_abort_error, rich_format_error, rich_format_help
from rich_click.rich_context import RichContext
from rich_click.rich_help_formatter import RichHelpFormatter


class RichMixin(click.BaseCommand):
    """Rich formatting mixin for click objects."""

    context_class: ClassVar[Type[RichContext]] = RichContext
    _formatter: Optional[RichHelpFormatter] = None

    @property
    def console(self):
        """Rich Console.

        This is a separate instance from the help formatter that allows full control of the
        console configuration.

        See `rich_config` decorator for how to apply the settings.
        """
        return self.context_settings.get("rich_console")

    @property
    def help_config(self):
        """Rich Help Configuration."""
        return self.context_settings.get("rich_help_config")

    @property
    def formatter(self) -> RichHelpFormatter:
        """Rich Help Formatter.

        This is separate instance from the formatter used to display help,
        but is created from the same `RichHelpConfiguration`. Currently only used
        for error reporting.
        """
        if self._formatter is None:
            self._formatter = RichHelpFormatter(config=self.help_config)
        return self._formatter

    @wraps(click.BaseCommand.main)
    def main(
        self,
        args: Optional[Sequence[str]] = None,
        prog_name: Optional[str] = None,
        complete_var: Optional[str] = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: Any,
    ) -> Any:
        # It's not feasible to use super().main() in this context and retain exact parity in behavior.
        # The reason why is explained in a comment in click's source code in the "except Exit as e" block.

        if args is None:
            args = sys.argv[1:]

            if os.name == "nt" and windows_expand_args:
                args = _expand_args(args)
        else:
            args = list(args)

        if prog_name is None:
            prog_name = _detect_program_name()

        # Process shell completion requests and exit early.
        self._main_shell_completion(extra, prog_name, complete_var)

        try:
            try:
                with self.make_context(prog_name, args, **extra) as ctx:
                    rv = self.invoke(ctx)
                    if not standalone_mode:
                        return rv
                    # it's not safe to `ctx.exit(rv)` here!
                    # note that `rv` may actually contain data like "1" which
                    # has obvious effects
                    # more subtle case: `rv=[None, None]` can come out of
                    # chained commands which all returned `None` -- so it's not
                    # even always obvious that `rv` indicates success/failure
                    # by its truthiness/falsiness
                    ctx.exit()
            except (EOFError, KeyboardInterrupt):
                click.echo(file=sys.stderr)
                raise click.exceptions.Abort() from None
            except click.exceptions.ClickException as e:
                rich_format_error(e, self.formatter)
                if not standalone_mode:
                    raise
                sys.stderr.write(self.formatter.getvalue())
                sys.exit(e.exit_code)
            except OSError as e:
                if e.errno == errno.EPIPE:
                    sys.stdout = cast(TextIO, PacifyFlushWrapper(sys.stdout))
                    sys.stderr = cast(TextIO, PacifyFlushWrapper(sys.stderr))
                    sys.exit(1)
                else:
                    raise
        except click.exceptions.Exit as e:
            if standalone_mode:
                sys.exit(e.exit_code)
            else:
                return e.exit_code
        except click.exceptions.Abort:
            rich_abort_error(self.formatter)
            if not standalone_mode:
                raise
            sys.stderr.write(self.formatter.getvalue())
            sys.exit(1)

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter):
        rich_format_help(self, ctx, formatter)
