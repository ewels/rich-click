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

from rich_click._agent_detection import is_agent_mode
from rich_click.rich_command import RichCommand, RichGroup
from rich_click.rich_context import RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration
from rich_click.rich_panel import RichCommandPanel, RichOptionPanel, RichPanel
from rich_click.rich_parameter import RichArgument, RichHelpOption, RichOption


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
    Group decorator function.

    Defines the group() function so that it uses the RichGroup class by default.
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
    Command decorator function.

    Defines the command() function so that it uses the RichCommand class by default.
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

        return click_command(name, cls, **attrs)(f)

    if func is not None:
        return decorator(func)

    return decorator


def _context_settings_memo(f: Callable[..., Any], extra: dict[str, Any]) -> None:
    if isinstance(f, RichCommand):
        f.context_settings.update(extra)
    else:
        if not hasattr(f, "__rich_context_settings__"):
            f.__rich_context_settings__ = {}  # type: ignore

        f.__rich_context_settings__.update(extra)  # type: ignore


def _rich_panel_memo(f: Callable[..., Any], panel: RichPanel[Any, Any]) -> None:
    if isinstance(f, RichCommand):
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
    Use decorator to configure Rich Click settings.

    Args:
    ----
        help_config: Rich help configuration that is used internally to format help messages and exceptions
            Defaults to None.
        console: A Rich Console that will be accessible from the `RichContext`, `RichCommand`, and `RichGroup` instances
            Defaults to None.

    """
    from rich.console import Console

    if isinstance(help_config, Console) and console is None:
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
    Use decorator to create a RichOptionPanel.

    Args:
    ----
        name: Name of the RichOptionPanel instance being created.
        cls: The class of the RichPanel; defaults to RichOptionPanel.
        attrs: Additional attributes to pass to the RichOptionPanel.

    """
    return _panel(name, cls, **attrs)


