import click
from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme
import re
import sys

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
STYLE_ERRORS_PANEL_BORDER = "red"
ALIGN_ERRORS_PANEL = "left"
MAX_WIDTH = None  # Set to an int to limit to that many characters

# Fixed strings
DEPRECATED_STRING = "(Deprecated) "
DEFAULT_STRING = "[default: {}]"
REQUIRED_SHORT_STRING = "*"
REQUIRED_LONG_STRING = "[required]"
RANGE_STRING = " [{}]"
ARGUMENTS_PANEL_TITLE = "Arguments"
OPTIONS_PANEL_TITLE = "Options"
COMMANDS_PANEL_TITLE = "Commands"
ERRORS_PANEL_TITLE = "Error"

# Behaviours
SHOW_ARGUMENTS = False
GROUP_ARGUMENTS_OPTIONS = False
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
    """Take a string and return styled text

    By default, return the text as a Rich Text with the request style.
    If USE_RICH_MARKUP is True, also parse the text for Rich markup strings.
    If USE_MARKDOWN is True, parse as Markdown.

    Only one of USE_MARKDOWN or USE_RICH_MARKUP can be True.
    If both are True, USE_MARKDOWN takes precedence.

    Args:
        text (str): Text to style
        style (str): Rich style to apply

    Returns:
        MarkdownElement or Text: Styled text object
    """
    if USE_MARKDOWN:
        return Markdown(text, style=style)
    if USE_RICH_MARKUP:
        return highlighter(Text.from_markup(text, style=style))
    else:
        return highlighter(Text(text, style=style))


def _get_help_text(obj):
    """Build primary help text for a click command or group.

    Returns the prose help text for a command or group, rendered either as a
    Rich Text object or as Markdown.
    If the command is marked as depreciated, the depreciated string will be prepended.

    Args:
        obj (click.Command or click.Group): Command or group to build help text for

    Returns:
        Columns: A columns element with multiple styled objects (depreciated, usage)
    """

    items = []

    # Prepend deprecated status
    if obj.deprecated:
        items.append(Text(DEPRECATED_STRING, style=STYLE_DEPRECATED))

    # Get the first line
    first_line = obj.help.split("\n\n")[0]
    # Remove single linebreaks
    first_line = first_line.replace("\n", " ").strip()
    items.append(_make_rich_rext(first_line, STYLE_HELPTEXT_FIRST_LINE))

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
        items.append(_make_rich_rext(remaining_lines, STYLE_HELPTEXT))

    # Use Columns - this allows us to group different renderable types
    # (Text, Markdown) onto a single line.
    return Columns(items)


def _get_parameter_help(param, ctx):
    """Build primary help text for a click option or argument.

    Returns the prose help text for an option or argument, rendered either
    as a Rich Text object or as Markdown.
    Additional elements are appended to show the default and required status if applicable.

    Args:
        param (click.Option or click.Argument): Option or argument to build help text for
        ctx (click.Context): Click Context object

    Returns:
        Columns: A columns element with multiple styled objects (help, default, required)
    """

    items = []

    if getattr(param, "help", None):
        items.append(_make_rich_rext(param.help, STYLE_OPTION_HELP))

    # Default value
    if getattr(param, "show_default", None):
        # param.default is the value, but click is a bit clever in choosing what to show here
        # eg. --debug/--no-debug, default=False will show up as [default: no-debug] instead of [default: False]
        # To avoid duplicating loads of code, let's just pull out the string from click with a regex
        default_str_match = re.search(
            r"\[default: (.*)\]", param.get_help_record(ctx)[-1]
        )
        if default_str_match:
            # Don't show the required string, as we show that afterwards anyway
            default_str = default_str_match.group(1).replace("; required", "")
            items.append(
                Text(
                    DEFAULT_STRING.format(default_str),
                    style=STYLE_OPTION_DEFAULT,
                )
            )

    # Required?
    if param.required:
        items.append(Text(REQUIRED_LONG_STRING, style=STYLE_REQUIRED_LONG))

    # Use Columns - this allows us to group different renderable types
    # (Text, Markdown) onto a single line.
    return Columns(items)


