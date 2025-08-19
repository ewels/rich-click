from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Tuple, Union

from rich_click.rich_help_configuration import force_terminal_default, terminal_width_default
from rich_click.utils import CommandGroupDict, OptionGroupDict, notset


if TYPE_CHECKING:  # pragma: no cover
    import rich.align
    import rich.box
    import rich.color
    import rich.padding
    import rich.style
    import rich.text
    from rich.padding import PaddingDimensions


# Default styles
THEME: Optional[str] = None
ENABLE_THEME_ENV_VAR: bool = True

STYLE_OPTION: "rich.style.StyleType" = "bold cyan"
STYLE_ARGUMENT: "rich.style.StyleType" = "bold cyan"
STYLE_COMMAND: "rich.style.StyleType" = "bold cyan"
STYLE_SWITCH: "rich.style.StyleType" = "bold green"
STYLE_METAVAR: "rich.style.StyleType" = "bold yellow"
STYLE_METAVAR_APPEND: "rich.style.StyleType" = "dim yellow"
STYLE_METAVAR_SEPARATOR: "rich.style.StyleType" = "dim"
STYLE_HEADER_TEXT: "rich.style.StyleType" = ""
STYLE_EPILOG_TEXT: "rich.style.StyleType" = ""
STYLE_FOOTER_TEXT: "rich.style.StyleType" = ""
STYLE_USAGE: "rich.style.StyleType" = "yellow"
STYLE_USAGE_COMMAND: "rich.style.StyleType" = "bold"
STYLE_DEPRECATED: "rich.style.StyleType" = "red"
STYLE_HELPTEXT_FIRST_LINE: "rich.style.StyleType" = ""
STYLE_HELPTEXT: "rich.style.StyleType" = "dim"
STYLE_OPTION_HELP: "rich.style.StyleType" = ""
STYLE_OPTION_DEFAULT: "rich.style.StyleType" = "dim"
STYLE_OPTION_ENVVAR: "rich.style.StyleType" = "dim yellow"
STYLE_REQUIRED_SHORT: "rich.style.StyleType" = "red"
STYLE_REQUIRED_LONG: "rich.style.StyleType" = "dim red"
STYLE_OPTIONS_PANEL_BORDER: "rich.style.StyleType" = "dim"
STYLE_OPTIONS_PANEL_INLINE_HELP_IN_TITLE: bool = False
STYLE_OPTIONS_PANEL_BOX: Optional[Union[str, "rich.box.Box"]] = "ROUNDED"
STYLE_OPTIONS_PANEL_HELP_STYLE: "rich.style.StyleType" = ""
STYLE_OPTIONS_PANEL_TITLE_STYLE: "rich.style.StyleType" = ""
STYLE_OPTIONS_PANEL_PADDING: "rich.padding.PaddingDimensions" = (0, 1)
ALIGN_OPTIONS_PANEL: "rich.align.AlignMethod" = "left"
STYLE_OPTIONS_TABLE_SHOW_LINES: bool = False
STYLE_OPTIONS_TABLE_LEADING: int = 0
STYLE_OPTIONS_TABLE_PAD_EDGE: bool = False
STYLE_OPTIONS_TABLE_PADDING: "rich.padding.PaddingDimensions" = (0, 1)
STYLE_OPTIONS_TABLE_BOX: Optional[Union[str, "rich.box.Box"]] = None
STYLE_OPTIONS_TABLE_ROW_STYLES: Optional[List["rich.style.StyleType"]] = None
STYLE_OPTIONS_TABLE_BORDER_STYLE: Optional["rich.style.StyleType"] = None
STYLE_COMMANDS_PANEL_BORDER: "rich.style.StyleType" = "dim"
STYLE_COMMANDS_PANEL_INLINE_HELP_IN_TITLE: bool = False
STYLE_COMMANDS_PANEL_BOX: Optional[Union[str, "rich.box.Box"]] = "ROUNDED"
STYLE_COMMANDS_PANEL_HELP_STYLE: "rich.style.StyleType" = ""
STYLE_COMMANDS_PANEL_TITLE_STYLE: "rich.style.StyleType" = ""
STYLE_COMMANDS_PANEL_PADDING: "rich.padding.PaddingDimensions" = (0, 1)
ALIGN_COMMANDS_PANEL: "rich.align.AlignMethod" = "left"
STYLE_COMMANDS_TABLE_SHOW_LINES: bool = False
STYLE_COMMANDS_TABLE_LEADING: int = 0
STYLE_COMMANDS_TABLE_PAD_EDGE: bool = False
STYLE_COMMANDS_TABLE_PADDING: "rich.padding.PaddingDimensions" = (0, 1)
STYLE_COMMANDS_TABLE_BOX: Optional[Union[str, "rich.box.Box"]] = None
STYLE_COMMANDS_TABLE_ROW_STYLES: Optional[List["rich.style.StyleType"]] = None
STYLE_COMMANDS_TABLE_BORDER_STYLE: Optional["rich.style.StyleType"] = None
STYLE_COMMANDS_TABLE_COLUMN_WIDTH_RATIO: Optional[Union[Tuple[None, None], Tuple[int, int]]] = (None, None)
STYLE_ERRORS_PANEL_BORDER: "rich.style.StyleType" = "red"
STYLE_ERRORS_PANEL_BOX: Optional[Union[str, "rich.box.Box"]] = "ROUNDED"
ALIGN_ERRORS_PANEL: "rich.align.AlignMethod" = "left"
STYLE_ERRORS_SUGGESTION: "rich.style.StyleType" = "dim"
STYLE_ERRORS_SUGGESTION_COMMAND: "rich.style.StyleType" = "blue"
STYLE_ABORTED: "rich.style.StyleType" = "red"
WIDTH: Optional[int] = terminal_width_default()
MAX_WIDTH: Optional[int] = terminal_width_default()
COLOR_SYSTEM: Optional[Literal["auto", "standard", "256", "truecolor", "windows"]] = (
    "auto"  # Set to None to disable colors
)
FORCE_TERMINAL: Optional[bool] = force_terminal_default()

