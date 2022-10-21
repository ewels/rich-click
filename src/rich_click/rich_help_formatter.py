from io import StringIO
from os import getenv
from typing import Dict, List, Optional, Union

import click
from rich.console import Console
from rich.theme import Theme

from rich_click.rich_click import highlighter


class RichHelpConfiguration:
    def __init__(
        self,
        style_option="bold cyan",
        style_argument="bold cyan",
        style_switch="bold green",
        style_metavar="bold yellow",
        style_metavar_append="dim yellow",
        style_metavar_separator="dim",
        style_header_text="",
        style_footer_text="",
        style_usage="yellow",
        style_usage_command="bold",
        style_deprecated="red",
        style_helptext_first_line="",
        style_helptext="dim",
        style_option_help="",
        style_option_default="dim",
        style_option_envvar="dim yellow",
        style_required_short="red",
        style_required_long="dim red",
        style_options_panel_border="dim",
        align_options_panel="left",
        style_options_table_show_lines=False,
        style_options_table_leading=0,
        style_options_table_pad_edge=False,
        style_options_table_padding=(0, 1),
        style_options_table_box="",
        style_options_table_row_styles=None,
        style_options_table_border_style=None,
        style_commands_panel_border="dim",
        align_commands_panel="left",
        style_commands_table_show_lines=False,
        style_commands_table_leading=0,
        style_commands_table_pad_edge=False,
        style_commands_table_padding=(0, 1),
        style_commands_table_box="",
        style_commands_table_row_styles=None,
        style_commands_table_border_style=None,
        style_errors_panel_border="red",
        align_errors_panel="left",
        style_errors_suggestion="dim",
        style_aborted="red",
        max_width=int(getenv("TERMINAL_WIDTH")) if getenv("TERMINAL_WIDTH") else None,  # type: ignore
        color_system: Optional[str] = "auto",
        force_terminal=True if getenv("GITHUB_ACTIONS") or getenv("FORCE_COLOR") or getenv("PY_COLORS") else None,
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None,
        deprecated_string="(Deprecated) ",
        default_string="[default: {}]",
        envvar_string="[env var: {}]",
        required_short_string="*",
        required_long_string="[required]",
        range_string=" [{}]",
        append_metavars_help_string="({})",
        arguments_panel_title="Arguments",
        options_panel_title="Options",
        commands_panel_title="Commands",
        errors_panel_title="Error",
        errors_suggestion: Optional[str] = None,
        errors_epilogue: Optional[str] = None,
        aborted_text="Aborted.",
        show_arguments=False,
        show_metavars_column=True,
        append_metavars_help=False,
        group_arguments_options=False,
        option_envvar_first=False,
        use_markdown=False,
        use_markdown_emoji=True,
        use_rich_markup=False,
        command_groups: Dict[str, List[Dict[str, Union[str, List[str]]]]] = {},
        option_groups: Dict[str, List[Dict[str, Union[str, List[str]]]]] = {},
        use_click_short_help=False,
    ):
        """Rich Help Configuration Class

        Args:
            style_option:
                Defaults to "bold cyan".
            style_argument:
                Defaults to "bold cyan".
            style_switch:
                Defaults to "bold green".
            style_metavar:
                Defaults to "bold yellow".
            style_metavar_append:
                Defaults to "dim yellow".
            style_metavar_separator: Style for metavar separator.
                Defaults to "dim".
            style_header_text:
                Defaults to "".
            style_footer_text:
                Defaults to "".
            style_usage:
                Defaults to "yellow".
            style_usage_command:
                Defaults to "bold".
            style_deprecated:
                Defaults to "red".
            style_helptext_first_line:
                Defaults to "".
            style_helptext:
                Defaults to "dim".
            style_option_help:
                Defaults to "".
            style_option_default:
                Defaults to "dim".
            style_option_envvar:
                Defaults to "dim yellow".
            style_required_short:
                Defaults to "red".
            style_required_long:
                Defaults to "dim red".
            style_options_panel_border:
                Defaults to "dim".
            align_options_panel:
                Defaults to "left".
            style_options_table_show_lines:
                Defaults to False.
            style_options_table_leading:
                Defaults to 0.
            style_options_table_pad_edge:
                Defaults to False.
            style_options_table_padding:
                Defaults to (0, 1).
            style_options_table_box:
                Defaults to "".
            style_options_table_row_styles:
                Defaults to None.
            style_options_table_border_style:
                Defaults to None.
            style_commands_panel_border:
                Defaults to "dim".
            align_commands_panel:
                Defaults to "left".
            style_commands_table_show_lines:
                Defaults to False.
            style_commands_table_leading:
                Defaults to 0.
            style_commands_table_pad_edge:
                Defaults to False.
            style_commands_table_padding:
                Defaults to (0, 1).
            style_commands_table_box:
                Defaults to "".
            style_commands_table_row_styles:
                Defaults to None.
            style_commands_table_border_style:
                Defaults to None.
            style_errors_panel_border:
                Defaults to "red".
            align_errors_panel:
                Defaults to "left".
            style_errors_suggestion:
                Defaults to "dim".
            style_aborted:
                Defaults to "red".
            max_width:
            force_terminal:
            header_text:
                Defaults to None.
            footer_text:
                Defaults to None.
            deprecated_string:
                Defaults to "(Deprecated) ".
            default_string:
                Defaults to "[default: {}]".
            envvar_string:
                Defaults to "[env var: {}]".
            required_short_string:
                Defaults to "*".
            required_long_string:
                Defaults to "[required]".
            range_string:
                Defaults to " [{}]".
            append_metavars_help_string:
                Defaults to "({})".
            arguments_panel_title:
                Defaults to "Arguments".
            options_panel_title:
                Defaults to "Options".
            commands_panel_title:
                Defaults to "Commands".
            errors_panel_title:
                Defaults to "Error".
            errors_suggestion:
                Defaults to  Try 'cmd -h' for help. Set to False to disable.
            errors_epilogue:
                Defaults to None.
            aborted_text:
                Defaults to "Aborted.".
            show_arguments: Show positional arguments
                Defaults to False.
            show_metavars_column: Show a column with the option metavar (eg. INTEGER)
                Defaults to True.
            append_metavars_help: Append metavar (eg. [TEXT]) after the help text
                Defaults to False.
            group_arguments_options: Show arguments with options instead of in own panel
                Defaults to False.
            option_envvar_first: Show env vars before option help text instead of avert
                Defaults to False.
            use_markdown:
                Defaults to False.
            use_markdown_emoji: Parse emoji codes in markdown :smile:
                Defaults to True.
            use_rich_markup: Parse help strings for rich markup (eg. [red]my text[/])
                Defaults to False.
            command_groups: Define sorted groups of panels to display subcommands
                Defaults to {}.
            option_groups: Define sorted groups of panels to display options and arguments
                Defaults to {}.
            use_click_short_help: Use click's default function to truncate help text
                Defaults to False.
        """
        # Default styles
        self.style_option = style_option
        self.style_argument = style_argument
        self.style_switch = style_switch
        self.style_metavar = style_metavar
        self.style_metavar_append = style_metavar_append
        self.style_metavar_separator = style_metavar_separator
        self.style_header_text = style_header_text
        self.style_footer_text = style_footer_text
        self.style_usage = style_usage
        self.style_usage_command = style_usage_command
        self.style_deprecated = style_deprecated
        self.style_helptext_first_line = style_helptext_first_line
        self.style_helptext = style_helptext
        self.style_option_help = style_option_help
        self.style_option_default = style_option_default
        self.style_option_envvar = style_option_envvar
        self.style_required_short = style_required_short
        self.style_required_long = style_required_long
        self.style_options_panel_border = style_options_panel_border
        self.align_options_panel = align_options_panel
        self.style_options_table_show_lines = style_options_table_show_lines
        self.style_options_table_leading = style_options_table_leading
        self.style_options_table_pad_edge = style_options_table_pad_edge
        self.style_options_table_padding = style_options_table_padding
        self.style_options_table_box = style_options_table_box
        self.style_options_table_row_styles = style_options_table_row_styles
        self.style_options_table_border_style = style_options_table_border_style
        self.style_commands_panel_border = style_commands_panel_border
        self.align_commands_panel = align_commands_panel
        self.style_commands_table_show_lines = style_commands_table_show_lines
        self.style_commands_table_leading = style_commands_table_leading
        self.style_commands_table_pad_edge = style_commands_table_pad_edge
        self.style_commands_table_padding = style_commands_table_padding
        self.style_commands_table_box = style_commands_table_box
        self.style_commands_table_row_styles = style_commands_table_row_styles
        self.style_commands_table_border_style = style_commands_table_border_style
        self.style_errors_panel_border = style_errors_panel_border
        self.align_errors_panel = align_errors_panel
        self.style_errors_suggestion = style_errors_suggestion
        self.style_aborted = style_aborted
        self.max_width = max_width
        self.color_system = color_system
        self.force_terminal = force_terminal

        # Fixed strings
        self.header_text: Optional[str] = header_text
        self.footer_text: Optional[str] = footer_text
        self.deprecated_string = deprecated_string
        self.default_string = default_string
        self.envvar_string = envvar_string
        self.required_short_string = required_short_string
        self.required_long_string = required_long_string
        self.range_string = range_string
        self.append_metavars_help_string = append_metavars_help_string
        self.arguments_panel_title = arguments_panel_title
        self.options_panel_title = options_panel_title
        self.commands_panel_title = commands_panel_title
        self.errors_panel_title = errors_panel_title
        self.errors_suggestion: Optional[str] = errors_suggestion
        self.errors_epilogue: Optional[str] = errors_epilogue
        self.aborted_text = aborted_text

        # Behaviours
        self.show_arguments = show_arguments
        self.show_metavars_column = show_metavars_column
        self.append_metavars_help = append_metavars_help
        self.group_arguments_options = group_arguments_options
        self.option_envvar_first = option_envvar_first
        self.use_markdown = use_markdown
        self.use_markdown_emoji = use_markdown_emoji
        self.use_rich_markup = use_rich_markup
        self.command_groups = command_groups
        self.option_groups = option_groups
        self.use_click_short_help = use_click_short_help


