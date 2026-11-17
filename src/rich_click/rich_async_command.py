"""
Rich-formatted command classes for asyncclick.

[asyncclick](https://github.com/python-trio/asyncclick) is a fork of click with async command
methods (`main`, `invoke`, `make_context` and `parse_args`). The rich-click mixins
(`RichCommandMixin`, `RichGroupMixin` and `RichContextMixin`) have no click base class, so these
classes combine them with the asyncclick classes.

Most code does not import these classes. Call `rich_click.patch.patch(module=asyncclick)` instead.
It puts these classes into the asyncclick namespace, so `@asyncclick.command` CLIs get rich-click help.

Note:
    This module needs asyncclick: install `rich-click[async]`. The rest of rich-click never imports it.
"""

from __future__ import annotations

import sys
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from gettext import gettext
from typing import Any, cast

import asyncclick

from rich_click._click_types_cache import register_click_impl
from rich_click.rich_command import RichCommandMixin, RichGroupMixin
from rich_click.rich_context import RichContextMixin


# Register asyncclick's parallel type tree so rich-click's renderer detects its
# Argument/Option/Group/etc. This is idempotent and safe to run on import.
register_click_impl(asyncclick)


class RichAsyncContext(RichContextMixin, asyncclick.Context):
    """An asyncclick Context that formats help and errors with Rich."""


class RichAsyncCommand(RichCommandMixin, asyncclick.Command):
    """
    Richly formatted asyncclick Command.

    Combines rich-click's :class:`RichCommandMixin` (help/error formatting) with
    asyncclick's asynchronous :class:`asyncclick.Command` (async ``main``/``invoke``).
    """

    context_class: type[RichAsyncContext] = RichAsyncContext

    def _make_help_option(self, *help_option_names: str) -> asyncclick.Option:
        async def show_help(ctx: asyncclick.Context, param: asyncclick.Parameter, value: bool) -> None:
            if value and not ctx.resilient_parsing:
                if getattr(ctx, "help_to_stderr", False):
                    print(ctx.get_help(), file=sys.stderr)
                else:
                    print(ctx.get_help())
                await ctx.aexit()

        asyncclick.option(
            *help_option_names,
            is_flag=True,
            expose_value=False,
            is_eager=True,
            help=gettext("Show this message and exit."),
            callback=show_help,
        )(self)
        return cast(asyncclick.Option, self.params.pop())

    async def to_info_dict(self, ctx: asyncclick.Context) -> dict[str, Any]:
        info: dict[str, Any] = await super().to_info_dict(ctx)
        info["panels"] = [p.to_info_dict(ctx) for p in self.panels]
        info["aliases"] = list(self.aliases) if self.aliases is not None else None
        return info

    _rich_standalone: bool = False

    async def main(
        self,
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = True,
        **extra: Any,
    ) -> Any:
        self._rich_standalone = standalone_mode
        try:
            return await super().main(args, prog_name, complete_var, standalone_mode, **extra)
        finally:
            self._rich_standalone = False

    # asyncclick's standalone main prints errors in plain text. Errors surface through the
    # top-level make_context/invoke first, so render them there and hand main an Exit.
    async def make_context(self, *args: Any, **kwargs: Any) -> Any:
        with self._render_errors():
            return await super().make_context(*args, **kwargs)

    async def invoke(self, ctx: asyncclick.Context) -> Any:
        with self._render_errors():
            return await super().invoke(ctx)

    @contextmanager
    def _render_errors(self) -> Iterator[None]:
        if not self._rich_standalone:
            yield
            return
        try:
            yield
        except asyncclick.exceptions.NoArgsIsHelpError as e:
            print(e.message)
            raise asyncclick.exceptions.Exit(e.exit_code) from None
        except asyncclick.ClickException as e:
            self._print_error(e)
            raise asyncclick.exceptions.Exit(e.exit_code) from None
        except (asyncclick.Abort, EOFError, KeyboardInterrupt) as e:
            if not isinstance(e, asyncclick.Abort):
                asyncclick.echo(file=sys.stderr)
            self._print_abort()
            raise asyncclick.exceptions.Exit(1) from None


class RichAsyncGroup(RichGroupMixin, RichAsyncCommand, asyncclick.Group):
    """
    Richly formatted asyncclick Group.

    Subcommands and subgroups created from this group inherit the async rich classes
    via ``command_class``/``group_class``, so the whole command tree renders richly.
    """

    context_class: type[RichAsyncContext] = RichAsyncContext
    command_class: type[RichAsyncCommand] | None = RichAsyncCommand
    group_class: Any | None = type


class RichAsyncCommandCollection(asyncclick.CommandCollection, RichAsyncGroup):
    """Richly formatted asyncclick CommandCollection."""


__all__ = [
    "RichAsyncCommand",
    "RichAsyncCommandCollection",
    "RichAsyncContext",
    "RichAsyncGroup",
]