# Fixed strings
HEADER_TEXT: Optional[Union[str, "rich.text.Text"]] = None
FOOTER_TEXT: Optional[Union[str, "rich.text.Text"]] = None
DEPRECATED_STRING: str = "[deprecated]"
DEPRECATED_WITH_REASON_STRING: str = "[deprecated: {}]"
DEFAULT_STRING: str = "[default: {}]"
ENVVAR_STRING: str = "[env var: {}]"
REQUIRED_SHORT_STRING: str = "*"
REQUIRED_LONG_STRING: str = "[required]"
RANGE_STRING: str = " [{}]"
APPEND_METAVARS_HELP_STRING: str = "[{}]"
ARGUMENTS_PANEL_TITLE: str = "Arguments"
OPTIONS_PANEL_TITLE: str = "Options"
COMMANDS_PANEL_TITLE: str = "Commands"
ERRORS_PANEL_TITLE: str = "Error"
ERRORS_SUGGESTION: Optional[Union[str, "rich.text.Text"]] = (
    None  # Default: Try 'cmd -h' for help. Set to False to disable.
)
ERRORS_EPILOGUE: Optional[Union[str, "rich.text.Text"]] = None
ABORTED_TEXT: str = "Aborted."

PADDING_HEADER_TEXT: "PaddingDimensions" = (1, 1, 0, 1)
PADDING_USAGE: "PaddingDimensions" = 1
PADDING_HELPTEXT: "PaddingDimensions" = (0, 1, 1, 1)
PADDING_HELPTEXT_DEPRECATED: "PaddingDimensions" = 0
PADDING_HELPTEXT_FIRST_LINE: "PaddingDimensions" = 0
PADDING_EPILOG: "PaddingDimensions" = 1
PADDING_FOOTER_TEXT: "PaddingDimensions" = (1, 1, 0, 1)
PADDING_ERRORS_PANEL: "PaddingDimensions" = (0, 0, 1, 0)
PADDING_ERRORS_SUGGESTION: "PaddingDimensions" = (0, 1, 0, 1)
PADDING_ERRORS_EPILOGUE: "PaddingDimensions" = (0, 1, 1, 1)

# Behaviours
SHOW_ARGUMENTS: Optional[bool] = None  # Show positional arguments
SHOW_METAVARS_COLUMN: Optional[bool] = None  # Show a column with the option metavar (eg. INTEGER)
COMMANDS_BEFORE_OPTIONS: bool = False  # If set, the commands panel show above the options panel.
APPEND_METAVARS_HELP: bool = False  # Append metavar (eg. [TEXT]) after the help text
GROUP_ARGUMENTS_OPTIONS: bool = False  # Show arguments with options instead of in own panel
OPTION_ENVVAR_FIRST: bool = False  # Show env vars before option help text instead of avert
TEXT_MARKUP: Literal["ansi", "rich", "markdown", None] = notset  # type: ignore[assignment]
TEXT_KWARGS: Optional[Dict[str, Any]] = None
TEXT_EMOJIS: bool = notset  # type: ignore[assignment]
TEXT_PARAGRAPH_LINEBREAKS: Optional[str] = None
# If set, parse emoji codes and replace with actual emojis, e.g. :smiley_cat: -> 😺
USE_MARKDOWN: Optional[bool] = None  # Parse help strings as markdown
USE_MARKDOWN_EMOJI: Optional[bool] = None  # Parse emoji codes in markdown :smile:
USE_RICH_MARKUP: Optional[bool] = None  # Parse help strings for rich markup (eg. [red]my text[/])
# Define sorted groups of panels to display subcommands
COMMAND_GROUPS: Dict[str, List[CommandGroupDict]] = {}
# Define sorted groups of panels to display options and arguments
OPTION_GROUPS: Dict[str, List[OptionGroupDict]] = {}
USE_CLICK_SHORT_HELP: bool = False  # Use click's default function to truncate help text


def __getattr__(name: str) -> Any:
    if name == "get_module_help_configuration":
        import warnings

        warnings.warn(
            "get_module_help_configuration() is deprecated. Use RichHelpConfiguration.load_from_globals() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        from rich_click.rich_help_configuration import RichHelpConfiguration

        return RichHelpConfiguration.load_from_globals
    if name == "highlighter":
        import warnings

        warnings.warn(
            "`highlighter` config option is deprecated."
            " Please do one of the following instead: either set HIGHLIGHTER_PATTERNS = [...] if you want"
            " to use regex; or for more advanced use cases where you'd like to use a different type"
            " of rich.highlighter.Highlighter, subclass the `RichHelpFormatter` and update its `highlighter`.",
            DeprecationWarning,
            stacklevel=2,
        )

        from rich_click.rich_help_configuration import OptionHighlighter

        globals()["highlighter"] = highlighter = OptionHighlighter()
        return highlighter

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
            f"{name}() is no longer located in the `rich_click` module. It is now in the `rich_help_rendering` module.",
            DeprecationWarning,
            stacklevel=2,
        )
        import rich_click.rich_help_rendering

        return getattr(rich_click.rich_help_rendering, name)
    else:
        raise AttributeError
