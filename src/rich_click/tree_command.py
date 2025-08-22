from __future__ import annotations

from typing import Any, Callable, Optional, Type, Union

from click import Group

from rich_click.rich_command import RichCommand, RichGroup

from rich_click.tree_help_rendering import tree_format_help

from rich_click.rich_context import RichContext

from rich_click.rich_help_formatter import RichHelpFormatter


class TreeRichCommand(RichCommand):
    """Custom Command with tree-formatted help."""

    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:
        tree_format_help(ctx, formatter, False)


class TreeRichGroup(RichGroup):
    """Custom Group with tree-formatted help."""

    command_class: Optional[Type[RichCommand]] = TreeRichCommand
    group_class: Optional[Union[Type[Group], Type[type]]] = type

    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:
        tree_format_help(ctx, formatter, True)

    def add_command(self, cmd, name=None):
        name = name or cmd.name
        super().add_command(cmd, name)

    def command(self, *args, **kwargs):
        parent_command = super().command
        def decorator(f):
            cmd = parent_command(*args, **kwargs)(f)
            return cmd
        return decorator

