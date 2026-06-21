"""
Rich-formatted command classes for asyncclick.

`asyncclick <https://github.com/python-trio/asyncclick>`_ is a fork of click whose
command machinery (``main``/``invoke``/``make_context``/``parse_args``) is asynchronous.
rich-click's formatting behavior lives in baseless mixins (:class:`RichCommandMixin`,
:class:`RichGroupMixin`, :class:`RichContextMixin`), so it composes with asyncclick's
async bases just as it does with click's synchronous ones.

This module is only importable when ``asyncclick`` is installed (``pip install
rich-click[async]``). rich-click's core never imports it, so the dependency stays
optional. Most users do not import these classes directly; instead they call
:func:`rich_click.patch.patch` with ``module=asyncclick`` (see that function), which
installs these classes into the asyncclick namespace so plain ``@asyncclick.command``
CLIs render richly with no further changes.
"""

from __future__ import annotations

import errno
import os
import sys
from typing import Any, Dict, Optional, Sequence, Type

import asyncclick

from rich_click._click_types_cache import register_click_impl
from rich_click.rich_command import RichCommandMixin, RichGroupMixin
from rich_click.rich_context import RichContextMixin


# Register asyncclick's parallel type tree so rich-click's renderer detects its
# Argument/Option/Group/etc. This is idempotent and safe to run on import.
register_click_impl(asyncclick)


class RichAsyncContext(RichContextMixin, asyncclick.Context):
    """asyncclick Context endowed with rich-click's Rich help formatting."""


class RichAsyncCommand(RichCommandMixin, asyncclick.Command):
    """
    Richly formatted asyncclick Command.

    Combines rich-click's :class:`RichCommandMixin` (help/error formatting) with
    asyncclick's asynchronous :class:`asyncclick.Command` (async ``main``/``invoke``).
    """

    context_class: Type[RichAsyncContext] = RichAsyncContext

    async def to_info_dict(self, ctx: asyncclick.Context) -> Dict[str, Any]:
        info: Dict[str, Any] = await super().to_info_dict(ctx)
        info["panels"] = [p.to_info_dict(ctx) for p in self.panels]
        info["aliases"] = list(self.aliases) if self.aliases is not None else None
        return info

    async def main(
        self,
        args: Optional[Sequence[str]] = None,
        prog_name: Optional[str] = None,
        complete_var: Optional[str] = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: Any,
    ) -> Any:
        # Async counterpart of RichCommand.main. It mirrors asyncclick.Command.main
        # (awaiting make_context/invoke/aexit) but renders ClickException and Abort
        # through rich-click's formatter instead of asyncclick's plain output.
        if args is None:
            args = sys.argv[1:]
            if os.name == "nt" and windows_expand_args:
                args = asyncclick.utils._expand_args(args)
        else:
            args = list(args)

        if prog_name is None:
            prog_name = asyncclick.utils._detect_program_name()

        await self._main_shell_completion(extra, prog_name, complete_var)

        try:
            try:
                async with await self.make_context(prog_name, args, **extra) as ctx:
                    rv = await self.invoke(ctx)
                    if not standalone_mode:
                        return rv
                    await ctx.aexit()
            except (EOFError, KeyboardInterrupt) as e:
                asyncclick.echo(file=sys.stderr)
                raise asyncclick.exceptions.Abort() from e
            except asyncclick.exceptions.ClickException as e:
                if isinstance(e, asyncclick.exceptions.NoArgsIsHelpError):
                    print(e.format_message())
                    sys.exit(e.exit_code)
                if not standalone_mode:
                    raise
                formatter = self._error_formatter()
                formatter.write_error(e)
                print(formatter.getvalue(), file=sys.stderr, end="")
                sys.exit(e.exit_code)
            except OSError as e:
                if e.errno == errno.EPIPE:
                    sys.stdout = asyncclick.utils.PacifyFlushWrapper(sys.stdout)
                    sys.stderr = asyncclick.utils.PacifyFlushWrapper(sys.stderr)
                    sys.exit(1)
                raise
        except asyncclick.exceptions.Exit as e:
            if standalone_mode:
                sys.exit(e.exit_code)
            return e.exit_code
        except asyncclick.exceptions.Abort:
            if not standalone_mode:
                raise
            try:
                formatter = self._error_formatter()
            except Exception:
                asyncclick.echo("Aborted!", file=sys.stderr)
            else:
                formatter.write_abort()
                print(formatter.getvalue(), file=sys.stderr, end="")
            finally:
                sys.exit(1)


class RichAsyncGroup(RichGroupMixin, RichAsyncCommand, asyncclick.Group):
    """
    Richly formatted asyncclick Group.

    Subcommands and subgroups created from this group inherit the async rich classes
    via ``command_class``/``group_class``, so the whole command tree renders richly.
    """

    context_class: Type[RichAsyncContext] = RichAsyncContext
    command_class: Optional[Type[RichAsyncCommand]] = RichAsyncCommand
    group_class: Optional[Any] = None


# Self-reference must be set after the class body so subgroups reuse the async group.
RichAsyncGroup.group_class = RichAsyncGroup


RichAsyncMultiCommand = RichAsyncGroup


class RichAsyncCommandCollection(asyncclick.CommandCollection, RichAsyncGroup):
    """Richly formatted asyncclick CommandCollection."""


__all__ = [
    "RichAsyncCommand",
    "RichAsyncCommandCollection",
    "RichAsyncContext",
    "RichAsyncGroup",
    "RichAsyncMultiCommand",
]
