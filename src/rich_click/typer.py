from shutil import get_terminal_size as get_terminal_size
from typing import Any, Callable, Dict, Optional, Type

import click
from click.exceptions import Abort as Abort
from click.exceptions import BadParameter as BadParameter
from click.exceptions import Exit as Exit
from click.termui import clear as clear
from click.termui import confirm as confirm
from click.termui import echo_via_pager as echo_via_pager
from click.termui import edit as edit
from click.termui import getchar as getchar
from click.termui import launch as launch
from click.termui import pause as pause
from click.termui import progressbar as progressbar
from click.termui import prompt as prompt
from click.termui import secho as secho
from click.termui import style as style
from click.termui import unstyle as unstyle
from click.utils import echo as echo
from click.utils import format_filename as format_filename
from click.utils import get_app_dir as get_app_dir
from click.utils import get_binary_stream as get_binary_stream
from click.utils import get_text_stream as get_text_stream
from click.utils import open_file as open_file
from typer import colors as colors
from typer import Typer as BaseTyper
from typer.models import CallbackParam as CallbackParam
from typer.models import CommandFunctionType
from typer.models import Context as Context
from typer.models import Default
from typer.models import FileBinaryRead as FileBinaryRead
from typer.models import FileBinaryWrite as FileBinaryWrite
from typer.models import FileText as FileText
from typer.models import FileTextWrite as FileTextWrite
from typer.params import Argument as Argument
from typer.params import Option as Option

from rich_click import RichCommand, RichGroup


class Typer(BaseTyper):
    """A custom subclassed version of typer.Typer to allow rich help."""

    def __init__(
        self,
        *,
        name: Optional[str] = Default(None),
        cls: Optional[Type[click.Command]] = RichGroup,
        invoke_without_command: bool = Default(False),
        no_args_is_help: bool = Default(False),
        subcommand_metavar: Optional[str] = Default(None),
        chain: bool = Default(False),
        result_callback: Optional[Callable[..., Any]] = Default(None),
        # Command
        context_settings: Optional[Dict[Any, Any]] = Default(None),
        callback: Optional[Callable[..., Any]] = Default(None),
        help: Optional[str] = Default(None),
        epilog: Optional[str] = Default(None),
        short_help: Optional[str] = Default(None),
        options_metavar: str = Default("[OPTIONS]"),
        add_help_option: bool = Default(True),
        hidden: bool = Default(False),
        deprecated: bool = Default(False),
        add_completion: bool = True,
    ) -> None:
        """Initialise with a RichGroup class as the default."""
        super().__init__(
            name=name,
            cls=cls,
            invoke_without_command=invoke_without_command,
            no_args_is_help=no_args_is_help,
            subcommand_metavar=subcommand_metavar,
            chain=chain,
            result_callback=result_callback,
            context_settings=context_settings,
            callback=callback,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            hidden=hidden,
            deprecated=deprecated,
            add_completion=add_completion,
        )

    def command(
        self,
        name: Optional[str] = None,
        *,
        cls: Optional[Type[click.Command]] = RichCommand,
        context_settings: Optional[Dict[Any, Any]] = None,
        help: Optional[str] = None,
        epilog: Optional[str] = None,
        short_help: Optional[str] = None,
        options_metavar: str = "[OPTIONS]",
        add_help_option: bool = True,
        no_args_is_help: bool = False,
        hidden: bool = False,
        deprecated: bool = False,
    ) -> Callable[[CommandFunctionType], CommandFunctionType]:
        return super().command(
            name=name,
            cls=cls,
            context_settings=context_settings,
            help=help,
            epilog=epilog,
            short_help=short_help,
            options_metavar=options_metavar,
            add_help_option=add_help_option,
            no_args_is_help=no_args_is_help,
            hidden=hidden,
            deprecated=deprecated,
        )


def run(function: Callable[..., Any]) -> Any:
    """Redefine typer.run() to use our custom Typer class."""  # noqa D402
    app = Typer()
    app.command()(function)
    app()
