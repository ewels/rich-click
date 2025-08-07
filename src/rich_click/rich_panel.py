from collections import OrderedDict
from fnmatch import fnmatch
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Generator,
    Generic,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

import click

from rich_click.rich_parameter import RichArgument, RichParameter
from rich_click.utils import CommandGroupDict, OptionGroupDict


if TYPE_CHECKING:
    from rich.panel import Panel
    from rich.table import Table

    from rich_click.rich_command import RichCommand
    from rich_click.rich_context import RichContext
    from rich_click.rich_help_formatter import RichHelpFormatter


T = TypeVar("T")
GroupType = TypeVar("GroupType", OptionGroupDict, CommandGroupDict)


class RichPanel(Generic[T]):
    """RichPanel base class."""

    panel_class: Optional[Type["Panel"]] = None
    table_class: Optional[Type["Table"]] = None
    _highlight: ClassVar[bool] = False
    _object_attr: ClassVar[Optional[str]] = None

    def __init__(
        self,
        name: str,
        *,
        objects: Optional[List[T]] = None,
        table_styles: Optional[Dict[str, Any]] = None,
        panel_styles: Optional[Dict[str, Any]] = None,
        deduplicate: bool = True,
    ) -> None:
        """Create RichPanel instance."""
        self.name = name
        self.table_styles = table_styles or {}
        self.panel_styles = panel_styles or {}
        self.deduplicate = deduplicate
        self.objects: List[T] = objects or []

    def _get_base_table(self, **defaults: Any) -> "Table":
        if self.table_class is None:
            from rich.table import Table

            self.table_class = Table

        kw = {
            "highlight": self._highlight,
            "show_header": False,
            "expand": True,
        }
        kw.update(defaults)
        kw.update(self.table_styles)
        return self.table_class(**kw)

    def get_table(
        self,
        command: "RichCommand",
        ctx: click.Context,
        formatter: "RichHelpFormatter",
    ) -> "Table":
        raise NotImplementedError()

    def _get_base_panel(self, table: "Table", **defaults: Any) -> "Panel":
        if self.panel_class is None:
            from rich.panel import Panel

            self.panel_class = Panel
        kw = defaults
        kw["title"] = self.name
        kw.update(self.panel_styles)
        return self.panel_class(table, **kw)

    def list_objects(self) -> List[T]:
        """Returns objects in order of their priority."""
        li = []
        for obj in self.objects:
            panels = getattr(obj, "panels", [])
            for p in panels:
                if p[0] == self.name:
                    li.append((obj, p[1]))
                    if self.deduplicate:
                        break

        def _() -> Generator[T]:
            for o, *_ in sorted(li, key=lambda _: _[1]):
                yield o

        return list(_())

    def get_objects_in_panel(
        self,
        command: click.Command,
        ctx: click.Context,
    ) -> Generator[T]:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"


