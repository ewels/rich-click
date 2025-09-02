"""The command line interface."""

from __future__ import annotations

# ruff: noqa: D103
from typing import Dict, List, Optional, Union

import click

import rich_click
from rich_click.decorators import command as _rich_command
from rich_click.decorators import group as _rich_group
from rich_click.rich_command import RichCommand, RichCommandCollection, RichGroup, RichMultiCommand
from rich_click.rich_context import RichContext
from rich_click.rich_help_configuration import RichHelpConfiguration
from rich_click.rich_help_formatter import RichHelpFormatter
from rich_click.rich_panel import RichCommandPanel
from rich_click.rich_parameter import RichArgument, RichOption


class _PatchedRichCommand(RichCommand):
    pass


class _PatchedRichMultiCommand(RichMultiCommand, _PatchedRichCommand):
    pass


class _PatchedRichCommandCollection(RichCommandCollection, _PatchedRichCommand):
    pass


class _PatchedRichGroup(RichGroup, _PatchedRichCommand):
    pass


def rich_command(*args, **kwargs):  # type: ignore[no-untyped-def]
    kwargs.setdefault("cls", _PatchedRichCommand)
    kwargs["__rich_click_cli_patch"] = True
    return _rich_command(*args, **kwargs)


def rich_group(*args, **kwargs):  # type: ignore[no-untyped-def]
    kwargs.setdefault("cls", _PatchedRichGroup)
    kwargs["__rich_click_cli_patch"] = True
    return _rich_group(*args, **kwargs)


def patch_typer(
    rich_config: Optional[RichHelpConfiguration] = None,
) -> None:
    return patch(rich_config=rich_config, patch_typer=True)


def _patch_typer():
    try:
        import typer.core
        import typer.main
        from typer.models import DefaultPlaceholder
    except ImportError:
        import warnings

        warnings.warn("Attempted to patch Typer, but Typer is not installed.", ImportWarning, stacklevel=2)
        return

    class _PatchedRichContext(RichContext, typer.Context):

        def __init__(self, *args, **kwargs):
            RichContext.__init__(self, *args, **kwargs)

        def make_formatter(self, error_mode: bool = False) -> RichHelpFormatter:
            """Create the Rich Help Formatter."""
            formatter = super().make_formatter(error_mode=error_mode)
            if hasattr(self.command, "rich_markup_mode") and self.command.rich_markup_mode == "rich":
                formatter.config.text_markup = "rich"
                formatter.config.text_emojis = True
            return formatter

        def get_help(self) -> str:
            """
            Format the help into a string and returns it.

            Calls :meth:`format_help` internally.
            """
            if isinstance(self.command, click.Group):
                command_panels: Dict[str, List[str]] = {}
                for cmd_name in self.command.commands:
                    cmd = self.command.commands[cmd_name]
                    if (
                        isinstance(cmd, (typer.core.TyperCommand, typer.core.TyperGroup))
                        and cmd.rich_help_panel is not None
                        and not isinstance(cmd.rich_help_panel, DefaultPlaceholder)
                    ):
                        command_panels.setdefault(cmd.rich_help_panel, [])
                        command_panels[cmd.rich_help_panel].append(cmd_name)
                for name, commands in command_panels.items():
                    self.command.panels.append(RichCommandPanel(name, commands=commands))

            return super().get_help()

    class _PatchedTyperCommand(_PatchedRichCommand, typer.core.TyperCommand):

        context_class = _PatchedRichContext

        def __init__(self, *args, rich_help_panel: Union[str, None] = None, **kwargs):
            _PatchedRichCommand.__init__(self, *args, **kwargs)
            self.rich_help_panel = rich_help_panel

    class _PatchedTyperGroup(_PatchedRichGroup, typer.core.TyperGroup):

        context_class = _PatchedRichContext

        def __init__(self, *args, rich_help_panel: Union[str, None] = None, **kwargs):
            _PatchedRichGroup.__init__(self, *args, **kwargs)
            self.rich_help_panel = rich_help_panel

    class _PatchedTyperOption(RichOption, typer.core.TyperOption):

        def __init__(self, *args, rich_help_panel: Union[str, None] = None, **kwargs):
            RichOption.__init__(self, *args, **kwargs)
            if rich_help_panel:
                self.panel = rich_help_panel

    class _PatchedTyperArgument(RichArgument, typer.core.TyperArgument):

        def __init__(self, *args, rich_help_panel: Union[str, None] = None, **kwargs):
            RichArgument.__init__(self, *args, **kwargs)
            if rich_help_panel:
                self.panel = rich_help_panel

    typer.core.TyperCommand = _PatchedTyperCommand
    typer.core.TyperGroup = _PatchedTyperGroup
    typer.core.TyperArgument = _PatchedTyperArgument
    typer.core.TyperOption = _PatchedTyperOption

    typer.main.TyperCommand = _PatchedTyperCommand
    typer.main.TyperGroup = _PatchedTyperGroup
    typer.main.TyperArgument = _PatchedTyperArgument
    typer.main.TyperOption = _PatchedTyperOption


def patch(
    rich_config: Optional[RichHelpConfiguration] = None, *, patch_rich_click: bool = False, patch_typer: bool = False
) -> None:
    """Patch Click internals to use rich-click types."""
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)

        rich_click.rich_command.OVERRIDES_GUARD = True
        click.group = rich_group
        click.command = rich_command
        click.Group = _PatchedRichGroup  # type: ignore[misc]
        click.Command = _PatchedRichCommand  # type: ignore[misc]
        click.CommandCollection = _PatchedRichCommandCollection  # type: ignore[misc]

        if hasattr(click, "MultiCommand"):
            click.MultiCommand = _PatchedRichMultiCommand  # type: ignore[assignment,misc,unused-ignore]
        if patch_rich_click:
            rich_click.group = rich_group
            rich_click.command = rich_command
            rich_click.Group = _PatchedRichGroup  # type: ignore[misc]
            rich_click.Command = _PatchedRichCommand  # type: ignore[misc]
            rich_click.CommandCollection = _PatchedRichCommandCollection  # type: ignore[misc]
            if hasattr(click, "MultiCommand"):
                rich_click.MultiCommand = _PatchedRichMultiCommand  # type: ignore[assignment,misc,unused-ignore]

    if patch_typer:
        _patch_typer()

    if rich_config is not None:
        rich_config.dump_to_globals()


__all__ = ["patch", "patch_typer"]
