from __future__ import annotations

import json
import os
from dataclasses import MISSING, dataclass, field
from types import ModuleType
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Tuple, TypeVar, Union

from rich_click.rich_theme import THEMES
from rich_click.utils import CommandGroupDict, OptionGroupDict, notset, truthy


if TYPE_CHECKING:  # pragma: no cover
    import rich.align
    import rich.box
    import rich.highlighter
    import rich.padding
    import rich.style
    import rich.text
    from rich.padding import PaddingDimensions


T = TypeVar("T", bound="RichHelpConfiguration")


OptionColumnType = Literal[
    "required",
    "opt_primary",
    "opt_secondary",
    "opt_long",
    "opt_short",
    "opt_all",
    "metavar",
    "help",
    "default",
    "envvar",
]

CommandColumnType = Literal["name", "help"]

ColumnType = Union[OptionColumnType, CommandColumnType]


def force_terminal_default() -> Optional[bool]:
    """Use as the default factory for `force_terminal`."""
    env_vars = ["FORCE_COLOR", "PY_COLORS", "GITHUB_ACTIONS"]
    for env_var in env_vars:
        if env_var in os.environ:
            return truthy(os.getenv(env_var))
    else:
        return None


def terminal_width_default() -> Optional[int]:
    """Use as the default factory for `width` and `max_width`."""
    width = os.getenv("TERMINAL_WIDTH")
    if width:
        try:
            return int(width)
        except ValueError:
            import warnings

            warnings.warn(
                "Environment variable `TERMINAL_WIDTH` cannot be cast to an integer.", UserWarning, stacklevel=2
            )
            return None
    return None