class RichOptionPanel(RichPanel[click.Parameter]):
    """Panel for parameters."""

    _highlight: ClassVar[bool] = True
    _object_attr: ClassVar[Optional[str]] = "options"

    def __init__(
        self,
        name: str,
        options: Optional[List[str]] = None,
        **kwargs,
    ) -> None:
        super().__init__(name, **kwargs)
        self.options = options or []

    def get_table(
        self,
        command: "RichCommand",
        ctx: click.Context,
        formatter: "RichHelpFormatter",
    ) -> "Table":
        t_styles = {
            "show_lines": formatter.config.style_options_table_show_lines,
            "leading": formatter.config.style_options_table_leading,
            "box": formatter.config.style_options_table_box,
            "border_style": formatter.config.style_options_table_border_style,
            "row_styles": formatter.config.style_options_table_row_styles,
            "pad_edge": formatter.config.style_options_table_pad_edge,
            "padding": formatter.config.style_options_table_padding,
        }
        if formatter.config.style_options_table_box and isinstance(formatter.config.style_options_table_box, str):
            from rich import box

            t_styles["box"] = getattr(box, t_styles.pop("box"), None)  # type: ignore[arg-type]
        table = super()._get_base_table(**t_styles)
        options_rows = []
        for opt in self.options:
            # Get the param
            for param in command.get_params(ctx):
                if any([opt in [*param.opts, param.name]]):
                    break
            # Skip if option is not listed in this group
            else:
                continue

            from rich_click.rich_help_rendering import get_rich_table_row

            cols = (
                param.get_rich_table_row(ctx, formatter)
                if isinstance(param, RichParameter)
                else get_rich_table_row(param, ctx, formatter)  # type: ignore[arg-type]
            )

            options_rows.append(cols)

        if all([x[0] == "" for x in options_rows]):
            options_rows = [x[1:] for x in options_rows]
            _opt_col = 0
        else:
            _opt_col = 1

        for row in options_rows:
            table.add_row(*row)

        if len(table.columns) > _opt_col:
            table.columns[_opt_col].overflow = "fold"

        return table

    def render(
        self,
        command: "RichCommand",
        ctx: click.Context,
        formatter: "RichHelpFormatter",
    ) -> "Panel":

        table = self.get_table(command, ctx, formatter)

        p_styles = {
            "border_style": formatter.config.style_options_panel_border,
            "title_align": formatter.config.align_options_panel,
            "box": formatter.config.style_options_panel_box,
        }
        if formatter.config.style_options_panel_box and isinstance(formatter.config.style_options_panel_box, str):
            from rich import box

            p_styles["box"] = getattr(box, p_styles.pop("box"), None)  # type: ignore[arg-type]

        panel = self._get_base_panel(table, **p_styles)
        return panel

    def get_objects_in_panel(
        self,
        command: click.Command,
        ctx: click.Context,
    ) -> Generator[click.Parameter]:
        li: List[Tuple[click.Parameter, int]] = []
        for param in command.get_params(ctx):
            panels = getattr(param, "panels", [])
            for p in panels:
                if p[0] == self.name:
                    li.append((param, p[1]))
                    if self.deduplicate:
                        break
        for parm, *_ in sorted(li, key=lambda _: _[1]):
            yield parm


class RichCommandPanel(RichPanel[click.Command]):
    """Panel for parameters."""

    _object_attr: ClassVar[Optional[str]] = "commands"

    def __init__(
        self,
        name: str,
        commands: Optional[List[Union[str, Tuple[str, int]]]] = None,
        **kwargs,
    ) -> None:
        super().__init__(name, **kwargs)
        self.commands = commands or []

    def get_objects_in_panel(
        self,
        command: click.Command,
        ctx: click.Context,
    ) -> Generator[click.Command]:
        if not isinstance(command, click.Group):
            return
        li: List[Tuple[click.Command, int]] = []
        for cmd_name in command.list_commands(ctx):
            cmd = command.get_command(ctx, cmd_name)
            if cmd is None:
                continue
            panels = getattr(cmd, "panels", [])
            for p in panels:
                if p[0] == self.name:
                    li.append((cmd, p[1]))
                    if self.deduplicate:
                        break
        for cmd, *_ in sorted(li, key=lambda _: _[1]):
            yield cmd

    def get_table(
        self,
        command: "RichCommand",
        ctx: click.Context,
        formatter: "RichHelpFormatter",
    ) -> "Table":
        t_styles = {
            "show_lines": formatter.config.style_commands_table_show_lines,
            "leading": formatter.config.style_commands_table_leading,
            "box": formatter.config.style_commands_table_box,
            "border_style": formatter.config.style_commands_table_border_style,
            "row_styles": formatter.config.style_commands_table_row_styles,
            "pad_edge": formatter.config.style_commands_table_pad_edge,
            "padding": formatter.config.style_commands_table_padding,
        }
        if formatter.config.style_commands_table_box and isinstance(formatter.config.style_commands_table_box, str):
            from rich import box

            t_styles["box"] = getattr(box, t_styles.pop("box"), None)  # type: ignore[arg-type]

        table = self._get_base_table(**t_styles)

        # Define formatting in first column, as commands don't match highlighter regex
        # and set column ratio for first and second column, if a ratio has been set
        if formatter.config.style_commands_table_column_width_ratio is None:
            table_column_width_ratio: Union[Tuple[None, None], Tuple[int, int]] = (None, None)
        else:
            table_column_width_ratio = formatter.config.style_commands_table_column_width_ratio

        table.add_column(style=formatter.config.style_command, no_wrap=True, ratio=table_column_width_ratio[0])
        table.add_column(
            no_wrap=False,
            ratio=table_column_width_ratio[1],
        )

        if not isinstance(command, click.Group):
            return table

        for cmd_name in self.commands:
            # Skip if command does not exist
            if cmd_name not in command.list_commands(ctx):
                continue
            cmd = command.get_command(ctx, cmd_name)
            if TYPE_CHECKING:  # pragma: no cover
                assert cmd is not None
            if cmd.hidden:
                continue
            # Use the truncated short text as with vanilla text if requested
            if formatter.config.use_click_short_help:
                helptext = cmd.get_short_help_str()
            else:
                # Use short_help function argument if used, or the full help
                helptext = cmd.short_help or cmd.help or ""
            from rich_click.rich_help_rendering import _make_command_help

            table.add_row(cmd_name, _make_command_help(helptext, formatter, deprecated=cmd.deprecated))

        return table

    def render(
        self,
        command: "RichCommand",
        ctx: click.Context,
        formatter: "RichHelpFormatter",
    ) -> "Panel":

        table = self.get_table(command, ctx, formatter)

        p_styles = {
            "border_style": formatter.config.style_commands_panel_border,
            "title_align": formatter.config.align_commands_panel,
            "box": formatter.config.style_commands_panel_box,
        }
        if formatter.config.style_commands_panel_box and isinstance(formatter.config.style_commands_panel_box, str):
            from rich import box

            p_styles["box"] = getattr(box, p_styles.pop("box"), None)  # type: ignore[arg-type]

        panel = self._get_base_panel(table, **p_styles)
        return panel


