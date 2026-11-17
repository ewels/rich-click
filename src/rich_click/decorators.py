from __future__ import annotations

import sys
from collections.abc import Callable
from gettext import gettext
from typing import (
    TYPE_CHECKING,
    Any,
    Concatenate,
    ParamSpec,
    TypeVar,
    cast,
    overload,
)

from click import Argument, Command, Context, Group, Option, Parameter
from click import argument as click_argument
from click import command as click_command
from click import confirmation_option as click_confirmation_option
from click import option as click_option
from click import pass_context as click_pass_context
from click import password_option as click_password_option
from click import version_option as click_version_option

from rich_click._click_types_cache import get_command_decorator
from rich_click.rich_command import RichCommand, RichCommandMixin, RichGroup
from rich_click.rich_context import RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration
from rich_click.rich_panel import RichCommandPanel, RichOptionPanel, RichPanel
from rich_click.rich_parameter import RichArgument, RichOption


if TYPE_CHECKING:  # pragma: no cover
    from rich.console import Console


_AnyCallable = Callable[..., Any]
F = TypeVar("F", bound=Callable[..., Any])
FC = TypeVar("FC", bound=Command | _AnyCallable)
C = TypeVar("C", bound=Command)


G = TypeVar("G", bound=Group)


# variant: no call, directly as decorator for a function.
@overload
def group(name: _AnyCallable) -> RichGroup: ...


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
) -> Group | Callable[[_AnyCallable], RichGroup | G]:
    """
    Create a group of subcommands.

    The same as `click.group`, but the group is a `RichGroup` unless you set `cls`.
    """
    if cls is None:
        cls = cast(type[G], RichGroup)

    if callable(name):
        return command(cls=cls, **attrs)(name)

    return command(name, cls, **attrs)


CmdType = TypeVar("CmdType", bound=Command)


# variant: no call, directly as decorator for a function.
@overload
def command(name: _AnyCallable) -> RichCommand: ...


# variant: with positional name and with positional or keyword cls argument:
# @command(namearg, CommandCls, ...) or @command(namearg, cls=CommandCls, ...)
@overload
def command(
    name: str | None,
    cls: type[CmdType],
    **attrs: Any,
) -> Callable[[_AnyCallable], CmdType]: ...


# variant: name omitted, cls _must_ be a keyword argument, @command(cls=CommandCls, ...)
@overload
def command(
    name: None = None,
    *,
    cls: type[CmdType],
    **attrs: Any,
) -> Callable[[_AnyCallable], CmdType]: ...


# variant: with optional string name, no cls argument provided.
@overload
def command(name: str | None = ..., cls: None = None, **attrs: Any) -> Callable[[_AnyCallable], RichCommand]: ...


def command(
    name: str | None | _AnyCallable = None,
    cls: type[CmdType] | None = None,
    **attrs: Any,
) -> Command | Callable[[_AnyCallable], RichCommand | CmdType]:
    """
    Create a command.

    The same as `click.command`, but the command is a `RichCommand` unless you set `cls`.
    """
    func = None
    if callable(name):
        func = name
        name = None
        if "__rich_click_cli_patch" not in attrs:
            assert cls is None, "Use 'command(cls=cls)(callable)' to specify a class."
        attrs.pop("__rich_click_cli_patch", None)
        assert not attrs, "Use 'command(**kwargs)(callable)' to provide arguments."
    else:
        attrs.pop("__rich_click_cli_patch", None)

    if cls is None:
        cls = cast(type[CmdType], RichCommand)

    def decorator(f: _AnyCallable) -> CmdType:
        cs = getattr(f, "__rich_context_settings__", None)
        if cs is not None:
            attr_cs = attrs.pop("context_settings", None)
            attr_cs = attr_cs if attr_cs is not None else {}
            attr_cs.update(cs)
            attrs["context_settings"] = attr_cs
            del f.__rich_context_settings__  # type: ignore[attr-defined]

        panels = getattr(f, "__rich_panels__", None)
        if panels is not None:
            attr_panels = attrs.pop("panels", None)
            attr_panels = attr_panels if attr_panels is not None else []
            attr_panels.extend(reversed(panels))
            attrs["panels"] = attr_panels
            del f.__rich_panels__  # type: ignore[attr-defined]

        command_decorator = get_command_decorator(cls) or click_command
        return command_decorator(name, cls, **attrs)(f)

    if func is not None:
        return decorator(func)

    return decorator


