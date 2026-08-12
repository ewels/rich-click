from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from rich_click.rich_help_configuration import (
    FROM_THEME,
    CommandColumnType,
    CommandHelpSectionType,
    OptionColumnType,
    OptionHelpSectionType,
    force_terminal_default,
    terminal_width_default,
)
from rich_click.utils import CommandGroupDict, OptionGroupDict, notset


if TYPE_CHECKING:  # pragma: no cover
    from rich.align import AlignMethod
    from rich.box import Box
    from rich.padding import PaddingDimensions
    from rich.style import StyleType
    from rich.text import Text

    from rich_click.rich_click_theme import RichClickTheme

#!STARTCONFIG

# Default styles
THEME: str | RichClickTheme | None = None
ENABLE_THEME_ENV_VAR: bool = True

STYLE_OPTION: StyleType = FROM_THEME
STYLE_OPTION_NEGATIVE: StyleType | None = FROM_THEME
STYLE_ARGUMENT: StyleType = FROM_THEME
STYLE_COMMAND: StyleType = FROM_THEME
STYLE_COMMAND_ALIASES: StyleType = FROM_THEME
STYLE_SWITCH: StyleType = FROM_THEME
STYLE_SWITCH_NEGATVE: StyleType | None = FROM_THEME
STYLE_METAVAR: StyleType = FROM_THEME
STYLE_METAVAR_APPEND: StyleType = FROM_THEME
STYLE_METAVAR_SEPARATOR: StyleType = FROM_THEME
STYLE_RANGE_APPEND: StyleType = FROM_THEME
STYLE_USAGE: StyleType = FROM_THEME
STYLE_USAGE_COMMAND: StyleType = FROM_THEME
STYLE_USAGE_SEPARATOR: StyleType = FROM_THEME
STYLE_DEPRECATED: StyleType = FROM_THEME
STYLE_HELPTEXT_FIRST_LINE: StyleType = FROM_THEME
STYLE_HELPTEXT: StyleType = FROM_THEME
STYLE_HELPTEXT_ALIASES: StyleType | None = None
STYLE_OPTION_HELP: StyleType = FROM_THEME
STYLE_COMMAND_HELP: StyleType = FROM_THEME
STYLE_OPTION_DEFAULT: StyleType = FROM_THEME
STYLE_OPTION_ENVVAR: StyleType = FROM_THEME
STYLE_REQUIRED_SHORT: StyleType = FROM_THEME
STYLE_REQUIRED_LONG: StyleType = FROM_THEME
STYLE_OPTIONS_PANEL_BORDER: StyleType = FROM_THEME
STYLE_OPTIONS_PANEL_BOX: str | Box | None = FROM_THEME
STYLE_OPTIONS_PANEL_HELP_STYLE: StyleType = FROM_THEME
STYLE_OPTIONS_PANEL_TITLE_STYLE: StyleType = FROM_THEME
STYLE_OPTIONS_PANEL_PADDING: PaddingDimensions = FROM_THEME
STYLE_OPTIONS_PANEL_STYLE: StyleType = FROM_THEME
ALIGN_OPTIONS_PANEL: AlignMethod = "left"
STYLE_OPTIONS_TABLE_SHOW_LINES: bool = False
STYLE_OPTIONS_TABLE_LEADING: int = 0
STYLE_OPTIONS_TABLE_PAD_EDGE: bool = False
STYLE_OPTIONS_TABLE_PADDING: PaddingDimensions = (0, 1)
STYLE_OPTIONS_TABLE_EXPAND: bool = FROM_THEME
STYLE_OPTIONS_TABLE_BOX: str | Box | None = FROM_THEME
STYLE_OPTIONS_TABLE_ROW_STYLES: list[StyleType] | None = None
STYLE_OPTIONS_TABLE_BORDER_STYLE: StyleType | None = FROM_THEME
STYLE_COMMANDS_PANEL_BORDER: StyleType = FROM_THEME
PANEL_INLINE_HELP_IN_TITLE: bool = FROM_THEME
PANEL_INLINE_HELP_DELIMITER: str = FROM_THEME
STYLE_COMMANDS_PANEL_BOX: str | Box | None = FROM_THEME
STYLE_COMMANDS_PANEL_HELP_STYLE: StyleType = FROM_THEME
STYLE_COMMANDS_PANEL_TITLE_STYLE: StyleType = FROM_THEME
STYLE_COMMANDS_PANEL_PADDING: PaddingDimensions = FROM_THEME
STYLE_COMMANDS_PANEL_STYLE: StyleType = FROM_THEME
ALIGN_COMMANDS_PANEL: AlignMethod = "left"
STYLE_COMMANDS_TABLE_SHOW_LINES: bool = False
STYLE_COMMANDS_TABLE_LEADING: int = 0
STYLE_COMMANDS_TABLE_PAD_EDGE: bool = False
STYLE_COMMANDS_TABLE_PADDING: PaddingDimensions = (0, 1)
STYLE_COMMANDS_TABLE_EXPAND: bool = FROM_THEME
STYLE_COMMANDS_TABLE_BOX: str | Box | None = FROM_THEME
STYLE_COMMANDS_TABLE_ROW_STYLES: list[StyleType] | None = None
STYLE_COMMANDS_TABLE_BORDER_STYLE: StyleType | None = FROM_THEME
STYLE_COMMANDS_TABLE_COLUMN_WIDTH_RATIO: tuple[None, None] | tuple[int, int] | None = (None, None)
STYLE_ERRORS_PANEL_BORDER: StyleType = FROM_THEME
STYLE_ERRORS_PANEL_BOX: str | Box | None = FROM_THEME
ALIGN_ERRORS_PANEL: AlignMethod = "left"
STYLE_ERRORS_SUGGESTION: StyleType | None = None
STYLE_ERRORS_SUGGESTION_COMMAND: StyleType | None = None
STYLE_PADDING_ERRORS: StyleType = FROM_THEME
STYLE_ABORTED: StyleType = "red"
STYLE_PADDING_USAGE: StyleType = FROM_THEME
STYLE_PADDING_HELPTEXT: StyleType = FROM_THEME
STYLE_PADDING_EPILOG: StyleType = FROM_THEME
STYLE_HEADER_TEXT: StyleType = FROM_THEME
STYLE_EPILOG_TEXT: StyleType = FROM_THEME
STYLE_FOOTER_TEXT: StyleType = FROM_THEME