def command_panel(
    name: str,
    cls: type[RichPanel[Command, Any]] = RichCommandPanel,
    **attrs: Any,
) -> Callable[[FC], FC]:
    """
    Use decorator to create a RichCommandPanel.

    Args:
    ----
        name: Name of the RichCommandPanel instance being created.
        cls: The class of the RichPanel; defaults to RichCommandPanel.
        attrs: Additional attributes to pass to the RichCommandPanel.

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


#: Sentinel ``flag_value`` for a bare ``--help`` (no attached format). Distinct from any real format
#: name and from ``True`` (a plain boolean flag), so the callback can tell "show normal help" apart from
#: "render format X". The null bytes make an accidental collision with a real CLI value impossible.
HELP_PLAIN_VALUE = "\x00__rich_click_plain_help__\x00"


def _emit_help_text(ctx: Context, text: str) -> None:
    # Avoid click.echo(), which ignores console settings like force_terminal. Every help
    # document goes through here -- human and machine-readable alike -- so ``help_to_stderr``
    # keeps stdout clean whichever one is rendered.
    if getattr(ctx, "help_to_stderr", False):
        print(text, file=sys.stderr)
    else:
        print(text)


def _show_legacy_help(ctx: Context, param: Parameter, value: bool) -> None:
    """Print normal help for the legacy Boolean flag."""
    if value and not ctx.resilient_parsing:
        _emit_help_text(ctx, ctx.get_help())
        ctx.exit()


def _base_help_option_defaults() -> dict[str, Any]:
    """Defaults shared by the legacy Boolean flag and the format-aware ``--help`` option."""
    return {
        "expose_value": False,
        "is_eager": True,
        "help": gettext("Show this message and exit."),
    }


def _legacy_help_option_attrs(kwargs: dict[str, Any]) -> dict[str, Any]:
    """Apply the defaults from the help option used before structured formats."""
    attrs = dict(kwargs)
    for key, value in _base_help_option_defaults().items():
        attrs.setdefault(key, value)
    attrs.setdefault("is_flag", True)
    attrs.setdefault("callback", _show_legacy_help)
    attrs.setdefault("cls", RichOption)
    return attrs


def _legacy_help_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]:
    """Build the Boolean help flag used before machine-readable formats were added."""
    if not param_decls:
        param_decls = ("--help",)
    return click_option(*param_decls, **_legacy_help_option_attrs(kwargs))


def _legacy_help_option_from(option: RichHelpOption) -> RichOption:
    """Return the cached legacy form of an explicitly declared format-aware help option."""
    cached = getattr(option, "_rich_click_legacy_option", None)
    if cached is not None:
        return cast(RichOption, cached)

    metadata = getattr(option, "_rich_click_legacy_declaration", None)
    if metadata is None:
        param_decls = (*option.opts, *option.secondary_opts)
        kwargs = {
            "help": option.help,
            "hidden": option.hidden,
            "panel": option.panel,
            "help_style": option.help_style,
        }
    else:
        param_decls, kwargs = metadata

    attrs = _legacy_help_option_attrs(kwargs)
    option_class = attrs.pop("cls")
    legacy = option_class(param_decls, **attrs)
    option._rich_click_legacy_option = legacy  # type: ignore[attr-defined]
    return cast(RichOption, legacy)


def help_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]:
    """
    Pre-configured ``--help`` option which immediately prints the help page
    and exits the program.

    Accepts an optional format value so the same flag can also emit machine-readable help:
    ``--help compact`` (character-lean, whole tree), ``--help markdown`` (LLM-friendly), and
    ``--help json`` (structured data). Installed plugins can add more values. The space
    form is the documented one, though the attached form (``--help=json``) works too. An unrecognized
    value falls back to the normal help rather than erroring (just as the plain ``--help`` always ignored
    anything that followed it).

    A bare ``--help`` renders the normal human-readable help, except in a detected AI agent environment,
    where it renders the ``agent_help_format`` config option's format (``compact`` by default; ``None``
    disables the switch).

    :param param_decls: One or more option names. Defaults to the single
        value ``"--help"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    """
    legacy_kwargs = dict(kwargs)

    def show_help(ctx: Context, param: Parameter, value: Any) -> None:
        """Callback that prints the help page (human or machine-readable) and exits."""
        # ``None`` / ``False`` mean the flag was not given; an empty string (``--help=``) is still a
        # request for help -- it falls through to the normal help below, like a bare ``--help``.
        if value is None or value is False or ctx.resilient_parsing:
            return
        # A real format was given (e.g. ``--help json``); the sentinel / ``True`` / empty string (``--help=``)
        # all mean a bare ``--help``.
        if value and value is not True and value != HELP_PLAIN_VALUE:
            get_help_for_format = getattr(ctx.command, "get_help_for_format", None)
            if get_help_for_format is not None:
                rendered = get_help_for_format(ctx, value)
                if rendered is not None:
                    _emit_help_text(ctx, rendered)
                    ctx.exit()
            # Unknown format (or a non-rich command): fall through to normal help.
        else:
            # Bare ``--help`` in a detected AI agent environment: render the configured machine-readable
            # format instead, so an agent gets help it can parse without having to know the format exists.
            # Only a bare ``--help`` is redirected -- an explicit ``--help <format>`` above is always
            # honoured verbatim, in any environment.
            agent_help_format = getattr(getattr(ctx, "help_config", None), "agent_help_format", None)
            if agent_help_format is not None and is_agent_mode():
                get_help_for_format = getattr(ctx.command, "get_help_for_format", None)
                if get_help_for_format is not None:
                    # Flagged for the duration of the render, so a format can tell "the agent default"
                    # apart from "asked for by name" -- `--help compact` renders the whole tree, while
                    # the same format as the agent default adapts to `agent_help_max_chars`.
                    agent_ctx = ctx if isinstance(ctx, RichContext) else None
                    if agent_ctx is not None:
                        agent_ctx.agent_help_default = True
                    try:
                        rendered = get_help_for_format(ctx, agent_help_format)
                    finally:
                        if agent_ctx is not None:
                            agent_ctx.agent_help_default = False
                    if rendered is not None:
                        _emit_help_text(ctx, rendered)
                        ctx.exit()
                # Unregistered format name: fall through to the normal help rather than erroring.
        # Do not print() if empty string; assume console was record=False.
        _emit_help_text(ctx, ctx.get_help())
        ctx.exit()

    if not param_decls:
        param_decls = ("--help",)

    # Optional-value flag: ``flag_value`` is what a bare ``--help`` yields; a format given after it
    # (``--help json``) is passed through verbatim. ``RichHelpOption`` shows a ``FORMAT`` metavar, so the
    # optional value is conveyed the same way as any other value-taking option rather than via help text.
    for key, value in _base_help_option_defaults().items():
        kwargs.setdefault(key, value)
    kwargs.setdefault("is_flag", False)
    kwargs.setdefault("flag_value", HELP_PLAIN_VALUE)
    kwargs.setdefault("callback", show_help)
    kwargs.setdefault("cls", RichHelpOption)

    option_decorator = click_option(*param_decls, **kwargs)

    def decorator(obj: FC) -> FC:
        result = option_decorator(obj)
        # click.option() always appends the new parameter to the end of the target's params list.
        params = getattr(result, "params", getattr(result, "__click_params__", []))
        added = params[-1]
        added._rich_click_legacy_declaration = (param_decls, legacy_kwargs)
        return result

    return decorator


def argument(*param_decls: str, cls: type[Argument] | None = None, **attrs: Any) -> Callable[[FC], FC]:
    """
    Attaches an argument to the command.  All positional arguments are
    passed as parameter declarations to :class:`Argument`; all keyword
    arguments are forwarded unchanged (except ``cls``).
    This is equivalent to creating an :class:`Argument` instance manually
    and attaching it to the :attr:`Command.params` list.

    For the default argument class, refer to :class:`Argument` and
    :class:`Parameter` for descriptions of parameters.

    :param cls: the argument class to instantiate.  This defaults to
                :class:`Argument`.
    :param param_decls: Passed as positional arguments to the constructor of
        ``cls``.
    :param attrs: Passed as keyword arguments to the constructor of ``cls``.
    """
    if cls is None:
        cls = RichArgument

    return click_argument(*param_decls, cls=cls, **attrs)


def option(*param_decls: str, cls: type[Option] | None = None, **attrs: Any) -> Callable[[FC], FC]:
    """
    Attaches an option to the command.  All positional arguments are
    passed as parameter declarations to :class:`Option`; all keyword
    arguments are forwarded unchanged (except ``cls``).
    This is equivalent to creating an :class:`Option` instance manually
    and attaching it to the :attr:`Command.params` list.

    For the default option class, refer to :class:`Option` and
    :class:`Parameter` for descriptions of parameters.

    :param cls: the option class to instantiate.  This defaults to
                :class:`Option`.
    :param param_decls: Passed as positional arguments to the constructor of
        ``cls``.
    :param attrs: Passed as keyword arguments to the constructor of ``cls``.
    """
    if cls is None:
        cls = RichOption

    return click_option(*param_decls, cls=cls, **attrs)


def confirmation_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]:
    """
    Add a ``--yes`` option which shows a prompt before continuing if
    not passed. If the prompt is declined, the program will exit.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--yes"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    """
    kwargs.setdefault("cls", RichOption)
    return click_confirmation_option(*param_decls, **kwargs)