@dataclass
class RichHelpConfiguration:
    """
    Rich Help Configuration class.

    When merging multiple RichHelpConfigurations together, user-defined values always
    take precedence over the class's defaults. When there are multiple user-defined values
    for a given field, the right-most field is used.
    """

    theme: Optional[str] = field(default=None)
    enable_theme_env_var: bool = field(default=True)

    # Default styles
    style_option: "rich.style.StyleType" = field(default="bold cyan")
    style_argument: "rich.style.StyleType" = field(default="bold cyan")
    style_command: "rich.style.StyleType" = field(default="bold cyan")
    style_switch: "rich.style.StyleType" = field(default="bold green")
    style_metavar: "rich.style.StyleType" = field(default="bold yellow")
    style_metavar_append: "rich.style.StyleType" = field(default="dim yellow")
    style_metavar_separator: "rich.style.StyleType" = field(default="dim")
    style_header_text: "rich.style.StyleType" = field(default="")
    style_epilog_text: "rich.style.StyleType" = field(default="")
    style_footer_text: "rich.style.StyleType" = field(default="")
    style_usage: "rich.style.StyleType" = field(default="yellow")
    style_usage_command: "rich.style.StyleType" = field(default="bold")
    style_deprecated: "rich.style.StyleType" = field(default="red")
    style_helptext_first_line: "rich.style.StyleType" = field(default="")
    style_helptext: "rich.style.StyleType" = field(default="dim")
    style_option_help: "rich.style.StyleType" = field(default="")
    style_option_default: "rich.style.StyleType" = field(default="dim")
    style_option_envvar: "rich.style.StyleType" = field(default="dim yellow")
    style_required_short: "rich.style.StyleType" = field(default="red")
    style_required_long: "rich.style.StyleType" = field(default="dim red")
    style_options_panel_border: "rich.style.StyleType" = field(default="dim")
    style_options_panel_inline_help_in_title: bool = field(default=False)
    style_options_panel_box: Optional[Union[str, "rich.box.Box"]] = field(default="ROUNDED")
    style_options_panel_help_style: "rich.style.StyleType" = field(default="")
    style_options_panel_title_style: "rich.style.StyleType" = field(default="")
    style_options_panel_padding: "rich.padding.PaddingDimensions" = field(default=(0, 1))
    align_options_panel: "rich.align.AlignMethod" = field(default="left")
    style_options_table_show_lines: bool = field(default=False)
    style_options_table_leading: int = field(default=0)
    style_options_table_pad_edge: bool = field(default=False)
    style_options_table_padding: "rich.padding.PaddingDimensions" = field(default_factory=lambda: (0, 1))
    style_options_table_box: Optional[Union[str, "rich.box.Box"]] = field(default=None)
    style_options_table_row_styles: Optional[List["rich.style.StyleType"]] = field(default=None)
    style_options_table_border_style: Optional["rich.style.StyleType"] = field(default=None)
    style_commands_panel_border: "rich.style.StyleType" = field(default="dim")
    style_commands_panel_inline_help_in_title: bool = field(default=False)
    style_commands_panel_box: Optional[Union[str, "rich.box.Box"]] = field(default="ROUNDED")
    style_commands_panel_help_style: "rich.style.StyleType" = field(default="")
    style_commands_panel_title_style: "rich.style.StyleType" = field(default="")
    style_commands_panel_padding: "rich.padding.PaddingDimensions" = field(default=(0, 1))
    align_commands_panel: "rich.align.AlignMethod" = field(default="left")
    style_commands_table_show_lines: bool = field(default=False)
    style_commands_table_leading: int = field(default=0)
    style_commands_table_pad_edge: bool = field(default=False)
    style_commands_table_padding: "rich.padding.PaddingDimensions" = field(default_factory=lambda: (0, 1))
    style_commands_table_box: Optional[Union[str, "rich.box.Box"]] = field(default=None)
    style_commands_table_row_styles: Optional[List["rich.style.StyleType"]] = field(default=None)
    style_commands_table_border_style: Optional["rich.style.StyleType"] = field(default=None)
    style_commands_table_column_width_ratio: Optional[Union[Tuple[None, None], Tuple[int, int]]] = field(
        default_factory=lambda: (None, None)
    )
    style_errors_panel_border: "rich.style.StyleType" = field(default="red")
    style_errors_panel_box: Optional[Union[str, "rich.box.Box"]] = field(default="ROUNDED")
    align_errors_panel: "rich.align.AlignMethod" = field(default="left")
    style_errors_suggestion: "rich.style.StyleType" = field(default="dim")
    style_errors_suggestion_command: "rich.style.StyleType" = field(default="blue")
    style_aborted: "rich.style.StyleType" = field(default="red")
    width: Optional[int] = field(default_factory=terminal_width_default)
    max_width: Optional[int] = field(default_factory=terminal_width_default)
    color_system: Optional[Literal["auto", "standard", "256", "truecolor", "windows"]] = field(default="auto")
    force_terminal: Optional[bool] = field(default_factory=force_terminal_default)

    options_table_columns: List[OptionColumnType] = field(
        default_factory=lambda: ["required", "opt_long", "opt_short", "metavar", "help"]
    )
    arguments_table_columns: List[OptionColumnType] = field(
        default_factory=lambda: ["required", "opt_long", "opt_short", "metavar", "help"]
    )
    commands_table_columns: List[CommandColumnType] = field(default_factory=lambda: ["name", "help"])

    # Fixed strings
    header_text: Optional[Union[str, "rich.text.Text"]] = field(default=None)
    footer_text: Optional[Union[str, "rich.text.Text"]] = field(default=None)
    deprecated_string: str = field(default="[deprecated]")
    deprecated_with_reason_string: str = field(default="[deprecated: {}]")
    default_string: str = field(default="[default: {}]")
    envvar_string: str = field(default="[env var: {}]")
    required_short_string: str = field(default="*")
    required_long_string: str = field(default="[required]")
    range_string: str = field(default=" [{}]")
    append_metavars_help_string: str = field(default="[{}]")
    arguments_panel_title: str = field(default="Arguments")
    options_panel_title: str = field(default="Options")
    commands_panel_title: str = field(default="Commands")
    errors_panel_title: str = field(default="Error")
    errors_suggestion: Optional[Union[str, "rich.text.Text"]] = field(default=None)
    """Defaults to Try 'cmd -h' for help. Set to False to disable."""
    errors_epilogue: Optional[Union[str, "rich.text.Text"]] = field(default=None)
    aborted_text: str = field(default="Aborted.")

    padding_header_text: "PaddingDimensions" = (1, 1, 0, 1)
    padding_usage: "PaddingDimensions" = field(default=1)
    padding_helptext: "PaddingDimensions" = field(default=(0, 1, 1, 1))
    padding_helptext_deprecated: "PaddingDimensions" = field(default=0)
    padding_helptext_first_line: "PaddingDimensions" = field(default=0)
    padding_epilog: "PaddingDimensions" = field(default=1)
    padding_footer_text: "PaddingDimensions" = field(default=(1, 1, 0, 1))
    padding_errors_panel: "PaddingDimensions" = field(default=(0, 0, 1, 0))
    padding_errors_suggestion: "PaddingDimensions" = field(default=(0, 1, 0, 1))
    padding_errors_epilogue: "PaddingDimensions" = field(default=(0, 1, 1, 1))

    # Behaviours
    show_arguments: Optional[bool] = field(default=None)
    """Show positional arguments"""
    show_metavars_column: Optional[bool] = field(default=None)
    """Show a column with the option metavar (eg. INTEGER)"""
    commands_before_options: bool = field(default=False)
    """If set, the commands panel show above the options panel."""
    append_metavars_help: bool = field(default=False)
    """Append metavar (eg. [TEXT]) after the help text"""
    group_arguments_options: bool = field(default=False)
    """Show arguments with options instead of in own panel"""
    option_envvar_first: bool = field(default=False)
    """Show env vars before option help text instead of after"""
    text_markup: Literal["ansi", "rich", "markdown", None] = field(default=notset)  # type: ignore[arg-type]
    """What engine to use to render the text. Default is 'ansi'."""
    text_kwargs: Optional[Dict[str, Any]] = field(default=None)
    """Additional kwargs to pass to Rich text rendering. Kwargs differ by text_markup chosen."""
    text_paragraph_linebreaks: Optional[str] = field(default=None)
    text_emojis: bool = field(default=notset)  # type: ignore[assignment]
    """If set, parse emoji codes and replace with actual emojis, e.g. :smiley_cat: -> 😺"""
    use_markdown: Optional[bool] = field(default=None)
    """Silently deprecated; use `text_markup` field instead."""
    use_markdown_emoji: Optional[bool] = field(default=None)
    """Silently deprecated; use `text_emojis` instead."""
    use_rich_markup: Optional[bool] = field(default=None)
    """Silently deprecated; use `text_markup` field instead."""
    command_groups: Dict[str, List[CommandGroupDict]] = field(default_factory=lambda: {})
    """Define sorted groups of panels to display subcommands"""
    option_groups: Dict[str, List[OptionGroupDict]] = field(default_factory=lambda: {})
    """Define sorted groups of panels to display options and arguments"""
    use_click_short_help: bool = field(default=False)
    """Use click's default function to truncate help text"""
    highlighter: Optional["rich.highlighter.Highlighter"] = field(default=None, repr=False, compare=False)
    """(Deprecated) Rich regex highlighter for help highlighting"""

    highlighter_patterns: List[str] = field(
        default_factory=lambda: [
            r"(^|[^\w\-])(?P<switch>-([^\W0-9][\w\-]*\w|[^\W0-9]))",
            r"(^|[^\w\-])(?P<option>--([^\W0-9][\w\-]*\w|[^\W0-9]))",
            r"(?P<metavar><[^>]+>)",
            r"(?P<deprecated>\(DEPRECATED(?:\: .*?)?\))$",
        ]
    )
    """Patterns to use with the option highlighter."""

    legacy_windows: Optional[bool] = field(default=None)

    def __post_init__(self) -> None:  # noqa: D105

        if self.highlighter is not None:
            import warnings

            warnings.warn(
                "`highlighter` kwarg is deprecated in RichHelpConfiguration."
                " Please do one of the following instead: either set highlighter_patterns=[...] if you want"
                " to use regex; or for more advanced use cases where you'd like to use a different type"
                " of rich.highlighter.Highlighter, subclass the `RichHelpFormatter` and update its `highlighter`.",
                DeprecationWarning,
                stacklevel=2,
            )

        if self.use_markdown is not None:
            import warnings

            warnings.warn(
                "`use_markdown=` will be deprecated in a future version of rich-click."
                " Please use `text_markup=` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        if self.use_rich_markup is not None:
            import warnings

            warnings.warn(
                "`use_rich_markup=` will be deprecated in a future version of rich-click."
                " Please use `text_markup=` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        if self.text_markup is notset:
            if self.use_markdown:
                self.text_markup = "markdown"
            elif self.use_rich_markup:
                self.text_markup = "rich"
            else:
                self.text_markup = "ansi"

        if self.show_metavars_column is not None:
            import warnings

            warnings.warn(
                "`show_metavars_column=` will be deprecated in a future version of rich-click."
                " Please use `options_table_columns=` instead."
                " The `option_table_columns` config option lets you specify an ordered list"
                " of which columns are rendered.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
            if self.show_metavars_column is False:
                self.options_table_columns.remove("metavar")

        if self.use_markdown_emoji is not None:
            import warnings

            warnings.warn(
                "`use_markdown_emoji=` will be deprecated in a future version of rich-click."
                " Please use `text_emojis=` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
            if self.text_emojis is notset:
                self.text_emojis = self.use_markdown_emoji
        elif self.text_emojis is notset:
            self.text_emojis = self.text_markup in {"markdown", "rich"}

        self.__dataclass_fields__.pop("highlighter", None)

        if self.enable_theme_env_var and self.theme is None:
            self.theme = os.environ.get("RICH_CLICK_THEME")

        # Apply theme if specified
        if self.theme:
            try:
                if self.theme.strip().startswith("{"):
                    data = json.loads(self.theme.strip())
                    for k, v in data.items():
                        if hasattr(self, k):
                            setattr(self, k, v)
                        else:
                            raise TypeError(f"'{type(self)}' has no attribute '{k}'")
            except Exception as e:
                import warnings

                warnings.warn(f"RICH_CLICK_THEME= failed to parse: {e.__class__.__name__}{e.args}", UserWarning)
        theme_settings = THEMES.get(self.theme)  # type: ignore[arg-type]
        if theme_settings:
            for k, v in theme_settings.items():
                current = getattr(self, k)
                default = self.__dataclass_fields__[k].default

                # Only override default theme if the user didn't provide a theme value.
                if current == default or default is MISSING:
                    setattr(self, k, v)

    @classmethod
    def load_from_globals(cls, module: Optional[ModuleType] = None, **extra: Any) -> "RichHelpConfiguration":
        """
        Build a RichHelpConfiguration from globals in rich_click.rich_click.

        When building from globals, all fields are treated as having been set by the user,
        meaning they will overwrite other fields when "merged".
        """
        if module is None:
            import rich_click.rich_click as rc

            module = rc
        kw = {}
        for k, v in cls.__dataclass_fields__.items():
            if v.init:
                if k != "highlighter" and hasattr(module, k.upper()):
                    kw[k] = getattr(module, k.upper())

        kw.update(extra)
        inst = cls(**kw)
        return inst

    def dump_to_globals(self, module: Optional[ModuleType] = None) -> None:
        if module is None:
            import rich_click.rich_click as rc

            module = rc
        for k, v in self.__dataclass_fields__.items():
            if v.init:
                if hasattr(module, k.upper()):
                    setattr(module, k.upper(), getattr(self, k))


def __getattr__(name: str) -> Any:
    if name == "OptionHighlighter":
        from rich.highlighter import RegexHighlighter

        class OptionHighlighter(RegexHighlighter):
            """Highlights our special options."""

            highlights = [
                r"(^|[^\w\-])(?P<switch>-([^\W0-9][\w\-]*\w|[^\W0-9]))",
                r"(^|[^\w\-])(?P<option>--([^\W0-9][\w\-]*\w|[^\W0-9]))",
                r"(?P<metavar><[^>]+>)",
            ]

        import warnings

        warnings.warn(
            "OptionHighlighter is deprecated and will be removed in a future version.",
            DeprecationWarning,
            stacklevel=2,
        )

        globals()["OptionHighlighter"] = OptionHighlighter

        return OptionHighlighter

    else:
        raise AttributeError
