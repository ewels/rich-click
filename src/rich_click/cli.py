"""The command line interface."""

from __future__ import annotations

import os
import sys
from functools import wraps
from gettext import gettext
from importlib import (
    import_module,
    metadata,  # type: ignore[import,unused-ignore]
)
from typing import Any, List, Literal, Optional, Tuple, Union

import click

from rich_click.decorators import argument as _rich_argument
from rich_click.decorators import command as _rich_command
from rich_click.decorators import pass_context
from rich_click.patch import patch as _patch
from rich_click.rich_command import RichCommand
from rich_click.rich_context import RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration


def entry_points(*, group: str) -> "metadata.EntryPoints":  # type: ignore[name-defined]
    """entry_points function that is compatible with Python 3.7+."""
    if sys.version_info >= (3, 10):
        return metadata.entry_points(group=group)

    epg = metadata.entry_points()

    return epg.get(group, [])


@wraps(_patch)
def patch(*args: Any, **kwargs: Any) -> None:  # noqa: D103
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
                    print(ctx.get_help())
                    ctx.exit()
                else:
                    raise e


def _get_module_path_and_function_name(script: str, suppress_warnings: bool) -> Tuple[str, str]:
    _selected: List[str] = []
    module_path = ""
    function_name = ""

    for s in entry_points(group="console_scripts"):
        if script == s.name:
            if not _selected:
                module_path, function_name = s.value.split(":", 1)
                if " [" in function_name and function_name.endswith("]"):
                    function_name = function_name.split(" [")[0]
            if suppress_warnings:
                break
            if s.value not in _selected:
                _selected.append(s.value)

    if len(_selected) > 1 and not suppress_warnings:
        # This is an extremely rare edge case that comes up when the user sets the PYTHONPATH themselves.
        if script in sys.argv:
            _args = sys.argv.copy()
            _args[_args.index(script)] = f"{module_path}:{function_name}"
        else:
            _args = ["rich-click", f"{module_path}:{function_name}"]

        import rich

        rich.print(
            f"[red]WARNING: Multiple entry_points correspond with script '{script}': {_selected!r}."
            "\nThis can happen when an 'egg-info' directory exists, you're using a virtualenv,"
            " and you have set a custom PYTHONPATH."
            f"\n\nThe selected script is '{module_path}:{function_name}', which is being executed now."
            "\n\nIt is safer and recommended that you specify the MODULE:CLICK_COMMAND"
            f" ('{module_path}:{function_name}') instead of the script ('{script}'), like this:"
            f"\n\n>>> {' '.join(_args)}"
            "\n\nAlternatively, you can pass --suppress-warnings to the rich-click CLI,"
            " which will disable this message.[/]",
        )

    if ":" in script and not module_path:
        # the path to a function was passed
        module_path, function_name = script.split(":", 1)

    if not module_path:
        raise click.ClickException(f"No such script: {script}")

    return module_path, function_name


@_rich_command("rich-click", context_settings=dict(allow_interspersed_args=False, help_option_names=[]))
@_rich_argument(
    "script_and_args",
    nargs=-1,
    metavar="[SCRIPT | MODULE:CLICK_COMMAND] [-- SCRIPT_ARGS...]",
    help="The script you want to run. If it's a Click CLI and you are rendering help text;"
    " then the help text will render"
    " [#FF6B6B bold]r[/][#FF8E53 bold]i[/][#FFB347 bold]c[/][#4ECDC4 bold]h[/]"
    "[#45B7D1 bold]l[/][#74B9FF bold]y[/]. Otherwise, the script will run normally.",
)
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
    type=click.Choice(["html", "svg", "text"], case_sensitive=False),
    help="Optionally render help text as HTML or SVG or plain text. By default, help text is rendered normally.",
)
@click.option(
    "--errors-in-output-format",
    is_flag=True,
    help="If set, forces the CLI to render CLI error messages"
    " in the format specified by the --output option."
    " By default, error messages render normally, i.e. they are not converted to html or svg.",
)
@click.option(
    "--suppress-warnings/--do-not-suppress-warnings",
    is_flag=True,
    default=False,
    hidden=True,
    help="Suppress warnings when there are conflicting entry_points."
    " (This option is hidden because this situation is extremely rare).",
)
@click.option(
    "--patch-rich-click/--no-patch-rich-click",
    is_flag=True,
    default=True,
    help="If set, patch [code]rich_click.Command[/code], not just [code]click.Command[/code].",
)
@click.option(
    # The rich-click CLI uses a special implementation of --help,
    # which is aware of the --rich-config object.
    "--help",
    "-h",
    "show_help",
    is_eager=True,
    is_flag=True,
    help=gettext("Show this message and exit."),
    # callback=help_callback
)
@pass_context
def main(
    ctx: RichContext,
    script_and_args: List[str],
    output: Literal[None, "html", "svg"],
    errors_in_output_format: bool,
    suppress_warnings: bool,
    patch_rich_click: bool,
    rich_config: Optional[RichHelpConfiguration],
    show_help: bool,
) -> None:
    """
    The [link=https://github.com/ewels/rich-click]rich-click[/] CLI provides
    [#FF6B6B bold]r[/][#FF8E53 bold]i[/][#FFB347 bold]c[/][#4ECDC4 bold]h[/][#45B7D1 bold]l[/][#74B9FF bold]y[/]
    formatted help output from any
    tool using [link=https://click.palletsprojects.com/]click[/], formatted with
    [link=https://github.com/Textualize/rich]rich[/].

    Full docs here: [link=https://ewels.github.io/rich-click/latest/documentation/rich_click_cli/]\
https://ewels.github.io/rich-click/latest/documentation/rich_click_cli/[/]

    The rich-click command line tool can be prepended before any Python package
    using native click to provide attractive richified click help output.

    For example, if you have a package called [argument]my_package[/] that uses click,
    you can run:

    >>> [command]rich-click[/] [argument]my_package[/] [option]--help[/]

    When not rendering help text, the provided command will run normally,
    so it is safe to replace calls to the tool with [command]rich-click[/] in front, e.g.:

    >>> [command]rich-click[/] [argument]my_package[/] [argument]cmd[/] [option]--foo[/] 3
    """  # noqa: D401
    if (show_help or not script_and_args) and not ctx.resilient_parsing:
        if rich_config is None:
            rich_config = RichHelpConfiguration(text_markup="rich")
        else:
            rich_config.use_markdown = False
            rich_config.use_rich_markup = True
            rich_config.text_markup = "rich"
            if rich_config.show_arguments is None:
                rich_config.show_arguments = False
        ctx.help_config = rich_config
        print(ctx.get_help())
        ctx.exit()

    # patch click before importing the program function
    _patch(rich_config=rich_config, patch_rich_click=patch_rich_click)

    script, *args = script_and_args

    # import the program function
    try:
        module_path, function_name = _get_module_path_and_function_name(script, suppress_warnings)
        module = import_module(module_path)
    except (ModuleNotFoundError, click.ClickException):
        sys.path.append(os.path.abspath("."))
        # PYTHONPATH can change output of entry_points(group="console_scripts") in rare cases,
        # so we want to rerun the whole search
        module_path, function_name = _get_module_path_and_function_name(script, suppress_warnings)
        module = import_module(module_path)

    function = getattr(module, function_name)

    prog = module_path.split(".", 1)[0]
    sys.argv = [prog, *args]
    if ctx.resilient_parsing and isinstance(function, RichCommand):
        function.main(resilient_parsing=True)
    else:
        RichContext.export_console_as = ctx.export_console_as = output
        RichContext.errors_in_output_format = errors_in_output_format
        function()
