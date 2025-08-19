# Some influence take from stubs in Cloup:
# https://github.com/janluke/cloup
# Copyright (c) 2021, Gianluca Gippetto MIT
from __future__ import annotations

import sys
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypedDict,
    TypeVar,
    Union,
    overload,
)

import click
from click.shell_completion import CompletionItem
from click.types import ParamType
from rich.align import AlignMethod
from rich.box import Box
from rich.console import Console, JustifyMethod
from rich.padding import PaddingDimensions
from rich.text import Text, TextType

from rich_click.rich_command import RichCommand, RichGroup
from rich_click.rich_context import RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration
from rich_click.rich_panel import RichOptionPanel, RichPanel
from rich_click.utils import CommandGroupDict, OptionGroupDict

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired
else:
    from typing import NotRequired

if sys.version_info < (3, 10):
    from typing_extensions import Concatenate, ParamSpec
else:
    from typing import Concatenate, ParamSpec

_AnyCallable = Callable[..., Any]

StyleType = str  # Pyright gets upset at rich.style.Style, so just use str
FC = TypeVar("FC", bound=Union[click.Command, _AnyCallable])
P = TypeVar("P", bound=click.Parameter)
C = TypeVar("C", bound=click.Command)
G = TypeVar("G", bound=click.Group)
RP = TypeVar("RP", bound=RichPanel[Any])

ShellCompleteArg = Callable[
    [click.Context, P, str],
    Union[List[CompletionItem], List[str]],
]
ParamDefault = Union[Any, Callable[[], Any]]
ParamCallback = Callable[[click.Context, P, Any], Any]

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
    rich_console: NotRequired[Optional["Console"]]
    rich_help_config: NotRequired[Optional[Union[Mapping[str, Any], RichHelpConfiguration]]]
    export_console_as: NotRequired[Optional[Literal["html", "svg", "text"]]]
    errors_in_output_format: NotRequired[Optional[bool]]
    help_to_stderr: NotRequired[Optional[bool]]

class TableKwargs(TypedDict):
    title: NotRequired[Optional[TextType]]
    caption: NotRequired[Optional[TextType]]
    width: NotRequired[Optional[int]]
    min_width: NotRequired[Optional[int]]
    box: NotRequired[Optional[Union[str, Box]]]
    safe_box: NotRequired[Optional[bool]]
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
    row_styles: NotRequired[Optional[Iterable[StyleType]]]
    header_style: NotRequired[Optional[StyleType]]
    footer_style: NotRequired[Optional[StyleType]]
    border_style: NotRequired[Optional[StyleType]]
    title_style: NotRequired[Optional[StyleType]]
    caption_style: NotRequired[Optional[StyleType]]
    title_justify: NotRequired[JustifyMethod]
    caption_justify: NotRequired[JustifyMethod]
    highlight: NotRequired[bool]

class PanelKwargs(TypedDict):
    box: NotRequired[Union[str, Box]]
    title: NotRequired[Optional[TextType]]
    title_align: NotRequired[AlignMethod]
    subtitle: NotRequired[Optional[TextType]]
    subtitle_align: NotRequired[AlignMethod]
    safe_box: NotRequired[Optional[bool]]
    expand: NotRequired[bool]
    style: NotRequired[StyleType]
    border_style: NotRequired[StyleType]
    width: NotRequired[Optional[int]]
    height: NotRequired[Optional[int]]
    padding: NotRequired[PaddingDimensions]
    highlight: NotRequired[bool]

