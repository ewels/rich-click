import click
from rich.align import Align
from rich.console import Console, group
from rich.highlighter import RegexHighlighter
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
import re

# Default styles
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
MAX_WIDTH = None  # Set to an int to limit to that many characters

# Fixed strings
DEPRECATED_STRING = "(Deprecated) "
DEFAULT_STRING = " [default: {}]"
REQUIRED_SHORT_STRING = "*"
REQUIRED_LONG_STRING = " [required]"
RANGE_STRING = " [{}]"
OPTIONS_PANEL_TITLE = "Options"
COMMANDS_PANEL_TITLE = "Commands"

# Behaviours
SHOW_ARGUMENTS = False
USE_MARKDOWN = False
USE_RICH_MARKUP = False
COMMAND_GROUPS = {}
OPTION_GROUPS = {}


# Rich regex highlighter
class OptionHighlighter(RegexHighlighter):
    highlights = [
        r"(^|\W)(?P<switch>\-\w+)(?!\S)",
        r"(^|\W)(?P<option>\-\-[\w\-]+)(?!\S)",
        r"(?P<metavar>\<[^\>]+\>)",
        r"(?P<usage>Usage: )",
    ]


highlighter = OptionHighlighter()


def _make_rich_rext(text, style=""):
    """
    Return styled text, either as Markdown, rich markup or plain,
    depending on user settings
    """
    # TODO: Doesn't work yet, not sure how to make a rich Markdown object into a Text object
    # https://github.com/Textualize/rich/discussions/1951#discussioncomment-2156145
    if USE_MARKDOWN:
        return Markdown(text, style=style)
    if USE_RICH_MARKUP:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))


@group()
def _get_help_text(obj):

    # Prepend deprecated status
    if obj.deprecated:
        yield Text(DEPRECATED_STRING, style=STYLE_DEPRECATED)

    # Get the first line
    first_line = obj.help.split("\n\n")[0]
    # Remove single linebreaks
    first_line = first_line.replace("\n", " ").strip()
    yield _make_rich_rext(first_line, STYLE_HELPTEXT_FIRST_LINE)

    # Get remaining lines, remove single line breaks and format as dim
    remaining_lines = obj.help.split("\n\n")[1:]
    if len(remaining_lines) > 0:
        # Remove single linebreaks
        remaining_lines = [x.replace("\n", " ").strip() for x in remaining_lines]
        # Join with double linebreaks if parsing as markdown, single otherwise
        if USE_MARKDOWN:
            remaining_lines = "\n\n" + "\n\n".join(remaining_lines)
        else:
            remaining_lines = "\n".join(remaining_lines)
        yield _make_rich_rext(remaining_lines, STYLE_HELPTEXT)


@group()
def _get_parameter_help(param, ctx):
    if getattr(param, "help", None):
        yield _make_rich_rext(param.help, STYLE_OPTION_HELP)

    # Default value
    if getattr(param, "show_default", None):
        # param.default is the value, but click is a bit clever in choosing what to show here
        # eg. --debug/--no-debug, default=False will show up as [default: no-debug] instead of [default: False]
        # To avoid duplicating loads of code, let's just pull out the string from click with a regex
        default_str = re.search(
            r"\[default: (.*)\]", param.get_help_record(ctx)[-1]
        ).group(1)
        yield Text(DEFAULT_STRING.format(default_str), style=STYLE_OPTION_DEFAULT)

    # Required?
    if param.required:
        yield Text(REQUIRED_LONG_STRING, style=STYLE_REQUIRED_LONG)


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

        # Print with a max width and some padding
        console.print(
            Padding(
                Align(_get_help_text(obj), width=MAX_WIDTH, pad=False),
                (0, 1, 1, 1),
            )
        )

    # Print the option flags
    options_rows = []
    for param in obj.get_params(ctx):

        # Skip positional arguments - they don't have opts or helptext and are covered in usage
        # See https://click.palletsprojects.com/en/8.0.x/documentation/#documenting-arguments
        if type(param) is click.core.Argument and not SHOW_ARGUMENTS:
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
        metavar = Text(style=STYLE_METAVAR)
        if param.metavar:
            metavar.append(f" {param.metavar}")
        else:
            metavar_str = param.type.get_metavar(param)
            if metavar_str:
                metavar.append(f" {metavar_str}")

        # Range - from https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2698-L2706
        if (
            isinstance(param.type, click.types._NumberRangeBase)
            # skip count with default range type
            and not (param.count and param.type.min == 0 and param.type.max is None)
        ):
            range_str = param.type._describe_range()
            if range_str:
                metavar.append(RANGE_STRING.format(range_str))

        # Required asterisk
        required = ""
        if param.required:
            required = Text(REQUIRED_SHORT_STRING, style=STYLE_REQUIRED_SHORT)

        options_rows.append(
            [
                required,
                highlighter(opt1),
                highlighter(opt2),
                metavar,
                _get_parameter_help(param, ctx),
            ]
        )

    if len(options_rows) > 0:
        options_table = Table(highlight=True, box=None, show_header=False)
        # Strip the required column if none are required
        if all([x[0] == "" for x in options_rows]):
            options_rows = [x[1:] for x in options_rows]
        for row in options_rows:
            options_table.add_row(*row)
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
        # Look through COMMAND_GROUPS for this command
        # stick anything unmatched into a default group at the end
        cmd_groups = COMMAND_GROUPS.get(ctx.command_path, []).copy()
        cmd_groups.append({"commands": []})
        for command in obj.list_commands(ctx):
            for cmd_group in cmd_groups:
                if command in cmd_group.get("commands", []):
                    break
            else:
                cmd_groups[-1]["commands"].append(command)

        # Print each command group panel
        for cmd_group in cmd_groups:
            commands_table = Table(highlight=False, box=None, show_header=False)
            # Define formatting in first column, as commands don't match highlighter regex
            commands_table.add_column(style="bold cyan", no_wrap=True)
            for command in obj.list_commands(ctx):
                # Skip if command is not listed in this group
                if command not in cmd_group.get("commands", []):
                    continue
                cmd = obj.get_command(ctx, command)
                helptext = cmd.help or ""
                commands_table.add_row(command, highlighter(helptext.split("\n")[0]))
            if commands_table.row_count > 0:
                console.print(
                    Panel(
                        commands_table,
                        border_style=STYLE_COMMANDS_PANEL_BORDER,
                        title=cmd_group.get("name", COMMANDS_PANEL_TITLE),
                        title_align=ALIGN_COMMANDS_PANEL,
                        width=MAX_WIDTH,
                    )
                )

    # Epilogue if we have it
    if obj.epilog:
        # Remove single linebreaks, replace double with single
        lines = obj.epilog.split("\n\n")
        epilogue = "\n".join([x.replace("\n", " ").strip() for x in lines])
        console.print(
            Padding(Align(highlighter(epilogue), width=MAX_WIDTH, pad=False), 1)
        )