# Using config to define panels is silently deprecated.
# We do not intend on removing this for a very long time, possibly ever.


def _resolve_panels_from_config(
    ctx: "RichContext",
    groups: Dict[str, List[GroupType]],
    panel_cls: Type[RichPanel[T]],
) -> List[RichPanel[T]]:
    """Logic for resolving the groups."""
    # Step 1: get valid name(s) for the command currently being executed
    assert panel_cls._object_attr is not None, "RichPanel must have a defined _object_attr"

    cmd_name = ctx.command.name
    _ctx: "RichContext" = ctx
    while _ctx.parent is not None:
        _ctx = _ctx.parent  # type: ignore[assignment]
        cmd_name = f"{_ctx.command.name} {cmd_name}"
    # 'command_path' is sometimes the file name, e.g. hello.py.
    # We also want to make sure that the actual command name is supported as well.
    if cmd_name != ctx.command_path:
        paths = [cmd_name, ctx.command_path]
    else:
        paths = [cmd_name]
    # Also handle 'python -m foo' when the user specifies a key of 'foo':
    if ctx.command_path.startswith("python -m "):
        extra = ctx.command_path.replace("python -m ", "", 1)
        paths.append(extra)
    final_groups_list: List[GroupType] = []

    # Step 2: Match currently executing command to keys
    # Assign wildcards, but make sure we do not overwrite anything already defined.
    for _path in paths:
        for mtch in reversed(sorted([_ for _ in groups if fnmatch(_path, _)])):
            wildcard_option_groups = groups[mtch]
            for grp in wildcard_option_groups:
                grp = grp.copy()
                opts = grp.get(panel_cls._object_attr, []).copy()  # type: ignore[attr-defined]
                traversed = []
                for opt in grp.get(panel_cls._object_attr, []):  # type: ignore[attr-defined]
                    if grp.get("deduplicate", True) and opt in [
                        _opt
                        for _grp in final_groups_list
                        for _opt in [*traversed, *_grp.get(panel_cls._object_attr, [])]  # type: ignore[has-type]
                    ]:
                        opts.remove(opt)
                    traversed.append(opt)
                grp[panel_cls._object_attr] = opts  # type: ignore[typeddict-unknown-key]
                final_groups_list.append(grp)

    return [panel_cls(**grp) for grp in final_groups_list]


@overload
def construct_panels(
    ctx: "RichContext",
    command: "RichCommand",
    formatter: "RichHelpFormatter",
    objs: List[click.Parameter],
    panel_cls: Type[RichOptionPanel],
    panel_type: Literal["option"],
) -> List[RichOptionPanel]: ...