class RichHelpConfigurationDict(TypedDict):
    """Typed dict for rich_config() kwargs."""

    style_option: NotRequired[StyleType]
    style_argument: NotRequired[StyleType]
    style_command: NotRequired[StyleType]
    style_switch: NotRequired[StyleType]
    style_metavar: NotRequired[StyleType]
    style_metavar_append: NotRequired[StyleType]
    style_metavar_separator: NotRequired[StyleType]
    style_header_text: NotRequired[StyleType]
    style_epilog_text: NotRequired[StyleType]
    style_footer_text: NotRequired[StyleType]
    style_usage: NotRequired[StyleType]
    style_usage_command: NotRequired[StyleType]
    style_deprecated: NotRequired[StyleType]
    style_helptext_first_line: NotRequired[StyleType]
    style_helptext: NotRequired[StyleType]
    style_option_help: NotRequired[StyleType]
    style_option_default: NotRequired[StyleType]
    style_option_envvar: NotRequired[StyleType]
    style_required_short: NotRequired[StyleType]
    style_required_long: NotRequired[StyleType]
    style_options_panel_border: NotRequired[StyleType]
    style_options_panel_inline_help_in_title: NotRequired[bool]
    style_options_panel_box: NotRequired[Optional[Union[str, Box]]]
    style_options_panel_help_style: NotRequired[StyleType]
    style_options_panel_title_style: NotRequired[StyleType]
    style_options_panel_padding: NotRequired[PaddingDimensions]
    align_options_panel: NotRequired[AlignMethod]
    style_options_table_show_lines: NotRequired[bool]
    style_options_table_leading: NotRequired[int]
    style_options_table_pad_edge: NotRequired[bool]
    style_options_table_padding: NotRequired[PaddingDimensions]
    style_options_table_box: NotRequired[Optional[Union[str, Box]]]
    style_options_table_row_styles: NotRequired[Optional[List[StyleType]]]
    style_options_table_border_style: NotRequired[Optional[StyleType]]
    style_commands_panel_border: NotRequired[StyleType]
    style_commands_panel_inline_help_in_title: NotRequired[bool]
    style_commands_panel_box: NotRequired[Optional[Union[str, Box]]]
    style_commands_panel_help_style: NotRequired[StyleType]
    style_commands_panel_title_style: NotRequired[StyleType]
    style_commands_panel_padding: NotRequired[PaddingDimensions]
    align_commands_panel: NotRequired[AlignMethod]
    style_commands_table_show_lines: NotRequired[bool]
    style_commands_table_leading: NotRequired[int]
    style_commands_table_pad_edge: NotRequired[bool]
    style_commands_table_padding: NotRequired[PaddingDimensions]
    style_commands_table_box: NotRequired[Optional[Union[str, Box]]]
    style_commands_table_row_styles: NotRequired[Optional[List[StyleType]]]
    style_commands_table_border_style: NotRequired[Optional[StyleType]]
    style_commands_table_column_width_ratio: NotRequired[Optional[Union[Tuple[None, None], Tuple[int, int]]]]
    style_errors_panel_border: NotRequired[StyleType]
    style_errors_panel_box: NotRequired[Optional[Union[str, Box]]]
    align_errors_panel: NotRequired[AlignMethod]
    style_errors_suggestion: NotRequired[StyleType]
    style_errors_suggestion_command: NotRequired[StyleType]
    style_aborted: NotRequired[StyleType]
    width: NotRequired[Optional[int]]
    max_width: NotRequired[Optional[int]]
    color_system: NotRequired[Optional[Literal["auto", "standard", "256", "truecolor", "windows"]]]
    force_terminal: NotRequired[Optional[bool]]
    header_text: NotRequired[Optional[Union[str, Text]]]
    footer_text: NotRequired[Optional[Union[str, Text]]]
    deprecated_string: NotRequired[str]
    deprecated_with_reason_string: NotRequired[str]
    default_string: NotRequired[str]
    envvar_string: NotRequired[str]
    required_short_string: NotRequired[str]
    required_long_string: NotRequired[str]
    range_string: NotRequired[str]
    append_metavars_help_string: NotRequired[str]
    arguments_panel_title: NotRequired[str]
    options_panel_title: NotRequired[str]
    commands_panel_title: NotRequired[str]
    errors_panel_title: NotRequired[str]
    errors_suggestion: NotRequired[Optional[Union[str, Text]]]
    errors_epilogue: NotRequired[Optional[Union[str, Text]]]
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
    show_arguments: NotRequired[Optional[bool]]
    show_metavars_column: NotRequired[Optional[bool]]
    commands_before_options: NotRequired[bool]
    append_metavars_help: NotRequired[bool]
    group_arguments_options: NotRequired[bool]
    option_envvar_first: NotRequired[bool]
    text_markup: NotRequired[Literal["ansi", "rich", "markdown", None]]
    text_kwargs: NotRequired[Optional[Dict[str, Any]]]
    text_emojis: NotRequired[bool]
    text_paragraph_linebreaks: NotRequired[Optional[str]]
    use_markdown: NotRequired[Optional[bool]]
    use_markdown_emoji: NotRequired[Optional[bool]]
    use_rich_markup: NotRequired[Optional[bool]]
    command_groups: NotRequired[Dict[str, List[CommandGroupDict]]]
    option_groups: NotRequired[Dict[str, List[OptionGroupDict]]]
    use_click_short_help: NotRequired[bool]
    highlighter_patterns: NotRequired[List[str]]
    legacy_windows: NotRequired[Optional[bool]]

