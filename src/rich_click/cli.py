"""The command line interface."""

# ruff: noqa: D103

import os
import sys
from functools import wraps
from gettext import gettext as _
from importlib import import_module
from typing import Any, List, Optional, Union

from typing_extensions import Literal


try:
    from importlib import metadata  # type: ignore[import,unused-ignore]
except ImportError:
    # Python < 3.8
    import importlib_metadata as metadata  # type: ignore[no-redef,import-not-found,unused-ignore]

import click

from rich_click.decorators import command as _rich_command
from rich_click.decorators import pass_context
from rich_click.decorators import rich_config as rich_config_decorator
from rich_click.patch import patch as _patch
from rich_click.rich_context import RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration


def entry_points(*, group: str) -> "metadata.EntryPoints":  # type: ignore[name-defined]
    """entry_points function that is compatible with Python 3.7+."""
    if sys.version_info >= (3, 10):
        return metadata.entry_points(group=group)

    epg = metadata.entry_points()

    if sys.version_info < (3, 8) and hasattr(epg, "select"):
        return epg.select(group=group)

    return epg.get(group, [])


@wraps(_patch)
def patch(*args: Any, **kwargs: Any) -> None:
    import warnings

    warnings.warn(
        "`rich_click.cli.patch()` has moved to `rich_click.patch.patch()`."
        " Importing `patch()` from `rich_click.cli` is deprecated; please import from `rich_click.patch` instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    return _patch(*args, **kwargs)


class _RichHelpConfigurationParamType(click.ParamType):

    name = "JSON"

    def __repr__(self) -> str:
        return "JSON"

    def convert(
        self,
        value: Optional[Union[RichHelpConfiguration, str]],
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> Optional[RichHelpConfiguration]:

        if value is None or isinstance(value, RichHelpConfiguration):
            return value
        else:
            try:
                import json

                if value.startswith("@"):
                    with open(value[1:], "r") as f:
                        data = json.load(f)
                else:
                    data = json.loads(value)
                if not isinstance(data, dict):
                    raise ValueError("--rich-config needs to be a JSON.")
                return RichHelpConfiguration.load_from_globals(**data)
            except Exception as e:
                # In normal circumstances, a bad arg to a CLI doesn't
                # prevent the help text from rendering.
                if ctx is not None and ctx.params.get("show_help", False):
                    click.echo(ctx.get_help(), color=ctx.color)
                    ctx.exit()
                else:
                    raise e


@_rich_command("rich-click", context_settings=dict(allow_interspersed_args=False, help_option_names=[]))
@click.argument("script_and_args", nargs=-1, metavar="[SCRIPT | MODULE:CLICK_COMMAND] [-- SCRIPT_ARGS...]")
@click.option(
    "--rich-config",
    "-c",
    type=_RichHelpConfigurationParamType(),
    help="Keyword arguments to pass into the [de]RichHelpConfiguration()[/] used"
    " to render the help text of the command. You can pass either a JSON directly, or a file"
    " prefixed with `@` (for example: '@rich_config.json'). Note that the --rich-config"
    " option is also used to render this help text you're reading right now!",
)
@click.option(
    "--output",
    "-o",
    type=click.Choice(["html", "svg"], case_sensitive=False),
    help="Optionally render help text as HTML or SVG. By default, help text is rendered normally.",
)
@click.option(
    # The rich-click CLI uses a special implementation of --help,
    # which is aware of the --rich-config object.
    "--help",
    "-h",
    "show_help",
    is_eager=True,
    is_flag=True,
    help=_("Show this message and exit."),
    # callback=help_callback
)
@pass_context
@rich_config_decorator(
    help_config={
        "text_markup": "rich",
        "errors_epilogue": "[d]Please run [yellow bold]rich-click --help[/] for usage information.[/]",
    }
)
def main(
    ctx: RichContext,
    script_and_args: List[str],
    output: Literal[None, "html", "svg"],
    rich_config: Optional[RichHelpConfiguration],
    show_help: bool,
) -> None:
    """
    The [link=https://github.com/ewels/rich-click]rich-click[/] CLI provides attractive help output from any
    tool using [link=https://click.palletsprojects.com/]click[/], formatted with
    [link=https://github.com/Textualize/rich]rich[/].

    The rich-click command line tool can be prepended before any Python package
    using native click to provide attractive richified click help output.

    For example, if you have a package called [argument]my_package[/] that uses click,
    you can run:

    >>> [command]rich-click[/] [argument]my_package[/] [option]--help[/]

    This does not always work if the package is using customised [b]click.group()[/]
    or [b]click.command()[/] classes.
    If in doubt, please suggest to the authors that they use rich_click within their
    tool natively - this will always give a better experience.

    You can also use this tool to print your own RichCommands as HTML with the
    --html flag.
    """  # noqa: D400, D401
    if (show_help or not script_and_args) and not ctx.resilient_parsing:
        if rich_config is not None:
            rich_config.use_markdown = False
            rich_config.use_rich_markup = True
            ctx.help_config = rich_config
        click.echo(ctx.get_help(), color=ctx.color)
        ctx.exit()

    sys.path.append(".")

    script, *args = script_and_args

    _from_entry_points = False

    scripts = {script.name: script for script in entry_points(group="console_scripts")}
    if script in scripts:
        module_path, function_name = scripts[script].value.split(":", 1)
        _from_entry_points = True
    elif ":" in script:
        # the path to a function was passed
        module_path, function_name = script.split(":", 1)
    else:
        raise click.ClickException(f"No such script: {script_and_args[0]}")

    prog = module_path.split(".", 1)[0]
    sys.argv = [prog, *args]

    # patch click before importing the program function
    _patch(rich_config=rich_config)
    # import the program function
    module = import_module(module_path)
    function = getattr(module, function_name)
    # simply run it: it should be patched as well
    if output is not None:
        ctx.help_config = RichHelpConfiguration.load_from_globals()
        RichContext.console = console = ctx.make_formatter().console
        console.record = True
        console.file = open(os.devnull, "w")
        RichContext.export_console_as = output

    if ctx.resilient_parsing and isinstance(function, click.Command):
        function.main(resilient_parsing=True)
    else:
        function()