@overload
def construct_panels(
    ctx: "RichContext",
    command: "RichCommand",
    formatter: "RichHelpFormatter",
    objs: List[click.Command],
    panel_cls: Type[RichCommandPanel],
    panel_type: Literal["command"],
) -> List[RichCommandPanel]: ...


def construct_panels(
    ctx: "RichContext",
    command: "RichCommand",
    formatter: "RichHelpFormatter",
    objs: List[T],
    panel_cls: Type[RichPanel[T]],
    panel_type: Literal["command", "option"],
) -> List[RichPanel[T]]:
    # First step is building out panel_base
    # We use this later to construct the actual panels more easily.
    panel_base: Dict[str, List[T]]

    if panel_type == "command":
        panel_base = {
            p.name: getattr(p, panel_cls._object_attr, []) for p in command.panels if isinstance(p, RichCommandPanel)
        }
        panel_base.setdefault(formatter.config.commands_panel_title, [])
        cfg_groups = formatter.config.command_groups

        def _default(o: click.Command) -> None:
            panel_base[formatter.config.commands_panel_title].append(o.name)

    elif panel_type == "option":
        panel_base = {
            p.name: getattr(p, panel_cls._object_attr, []) for p in command.panels if isinstance(p, RichOptionPanel)
        }
        panel_base.setdefault(formatter.config.options_panel_title, [])
        if not formatter.config.group_arguments_options:
            panel_base.setdefault(formatter.config.arguments_panel_title, [])
        cfg_groups = formatter.config.option_groups

        def _default(o: click.Parameter) -> None:
            if isinstance(o, click.Argument):
                if formatter.config.show_arguments is False:
                    return
                elif formatter.config.group_arguments_options:
                    panel_base[formatter.config.options_panel_title].append(o.name)
                else:
                    panel_base[formatter.config.arguments_panel_title].append(o.name)
            else:
                panel_base[formatter.config.options_panel_title].append(o.name)

    else:
        raise ValueError("panel_type must be one of 'parameter' or 'command'")

    _show_arguments = formatter.config.show_arguments

    groups_from_config = []
    if cfg_groups:
        groups_from_config = _resolve_panels_from_config(ctx, cfg_groups, panel_cls)[::-1]

    assigned_objs = set([o for p in panel_base.values() for o in p])
    for p in groups_from_config:
        panel_base[p.name] = getattr(p, panel_cls._object_attr, [])
        assigned_objs.update(panel_base[p.name])

    for obj in objs:
        names = [obj.name]
        if hasattr(obj, "opts"):
            names.extend(obj.opts)
        assigned = any(i in assigned_objs for i in names)
        if isinstance(obj, click.Parameter):
            if getattr(obj, "hidden", False):
                continue
        if hasattr(obj, "panel"):
            if isinstance(obj.panel, str):
                panel_list = [obj.panel]
            elif obj.panel is None:
                panel_list = []
            else:
                panel_list = obj.panel
            for panel in panel_list:
                panel_base.setdefault(panel, [])
                panel_base[panel].append(obj)
                assigned = True
                if _show_arguments is None and panel == formatter.config.arguments_panel_title:
                    _show_arguments = True
        if not assigned:
            _default(obj)
            if _show_arguments is None and isinstance(obj, RichArgument) and obj.help is not None:
                _show_arguments = True

    if not _show_arguments and panel_type == "option":
        del panel_base[formatter.config.arguments_panel_title]

    # The reason final_panels is split from available_panels
    # is to preserve the order of how things are defined in panel_base.
    final_panels: Dict[str, Optional[RichPanel]] = {
        p: None for p in panel_base
    }

    available_panels: Dict[str, RichPanel] = {
        p.name: p for p in [
            *groups_from_config,
            *filter(lambda _: isinstance(_, panel_cls), command.panels)
        ]
    }

    # Now panel_base is done
    # we can construct the final list of panels
    for panel_name, obj_list in panel_base.items():
        if not final_panels.get(panel_name):
            if panel_name in available_panels:
                final_panels[panel_name] = available_panels.pop(panel_name)
            else:
                final_panels[panel_name] = panel_cls(panel_name)
        for i in obj_list:
            li = getattr(final_panels[panel_name], panel_cls._object_attr, [])
            if i not in li:
                li.append(i)

    return list(final_panels.values())[::-1]
