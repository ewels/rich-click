from __future__ import annotations

import errno
import os
import sys
import warnings
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    TextIO,
    Type,
    Union,
    cast,
    overload,
)

import click

# Group, Command, and CommandCollection need to be imported directly,
# or else rich_click.cli.patch() causes a recursion error.
from click import CommandCollection, Group
from click.utils import PacifyFlushWrapper

from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_9X, CLICK_IS_BEFORE_VERSION_82
from rich_click.rich_context import RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration
from rich_click.rich_help_formatter import RichHelpFormatter
from rich_click.rich_panel import construct_panels
from rich_click.tree_help_rendering import tree_format_help


if TYPE_CHECKING:  # pragma: no cover
    from types import TracebackType

    from rich.console import Console

    from rich_click.rich_panel import RichPanel


# TLDR: if a subcommand overrides one of the methods called by `RichCommand.format_help`,
# then the text won't render properly. The fix is to not rely on the composability of the API,
# and to instead force everything to use RichCommand's methods.
OVERRIDES_GUARD: bool = False


class RichCommand(click.Command):
    """
    Richly formatted click Command.

    Inherits click.Command and overrides help and error methods
    to print richly formatted output.

    This class can be used as a mixin for other click command objects.
    """

    context_class: Type[RichContext] = RichContext
    _formatter: Optional[RichHelpFormatter] = None

    def __init__(self, *args: Any, panels: Optional[List["RichPanel[Any]"]] = None, **kwargs: Any) -> None:
        """Create Rich Command instance."""
        super().__init__(*args, **kwargs)
        self.panels = panels or []
        if not hasattr(self, "_help_option"):
            self._help_option = None
        if not hasattr(self, "_tree_option"):
            self._tree_option = None

    @property
    def console(self) -> Optional["Console"]:
        """
        Rich Console.

        This is a separate instance from the help formatter that allows full control of the
        console configuration.

        See `rich_config` decorator for how to apply the settings.
        """
        import warnings

        warnings.warn(
            "RichCommand.console is deprecated. Please use the click.Context's console instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.context_settings.get("rich_console")

    def to_info_dict(self, ctx: click.Context) -> Dict[str, Any]:
        info = super().to_info_dict(ctx)
        info["panels"] = [p.to_info_dict(ctx) for p in self.panels]
        return info

    @property
    def help_config(self) -> Optional[RichHelpConfiguration]:
        """Rich Help Configuration."""
        import warnings

        warnings.warn(
            "RichCommand.help_config is deprecated. Please use the click.Context's help config instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        cfg = self.context_settings.get("rich_help_config")
        if isinstance(cfg, Mapping):
            return RichHelpConfiguration(**cfg)
        return cfg

    def _generate_rich_help_config(self) -> RichHelpConfiguration:
        """
        Use for error handling when a Context is not available.

        If the Context is available, then the help configuration in the Context
        should be preferred.
        """
        cfg = self.context_settings.get("rich_help_config", {})
        try:
            if isinstance(cfg, Mapping):
                return RichHelpConfiguration.load_from_globals(**cfg)
            elif isinstance(cfg, RichHelpConfiguration):
                return cfg
        except Exception as e:
            click.echo(f"{e.__class__.__name__}{e.args}", file=sys.stderr)
        return RichHelpConfiguration()

    def _error_formatter(self) -> RichHelpFormatter:
        from click import get_current_context

        try:
            ctx: RichContext = get_current_context()  # type: ignore[assignment]
        except RuntimeError:
            config = self._generate_rich_help_config()
            formatter = self.context_class.formatter_class(
                config=config,
                export_console_as=(
                    self.context_class.export_console_as if self.context_class.errors_in_output_format else None
                ),
            )
        else:
            formatter = ctx.make_formatter(error_mode=True)
        return formatter

    def main(
        self,
        args: Optional[Sequence[str]] = None,
        prog_name: Optional[str] = None,
        complete_var: Optional[str] = None,
        standalone_mode: bool = True,
        windows_expand_args: bool = True,
        **extra: Any,
    ) -> Any:
        # It's not feasible to use super().main() in this context and retain exact parity in behavior.
        # The reason why is explained in a comment in click's source code in the "except Exit as e" block.

        if args is None:
            args = sys.argv[1:]

            if os.name == "nt" and windows_expand_args:
                from click.utils import _expand_args

                args = _expand_args(args)
        else:
            args = list(args)

        if TYPE_CHECKING:  # pragma: no cover
            assert args is not None

        if prog_name is None:
            from click.utils import _detect_program_name

            prog_name = _detect_program_name()

        # Process shell completion requests and exit early.
        self._main_shell_completion(extra, prog_name, complete_var)

        ctx = None

        try:
            try:
                with self.make_context(prog_name, args, **extra) as ctx:
                    rv = self.invoke(ctx)
                    if not standalone_mode:
                        return rv
                    # it's not safe to `ctx.exit(rv)` here!
                    # note that `rv` may actually contain data like "1" which
                    # has obvious effects
                    # more subtle case: `rv=[None, None]` can come out of
                    # chained commands which all returned `None` -- so it's not
                    # even always obvious that `rv` indicates success/failure
                    # by its truthiness/falsiness
                    ctx.exit()
            except (EOFError, KeyboardInterrupt):
                click.echo(file=sys.stderr)
                raise click.exceptions.Abort() from None
            except click.exceptions.ClickException as e:
                if not CLICK_IS_BEFORE_VERSION_82:
                    # `except click.exceptions.NoArgsIsHelpError as e:` breaks for click<8.2.
                    if isinstance(e, click.exceptions.NoArgsIsHelpError):
                        print(e.message)
                        sys.exit(e.exit_code)
                if not standalone_mode:
                    raise
                formatter = self._error_formatter()
                formatter.write_error(e)
                print(formatter.getvalue(), file=sys.stderr, end="")
                sys.exit(e.exit_code)
            except OSError as e:
                if e.errno == errno.EPIPE:
                    sys.stdout = cast(TextIO, PacifyFlushWrapper(sys.stdout))
                    sys.stderr = cast(TextIO, PacifyFlushWrapper(sys.stderr))
                    sys.exit(1)
                else:
                    raise
        except click.exceptions.Exit as e:
            if standalone_mode:
                sys.exit(e.exit_code)
            else:
                return e.exit_code
        except click.exceptions.Abort:
            if not standalone_mode:
                raise
            try:
                formatter = self._error_formatter()
            except Exception:
                click.echo("Aborted!", file=sys.stderr)
            else:
                formatter.write_abort()
                print(formatter.getvalue(), file=sys.stderr, end="")
            finally:
                sys.exit(1)

    def make_context(
        self,
        info_name: str | None,
        args: list[str],
        parent: Context | None = None,
        **extra: Any,
    ) -> Context:
        known_context_keys = {
            "help_option_names",
            "auto_envvar_prefix",
            "default_map",
            "token_normalize_func",
            "ignore_unknown_options",
            "allow_extra_args",
            "allow_interspersed_args",
            "color",
            "max_content_width",
            "terminal_width",
            "show_default",
            "resilient_parsing",
        }
        known_rich_keys = {
            "rich_console",
            "rich_help_config",
            "export_console_as",
            "errors_in_output_format",
            "help_to_stderr",
        }
        custom_keys = known_rich_keys | {"tree_option_names"}

        # Merge only known context_settings
        for key, value in self.context_settings.items():
            if key in known_context_keys and key not in extra:
                extra[key] = value
            elif key in known_rich_keys and key not in extra:
                extra[key] = value
            # ignore other custom like tree_option_names

        ctx = self.context_class(self, info_name=info_name, parent=parent, **extra)

        # with augment_usage_errors(self, ctx=ctx):
        with ctx.scope(cleanup=False):
            self.parse_args(ctx, args)

        return ctx

    # Mypy complains about Liskov substitution principle violations.
    # We opt to ignore mypy here.

    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:  # type: ignore[override]
        from rich_click import TREE_OPTION_NAMES

        if TREE_OPTION_NAMES and set(TREE_OPTION_NAMES) & set(ctx.help_option_names):
            self.tree_format_help(ctx, formatter)
        elif OVERRIDES_GUARD:
            prevent_incompatible_overrides(self, "RichCommand", ctx, formatter)
        else:
            self.format_usage(ctx, formatter)
            self.format_help_text(ctx, formatter)
            self.format_options(ctx, formatter)
            self.format_epilog(ctx, formatter)

    def format_help_text(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:  # type: ignore[override]
        from rich_click.rich_help_rendering import get_rich_help_text

        get_rich_help_text(self, ctx, formatter)

    # TODO:
    #  Switching from base click to rich click causes mypy problems.
    #  Either we: (a) swap MRO (incompatible with click 9, without handling 8 and 9 differently)
    #  or (b) we allow issues when users attempt multiple inheritance with a RichCommand
    #  or (c) we use incorrect types here.
    #  We are looking for a solution that fixes all 3. For now, we opt for (c).
    def format_options(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        from rich.table import Table

        from rich_click.rich_panel import construct_panels

        panels = construct_panels(self, ctx, formatter)  # type: ignore[arg-type]
        for panel in panels:
            p = panel.render(self, ctx, formatter)  # type: ignore[arg-type]
            if not isinstance(p.renderable, Table) or len(p.renderable.rows) > 0:
                formatter.write(p)  # type: ignore[arg-type]

    def format_epilog(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:  # type: ignore[override]
        from rich_click.rich_help_rendering import get_rich_epilog

        get_rich_epilog(self, ctx, formatter)

    def get_help_option(self, ctx: click.Context) -> Union[click.Option, None]:
        """
        Return the help option object.

        Skipped if :attr:`add_help_option` is ``False``.

        .. versionchanged:: 8.1.8
            The help option is now cached to avoid creating it multiple times.
        """
        help_option_names = self.get_help_option_names(ctx)

        if not help_option_names or not self.add_help_option:
            return None

        # Cache the help option object in private _help_option attribute to
        # avoid creating it multiple times. Not doing this will break the
        # callback ordering by iter_params_for_processing(), which relies on
        # object comparison.
        if self._help_option is None:
            # Avoid circular import.
            from rich_click.decorators import help_option

            # Apply help_option decorator and pop resulting option
            help_option(*help_option_names)(self)
            self._help_option = self.params.pop()  # type: ignore[assignment]

        return self._help_option

    def get_tree_option(self, ctx: click.Context) -> Union[click.Option, None]:
        """
        Return the tree option object.

        Skipped if :attr:`add_help_option` is ``False`` (reusing the flag for simplicity).
        """
        tree_option_names = self.context_settings.get("tree_option_names")

        if not tree_option_names or not self.add_help_option:
            return None

        # Check if it overrides help
        if set(tree_option_names) & set(ctx.help_option_names):
            self.add_help_option = False

        # Cache the tree option object in private _tree_option attribute to
        # avoid creating it multiple times. Not doing this will break the
        # callback ordering by iter_params_for_processing(), which relies on
        # object comparison.
        if self._tree_option is None:
            # Avoid circular import.
            from rich_click.decorators import tree_option

            # Apply tree_option decorator and pop resulting option
            tree_option(*tree_option_names)(self)
            self._tree_option = self.params.pop()  # type: ignore[assignment]

        return self._tree_option

    def get_params(self, ctx: click.Context) -> List[click.Parameter]:
        params = super().get_params(ctx)
        tree_option = self.get_tree_option(ctx)
        if tree_option is not None:
            params.append(tree_option)
        return params

    def get_tree_help(self, ctx: RichContext) -> str:
        formatter = ctx.make_formatter()
        self.tree_format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def tree_format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:
        tree_format_help(ctx, formatter, isinstance(self, MultiCommand))


if CLICK_IS_BEFORE_VERSION_9X:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        from click import MultiCommand

else:
    MultiCommand = Group  # type: ignore[misc,assignment,unused-ignore]


class RichMultiCommand(RichCommand, MultiCommand):  # type: ignore[valid-type,misc]
    """
    Richly formatted click MultiCommand.

    Inherits click.MultiCommand and overrides help and error methods
    to print richly formatted output.
    """

    def format_commands(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        # Not used
        pass

    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:  # type: ignore[override]
        from rich_click import TREE_OPTION_NAMES

        if TREE_OPTION_NAMES and set(TREE_OPTION_NAMES) & set(ctx.help_option_names):
            self.tree_format_help(ctx, formatter)
        elif OVERRIDES_GUARD:
            prevent_incompatible_overrides(self, "RichMultiCommand", ctx, formatter)
        else:
            self.format_usage(ctx, formatter)
            self.format_help_text(ctx, formatter)
            self.format_options(ctx, formatter)
            self.format_epilog(ctx, formatter)

    def get_tree_help(self, ctx: RichContext) -> str:
        formatter = ctx.make_formatter()
        self.tree_format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def tree_format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:
        tree_format_help(ctx, formatter, isinstance(self, MultiCommand))


class RichGroup(RichMultiCommand, Group):
    """
    Richly formatted click Group.

    Inherits click.Group and overrides help and error methods
    to print richly formatted output.
    """

    command_class: Optional[Type[RichCommand]] = RichCommand
    group_class: Optional[Union[Type[Group], Type[type]]] = type

    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:  # type: ignore[override]
        # from rich_click import TREE_OPTION_NAMES
        # if TREE_OPTION_NAMES and set(TREE_OPTION_NAMES) & set(ctx.help_option_names):
        #     self.tree_format_help(ctx, formatter)
        # elif OVERRIDES_GUARD:
        #     prevent_incompatible_overrides(self, "RichGroup", ctx, formatter)
        # else:
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_options(ctx, formatter)
        self.format_epilog(ctx, formatter)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Alias for :meth:`main`."""
        # Include this here because I run into a false warning
        # in the PyCharm IDE otherwise; for some reason PyCharm doesn't
        # seem to think RichGroups are callable. (No issues with Mypy, though.)
        return super().__call__(*args, **kwargs)

    @overload
    def command(self, __func: Callable[..., Any]) -> RichCommand: ...

    @overload
    def command(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], RichCommand]: ...

    def command(self, *args: Any, **kwargs: Any) -> Union[Callable[[Callable[..., Any]], RichCommand], RichCommand]:
        """
        A shortcut decorator for declaring and attaching a command to
        the group. This takes the same arguments as :func:`command` and
        immediately registers the created command with this group by
        calling :meth:`add_command`.

        To customize the command class used, set the
        :attr:`command_class` attribute.

        .. versionchanged:: 8.1
            This decorator can be applied without parentheses.

        .. versionchanged:: 8.0
            Added the :attr:`command_class` attribute.
        """  # noqa: D401
        from rich_click.decorators import command

        func: Optional[Callable[..., Any]] = None

        if args and callable(args[0]):
            assert len(args) == 1 and not kwargs, "Use 'command(**kwargs)(callable)' to provide arguments."
            (func,) = args
            args = ()

        if self.command_class and kwargs.get("cls") is None:
            kwargs["cls"] = self.command_class

        def decorator(f: Callable[..., Any]) -> RichCommand:
            cmd: RichCommand = command(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd

        if func is not None:
            return decorator(func)

        return decorator

    @overload
    def group(self, __func: Callable[..., Any]) -> "RichGroup": ...

    @overload
    def group(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], "RichGroup"]: ...

    def group(self, *args: Any, **kwargs: Any) -> Union[Callable[[Callable[..., Any]], "RichGroup"], "RichGroup"]:
        """
        A shortcut decorator for declaring and attaching a group to
        the group. This takes the same arguments as :func:`group` and
        immediately registers the created group with this group by
        calling :meth:`add_command`.

        To customize the group class used, set the :attr:`group_class`
        attribute.

        .. versionchanged:: 8.1
            This decorator can be applied without parentheses.

        .. versionchanged:: 8.0
            Added the :attr:`group_class` attribute.
        """  # noqa: D401
        from rich_click.decorators import group

        func: Optional[Callable[..., Any]] = None

        if args and callable(args[0]):
            assert len(args) == 1 and not kwargs, "Use 'group(**kwargs)(callable)' to provide arguments."
            (func,) = args
            args = ()

        if self.group_class is not None and kwargs.get("cls") is None:
            if self.group_class is type:
                kwargs["cls"] = type(self)
            else:
                kwargs["cls"] = self.group_class

        def decorator(f: Callable[..., Any]) -> RichGroup:
            cmd: RichGroup = group(*args, **kwargs)(f)
            self.add_command(cmd)
            return cmd

        if func is not None:
            return decorator(func)

        return decorator


class RichCommandCollection(CommandCollection, RichGroup):
    """
    Richly formatted click CommandCollection.

    Inherits click.CommandCollection and overrides help and error methods
    to print richly formatted output.
    """

    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:  # type: ignore[override]
        from rich_click import TREE_OPTION_NAMES

        if TREE_OPTION_NAMES and set(TREE_OPTION_NAMES) & set(ctx.help_option_names):
            self.tree_format_help(ctx, formatter)
        elif OVERRIDES_GUARD:
            prevent_incompatible_overrides(self, "RichCommandCollection", ctx, formatter)
        else:
            self.format_usage(ctx, formatter)
            self.format_help_text(ctx, formatter)
            self.format_options(ctx, formatter)
            self.format_epilog(ctx, formatter)

    def get_tree_help(self, ctx: RichContext) -> str:
        formatter = ctx.make_formatter()
        self.tree_format_help(ctx, formatter)
        return formatter.getvalue().rstrip("\n")

    def tree_format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:
        tree_format_help(ctx, formatter, isinstance(self, MultiCommand))


def prevent_incompatible_overrides(
    cmd: RichCommand, class_name: str, ctx: RichContext, formatter: RichHelpFormatter
) -> None:
    """For use by the rich-click CLI."""
    import rich_click.patch
    from rich_click.utils import method_is_from_subclass_of

    cls: Type[RichCommand] = getattr(rich_click.patch, f"_Patched{class_name}")

    for method_name in ["format_usage", "format_help_text", "format_options", "format_epilog"]:
        if method_is_from_subclass_of(cmd.__class__, cls, method_name):
            getattr(RichCommand, method_name)(cmd, ctx, formatter)
        else:
            getattr(cmd, method_name)(ctx, formatter)