def get_default_console(config: RichHelpConfiguration):
    return Console(
        theme=Theme(
            {
                "option": config.style_option,
                "argument": config.style_argument,
                "switch": config.style_switch,
                "metavar": config.style_metavar,
                "metavar_sep": config.style_metavar_separator,
                "usage": config.style_usage,
            }
        ),
        highlighter=highlighter,
        color_system=config.color_system,  # type: ignore
        force_terminal=config.force_terminal,
        width=config.max_width,
        file=StringIO(),
    )


class RichHelpFormatter(click.HelpFormatter):
    """Rich Help Formatter"""

    def __init__(
        self,
        config: RichHelpConfiguration,
        console: Optional[Console] = None,
    ) -> None:
        self._config = config
        self._console = console or get_default_console(config)


#     def write(self, string: str) -> None:
#         """Writes a unicode string into the internal buffer."""
#         self.buffer.append(string)

#     def indent(self) -> None:
#         """Increases the indentation."""
#         self.current_indent += self.indent_increment

#     def dedent(self) -> None:
#         """Decreases the indentation."""
#         self.current_indent -= self.indent_increment

#     def write_usage(self, prog: str, args: str = "", prefix: t.Optional[str] = None) -> None:
#         """Writes a usage line into the buffer.

#         :param prog: the program name.
#         :param args: whitespace separated list of arguments.
#         :param prefix: The prefix for the first line. Defaults to
#             ``"Usage: "``.
#         """
#         if prefix is None:
#             prefix = f"{_('Usage:')} "

