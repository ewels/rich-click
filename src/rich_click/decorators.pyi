# Some influence take from stubs in Cloup:
# https://github.com/janluke/cloup
# Copyright (c) 2021, Gianluca Gippetto MIT
from __future__ import annotations

from collections.abc import Callable, Iterable, MutableMapping, Sequence
from typing import (
    Any,
    Concatenate,
    ParamSpec,
    TypeVar,
    overload,
)

import click
from click.shell_completion import CompletionItem
from click.types import ParamType
from rich.console import Console

from rich_click._internal_types import PanelKwargs, RichContextSettingsDict, RichHelpConfigurationDict, TableKwargs
from rich_click.rich_command import RichCommand, RichGroup
from rich_click.rich_context import RichContext
from rich_click.rich_help_configuration import CommandColumnType, OptionColumnType, RichHelpConfiguration
from rich_click.rich_panel import RichOptionPanel, RichPanel

_AnyCallable = Callable[..., Any]

StyleType = str  # Pyright gets upset at rich.style.Style, so just use str
FC = TypeVar("FC", bound=click.Command | _AnyCallable)
P = TypeVar("P", bound=click.Parameter)
C = TypeVar("C", bound=click.Command)
G = TypeVar("G", bound=click.Group)
RP = TypeVar("RP", bound=RichPanel[Any, Any])

ShellCompleteArg = Callable[
    [click.Context, P, str],
    list[CompletionItem] | list[str],
]
ParamDefault = Any | Callable[[], Any]
ParamCallback = Callable[[click.Context, P, Any], Any]

# variant: no call, directly as decorator for a function.
@overload
def command(name: _AnyCallable) -> RichCommand: ...
@overload
def command(
    name: str | None = ...,
    *,
    cls: type[C],
    context_settings: RichContextSettingsDict,
    callback: Callable[..., Any] | None = ...,
    params: list[click.Parameter] | None = ...,
    help: str | None = ...,
    epilog: str | None = ...,
    short_help: str | None = ...,
    options_metavar: str | None = ...,
    add_help_option: bool = ...,
    no_args_is_help: bool = ...,
    hidden: bool = ...,
    deprecated: bool | str = ...,
    aliases: Iterable[str] | None = ...,
    panels: list[RichPanel[Any, Any]] | None = ...,
) -> Callable[[_AnyCallable], C]: ...
@overload
def command(
    name: str | None = ...,
    *,
    cls: None,
    context_settings: RichContextSettingsDict,
    callback: Callable[..., Any] | None = ...,
    params: list[click.Parameter] | None = ...,
    help: str | None = ...,
    epilog: str | None = ...,
    short_help: str | None = ...,
    options_metavar: str | None = ...,
    add_help_option: bool = ...,
    no_args_is_help: bool = ...,
    hidden: bool = ...,
    deprecated: bool | str = ...,
    aliases: Iterable[str] | None = ...,
    panels: list[RichPanel[Any, Any]] | None = ...,
) -> Callable[[_AnyCallable], RichCommand]: ...
@overload
def command(
    name: str | None = ...,
    *,
    cls: type[C],
    context_settings: MutableMapping[str, Any] | None = ...,
    callback: Callable[..., Any] | None = ...,
    params: list[click.Parameter] | None = ...,
    help: str | None = ...,
    epilog: str | None = ...,
    short_help: str | None = ...,
    options_metavar: str | None = ...,
    add_help_option: bool = ...,
    no_args_is_help: bool = ...,
    hidden: bool = ...,
    deprecated: bool | str = ...,
    aliases: Iterable[str] | None = ...,
    panels: list[RichPanel[Any, Any]] | None = ...,
) -> Callable[[_AnyCallable], C]: ...
@overload
def command(
    name: str | None = None,
    *,
    cls: None,
    context_settings: MutableMapping[str, Any] | None = ...,
    callback: Callable[..., Any] | None = ...,
    params: list[click.Parameter] | None = ...,
    help: str | None = ...,
    epilog: str | None = ...,
    short_help: str | None = ...,
    options_metavar: str | None = ...,
    add_help_option: bool = ...,
    no_args_is_help: bool = ...,
    hidden: bool = ...,
    deprecated: bool | str = ...,
    aliases: Iterable[str] | None = ...,
    panels: list[RichPanel[Any, Any]] | None = ...,
    **attrs: Any,
) -> Callable[[_AnyCallable], RichCommand]: ...

