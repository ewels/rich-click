"""The command line interface."""

import sys
from textwrap import dedent
from importlib import import_module

try:
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points

import click
from rich.console import Console
from rich.padding import Padding
from rich.text import Text
from rich.theme import Theme
from rich_click import group as rich_group, command as rich_command
from rich_click.rich_click import (
    OptionHighlighter,
    _make_rich_rext,
    COLOR_SYSTEM,
    STYLE_HELPTEXT_FIRST_LINE,
    STYLE_HELPTEXT,
    STYLE_METAVAR,
    STYLE_OPTION,
    STYLE_SWITCH,
    STYLE_USAGE_COMMAND,
    STYLE_USAGE,
)


def main(args=None):
    """
    The [link=https://github.com/ewels/rich-click]rich-click[/] CLI
    provides attractive help output from any tool using [link=https://click.palletsprojects.com/]click[/],
    formatted with [link=https://github.com/Textualize/rich]rich[/].

    The rich-click command line tool can be prepended before any Python package
    using native click to provide attractive richified click help output.

    For example, if you have a package called [blue]my_package[/] that uses click,
    you can run:

    [blue]  rich-click my_package --help  [/]

    It only works if the package is using vanilla click without customised [cyan]group()[/]
    or [cyan]command()[/] classes.
    If in doubt, please suggest to the authors that they use rich_click within their
    tool natively - this will always give a better experience.
    """
    args = args or sys.argv[1:]
    if not args:
        # without args we assume we want to run rich-click on itself
        # TODO: rewrite using click
        script_name = "rich-click"
    else:
        script_name = args[0]
    scripts = {script.name: script for script in entry_points().get("console_scripts")}
    if script_name in scripts:
        # a valid script was passed
        script = scripts[script_name]
        module_path, function_name = script.value.split(":", 1)
        prog = script_name
    elif ":" in script_name:
        # the path to a function was passed
        module_path, function_name = args[0].split(":", 1)
        prog = module_path.split(".", 1)[0]
    else:
        highlighter = OptionHighlighter()
        console = Console(
            theme=Theme(
                {
                    "option": STYLE_OPTION,
                    "switch": STYLE_SWITCH,
                    "metavar": STYLE_METAVAR,
                    "usage": STYLE_USAGE,
                }
            ),
            highlighter=highlighter,
            color_system=COLOR_SYSTEM,
        )
        console.print(
            Padding(
                highlighter(
                    "Usage: rich-click [SCRIPT | MODULE:FUNCTION] [-- SCRIPT_ARGS...]"
                ),
                1,
            ),
            style=STYLE_USAGE_COMMAND,
        )
        help_paragraphs = dedent(main.__doc__).split("\n\n")
        help_paragraphs = [x.replace("\n", " ").strip() for x in help_paragraphs]
        console.print(
            Padding(
                Text.from_markup(help_paragraphs[0].strip()),
                (0, 1),
            ),
            style=STYLE_HELPTEXT_FIRST_LINE,
        )
        console.print(
            Padding(
                Text.from_markup("\n\n".join(help_paragraphs[1:]).strip()),
                (0, 1),
            ),
            style=STYLE_HELPTEXT,
        )
        sys.exit(1)
    if len(args) > 1:
        if args[1] == "--":
            del args[1]
    sys.argv = [prog, *args[1:]]
    # patch click before importing the program function
    click.group = rich_group
    click.command = rich_command
    # import the program function
    module = import_module(module_path)
    function = getattr(module, function_name)
    # simply run it: it should be patched as well
    return function()
