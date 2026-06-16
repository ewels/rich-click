"""
Contains types for .pyi files.
Import from this at your own risk.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Mapping, MutableMapping
from typing import (
    TYPE_CHECKING,
    Any,
    Literal,
    TypedDict,
)

from rich_click.utils import CommandGroupDict, OptionGroupDict


if TYPE_CHECKING:
    import sys

    from rich.align import AlignMethod
    from rich.box import Box
    from rich.console import Console, JustifyMethod
    from rich.padding import PaddingDimensions
    from rich.style import StyleType
    from rich.text import Text, TextType

    from rich_click.rich_click_theme import RichClickTheme
    from rich_click.rich_help_configuration import (
        CommandColumnType,
        CommandHelpSectionType,
        OptionColumnType,
        OptionHelpSectionType,
        RichHelpConfiguration,
    )

    if sys.version_info < (3, 11):
        from typing_extensions import NotRequired
    else:
        from typing import NotRequired


class RichContextSettingsDict(TypedDict):
    obj: NotRequired[Any | None]
    auto_envvar_prefix: NotRequired[str | None]
    default_map: NotRequired[MutableMapping[str, Any] | None]
    terminal_width: NotRequired[int | None]
    max_content_width: NotRequired[int | None]
    resilient_parsing: NotRequired[bool]
    allow_extra_args: NotRequired[bool | None]
    allow_interspersed_args: NotRequired[bool | None]
    ignore_unknown_options: NotRequired[bool | None]
    help_option_names: NotRequired[list[str] | None]
    token_normalize_func: NotRequired[Callable[[str], str] | None]
    color: NotRequired[bool | None]
    show_default: NotRequired[bool | None]
    rich_console: NotRequired[Console | None]
    rich_help_config: NotRequired[Mapping[str, Any] | RichHelpConfiguration | None]
    export_console_as: NotRequired[Literal["html", "svg", "text"] | None]
    errors_in_output_format: NotRequired[bool | None]
    help_to_stderr: NotRequired[bool | None]


class TableKwargs(TypedDict):
    title: NotRequired[TextType | None]
    caption: NotRequired[TextType | None]
    width: NotRequired[int | None]
    min_width: NotRequired[int | None]
    box: NotRequired[str | Box | None]
    safe_box: NotRequired[bool | None]
    padding: NotRequired[PaddingDimensions]
    collapse_padding: NotRequired[bool]
    pad_edge: NotRequired[bool]
    expand: NotRequired[bool]
    show_header: NotRequired[bool]
    show_footer: NotRequired[bool]
    show_edge: NotRequired[bool]
    show_lines: NotRequired[bool]
    leading: NotRequired[int]
    style: NotRequired[StyleType]
    row_styles: NotRequired[Iterable[StyleType] | None]
    header_style: NotRequired[StyleType | None]
    footer_style: NotRequired[StyleType | None]
    border_style: NotRequired[StyleType | None]
    title_style: NotRequired[StyleType | None]
    caption_style: NotRequired[StyleType | None]
    title_justify: NotRequired[JustifyMethod]
    caption_justify: NotRequired[JustifyMethod]
    highlight: NotRequired[bool]


class PanelKwargs(TypedDict):
    box: NotRequired[str | Box]
    title: NotRequired[TextType | None]
    title_align: NotRequired[AlignMethod]
    subtitle: NotRequired[TextType | None]
    subtitle_align: NotRequired[AlignMethod]
    safe_box: NotRequired[bool | None]
    expand: NotRequired[bool]
    style: NotRequired[StyleType]
    border_style: NotRequired[StyleType]
    width: NotRequired[int | None]
    height: NotRequired[int | None]
    padding: NotRequired[PaddingDimensions]
    highlight: NotRequired[bool]


class RichHelpConfigurationDict(TypedDict):
    """Typed dict for rich_config() kwargs."""

    theme: NotRequired[str | RichClickTheme | None]
    enable_theme_env_var: NotRequired[bool]
    style_option: NotRequired[StyleType]
    style_option_negative: NotRequired[StyleType | None]
    style_argument: NotRequired[StyleType]
    style_command: NotRequired[StyleType]
    style_command_aliases: NotRequired[StyleType]
    style_switch: NotRequired[StyleType]
    style_switch_negative: NotRequired[StyleType | None]
    style_metavar: NotRequired[StyleType]
    style_metavar_append: NotRequired[StyleType]
    style_metavar_separator: NotRequired[StyleType]
    style_range_append: NotRequired[StyleType]
    style_header_text: NotRequired[StyleType]
    style_epilog_text: NotRequired[StyleType]
    style_footer_text: NotRequired[StyleType]
    style_usage: NotRequired[StyleType]
    style_usage_command: NotRequired[StyleType]
    style_usage_separator: NotRequired[StyleType]
    style_deprecated: NotRequired[StyleType]
    style_helptext_first_line: NotRequired[StyleType]
    style_helptext: NotRequired[StyleType]
    style_helptext_aliases: NotRequired[StyleType | None]
    style_option_help: NotRequired[StyleType]
    style_command_help: NotRequired[StyleType]
    style_option_default: NotRequired[StyleType]
    style_option_envvar: NotRequired[StyleType]
    style_required_short: NotRequired[StyleType]
    style_required_long: NotRequired[StyleType]
    style_options_panel_border: NotRequired[StyleType]
    style_options_panel_box: NotRequired[str | Box | None]
    style_options_panel_help_style: NotRequired[StyleType]
    style_options_panel_title_style: NotRequired[StyleType]
    style_options_panel_padding: NotRequired[PaddingDimensions]
    style_options_panel_style: NotRequired[StyleType]
    align_options_panel: NotRequired[AlignMethod]
    style_options_table_show_lines: NotRequired[bool]
    style_options_table_leading: NotRequired[int]
    style_options_table_pad_edge: NotRequired[bool]
    style_options_table_padding: NotRequired[PaddingDimensions]
    style_options_table_expand: NotRequired[bool]
    style_options_table_box: NotRequired[str | Box | None]
    style_options_table_row_styles: NotRequired[list[StyleType] | None]
    style_options_table_border_style: NotRequired[StyleType | None]
    style_commands_panel_border: NotRequired[StyleType]
    panel_inline_help_in_title: NotRequired[bool]
    panel_inline_help_delimiter: NotRequired[str]
    style_commands_panel_box: NotRequired[str | Box | None]
    style_commands_panel_help_style: NotRequired[StyleType]
    style_commands_panel_title_style: NotRequired[StyleType]
    style_commands_panel_padding: NotRequired[PaddingDimensions]
    style_commands_panel_style: NotRequired[StyleType]
    align_commands_panel: NotRequired[AlignMethod]
    style_commands_table_show_lines: NotRequired[bool]
    style_commands_table_leading: NotRequired[int]
    style_commands_table_pad_edge: NotRequired[bool]
    style_commands_table_padding: NotRequired[PaddingDimensions]
    style_commands_table_expand: NotRequired[bool]
    style_commands_table_box: NotRequired[str | Box | None]
    style_commands_table_row_styles: NotRequired[list[StyleType] | None]
    style_commands_table_border_style: NotRequired[StyleType | None]
    style_commands_table_column_width_ratio: NotRequired[tuple[None, None] | tuple[int, int] | None]
    style_errors_panel_border: NotRequired[StyleType]
    style_errors_panel_box: NotRequired[str | Box | None]
    align_errors_panel: NotRequired[AlignMethod]
    style_errors_suggestion: NotRequired[StyleType | None]
    style_errors_suggestion_command: NotRequired[StyleType | None]
    style_padding_errors: NotRequired[StyleType]
    style_aborted: NotRequired[StyleType]
    style_padding_usage: NotRequired[StyleType]
    style_padding_helptext: NotRequired[StyleType]
    style_padding_epilog: NotRequired[StyleType]

    panel_title_padding: NotRequired[int]
    width: NotRequired[int | None]
    max_width: NotRequired[int | None]
    color_system: NotRequired[Literal["auto", "standard", "256", "truecolor", "windows"] | None]
    force_terminal: NotRequired[bool | None]
    options_table_column_types: NotRequired[list[OptionColumnType]]
    commands_table_column_types: NotRequired[list[CommandColumnType]]
    options_table_help_sections: NotRequired[list[OptionHelpSectionType]]
    commands_table_help_sections: NotRequired[list[CommandHelpSectionType]]

    header_text: NotRequired[str | Text | None]
    footer_text: NotRequired[str | Text | None]
    panel_title_string: NotRequired[str]
    deprecated_string: NotRequired[str]
    deprecated_with_reason_string: NotRequired[str]
    default_string: NotRequired[str]
    envvar_string: NotRequired[str]
    required_short_string: NotRequired[str]
    required_long_string: NotRequired[str]
    range_string: NotRequired[str]
    append_metavars_help_string: NotRequired[str]
    append_range_help_string: NotRequired[str]
    helptext_aliases_string: NotRequired[str]
    arguments_panel_title: NotRequired[str]
    options_panel_title: NotRequired[str]
    commands_panel_title: NotRequired[str]
    errors_panel_title: NotRequired[str]
    delimiter_comma: NotRequired[str]
    delimiter_slash: NotRequired[str]
    errors_suggestion: NotRequired[str | Text | None]
    errors_epilogue: NotRequired[str | Text | None]
    aborted_text: NotRequired[str]
    padding_header_text: NotRequired[PaddingDimensions]
    padding_helptext: NotRequired[PaddingDimensions]
    padding_helptext_deprecated: NotRequired[PaddingDimensions]
    padding_helptext_first_line: NotRequired[PaddingDimensions]
    padding_usage: NotRequired[PaddingDimensions]
    padding_epilog: NotRequired[PaddingDimensions]
    padding_footer_text: NotRequired[PaddingDimensions]
    padding_errors_panel: NotRequired[PaddingDimensions]
    padding_errors_suggestion: NotRequired[PaddingDimensions]
    padding_errors_epilogue: NotRequired[PaddingDimensions]

    # Behaviours
    show_arguments: NotRequired[bool | None]
    show_metavars_column: NotRequired[bool | None]
    commands_before_options: NotRequired[bool]
    default_panels_first: NotRequired[bool]
    append_metavars_help: NotRequired[bool | None]
    group_arguments_options: NotRequired[bool]
    option_envvar_first: NotRequired[bool | None]
    text_markup: NotRequired[Literal["ansi", "rich", "markdown", None]]
    text_kwargs: NotRequired[dict[str, Any] | None]
    text_emojis: NotRequired[bool]
    text_paragraph_linebreaks: NotRequired[Literal["\n", "\n\n"] | None]
    use_markdown: NotRequired[bool | None]
    use_markdown_emoji: NotRequired[bool | None]
    use_rich_markup: NotRequired[bool | None]
    command_groups: NotRequired[dict[str, list[CommandGroupDict]]]
    option_groups: NotRequired[dict[str, list[OptionGroupDict]]]
    use_click_short_help: NotRequired[bool]
    helptext_show_aliases: NotRequired[bool]
    highlighter_patterns: NotRequired[list[str]]
    legacy_windows: NotRequired[bool | None]