# variant: with positional name and with positional or keyword cls argument:
# @command(namearg, CommandCls, ...) or @command(namearg, cls=CommandCls, ...)
@overload
def command(
    name: str | None,
    cls: type[C],
    **attrs: Any,
) -> Callable[[_AnyCallable], C]: ...

# variant: name omitted, cls _must_ be a keyword argument, @command(cls=CommandCls, ...)
@overload
def command(
    name: None = None,
    *,
    cls: type[C],
    **attrs: Any,
) -> Callable[[_AnyCallable], C]: ...

# variant: with optional string name, no cls argument provided.
@overload
def command(name: str | None = ..., cls: None = None, **attrs: Any) -> Callable[[_AnyCallable], RichCommand]: ...
def command(
    name: str | None = None, *, cls: type[C] | None = None, **kwargs: Any
) -> Callable[[_AnyCallable], click.Command | C]: ...

# variant: no call, directly as decorator for a function.
@overload
def group(name: _AnyCallable) -> RichGroup: ...
@overload
def group(
    name: str | None = None,
    *,
    cls: type[G],
    commands: MutableMapping[str, click.Command] | Sequence[click.Command] | None = ...,
    invoke_without_command: bool = ...,
    no_args_is_help: bool | None = ...,
    subcommand_metavar: str | None = ...,
    chain: bool = ...,
    result_callback: Callable[..., Any] | None = ...,
    context_settings: RichContextSettingsDict,
    callback: Callable[..., Any] | None = ...,
    params: list[click.Parameter] | None = ...,
    help: str | None = ...,
    epilog: str | None = ...,
    short_help: str | None = ...,
    options_metavar: str | None = ...,
    add_help_option: bool = ...,
    hidden: bool = ...,
    deprecated: bool | str = ...,
    aliases: Iterable[str] | None = ...,
    panels: list[RichPanel[Any, Any]] | None = ...,
) -> Callable[[_AnyCallable], G]: ...
@overload
def group(
    name: str | None = ...,
    *,
    cls: None,
    commands: MutableMapping[str, click.Command] | Sequence[click.Command] | None = ...,
    invoke_without_command: bool = ...,
    no_args_is_help: bool | None = ...,
    subcommand_metavar: str | None = ...,
    chain: bool = ...,
    result_callback: Callable[..., Any] | None = ...,
    context_settings: MutableMapping[str, Any] | None = ...,
    callback: Callable[..., Any] | None = ...,
    params: list[click.Parameter] | None = ...,
    help: str | None = ...,
    epilog: str | None = ...,
    short_help: str | None = ...,
    options_metavar: str | None = ...,
    add_help_option: bool = ...,
    hidden: bool = ...,
    deprecated: bool | str = ...,
    aliases: Iterable[str] | None = ...,
    panels: list[RichPanel[Any, Any]] | None = ...,
) -> Callable[[_AnyCallable], RichGroup]: ...
@overload
def group(
    name: str | None = None,
    *,
    cls: type[G],
    commands: MutableMapping[str, click.Command] | Sequence[click.Command] | None = ...,
    invoke_without_command: bool = ...,
    no_args_is_help: bool | None = ...,
    subcommand_metavar: str | None = ...,
    chain: bool = ...,
    result_callback: Callable[..., Any] | None = ...,
    context_settings: MutableMapping[str, Any] | None = ...,
    callback: Callable[..., Any] | None = ...,
    params: list[click.Parameter] | None = ...,
    help: str | None = ...,
    epilog: str | None = ...,
    short_help: str | None = ...,
    options_metavar: str | None = ...,
    add_help_option: bool = ...,
    hidden: bool = ...,
    deprecated: bool | str = ...,
    aliases: Iterable[str] | None = ...,
    panels: list[RichPanel[Any, Any]] | None = ...,
) -> Callable[[_AnyCallable], G]: ...
@overload
def group(
    name: str | None = ...,
    *,
    cls: None,
    commands: MutableMapping[str, click.Command] | Sequence[click.Command] | None = ...,
    invoke_without_command: bool = ...,
    no_args_is_help: bool | None = ...,
    subcommand_metavar: str | None = ...,
    chain: bool = ...,
    result_callback: Callable[..., Any] | None = ...,
    context_settings: RichContextSettingsDict,
    callback: Callable[..., Any] | None = ...,
    params: list[click.Parameter] | None = ...,
    help: str | None = ...,
    epilog: str | None = ...,
    short_help: str | None = ...,
    options_metavar: str | None = ...,
    add_help_option: bool = ...,
    hidden: bool = ...,
    deprecated: bool | str = ...,
    aliases: Iterable[str] | None = ...,
    panels: list[RichPanel[Any, Any]] | None = ...,
) -> Callable[[_AnyCallable], RichGroup]: ...

