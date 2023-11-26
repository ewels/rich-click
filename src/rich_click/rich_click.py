from typing import Any, Dict, List, Optional, Tuple, Union

import rich.text

# Due to how rich_click.cli.patch() works, it is safer to import Command types directly
# rather than use the click module e.g. click.Command
from click import Group
from typing_extensions import Literal

from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_9X
from rich_click.rich_help_configuration import force_terminal_default, OptionHighlighter, terminal_width_default

if CLICK_IS_BEFORE_VERSION_9X:
    pass
else:
    MultiCommand = Group  # type: ignore[misc,assignment,unused-ignore]


# Default styles
STYLE_OPTION: rich.style.StyleType = "bold cyan"
STYLE_ARGUMENT: rich.style.StyleType = "bold cyan"
STYLE_COMMAND: rich.style.StyleType = "bold cyan"
STYLE_SWITCH: rich.style.StyleType = "bold green"
STYLE_METAVAR: rich.style.StyleType = "bold yellow"
STYLE_METAVAR_APPEND: rich.style.StyleType = "dim yellow"
STYLE_METAVAR_SEPARATOR: rich.style.StyleType = "dim"
STYLE_HEADER_TEXT: rich.style.StyleType = ""
STYLE_FOOTER_TEXT: rich.style.StyleType = ""
STYLE_USAGE: rich.style.StyleType = "yellow"
STYLE_USAGE_COMMAND: rich.style.StyleType = "bold"
STYLE_DEPRECATED: rich.style.StyleType = "red"
STYLE_HELPTEXT_FIRST_LINE: rich.style.StyleType = ""
STYLE_HELPTEXT: rich.style.StyleType = "dim"
STYLE_OPTION_HELP: rich.style.StyleType = ""
STYLE_OPTION_DEFAULT: rich.style.StyleType = "dim"
STYLE_OPTION_ENVVAR: rich.style.StyleType = "dim yellow"
STYLE_REQUIRED_SHORT: rich.style.StyleType = "red"
STYLE_REQUIRED_LONG: rich.style.StyleType = "dim red"
STYLE_OPTIONS_PANEL_BORDER: rich.style.StyleType = "dim"
ALIGN_OPTIONS_PANEL: rich.align.AlignMethod = "left"
STYLE_OPTIONS_TABLE_SHOW_LINES: bool = False
STYLE_OPTIONS_TABLE_LEADING: int = 0
STYLE_OPTIONS_TABLE_PAD_EDGE: bool = False
STYLE_OPTIONS_TABLE_PADDING: rich.padding.PaddingDimensions = (0, 1)
STYLE_OPTIONS_TABLE_BOX: rich.style.StyleType = ""
STYLE_OPTIONS_TABLE_ROW_STYLES: Optional[List[rich.style.StyleType]] = None
STYLE_OPTIONS_TABLE_BORDER_STYLE: Optional[rich.style.StyleType] = None
STYLE_COMMANDS_PANEL_BORDER: rich.style.StyleType = "dim"
ALIGN_COMMANDS_PANEL: rich.align.AlignMethod = "left"
STYLE_COMMANDS_TABLE_SHOW_LINES: bool = False
STYLE_COMMANDS_TABLE_LEADING: int = 0
STYLE_COMMANDS_TABLE_PAD_EDGE: bool = False
STYLE_COMMANDS_TABLE_PADDING: rich.padding.PaddingDimensions = (0, 1)
STYLE_COMMANDS_TABLE_BOX: rich.style.StyleType = ""
STYLE_COMMANDS_TABLE_ROW_STYLES: Optional[List[rich.style.StyleType]] = None
STYLE_COMMANDS_TABLE_BORDER_STYLE: Optional[rich.style.StyleType] = None
STYLE_COMMANDS_TABLE_COLUMN_WIDTH_RATIO: Optional[Union[Tuple[None, None], Tuple[int, int]]] = (None, None)
STYLE_ERRORS_PANEL_BORDER: rich.style.StyleType = "red"
ALIGN_ERRORS_PANEL: rich.align.AlignMethod = "left"
STYLE_ERRORS_SUGGESTION: rich.style.StyleType = "dim"
STYLE_ERRORS_SUGGESTION_COMMAND: rich.style.StyleType = "blue"
STYLE_ABORTED: rich.style.StyleType = "red"
WIDTH: Optional[int] = terminal_width_default()
MAX_WIDTH: Optional[int] = terminal_width_default()
COLOR_SYSTEM: Optional[
    Literal["auto", "standard", "256", "truecolor", "windows"]
] = "auto"  # Set to None to disable colors
FORCE_TERMINAL: Optional[bool] = force_terminal_default()

