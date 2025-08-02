from typing import Any, Dict, Generator, Generic, List, Optional, Tuple, Type, TypeVar

import click
from rich.panel import Panel
from rich.table import Table


T = TypeVar("T")


class RichPanel(Generic[T]):
    """RichPanel base class."""

    panel_class: Optional[Type["Panel"]] = Panel
    table_class: Optional[Type["Table"]] = Table

    def __init__(
        self,
        name: str,
        table_styles: Optional[Dict[str, Any]] = None,
        panel_styles: Optional[Dict[str, Any]] = None,
        deduplicate: bool = True,
    ) -> None:
        """Create RichPanel instance."""
        self.name = name
        self.table_styles = table_styles or {}
        self.panel_styles = panel_styles or {}
        self.deduplicate = deduplicate

    def get_objects_in_panel(
        self,
        command: click.Command,
        ctx: click.Context,
    ) -> Generator[T]:
        raise NotImplementedError()


class RichParameterPanel(RichPanel[click.Parameter]):
    """Panel for parameters."""

    def get_objects_in_panel(
        self,
        command: click.Command,
        ctx: click.Context,
    ) -> Generator[click.Parameter]:
        li: List[Tuple[click.Parameter, int]] = []
        for param in command.get_params(ctx):
            panels = getattr(param, "panels", [])
            for p in panels:
                if p[0] == self.name:
                    li.append((param, p[1]))
                    if self.deduplicate:
                        break
        for parm, *_ in sorted(li, key=lambda _: _[1]):
            yield parm


class RichCommandPanel(RichPanel[click.Command]):
    """Panel for commands."""

    def get_objects_in_panel(
        self,
        command: click.Command,
        ctx: click.Context,
    ) -> Generator[click.Command]:
        if not isinstance(command, click.Group):
            return
        li: List[Tuple[click.Command, int]] = []
        for cmd_name in command.list_commands(ctx):
            cmd = command.get_command(ctx, cmd_name)
            if cmd is None:
                continue
            panels = getattr(cmd, "panels", [])
            for p in panels:
                if p[0] == self.name:
                    li.append((cmd, p[1]))
                    if self.deduplicate:
                        break
        for cmd, *_ in sorted(li, key=lambda _: _[1]):
            yield cmd