def _context_settings_memo(f: Callable[..., Any], extra: dict[str, Any]) -> None:
    if isinstance(f, RichCommandMixin):
        f.context_settings.update(extra)
    else:
        if not hasattr(f, "__rich_context_settings__"):
            f.__rich_context_settings__ = {}  # type: ignore

        f.__rich_context_settings__.update(extra)  # type: ignore


def _rich_panel_memo(f: Callable[..., Any], panel: RichPanel[Any, Any]) -> None:
    if isinstance(f, RichCommandMixin):
        f.add_panel(panel)
    else:
        if not hasattr(f, "__rich_panels__"):
            f.__rich_panels__ = []  # type: ignore

        f.__rich_panels__.append(panel)  # type: ignore


def rich_config(
    help_config: dict[str, Any] | RichHelpConfiguration | None = None,
    *,
    console: Console | None = None,
) -> Callable[[FC], FC]:
    """
    Set the help configuration and the Rich console of one command or group.

    Args:
        help_config: How to format help and errors, as a `RichHelpConfiguration` or a dict of its fields.
        console: Rich console to print help and errors with. The context makes it available as `ctx.console`.
    """
    # Avoid importing rich eagerly: a Console instance can only exist if rich.console is already imported.
    rich_console_module = sys.modules.get("rich.console")
    if console is None and rich_console_module is not None and isinstance(help_config, rich_console_module.Console):
        import warnings

        warnings.warn(
            "`rich_config()`'s args have been swapped."
            " Please set the config first, and use a kwarg to set the console.",
            DeprecationWarning,
            stacklevel=2,
        )
        console = help_config

    def decorator(obj: FC) -> FC:
        extra: dict[str, Any] = {}
        if console is not None:
            extra["rich_console"] = console
        if help_config is not None:
            extra["rich_help_config"] = help_config

        _context_settings_memo(obj, extra)

        return obj

    return decorator


def _panel(
    name: str,
    cls: type[RichPanel[Any, Any]],
    **attrs: Any,
) -> Callable[[FC], FC]:
    def decorator(obj: FC) -> FC:
        _rich_panel_memo(
            obj,
            cls(name=name, **attrs),
        )
        return obj

    return decorator


def option_panel(
    name: str,
    cls: type[RichPanel[Parameter, Any]] = RichOptionPanel,
    **attrs: Any,
) -> Callable[[FC], FC]:
    """
    Show a group of options in a panel of its own in the help output.

    Args:
        name: Title of the panel.
        cls: Panel class. Defaults to `RichOptionPanel`.
        **attrs: Other arguments for the panel class, such as `options` and `help`.
    """
    return _panel(name, cls, **attrs)


def command_panel(
    name: str,
    cls: type[RichPanel[Command, Any]] = RichCommandPanel,
    **attrs: Any,
) -> Callable[[FC], FC]:
    """
    Show a group of subcommands in a panel of its own in the help output.

    Args:
        name: Title of the panel.
        cls: Panel class. Defaults to `RichCommandPanel`.
        **attrs: Other arguments for the panel class, such as `commands` and `help`.
    """
    return _panel(name, cls, **attrs)


# Users of rich_click would face issues using mypy with this code,
# if not for wrapping `pass_context` with a new function signature:
#
# @click.command()
# @click.pass_context
# def cli(ctx: click.RichContext) -> None:
#    ...


P = ParamSpec("P")
R = TypeVar("R")


def pass_context(f: Callable[Concatenate[RichContext, P], R]) -> Callable[P, R]:
    # flake8: noqa: D400,D401
    """Marks a callback as wanting to receive the current context object as first argument."""
    return click_pass_context(f)  # type: ignore[arg-type,unused-ignore]