#         usage_prefix = f"{prefix:>{self.current_indent}}{prog} "
#         text_width = self.width - self.current_indent

#         if text_width >= (term_len(usage_prefix) + 20):
#             # The arguments will fit to the right of the prefix.
#             indent = " " * term_len(usage_prefix)
#             self.write(
#                 wrap_text(
#                     args,
#                     text_width,
#                     initial_indent=usage_prefix,
#                     subsequent_indent=indent,
#                 )
#             )
#         else:
#             # The prefix is too long, put the arguments on the next line.
#             self.write(usage_prefix)
#             self.write("\n")
#             indent = " " * (max(self.current_indent, term_len(prefix)) + 4)
#             self.write(wrap_text(args, text_width, initial_indent=indent, subsequent_indent=indent))

#         self.write("\n")

#     def write_heading(self, heading: str) -> None:
#         """Writes a heading into the buffer."""
#         self.write(f"{'':>{self.current_indent}}{heading}:\n")

#     def write_paragraph(self) -> None:
#         """Writes a paragraph into the buffer."""
#         if self.buffer:
#             self.write("\n")

#     def write_text(self, text: str) -> None:
#         """Writes re-indented text into the buffer.  This rewraps and
#         preserves paragraphs.
#         """
#         indent = " " * self.current_indent
#         self.write(
#             wrap_text(
#                 text,
#                 self.width,
#                 initial_indent=indent,
#                 subsequent_indent=indent,
#                 preserve_paragraphs=True,
#             )
#         )
#         self.write("\n")