@overload
def command(
    name: Optional[str] = None,
    *,
    cls: None = None,
    context_settings: RichContextSettingsDict,
    callback: Callable[..., Any] | None = None,
    params: list[click.Parameter] | None = None,
    help: str | None = None,
    epilog: str | None = None,
    short_help: str | None = None,
    options_metavar: str | None = "[OPTIONS]",
    add_help_option: bool = True,
    no_args_is_help: bool = False,
    hidden: bool = False,
    deprecated: bool | str = False,
    panels: Optional[List[RichPanel[Any]]] = None,
) -> Callable[[_AnyCallable], RichCommand]: ...
@overload
def command(
    name: Optional[str] = None,
    *,
    cls: None = None,
    context_settings: MutableMapping[str, Any] | None = None,
    callback: Callable[..., Any] | None = None,
    params: list[click.Parameter] | None = None,
    help: str | None = None,
    epilog: str | None = None,
    short_help: str | None = None,
    options_metavar: str | None = "[OPTIONS]",
    add_help_option: bool = True,
    no_args_is_help: bool = False,
    hidden: bool = False,
    deprecated: bool | str = False,
    panels: Optional[List[RichPanel[Any]]] = None,
) -> Callable[[_AnyCallable], RichCommand]: ...
@overload
def command(
    name: Optional[str] = None,
    *,
    cls: Type[C],
    context_settings: RichContextSettingsDict | MutableMapping[str, Any] | None = None,
    callback: Callable[..., Any] | None = None,
    params: list[click.Parameter] | None = None,
    help: str | None = None,
    epilog: str | None = None,
    short_help: str | None = None,
    options_metavar: str | None = "[OPTIONS]",
    add_help_option: bool = True,
    no_args_is_help: bool = False,
    hidden: bool = False,
    deprecated: bool | str = False,
    panels: Optional[List[RichPanel[Any]]] = None,
    **attrs: Any,
) -> Callable[[_AnyCallable], C]: ...
def command(
    name: Optional[str] = None, *, aliases: Optional[Iterable[str]] = None, cls: Optional[Type[C]] = None, **kwargs: Any
) -> Callable[[_AnyCallable], Union[click.Command, C]]: ...
@overload
def group(
    name: Optional[str] = None,
    *,
    cls: None = None,
    commands: RichContextSettingsDict,
    invoke_without_command: bool = False,
    no_args_is_help: bool | None = None,
    subcommand_metavar: str | None = None,
    chain: bool = False,
    result_callback: Callable[..., Any] | None = None,
    context_settings: MutableMapping[str, Any] | None = None,
    callback: Callable[..., Any] | None = None,
    params: list[click.Parameter] | None = None,
    help: str | None = None,
    epilog: str | None = None,
    short_help: str | None = None,
    options_metavar: str | None = "[OPTIONS]",
    add_help_option: bool = True,
    hidden: bool = False,
    deprecated: bool | str = False,
    panels: Optional[List[RichPanel[Any]]] = None,
) -> Callable[[_AnyCallable], RichGroup]: ...
@overload
def group(
    name: Optional[str] = None,
    *,
    cls: None = None,
    commands: MutableMapping[str, click.Command] | Sequence[click.Command] | None = None,
    invoke_without_command: bool = False,
    no_args_is_help: bool | None = None,
    subcommand_metavar: str | None = None,
    chain: bool = False,
    result_callback: Callable[..., Any] | None = None,
    context_settings: MutableMapping[str, Any] | None = None,
    callback: Callable[..., Any] | None = None,
    params: list[click.Parameter] | None = None,
    help: str | None = None,
    epilog: str | None = None,
    short_help: str | None = None,
    options_metavar: str | None = "[OPTIONS]",
    add_help_option: bool = True,
    hidden: bool = False,
    deprecated: bool | str = False,
    panels: Optional[List[RichPanel[Any]]] = None,
) -> Callable[[_AnyCallable], RichGroup]: ...
@overload
def group(
    name: Optional[str] = None,
    *,
    cls: Type[G],
    commands: MutableMapping[str, click.Command] | Sequence[click.Command] | None = None,
    invoke_without_command: bool = False,
    no_args_is_help: bool | None = None,
    subcommand_metavar: str | None = None,
    chain: bool = False,
    result_callback: Callable[..., Any] | None = None,
    context_settings: MutableMapping[str, Any] | None = None,
    callback: Callable[..., Any] | None = None,
    params: list[click.Parameter] | None = None,
    help: str | None = None,
    epilog: str | None = None,
    short_help: str | None = None,
    options_metavar: str | None = "[OPTIONS]",
    add_help_option: bool = True,
    hidden: bool = False,
    deprecated: bool | str = False,
    panels: Optional[List[RichPanel[Any]]] = None,
) -> Callable[[_AnyCallable], G]: ...
def group(
    name: Union[str, _AnyCallable, None] = None,
    cls: Optional[Type[G]] = None,
    **attrs: Any,
) -> Union[click.Group, Callable[[_AnyCallable], Union[RichGroup, G]]]: ...
def argument(
    *param_decls: str,
    cls: Optional[Type[click.Argument]] = None,
    type: ParamType | Any | None = None,
    required: bool = False,
    default: Any | Callable[[], Any] | None = None,
    callback: Callable[[click.Context, click.Parameter, Any], Any] | None = None,
    nargs: int | None = None,
    multiple: bool = False,
    metavar: str | None = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: str | Sequence[str] | None = None,
    shell_complete: Callable[[click.Context, click.Parameter, str], list[CompletionItem] | list[str]] | None = None,
    deprecated: bool | str = False,
    panel: Optional[Union[str, List[str]]] = None,
    help: Optional[str] = None,
    help_style: Optional[StyleType] = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...
def option(
    *param_decls: str,
    cls: Optional[Type[click.Option]] = None,
    type: Optional[Union["ParamType", Any]] = None,
    required: bool = False,
    default: Optional[Union[Any, Callable[[], Any]]] = None,
    callback: Optional[Callable[[click.Context, click.Parameter, Any], Any]] = None,
    nargs: Optional[int] = None,
    multiple: bool = False,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, Sequence[str]]] = None,
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[List[CompletionItem], List[str]],
        ]
    ] = None,
    show_default: Optional[Union[bool, str]] = False,
    prompt: Union[bool, str] = False,
    confirmation_prompt: Union[bool, str] = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: Optional[bool] = None,
    flag_value: Optional[Any] = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = False,
    panel: Optional[Union[str, List[str]]] = None,
    help_style: Optional[StyleType] = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...