def help_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]:
    """
    Add a `--help` option that prints the help and exits.

    Args:
        *param_decls: Option names. Defaults to `--help`.
        **kwargs: Other arguments for `option`.
    """

    def show_help(ctx: Context, param: Parameter, value: bool) -> None:
        """Callback that print the help page on ``<stdout>`` and exits."""
        if value and not ctx.resilient_parsing:
            # Avoid click.echo() because it ignores console settings like force_terminal.
            # Also, do not print() if empty string; assume console was record=False.
            if getattr(ctx, "help_to_stderr", False):
                print(ctx.get_help(), file=sys.stderr)
            else:
                print(ctx.get_help())
            ctx.exit()

    if not param_decls:
        param_decls = ("--help",)

    kwargs.setdefault("is_flag", True)
    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault("help", gettext("Show this message and exit."))
    kwargs.setdefault("callback", show_help)
    kwargs.setdefault("cls", RichOption)

    return click_option(*param_decls, **kwargs)


def argument(*param_decls: str, cls: type[Argument] | None = None, **attrs: Any) -> Callable[[FC], FC]:
    """
    Add a positional argument to the command.

    The same as `click.argument`, but the argument is a `RichArgument` unless you set `cls`.

    Args:
        *param_decls: Name of the argument.
        cls: Argument class. Defaults to `RichArgument`.
        **attrs: Other arguments for the `cls` constructor, such as `nargs` and `type`. See `click.Argument`.
    """
    if cls is None:
        cls = RichArgument

    return click_argument(*param_decls, cls=cls, **attrs)


def option(*param_decls: str, cls: type[Option] | None = None, **attrs: Any) -> Callable[[FC], FC]:
    """
    Add an option to the command.

    The same as `click.option`, but the option is a `RichOption` unless you set `cls`.

    Args:
        *param_decls: Names of the option, such as `"--count"` and `"-c"`.
        cls: Option class. Defaults to `RichOption`.
        **attrs: Other arguments for the `cls` constructor, such as `default` and `help`. See `click.Option`.
    """
    if cls is None:
        cls = RichOption

    return click_option(*param_decls, cls=cls, **attrs)


def confirmation_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]:
    """
    Add a `--yes` option. Without it, the command asks the user to confirm, and exits if they decline.

    Args:
        *param_decls: Option names. Defaults to `--yes`.
        **kwargs: Other arguments for `option`.
    """
    kwargs.setdefault("cls", RichOption)
    return click_confirmation_option(*param_decls, **kwargs)


def password_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]:
    """
    Add a `--password` option that prompts for the password two times and hides the input.

    Args:
        *param_decls: Option names. Defaults to `--password`.
        **kwargs: Other arguments for `option`.
    """
    if not param_decls:
        param_decls = ("--password",)

    kwargs.setdefault("prompt", True)
    kwargs.setdefault("confirmation_prompt", True)
    kwargs.setdefault("hide_input", True)
    kwargs.setdefault("cls", RichOption)
    return click_password_option(*param_decls, **kwargs)


def version_option(
    version: str | None = None,
    *param_decls: str,
    package_name: str | None = None,
    prog_name: str | None = None,
    message: str | None = None,
    **kwargs: Any,
) -> Callable[[FC], FC]:
    """
    Add a `--version` option that prints the version and exits.

    Args:
        version: Version to print. If not set, Click reads it from the metadata of the installed `package_name`.
        *param_decls: Option names. Defaults to `--version`.
        package_name: Installed package to read the version from. If not set, Click finds it from the
            stack frames, so the module name must match the name of the installed package.
        prog_name: Name of the CLI in the message. If not set, Click uses the name of the command.
        message: Message to print. It can use `%(prog)s`, `%(package)s` and `%(version)s`.
            Defaults to `"%(prog)s, version %(version)s"`.
        **kwargs: Other arguments for `option`.

    Raises:
        RuntimeError: Click cannot find the version.
    """
    kwargs.setdefault("cls", RichOption)
    return click_version_option(
        version, *param_decls, package_name=package_name, prog_name=prog_name, message=message, **kwargs
    )


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