#     def write_dl(
#         self,
#         rows: t.Sequence[t.Tuple[str, str]],
#         col_max: int = 30,
#         col_spacing: int = 2,
#     ) -> None:
#         """Writes a definition list into the buffer.  This is how options
#         and commands are usually formatted.

#         :param rows: a list of two item tuples for the terms and values.
#         :param col_max: the maximum width of the first column.
#         :param col_spacing: the number of spaces between the first and
#                             second column.
#         """
#         rows = list(rows)
#         widths = measure_table(rows)
#         if len(widths) != 2:
#             raise TypeError("Expected two columns for definition list")

#         first_col = min(widths[0], col_max) + col_spacing

#         for first, second in iter_rows(rows, len(widths)):
#             self.write(f"{'':>{self.current_indent}}{first}")
#             if not second:
#                 self.write("\n")
#                 continue
#             if term_len(first) <= first_col - col_spacing:
#                 self.write(" " * (first_col - term_len(first)))
#             else:
#                 self.write("\n")
#                 self.write(" " * (first_col + self.current_indent))

#             text_width = max(self.width - first_col - 2, 10)
#             wrapped_text = wrap_text(second, text_width, preserve_paragraphs=True)
#             lines = wrapped_text.splitlines()

#             if lines:
#                 self.write(f"{lines[0]}\n")

#                 for line in lines[1:]:
#                     self.write(f"{'':>{first_col + self.current_indent}}{line}\n")
#             else:
#                 self.write("\n")

#     @contextmanager
#     def section(self, name: str) -> t.Iterator[None]:
#         """Helpful context manager that writes a paragraph, a heading,
#         and the indents.

#         :param name: the section name that is written as heading.
#         """
#         self.write_paragraph()
#         self.write_heading(name)
#         self.indent()
#         try:
#             yield
#         finally:
#             self.dedent()

#     @contextmanager
#     def indentation(self) -> t.Iterator[None]:
#         """A context manager that increases the indentation."""
#         self.indent()
#         try:
#             yield
#         finally:
#             self.dedent()

#     def getvalue(self) -> str:
#         """Returns the buffer contents."""
#         return "".join(self.buffer)