def rich_format_help(obj, ctx, formatter):
    """Print nicely formatted help text using rich

    Based on original code from rich-cli, by @willmcgugan.
    https://github.com/Textualize/rich-cli/blob/8a2767c7a340715fc6fbf4930ace717b9b2fc5e5/src/rich_cli/__main__.py#L162-L236

    Replacement for the click function format_help().
    Takes a command or group and builds the help text output.

    Args:
        obj (click.Command or click.Group): Command or group to build help text for
        ctx (click.Context): Click Context object
        formatter (click.HelpFormatter): Click HelpFormatter object
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

    # Look through OPTION_GROUPS for this command
    # stick anything unmatched into a default group at the end
    option_groups = OPTION_GROUPS.get(ctx.command_path, []).copy()
    option_groups.append({"options": []})
    argument_groups = {"name": ARGUMENTS_PANEL_TITLE, "options": []}
    for param in obj.get_params(ctx):

        # Skip positional arguments - they don't have opts or helptext and are covered in usage
        # See https://click.palletsprojects.com/en/8.0.x/documentation/#documenting-arguments
        if type(param) is click.core.Argument and not SHOW_ARGUMENTS:
            continue

        # Skip if option is hidden
        if getattr(param, "hidden", False):
            continue

        # Already mentioned in a config option group
        for option_group in option_groups:
            if any([opt in option_group.get("options", []) for opt in param.opts]):
                break
        # No break, no mention - add to the default group
        else:
            if type(param) is click.core.Argument and not GROUP_ARGUMENTS_OPTIONS:
                argument_groups["options"].append(param.opts[0])
            else:
                option_groups[-1]["options"].append(param.opts[0])

    # If we're not grouping arguments and we got some, prepend before default options
    if len(argument_groups["options"]) > 0:
        option_groups.insert(len(option_groups) - 1, argument_groups)

    # Print each command group panel
    for option_group in option_groups:

        options_rows = []
        for param in obj.get_params(ctx):

            # Skip if command is not listed in this group
            if not any([opt in option_group.get("options", []) for opt in param.opts]):
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
                    title=option_group.get("name", OPTIONS_PANEL_TITLE),
                    title_align=ALIGN_OPTIONS_PANEL,
                    width=MAX_WIDTH,
                )
            )

    #
    # Groups only:
    # List click command groups
    #
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


def rich_format_error(self):
    """Print richly formatted click errors.

    Called by custom exception handler to print richly formatted click errors.
    Mimics original click.ClickException.echo() function but with rich formatting.

    Args:
        click.ClickException: Click exception to format.
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
    if self.ctx is not None:
        console.print(self.ctx.get_usage())
    if self.ctx is not None and self.ctx.command.get_help_option(self.ctx) is not None:
        console.print(
            "Try [blue]'{command} {option}'[/] for help.".format(
                command=self.ctx.command_path, option=self.ctx.help_option_names[0]
            ),
            style="dim",
        )

    console.print(
        Panel(
            highlighter(self.format_message()),
            border_style=STYLE_ERRORS_PANEL_BORDER,
            title=ERRORS_PANEL_TITLE,
            title_align=ALIGN_ERRORS_PANEL,
            width=MAX_WIDTH,
        )
    )


class RichCommand(click.Command):
    """Richly formatted click Command.

    Inherits click.Command and overrides help and error methods
    to print richly formatted output.
    """

    standalone_mode = False

    def main(self, *args, standalone_mode=True, **kwargs):
        try:
            return super().main(*args, standalone_mode=False, **kwargs)
        except click.ClickException as e:
            if not standalone_mode:
                raise
            rich_format_error(e)
            sys.exit(e.exit_code)

    def format_help(self, ctx, formatter):
        rich_format_help(self, ctx, formatter)


class RichGroup(click.Group):
    """Richly formatted click Group.

    Inherits click.Group and overrides help and error methods
    to print richly formatted output.
    """

    command_class = RichCommand

    def main(self, *args, standalone_mode=True, **kwargs):
        try:
            return super().main(*args, standalone_mode=False, **kwargs)
        except click.ClickException as e:
            if not standalone_mode:
                raise
            rich_format_error(e)
            sys.exit(e.exit_code)

    def format_help(self, ctx, formatter):
        rich_format_help(self, ctx, formatter)
