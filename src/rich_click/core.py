import click
from rich.align import Align
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.theme import Theme


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
                "option": "bold cyan",
                "switch": "bold green",
                "metavar": "bold yellow",
                "usage": "yellow",
            }
        ),
        highlighter=highlighter,
    )

    # Print usage
    console.print(Padding(highlighter(obj.get_usage(ctx)), 1), style="bold")

    # Print command / group help if we have some
    if obj.help:
        # Get the first line, remove single linebreaks
        first_line = obj.help.split("\n\n")[0].replace("\n", " ")
        helptext = Text(first_line)

        # Get remaining lines, remove single line breaks and format as dim
        remaining_lines = obj.help.split("\n\n")[1:]
        if len(remaining_lines) > 0:
            remaining_lines = "\n" + "\n".join(
                [x.replace("\n", " ") for x in remaining_lines]
            )
            helptext.append(remaining_lines, style="dim")

        # Print with a max width and some padding
        console.print(Padding(Align(helptext, width=100, pad=False), (0, 1, 1, 1)))

    # Print the option flags
    options_table = Table(highlight=True, box=None, show_header=False)
    for param in obj.get_params(ctx):

        # Skip positional arguments - they don't have opts or helptext and are covered in usage
        # See https://click.palletsprojects.com/en/8.0.x/documentation/#documenting-arguments
        if type(param) is click.core.Argument:
            continue

        # Short and long form
        if len(param.opts) == 2:
            # Always have the --long form first
            if "--" in param.opts[0]:
                opt1 = highlighter(param.opts[0])
                opt2 = highlighter(param.opts[1])
                if len(param.secondary_opts) == 2:
                    opt1 += highlighter("/" + param.secondary_opts[0])
                    opt2 += highlighter("/" + param.secondary_opts[1])
            else:
                opt1 = highlighter(param.opts[1])
                opt2 = highlighter(param.opts[0])
                if len(param.secondary_opts) == 2:
                    opt1 += highlighter("/" + param.secondary_opts[1])
                    opt2 += highlighter("/" + param.secondary_opts[1])
        # Just one form
        else:
            opt1 = highlighter(param.opts[0])
            opt2 = Text("")
            if len(param.secondary_opts) > 0:
                opt1 += highlighter("/" + param.secondary_opts[0])

        # Column for a metavar, if we have one
        metavar = ""
        if param.metavar:
            metavar = Text(f" {param.metavar}", style="bold yellow")

        # Help text
        help_record = param.get_help_record(ctx)
        if help_record is None:
            help = ""
        else:
            help = Text.from_markup(param.get_help_record(ctx)[-1], emoji=False)

        options_table.add_row(
            highlighter(opt1), highlighter(opt2), metavar, highlighter(help)
        )

    if options_table.row_count > 0:
        console.print(
            Panel(
                options_table,
                border_style="dim",
                title="Options",
                title_align="left",
                width=100,
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
                border_style="dim",
                title="Commands",
                title_align="left",
                width=100,
            )
        )
