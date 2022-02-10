import click
from rich.align import Align
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

# Default colours
STYLE_OPTION = "bold cyan"
STYLE_SWITCH = "bold green"
STYLE_METAVAR = "bold yellow"
STYLE_USAGE = "yellow"
STYLE_USAGE_COMMAND = "bold"
STYLE_DEPRECATED = "red"
STYLE_HELPTEXT_FIRST_LINE = ""
STYLE_HELPTEXT = "dim"
STYLE_METAVAR = "bold yellow"
STYLE_OPTION_HELP = ""
STYLE_OPTION_DEFAULT = "dim"
STYLE_REQUIRED_SHORT = "red"
STYLE_REQUIRED_LONG = "dim red"
STYLE_OPTIONS_PANEL_BORDER = "dim"
ALIGN_OPTIONS_PANEL = "left"
STYLE_COMMANDS_PANEL_BORDER = "dim"
ALIGN_COMMANDS_PANEL = "left"
MAX_WIDTH = 100

# Fixed strings
DEPRECATED_STRING = "(Deprecated) "
DEFAULT_STRING = " [default: {}]"
REQUIRED_SHORT_STRING = "*"
REQUIRED_LONG_STRING = " [required]"
OPTIONS_PANEL_TITLE = "Options"
COMMANDS_PANEL_TITLE = "Commands"

# Behaviours
SKIP_ARGUMENTS = True


def rich_format_help(obj, ctx, formatter):
    """
    Print nicely formatted help text using rich

    This code was shamelessly stolen from rich-cli, the
    original author was @willmcgugan - thanks Will!

    I've modified it a little to work with click groups
    and to spit out output in a style that fits well with our tool.

    If this the rich-click plugin gets made, we can probably strip
    this out and just use that instead.

    Original source:
    https://github.com/Textualize/rich-cli/blob/8a2767c7a340715fc6fbf4930ace717b9b2fc5e5/src/rich_cli/__main__.py#L162-L236
    """

    class OptionHighlighter(RegexHighlighter):
        highlights = [
            r"(?P<switch>\-\w)(?!\S)",
            r"(?P<option>\-\-[\w\-]+)(?!\S)",
            r"(?P<metavar>\<[^\>]+\>)",
            r"(?P<usage>Usage: )",
        ]

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
    )

    # Print usage
    console.print(
        Padding(highlighter(obj.get_usage(ctx)), 1), style=STYLE_USAGE_COMMAND
    )

    # Print command / group help if we have some
    if obj.help:
        helptext = Text()

        # Prepend deprecated status
        if obj.deprecated:
            helptext.append(DEPRECATED_STRING, style=STYLE_DEPRECATED)

        # Get the first line, remove single linebreaks
        first_line = obj.help.split("\n\n")[0].replace("\n", " ").strip()
        helptext.append(first_line, style=STYLE_HELPTEXT_FIRST_LINE)

        # Get remaining lines, remove single line breaks and format as dim
        remaining_lines = obj.help.split("\n\n")[1:]
        if len(remaining_lines) > 0:
            remaining_lines = "\n" + "\n".join(
                [x.replace("\n", " ").strip() for x in remaining_lines]
            )
            helptext.append(remaining_lines, style=STYLE_HELPTEXT)

        # Print with a max width and some padding
        console.print(
            Padding(Align(helptext, width=MAX_WIDTH, pad=False), (0, 1, 1, 1))
        )

    # Print the option flags
    options_table = Table(highlight=True, box=None, show_header=False)
    for param in obj.get_params(ctx):

        # Skip positional arguments - they don't have opts or helptext and are covered in usage
        # See https://click.palletsprojects.com/en/8.0.x/documentation/#documenting-arguments
        if type(param) is click.core.Argument and SKIP_ARGUMENTS:
            continue

        # Skip if option is hidden
        if getattr(param, "hidden", False):
            continue

        # Short and long form
        if len(param.opts) == 2:
            # Always have the --long form first
            if "--" in param.opts[0]:
                opt1 = highlighter(param.opts[0])
                opt2 = highlighter(param.opts[1])
                # Secondary opts (eg. --debug/--no-debug)
                if param.secondary_opts:
                    opt1 += highlighter("/" + param.secondary_opts[0])
                    opt2 += highlighter("/" + param.secondary_opts[1])
            else:
                opt1 = highlighter(param.opts[1])
                opt2 = highlighter(param.opts[0])
                # Secondary opts (eg. --debug/--no-debug)
                if param.secondary_opts:
                    opt1 += highlighter("/" + param.secondary_opts[1])
                    opt2 += highlighter("/" + param.secondary_opts[1])
        # Just one form
        else:
            opt1 = highlighter(param.opts[0])
            opt2 = Text("")
            if param.secondary_opts:
                opt1 += highlighter("/" + param.secondary_opts[0])

        # Column for a metavar, if we have one
        metavar = ""
        if param.metavar:
            metavar = Text(f" {param.metavar}", style=STYLE_METAVAR)

        # Help text
        help = Text("")
        if getattr(param, "help", None):
            help.append(param.help, style=STYLE_OPTION_HELP)

        # Default value
        ## TODO: This is not as extensive as the original click source and misses some cases
        ## eg. --debug/--no-debug, default=False, show_default=True will show up as [default: False] instead of [default: --no-debug]
        ## Need to think if we should copy and paste all of that code, or try to parse it from the function output somehow
        ## https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2662-L2696
        if getattr(param, "show_default", None):
            help.append(
                DEFAULT_STRING.format(param.default), style=STYLE_OPTION_DEFAULT
            )

        ## TODO: Numeric ranges, extra
        ## https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2698-L2706
        ## https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2711-L2713

        # Required?
        required = ""
        if param.required:
            required = Text(REQUIRED_SHORT_STRING, style=STYLE_REQUIRED_SHORT)
            help.append(REQUIRED_LONG_STRING, style=STYLE_REQUIRED_LONG)

        options_table.add_row(
            required, highlighter(opt1), highlighter(opt2), metavar, highlighter(help)
        )

    if options_table.row_count > 0:
        console.print(
            Panel(
                options_table,
                border_style=STYLE_OPTIONS_PANEL_BORDER,
                title=OPTIONS_PANEL_TITLE,
                title_align=ALIGN_OPTIONS_PANEL,
                width=MAX_WIDTH,
            )
        )

    # List click command groups
    if hasattr(obj, "list_commands"):
        commands_table = Table(highlight=False, box=None, show_header=False)
        # Define formatting in first column, as commands don't match highlighter regex
        commands_table.add_column(style="bold cyan", no_wrap=True)
        for command in obj.list_commands(ctx):
            cmd = obj.get_command(ctx, command)
            helptext = cmd.help or ""
            commands_table.add_row(command, highlighter(helptext.split("\n")[0]))

        console.print(
            Panel(
                commands_table,
                border_style=STYLE_COMMANDS_PANEL_BORDER,
                title=COMMANDS_PANEL_TITLE,
                title_align=ALIGN_COMMANDS_PANEL,
                width=MAX_WIDTH,
            )
        )

    # Epilogue if we have it
    if obj.epilog:
        # Remove single linebreaks, replace double with single
        lines = obj.epilog.split("\n\n")
        epilogue = "\n".join([x.replace("\n", " ").strip() for x in lines])
        console.print(Padding(Align(epilogue, width=MAX_WIDTH, pad=False), 1))
