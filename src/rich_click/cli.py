"""The command line interface."""

import sys
from gettext import gettext as _
from importlib import import_module
from typing import List, Optional, Union


try:
    from importlib import metadata  # type: ignore[import,unused-ignore]
except ImportError:
    # Python < 3.8
    import importlib_metadata as metadata  # type: ignore[no-redef,import-not-found,unused-ignore]

import click
from rich.console import Console

from rich_click.decorators import command as rich_command
from rich_click.decorators import group as rich_group
from rich_click.decorators import pass_context, rich_config
from rich_click.rich_command import RichCommand, RichCommandCollection, RichGroup, RichMultiCommand
from rich_click.rich_context import RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration


console = Console()


def patch(rich_config: Optional[RichHelpConfiguration] = None) -> None:
    """Patch Click internals to use Rich-Click types."""
    click.group = rich_group
    click.command = rich_command
    click.Group = RichGroup  # type: ignore[misc]
    click.Command = RichCommand  # type: ignore[misc]
    click.CommandCollection = RichCommandCollection  # type: ignore[misc]
    if "MultiCommand" in dir(click):
        click.MultiCommand = RichMultiCommand  # type: ignore[assignment,misc,unused-ignore]
    if rich_config is not None:
        rich_config._dump_into_globals()


def entry_points(*, group: str) -> "metadata.EntryPoints":  # type: ignore[name-defined]
    """entry_points function that is compatible with Python 3.7+."""
    if sys.version_info >= (3, 10):
        return metadata.entry_points(group=group)

    epg = metadata.entry_points()

    if sys.version_info < (3, 8) and hasattr(epg, "select"):
        return epg.select(group=group)

    return epg.get(group, [])


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
                return RichHelpConfiguration(**data)
            except Exception as e:
                # In normal circumstances, a bad arg to a CLI doesn't
                # prevent the help text from rendering.
                if ctx is not None and ctx.params.get("show_help", False):
                    click.echo(ctx.get_help(), color=ctx.color)
                    ctx.exit()
                else:
                    raise e


@rich_command("rich-click", context_settings=dict(allow_interspersed_args=False, help_option_names=[]))
@click.argument("script_and_args", nargs=-1, metavar="[SCRIPT | MODULE:CLICK_COMMAND] [-- SCRIPT_ARGS...]")
@click.option(
    "--rich-config",
    type=_RichHelpConfigurationParamType(),
    help="Keyword arguments to pass into the [de]RichHelpConfiguration()[/] used"
    " to render the help text of the command. You can pass either a JSON directly, or a file"
    " prefixed with `@` (for example: '@rich_config.json'). Note that the --rich-config"
    " option is also used to render this help text you're reading right now!",
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
)
@pass_context
@rich_config(
    help_config={
        "use_markdown": False,
        "use_rich_markup": True,
        "errors_epilogue": "[d]Please run [yellow bold]rich-click --help[/] for usage information.[/]",
    }
)
def main(
    ctx: RichContext,
    script_and_args: List[str],
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
    """  # noqa: D400, D401
    if (show_help or not script_and_args) and not ctx.resilient_parsing:
        if rich_config is not None:
            rich_config.use_markdown = False
            rich_config.use_rich_markup = True
            ctx.help_config = rich_config
        click.echo(ctx.get_help(), color=ctx.color)
        ctx.exit()

    script, *args = script_and_args

    scripts = {script.name: script for script in entry_points(group="console_scripts")}
    if script in scripts:
        module_path, function_name = scripts[script].value.split(":", 1)
    elif ":" in script:
        # the path to a function was passed
        module_path, function_name = script.split(":", 1)
    else:
        raise click.ClickException(f"No such script: {script_and_args[0]}")

    if len(args) > 1:
        if args[0] == "--":
            del args[0]

    prog = module_path.split(".", 1)[0]

    sys.argv = [prog, *args]
    # patch click before importing the program function
    patch(rich_config=rich_config)
    # import the program function
    module = import_module(module_path)
    function = getattr(module, function_name)
    # simply run it: it should be patched as well
    function()
