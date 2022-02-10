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
        helptext = Text()

        # Prepend deprecated status
        if obj.deprecated:
            helptext.append("(Deprecated) ", style="red")

        # Get the first line, remove single linebreaks
        first_line = obj.help.split("\n\n")[0].replace("\n", " ").strip()
        helptext.append(first_line)

        # Get remaining lines, remove single line breaks and format as dim
        remaining_lines = obj.help.split("\n\n")[1:]
        if len(remaining_lines) > 0:
            remaining_lines = "\n" + "\n".join(
                [x.replace("\n", " ").strip() for x in remaining_lines]
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

        # Skip if option is hidden
        if param.hidden:
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
            metavar = Text(f" {param.metavar}", style="bold yellow")

        # Help text
        help = Text("")
        if param.help:
            help.append(param.help)

        # Default value
        ## TODO: This is not as extensive as the original click source and misses some cases
        ## eg. --debug/--no-debug, default=False, show_default=True will show up as [default: False] instead of [default: --no-debug]
        ## Need to think if we should copy and paste all of that code, or try to parse it from the function output somehow
        ## https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2662-L2696
        if param.show_default:
            help.append(f" [default: {param.default}]", style="dim")

        ## TODO: Numeric ranges, extra
        ## https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2698-L2706
        ## https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2711-L2713

        # Required?
        required = ""
        if param.required:
            required = Text("*", style="red")
            help.append(f" [required]", style="dim red")

        options_table.add_row(
            required, highlighter(opt1), highlighter(opt2), metavar, highlighter(help)
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

    # Epilogue if we have it
    if obj.epilog:
        # Remove single linebreaks, replace double with single
        lines = obj.epilog.split("\n\n")
        epilogue = "\n".join([x.replace("\n", " ").strip() for x in lines])
        console.print(Padding(Align(epilogue, width=100, pad=False), 1))
