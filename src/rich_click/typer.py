from typing import Callable, Any

from rich_click import RichCommand, RichGroup
from typer import Typer as BaseTyper
from typer import *  # noqa
from typer.models import CommandFunctionType


class Typer(BaseTyper):
    """A custom subclassed version of typer.Typer to allow rich help"""

    def __init__(
        self,
        *args,
        cls=RichGroup,
        **kwargs,
    ) -> None:
        super().__init__(*args, cls=cls, **kwargs)

    def command(
        self,
        *args,
        cls=RichCommand,
        **kwargs,
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        return super().command(*args, cls=cls, **kwargs)


def run(function: Callable[..., Any]) -> Any:
    """Redefine typer.run() to use our custom Typer class."""
    app = Typer()
    app.command()(function)
    app()
