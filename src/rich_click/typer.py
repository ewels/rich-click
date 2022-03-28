from typing import Any, Callable

from typer import *  # noqa
from typer import Typer as BaseTyper
from typer.models import CommandFunctionType

from rich_click import RichCommand, RichGroup


class Typer(BaseTyper):
    """A custom subclassed version of typer.Typer to allow rich help."""

    def __init__(
        self,
        *args,
        cls=RichGroup,
        **kwargs,
    ) -> None:
        """Initialise with a RichGroup class as the default."""
        super().__init__(*args, cls=cls, **kwargs)

    def command(
        self,
        *args,
        cls=RichCommand,
        **kwargs,
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        return super().command(*args, cls=cls, **kwargs)


def run(function: Callable[..., Any]) -> Any:
    """Redefine typer.run() to use our custom Typer class."""  # noqa D402
    app = Typer()
    app.command()(function)
    app()