def password_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]:
    """
    Add a ``--password`` option which prompts for a password, hiding
    input and asking to enter the value again for confirmation.

    :param param_decls: One or more option names. Defaults to the single
        value ``"--password"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
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
    Add a ``--version`` option which immediately prints the version
    number and exits the program.

    If ``version`` is not provided, Click will try to detect it using
    :func:`importlib.metadata.version` to get the version for the
    ``package_name``. On Python < 3.8, the ``importlib_metadata``
    backport must be installed.

    If ``package_name`` is not provided, Click will try to detect it by
    inspecting the stack frames. This will be used to detect the
    version, so it must match the name of the installed package.

    :param version: The version number to show. If not provided, Click
        will try to detect it.
    :param param_decls: One or more option names. Defaults to the single
        value ``"--version"``.
    :param package_name: The package name to detect the version from. If
        not provided, Click will try to detect it.
    :param prog_name: The name of the CLI to show in the message. If not
        provided, it will be detected from the command.
    :param message: The message to show. The values ``%(prog)s``,
        ``%(package)s``, and ``%(version)s`` are available. Defaults to
        ``"%(prog)s, version %(version)s"``.
    :param kwargs: Extra arguments are passed to :func:`option`.
    :raise RuntimeError: ``version`` could not be detected.
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
