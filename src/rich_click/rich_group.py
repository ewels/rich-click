from typing import Any, Callable, overload, Type, Union

import click

from rich_click.rich_command import RichCommand
from rich_click.rich_mixin import RichMixin


class RichGroup(RichMixin, click.Group):
    """Richly formatted click Group.

    Inherits click.Group and overrides help and error methods
    to print richly formatted output.
    """

    command_class: Type[RichCommand] = RichCommand
    group_class = type

    @overload
    def command(self, __func: Callable[..., Any]) -> click.Command:
        ...

    @overload
    def command(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], click.Command]:
        ...

    def command(self, *args: Any, **kwargs: Any) -> Union[Callable[[Callable[..., Any]], click.Command], click.Command]:
        # This method override is required for Click 7.x compatibility.
        # (The command_class ClassVar was not added until 8.0.)
        kwargs.setdefault("cls", self.command_class)
        return super().command(*args, **kwargs)