# Fixed strings
HEADER_TEXT: Optional[str] = None
FOOTER_TEXT: Optional[str] = None
DEPRECATED_STRING: str = "(Deprecated) "
DEFAULT_STRING: str = "[default: {}]"
ENVVAR_STRING: str = "[env var: {}]"
REQUIRED_SHORT_STRING: str = "*"
REQUIRED_LONG_STRING: str = "[required]"
RANGE_STRING: str = " [{}]"
APPEND_METAVARS_HELP_STRING: str = "({})"
ARGUMENTS_PANEL_TITLE: str = "Arguments"
OPTIONS_PANEL_TITLE: str = "Options"
COMMANDS_PANEL_TITLE: str = "Commands"
ERRORS_PANEL_TITLE: str = "Error"
ERRORS_SUGGESTION: Optional[str] = None  # Default: Try 'cmd -h' for help. Set to False to disable.
ERRORS_EPILOGUE: Optional[str] = None
ABORTED_TEXT: str = "Aborted."

# Behaviours
SHOW_ARGUMENTS: bool = False  # Show positional arguments
SHOW_METAVARS_COLUMN: bool = True  # Show a column with the option metavar (eg. INTEGER)
APPEND_METAVARS_HELP: bool = False  # Append metavar (eg. [TEXT]) after the help text
GROUP_ARGUMENTS_OPTIONS: bool = False  # Show arguments with options instead of in own panel
OPTION_ENVVAR_FIRST: bool = False  # Show env vars before option help text instead of avert
USE_MARKDOWN: bool = False  # Parse help strings as markdown
USE_MARKDOWN_EMOJI: bool = True  # Parse emoji codes in markdown :smile:
USE_RICH_MARKUP: bool = False  # Parse help strings for rich markup (eg. [red]my text[/])
# Define sorted groups of panels to display subcommands
COMMAND_GROUPS: Dict[str, List[Dict[str, Union[str, List[str]]]]] = {}
# Define sorted groups of panels to display options and arguments
OPTION_GROUPS: Dict[str, List[Dict[str, Union[str, List[str], Dict[str, List[str]]]]]] = {}
USE_CLICK_SHORT_HELP: bool = False  # Use click's default function to truncate help text

highlighter: rich.highlighter.Highlighter = OptionHighlighter()


def __getattr__(name: str) -> Any:
    if name == "get_module_help_configuration":
        import warnings

        warnings.warn(
            "get_module_help_configuration() is deprecated." " Use RichHelpConfiguration.build_from_globals() instead.",
            DeprecationWarning,
        )
        from rich_click.rich_help_configuration import RichHelpConfiguration

        return RichHelpConfiguration.build_from_globals
    elif name in {
        "_make_rich_rext",
        "_get_help_text",
        "_get_option_help",
        "_make_command_help",
        "get_rich_usage",
        "rich_format_help",
        "rich_format_error",
        "rich_abort_error",
    }:
        import warnings

        warnings.warn(
            f"{name}() is no longer located in the `rich_click` module." " It is now in the `rich_markup` module.",
            DeprecationWarning,
        )
        import rich_click.rich_markup

        return getattr(rich_click.rich_markup, name)
    else:
        raise AttributeError