PANEL_TITLE_PADDING: int = FROM_THEME
WIDTH: int | None = terminal_width_default()
MAX_WIDTH: int | None = terminal_width_default()
COLOR_SYSTEM: Literal["auto", "standard", "256", "truecolor", "windows"] | None = (
    "auto"  # Set to None to disable colors
)
FORCE_TERMINAL: bool | None = force_terminal_default()

OPTIONS_TABLE_COLUMN_TYPES: list[OptionColumnType] = FROM_THEME
COMMANDS_TABLE_COLUMN_TYPES: list[CommandColumnType] = FROM_THEME

OPTIONS_TABLE_HELP_SECTIONS: list[OptionHelpSectionType] = FROM_THEME
COMMANDS_TABLE_HELP_SECTIONS: list[CommandHelpSectionType] = FROM_THEME

# Fixed strings
HEADER_TEXT: str | Text | None = None
FOOTER_TEXT: str | Text | None = None
PANEL_TITLE_STRING: str = FROM_THEME
DEPRECATED_STRING: str = FROM_THEME
DEPRECATED_WITH_REASON_STRING: str = FROM_THEME
DEFAULT_STRING: str = FROM_THEME
ENVVAR_STRING: str = FROM_THEME
REQUIRED_SHORT_STRING: str = FROM_THEME
REQUIRED_LONG_STRING: str = FROM_THEME
RANGE_STRING: str = FROM_THEME
APPEND_METAVARS_HELP_STRING: str = FROM_THEME
APPEND_RANGE_HELP_STRING: str = FROM_THEME
HELPTEXT_ALIASES_STRING: str = "Aliases: {}"
ARGUMENTS_PANEL_TITLE: str = "Arguments"
OPTIONS_PANEL_TITLE: str = "Options"
COMMANDS_PANEL_TITLE: str = "Commands"
ERRORS_PANEL_TITLE: str = "Error"
DELIMITER_COMMA: str = FROM_THEME
DELIMITER_SLASH: str = FROM_THEME
ERRORS_SUGGESTION: str | Text | None = None  # Default: Try 'cmd -h' for help. Set to False to disable.
ERRORS_EPILOGUE: str | Text | None = None
ABORTED_TEXT: str = "Aborted."

PADDING_HEADER_TEXT: PaddingDimensions = FROM_THEME
PADDING_USAGE: PaddingDimensions = FROM_THEME
PADDING_HELPTEXT: PaddingDimensions = FROM_THEME
PADDING_HELPTEXT_DEPRECATED: PaddingDimensions = 0
PADDING_HELPTEXT_FIRST_LINE: PaddingDimensions = 0
PADDING_EPILOG: PaddingDimensions = FROM_THEME
PADDING_FOOTER_TEXT: PaddingDimensions = FROM_THEME
PADDING_ERRORS_PANEL: PaddingDimensions = (0, 0, 1, 0)
PADDING_ERRORS_SUGGESTION: PaddingDimensions = (0, 1, 0, 1)
PADDING_ERRORS_EPILOGUE: PaddingDimensions = (0, 1, 1, 1)

# Behaviours
SHOW_ARGUMENTS: bool | None = None  # Show positional arguments
SHOW_METAVARS_COLUMN: bool | None = None  # Show a column with the option metavar (eg. INTEGER)
COMMANDS_BEFORE_OPTIONS: bool = False  # If set, the commands panel show above the options panel.
DEFAULT_PANELS_FIRST: bool = False  # If set, default panels appear before custom panels of the same type.
APPEND_METAVARS_HELP: bool | None = None  # Append metavar (eg. [TEXT]) after the help text
GROUP_ARGUMENTS_OPTIONS: bool = False  # Show arguments with options instead of in own panel
OPTION_ENVVAR_FIRST: bool | None = None  # Show env vars before option help text instead of avert
TEXT_MARKUP: Literal["ansi", "rich", "markdown", None] = notset
TEXT_KWARGS: dict[str, Any] | None = None
TEXT_EMOJIS: bool = notset
TEXT_PARAGRAPH_LINEBREAKS: Literal["\n", "\n\n"] | None = None
# If set, parse emoji codes and replace with actual emojis, e.g. :smiley_cat: -> 😺
USE_MARKDOWN: bool | None = None  # Parse help strings as markdown
USE_MARKDOWN_EMOJI: bool | None = None  # Parse emoji codes in markdown :smile:
USE_RICH_MARKUP: bool | None = None  # Parse help strings for rich markup (eg. [red]my text[/])
# Define sorted groups of panels to display subcommands
COMMAND_GROUPS: dict[str, list[CommandGroupDict]] = {}
# Define sorted groups of panels to display options and arguments
OPTION_GROUPS: dict[str, list[OptionGroupDict]] = {}
USE_CLICK_SHORT_HELP: bool = False  # Use click's default function to truncate help text
HELPTEXT_SHOW_ALIASES: bool = True

#!ENDCONFIG

_THEME_FROM_CLI: str | None = None


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