# variant: with positional name and with positional or keyword cls argument:
# @group(namearg, GroupCls, ...) or @group(namearg, cls=GroupCls, ...)
@overload
def group(
    name: str | None,
    cls: type[G],
    **attrs: Any,
) -> Callable[[_AnyCallable], G]: ...

# variant: name omitted, cls _must_ be a keyword argument, @group(cmd=GroupCls, ...)
@overload
def group(
    name: None = None,
    *,
    cls: type[G],
    **attrs: Any,
) -> Callable[[_AnyCallable], G]: ...

# variant: with optional string name, no cls argument provided.
@overload
def group(name: str | None = ..., cls: None = None, **attrs: Any) -> Callable[[_AnyCallable], RichGroup]: ...
def group(
    name: str | _AnyCallable | None = None,
    cls: type[G] | None = None,
    **attrs: Any,
) -> click.Group | Callable[[_AnyCallable], RichGroup | G]: ...
def argument(
    *param_decls: str,
    cls: type[click.Argument] | None = None,
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
    panel: str | list[str] | None = None,
    help: str | None = None,
    help_style: StyleType | None = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...
def option(
    *param_decls: str,
    cls: type[click.Option] | None = None,
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
    show_default: bool | str | None = False,
    prompt: bool | str = False,
    confirmation_prompt: bool | str = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: bool | None = None,
    flag_value: Any | None = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: str | None = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = False,
    panel: str | list[str] | None = None,
    help_style: StyleType | None = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...
def password_option(
    *param_decls: str,
    cls: type[click.Option] | None = None,
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
    show_default: bool | str | None = False,
    prompt: bool | str = False,
    confirmation_prompt: bool | str = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: bool | None = None,
    flag_value: Any | None = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: str | None = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = False,
    panel: str | list[str] | None = None,
    help_style: StyleType | None = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...
def version_option(
    version: str | None = None,
    *param_decls: str,
    package_name: str | None = None,
    prog_name: str | None = None,
    message: str | None = None,
    cls: type[click.Option] | None = None,
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
    show_default: bool | str | None = False,
    prompt: bool | str = False,
    confirmation_prompt: bool | str = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: bool | None = None,
    flag_value: Any | None = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: str | None = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = False,
    panel: str | list[str] | None = None,
    help_style: StyleType | None = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...
def help_option(
    *param_decls: str,
    cls: type[click.Option] | None = None,
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
    show_default: bool | str | None = False,
    prompt: bool | str = False,
    confirmation_prompt: bool | str = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: bool | None = None,
    flag_value: Any | None = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: str | None = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = False,
    panel: str | list[str] | None = None,
    help_style: StyleType | None = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...
def confirmation_option(
    *param_decls: str,
    cls: type[click.Option] | None = None,
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
    show_default: bool | str | None = False,
    prompt: bool | str = False,
    confirmation_prompt: bool | str = False,
    prompt_required: bool = True,
    hide_input: bool = False,
    is_flag: bool | None = None,
    flag_value: Any | None = None,
    count: bool = False,
    allow_from_autoenv: bool = True,
    help: str | None = None,
    hidden: bool = False,
    show_choices: bool = True,
    show_envvar: bool = False,
    panel: str | list[str] | None = None,
    help_style: StyleType | None = None,
    **attrs: Any,
) -> Callable[[FC], FC]: ...

# This is a way to trick PyCharm into adding autocompletion for typed dicts
# without jeopardizing anything on Mypy's side.
@overload
def rich_config(
    help_config: RichHelpConfigurationDict,
    *,
    console: Console | None = ...,
) -> Callable[[FC], FC]: ...
@overload
def rich_config(
    help_config: dict[str, Any] | RichHelpConfigurationDict | RichHelpConfiguration | None = ...,
    *,
    console: Console | None = ...,
) -> Callable[[FC], FC]: ...
def rich_config(
    help_config: dict[str, Any] | RichHelpConfigurationDict | RichHelpConfiguration | None = None,
    *,
    console: Console | None = None,
) -> Callable[[FC], FC]: ...
@overload
def option_panel(
    name: str,
    cls: type[RichPanel[click.Parameter]] = ...,
    *,
    options: list[str] | None = ...,
    help: str | None = ...,
    help_style: StyleType | None = ...,
    table_styles: TableKwargs,
    panel_styles: PanelKwargs,
    column_types: list[OptionColumnType] | None = ...,
    inline_help_in_title: bool | None = ...,
    title_style: StyleType | None = ...,
) -> Callable[[FC], FC]: ...
@overload
def option_panel(
    name: str,
    cls: type[RichPanel[click.Parameter]] = ...,
    *,
    options: list[str] | None = ...,
    help: str | None = ...,
    help_style: StyleType | None = ...,
    table_styles: dict[str, Any] | None = ...,
    panel_styles: dict[str, Any] | None = ...,
    column_types: list[OptionColumnType] | None = ...,
    inline_help_in_title: bool | None = ...,
    title_style: StyleType | None = ...,
) -> Callable[[FC], FC]: ...
def option_panel(
    name: str,
    cls: type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    options: list[str] | None = None,
    help: str | None = None,
    help_style: StyleType | None = None,
    table_styles: TableKwargs | dict[str, Any] | None = None,
    panel_styles: PanelKwargs | dict[str, Any] | None = None,
    column_types: list[OptionColumnType] | None = None,
    inline_help_in_title: bool | None = None,
    title_style: StyleType | None = None,
) -> Callable[[FC], FC]: ...
@overload
def command_panel(
    name: str,
    cls: type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    commands: list[str] | None = ...,
    help: str | None = ...,
    help_style: StyleType | None = ...,
    table_styles: TableKwargs,
    panel_styles: PanelKwargs,
    column_types: list[CommandColumnType] | None = ...,
    inline_help_in_title: bool | None = ...,
    title_style: StyleType | None = ...,
) -> Callable[[FC], FC]: ...
@overload
def command_panel(
    name: str,
    cls: type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    commands: list[str] | None = ...,
    help: str | None = ...,
    help_style: StyleType | None = ...,
    table_styles: dict[str, Any] | None = ...,
    panel_styles: dict[str, Any] | None = ...,
    column_types: list[CommandColumnType] | None = ...,
    inline_help_in_title: bool | None = ...,
    title_style: StyleType | None = ...,
) -> Callable[[FC], FC]: ...
@overload
def command_panel(
    name: str,
    cls: type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    commands: list[str] | None = ...,
    help: str | None = ...,
    help_style: StyleType | None = ...,
    table_styles: None,
    panel_styles: None,
    column_types: list[CommandColumnType] | None = ...,
    inline_help_in_title: bool | None = ...,
    title_style: StyleType | None = ...,
) -> Callable[[FC], FC]: ...
def command_panel(
    name: str,
    cls: type[RichPanel[click.Parameter]] = RichOptionPanel,
    *,
    commands: list[str] | None = None,
    help: str | None = None,
    help_style: StyleType | None = None,
    table_styles: dict[str, Any] | None = None,
    panel_styles: dict[str, Any] | None = None,
    column_types: list[CommandColumnType] | None = None,
    inline_help_in_title: bool | None = None,
    title_style: StyleType | None = None,
) -> Callable[[FC], FC]: ...

PSpec = ParamSpec("PSpec")
R = TypeVar("R")

def pass_context(f: Callable[Concatenate[RichContext, PSpec], R]) -> Callable[PSpec, R]: ...

__all__ = [
    "command",
    "group",
    "argument",
    "option",
    "password_option",
    "confirmation_option",
    "version_option",
    "help_option",
    "rich_config",
    "option_panel",
    "command_panel",
    "pass_context",
]