def password_option(
    *param_decls: str,
    cls: Optional[Type[click.Option]] = None,
    type: Optional[Union["ParamType", Any]] = None,
    required: bool = False,
    default: Optional[Union[Any, Callable[[], Any]]] = None,
    callback: Optional[Callable[[click.Context, click.Parameter, Any], Any]] = None,
    nargs: Optional[int] = None,
    multiple: bool = False,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, Sequence[str]]] = None,
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[List[CompletionItem], List[str]],
        ]
    ] = None,
    show_default: Optional[Union[bool, str]] = False,
    prompt: Union[bool, str] = False,
    confirmation_prompt: Union[bool, str] = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: Optional[bool] = None,
    flag_value: Optional[Any] = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = False,
    panel: Optional[Union[str, List[str]]] = None,
    help_style: Optional[StyleType] = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...
def version_option(
    version: Optional[str] = None,
    *param_decls: str,
    package_name: Optional[str] = None,
    prog_name: Optional[str] = None,
    message: Optional[str] = None,
    cls: Optional[Type[click.Option]] = None,
    type: Optional[Union["ParamType", Any]] = None,
    required: bool = False,
    default: Optional[Union[Any, Callable[[], Any]]] = None,
    callback: Optional[Callable[[click.Context, click.Parameter, Any], Any]] = None,
    nargs: Optional[int] = None,
    multiple: bool = False,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, Sequence[str]]] = None,
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[List[CompletionItem], List[str]],
        ]
    ] = None,
    show_default: Optional[Union[bool, str]] = False,
    prompt: Union[bool, str] = False,
    confirmation_prompt: Union[bool, str] = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: Optional[bool] = None,
    flag_value: Optional[Any] = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = False,
    panel: Optional[Union[str, List[str]]] = None,
    help_style: Optional[StyleType] = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...
def help_option(
    *param_decls: str,
    cls: Optional[Type[click.Option]] = None,
    type: Optional[Union["ParamType", Any]] = None,
    required: bool = False,
    default: Optional[Union[Any, Callable[[], Any]]] = None,
    callback: Optional[Callable[[click.Context, click.Parameter, Any], Any]] = None,
    nargs: Optional[int] = None,
    multiple: bool = False,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, Sequence[str]]] = None,
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[List[CompletionItem], List[str]],
        ]
    ] = None,
    show_default: Optional[Union[bool, str]] = False,
    prompt: Union[bool, str] = False,
    confirmation_prompt: Union[bool, str] = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: Optional[bool] = None,
    flag_value: Optional[Any] = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = False,
    panel: Optional[Union[str, List[str]]] = None,
    help_style: Optional[StyleType] = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...
