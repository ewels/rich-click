from __future__ import annotations

from collections.abc import Callable, Iterable, MutableMapping, Sequence
from typing import (
    Any,
    Literal,
    NoReturn,
    TypeVar,
    overload,
)

import click

# Group, Command, and CommandCollection need to be imported directly,
# or else rich_click.cli.patch() causes a recursion error.
from click import Group
from rich.console import Console

from rich_click._internal_types import RichContextSettingsDict
from rich_click.rich_context import RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration
from rich_click.rich_help_formatter import RichHelpFormatter
from rich_click.rich_help_rendering import RichPanelRow
from rich_click.rich_panel import RichCommandPanel, RichPanel

_AnyCallable = Callable[..., Any]
C = TypeVar("C", bound=click.Command)
G = TypeVar("G", bound=click.Group)

# TLDR: if a subcommand overrides one of the methods called by `RichCommand.format_help`,
# then the text won't render properly. The fix is to not rely on the composability of the API,
# and to instead force everything to use RichCommand's methods.
OVERRIDES_GUARD: bool = False

class RichCommand(click.Command):

    context_class: type[RichContext] = RichContext
    _formatter: RichHelpFormatter | None = None
    panels: list[RichPanel[Any, Any]]
    panel: str | None
    aliases: Iterable[str]

    def __init__(
        self,
        *args: Any,
        aliases: Iterable[str] | None = None,
        panels: list[RichPanel[Any, Any]] | None = None,
        panel: str | None = None,
        name: str | None,
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
    ) -> None: ...
    @property
    def console(self) -> Console | None: ...
    @property
    def help_config(self) -> RichHelpConfiguration | None: ...
    def _generate_rich_help_config(self) -> RichHelpConfiguration: ...
    def _error_formatter(self) -> RichHelpFormatter: ...
    @overload
    def main(
        self,
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: Literal[True] = True,
        **extra: Any,
    ) -> NoReturn: ...
    @overload
    def main(
        self,
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = ...,
        **extra: Any,
    ) -> Any: ...
    def main(
        self,
        args: Sequence[str] | None = None,
        prog_name: str | None = None,
        complete_var: str | None = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: Any,
    ) -> Any: ...
    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None: ...
    def format_help_text(self, ctx: RichContext, formatter: RichHelpFormatter) -> None: ...
    def format_options(self, ctx: RichContext, formatter: RichHelpFormatter) -> None: ...
    def format_epilog(self, ctx: RichContext, formatter: RichHelpFormatter) -> None: ...
    def get_help_option(self, ctx: RichContext) -> click.Option | None: ...
    def get_rich_table_row(
        self,
        ctx: RichContext,
        formatter: RichHelpFormatter,
        panel: RichCommandPanel | None = None,
    ) -> RichPanelRow: ...
    def add_panel(self, panel: RichPanel[Any, Any]) -> None: ...
    def add_command_to_panel(
        self,
        command_name: str,
        panel_name: str | Iterable[str],
    ) -> None: ...

class RichGroup(RichCommand, click.Group):
    """
    Richly formatted click Group.

    Inherits click.Group and overrides help and error methods
    to print richly formatted output.
    """

    command_class: type[RichCommand] | None = RichCommand
    group_class: type[Group] | type[type] | None = type
    _alias_mapping: dict[str, str]
    _panel_command_mapping: dict[str, list[str]]

    def __init__(
        self,
        panels: list[RichPanel[Any, Any]] | None = None,
        aliases: Iterable[str] | None = None,
        name: str | None = None,
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
    ) -> None: ...
    def format_commands(self, ctx: RichContext, formatter: RichHelpFormatter) -> None: ...
    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

    # variant: no call, directly as decorator for a function.
    @overload
    def command(self, name: _AnyCallable) -> RichCommand: ...
    @overload
    def command(
        self,
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
        panel: str | None = ...,
    ) -> Callable[[_AnyCallable], C]: ...
    @overload
    def command(
        self,
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
        panel: str | None = ...,
    ) -> Callable[[_AnyCallable], RichCommand]: ...
    @overload
    def command(
        self,
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
        panel: str | None = ...,
    ) -> Callable[[_AnyCallable], C]: ...
    @overload
    def command(
        self,
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
        panel: str | None = ...,
        **attrs: Any,
    ) -> Callable[[_AnyCallable], RichCommand]: ...

    # variant: with positional name and with positional or keyword cls argument:
    # @command(namearg, CommandCls, ...) or @command(namearg, cls=CommandCls, ...)
    @overload
    def command(
        self,
        name: str | None,
        cls: type[C],
        **attrs: Any,
    ) -> Callable[[_AnyCallable], C]: ...

    # variant: name omitted, cls _must_ be a keyword argument, @command(cls=CommandCls, ...)
    @overload
    def command(
        self,
        name: None = None,
        *,
        cls: type[C],
        **attrs: Any,
    ) -> Callable[[_AnyCallable], C]: ...

    # variant: with optional string name, no cls argument provided.
    @overload
    def command(
        self, name: str | None = ..., cls: None = None, **attrs: Any
    ) -> Callable[[_AnyCallable], RichCommand]: ...
    def command(
        self, name: str | None = None, *, cls: type[C] | None = None, **kwargs: Any
    ) -> Callable[[_AnyCallable], click.Command | C]: ...
    @overload
    def group(self, name: _AnyCallable) -> RichGroup: ...
    @overload
    def group(
        self,
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
        panel: str | None = ...,
    ) -> Callable[[_AnyCallable], G]: ...
    @overload
    def group(
        self,
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
        panel: str | None = ...,
    ) -> Callable[[_AnyCallable], RichGroup]: ...
    @overload
    def group(
        self,
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
        panel: str | None = ...,
    ) -> Callable[[_AnyCallable], G]: ...
    @overload
    def group(
        self,
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
        panel: str | None = ...,
    ) -> Callable[[_AnyCallable], RichGroup]: ...

    # variant: with positional name and with positional or keyword cls argument:
    # @group(namearg, GroupCls, ...) or @group(namearg, cls=GroupCls, ...)
    @overload
    def group(
        self,
        name: str | None,
        cls: type[G],
        **attrs: Any,
    ) -> Callable[[_AnyCallable], G]: ...

    # variant: name omitted, cls _must_ be a keyword argument, @group(cmd=GroupCls, ...)
    @overload
    def group(
        self,
        name: None = None,
        *,
        cls: type[G],
        **attrs: Any,
    ) -> Callable[[_AnyCallable], G]: ...

    # variant: with optional string name, no cls argument provided.
    @overload
    def group(self, name: str | None = ..., cls: None = None, **attrs: Any) -> Callable[[_AnyCallable], RichGroup]: ...
    def group(
        self,
        name: str | _AnyCallable | None = None,
        cls: type[G] | None = None,
        **attrs: Any,
    ) -> click.Group | Callable[[_AnyCallable], RichGroup | G]: ...
    def get_command(self, ctx: click.Context, cmd_name: str) -> click.Command | None: ...
    def add_command(
        self,
        cmd: click.Command,
        name: str | None = None,
        aliases: Iterable[str] | None = None,
        panel: str | None = None,
    ) -> None: ...
    def _handle_extras_add_command(
        self,
        cmd: click.Command,
        name: str | None = None,
        aliases: Iterable[str] | None = None,
        panel: str | list[str] | None = None,
    ) -> None: ...

class RichMultiCommand(RichGroup, click.CommandCollection):
    pass

class RichCommandCollection(RichGroup, click.CommandCollection):
    pass