def confirmation_option(
    *param_decls: str,
    cls: Optional[Type[click.Option]] = None,
    type: Optional[Union["ParamType", Any]] = None,
    required: bool = False,
    default: Optional[Union[Any, Callable[[], Any]]] = None,
    callback: Optional[Callable[[click.Context, click.Parameter, Any], Any]] = None,
    nargs: Optional[int] = None,
    multiple: bool = False,
    metavar: Optional[str] = None,
    expose_value: bool = True,
    is_eager: bool = False,
    envvar: Optional[Union[str, Sequence[str]]] = None,
    shell_complete: Optional[
        Callable[
            [click.Context, click.Parameter, str],
            Union[List[CompletionItem], List[str]],
        ]
    ] = None,
    show_default: Optional[Union[bool, str]] = False,
    prompt: Union[bool, str] = False,
    confirmation_prompt: Union[bool, str] = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: Optional[bool] = None,
    flag_value: Optional[Any] = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: Optional[str] = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = False,
    panel: Optional[Union[str, List[str]]] = None,
    help_style: Optional[StyleType] = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...

# This is a way to trick PyCharm into adding autocompletion for typed dicts
# without jeopardizing anything on Mypy's side.
@overload
def rich_config(
    help_config: RichHelpConfigurationDict,
    *,
    console: Optional[Console] = None,
) -> Callable[[FC], FC]: ...
@overload
def rich_config(
    help_config: Optional[Union[Dict[str, Any], RichHelpConfigurationDict, RichHelpConfiguration]] = None,
    *,
    console: Optional[Console] = None,
) -> Callable[[FC], FC]: ...
def rich_config(
    help_config: Optional[Union[Dict[str, Any], RichHelpConfigurationDict, RichHelpConfiguration]] = None,
    *,
    console: Optional[Console] = None,
) -> Callable[[FC], FC]: ...
@overload
def option_panel(
    name: str,
    cls: Type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    options: Optional[List[str]] = None,
    help: Optional[str] = None,
    help_style: StyleType = "",
    table_styles: TableKwargs,
    panel_styles: PanelKwargs,
) -> Callable[[FC], FC]: ...
@overload
def option_panel(
    name: str,
    cls: Type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    options: Optional[List[str]] = None,
    help: Optional[str] = None,
    help_style: StyleType = "",
    table_styles: Optional[Dict[str, Any]] = None,
    panel_styles: Optional[Dict[str, Any]] = None,
) -> Callable[[FC], FC]: ...
@overload
def option_panel(
    name: str,
    cls: Type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    options: Optional[List[str]] = None,
    help: Optional[str] = None,
    help_style: StyleType = "",
    table_styles: None,
    panel_styles: None,
) -> Callable[[FC], FC]: ...
def option_panel(
    name: str,
    cls: Type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    options: Optional[List[str]] = None,
    help: Optional[str] = None,
    help_style: StyleType = "",
    table_styles: Optional[Union[TableKwargs, Dict[str, Any]]] = None,
    panel_styles: Optional[Union[PanelKwargs, Dict[str, Any]]] = None,
) -> Callable[[FC], FC]: ...
@overload
def command_panel(
    name: str,
    cls: Type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    commands: Optional[List[str]] = None,
    help: Optional[str] = None,
    help_style: StyleType = "",
    table_styles: TableKwargs,
    panel_styles: PanelKwargs,
) -> Callable[[FC], FC]: ...
@overload
def command_panel(
    name: str,
    cls: Type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    commands: Optional[List[str]] = None,
    help: Optional[str] = None,
    help_style: StyleType = "",
    table_styles: Optional[Dict[str, Any]] = None,
    panel_styles: Optional[Dict[str, Any]] = None,
) -> Callable[[FC], FC]: ...
@overload
def command_panel(
    name: str,
    cls: Type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    commands: Optional[List[str]] = None,
    help: Optional[str] = None,
    help_style: StyleType = "",
    table_styles: None,
    panel_styles: None,
) -> Callable[[FC], FC]: ...
def command_panel(
    name: str,
    cls: Type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    commands: Optional[List[str]] = None,
    help: Optional[str] = None,
    help_style: StyleType = "",
    table_styles: Optional[Dict[str, Any]] = None,
    panel_styles: Optional[Dict[str, Any]] = None,
) -> Callable[[FC], FC]: ...

PSpec = ParamSpec("PSpec")
R = TypeVar("R")

def pass_context(f: Callable[Concatenate[RichContext, PSpec], R]) -> Callable[PSpec, R]: ...
