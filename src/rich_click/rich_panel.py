from __future__ import annotations

from collections.abc import Callable, Generator
from fnmatch import fnmatch
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Generic,
    TypeVar,
)

from click import Context, Parameter

from rich_click._click_types_cache import Argument, Command, Group
from rich_click.rich_help_configuration import (
    ColumnType,
    CommandColumnType,
    OptionColumnType,
    has_command_width_ratio,
)
from rich_click.rich_parameter import RichArgument, RichParameter
from rich_click.utils import CommandGroupDict, OptionGroupDict


if TYPE_CHECKING:
    from rich.box import Box
    from rich.console import Group as RenderGroup
    from rich.padding import PaddingDimensions
    from rich.panel import Panel
    from rich.style import StyleType
    from rich.table import Table

    from rich_click.rich_command import RichCommand
    from rich_click.rich_context import RichContext
    from rich_click.rich_help_formatter import RichHelpFormatter


ColT = TypeVar("ColT", bound=ColumnType)
CT = TypeVar("CT", Command, Parameter)
GroupType = TypeVar("GroupType", OptionGroupDict, CommandGroupDict)


def _panel_inner_width(formatter: RichHelpFormatter, padding: PaddingDimensions) -> int:
    """Measure the room a panel leaves its table: its own padding, inside two border characters."""
    from rich.padding import Padding

    _, right, _, left = Padding.unpack(padding)
    return max(formatter.width - 2 - left - right, 1)


def _column_budget(width: int) -> int:
    """Cap the columns before the help text at two thirds of a panel, leaving a third to read in."""
    return width * 2 // 3


def _wrap_threshold(setting: float | int | bool | None | Callable[[int], float | int], width: int) -> int:
    """Resolve `wrap_long_options` against a panel's width: a fraction of it, or a count of columns."""
    if callable(setting):
        setting = setting(width)
    if isinstance(setting, float):
        return int(width * setting)
    return int(setting or 0)


class RichPanel(Generic[CT, ColT]):
    """RichPanel base class."""

    panel_class: type[Panel] | None = None
    table_class: type[Table] | None = None
    _highlight: ClassVar[bool] = False
    _object_attr: ClassVar[str] = NotImplemented
    _column_types_attr: ClassVar[str] = NotImplemented

    def __init__(
        self,
        name: str,
        *,
        help: str | None = None,
        help_style: StyleType | None = None,
        table_styles: dict[str, Any] | None = None,
        panel_styles: dict[str, Any] | None = None,
        column_types: list[ColT] | None = None,
        inline_help_in_title: bool | None = None,
        title_style: StyleType | None = None,
    ) -> None:
        """Initialize a RichPanel."""
        self.name = name
        self.help = help
        self.help_style = help_style
        self.table_styles = table_styles or {}
        self.panel_styles = panel_styles or {}
        self.column_types = column_types
        self.inline_help_in_title = inline_help_in_title
        self.title_style = title_style
        # Set by align_panel_columns() for the duration of one render.
        self._alignment: tuple[list[ColT], list[int | None]] | None = None
        self._rows: tuple[RichHelpFormatter, list[list[Any]]] | None = None

    @property
    def objects(self) -> list[str]:
        if self._object_attr is NotImplemented:
            raise NotImplementedError()
        return getattr(self, self._object_attr)  # type: ignore[no-any-return]

    def add_object(self, o: str) -> None:
        if self._object_attr is NotImplemented:
            raise NotImplementedError()
        getattr(self, self._object_attr).append(o)

    def get_box(self, box: str | Box | None) -> Box | None:
        if box is None:
            return None
        from rich_click.rich_box import get_box

        return get_box(box)

    def to_info_dict(self, ctx: Context) -> dict[str, Any]:
        if self._object_attr is NotImplemented:
            raise NotImplementedError()
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "help": self.help,
            self._object_attr: [i.name for i in self.get_objects(ctx.command, ctx)],
        }

    @classmethod
    def list_all_objects(cls, ctx: Context) -> list[tuple[str, CT]]:
        """List all objects of the command that this panel type works with."""
        raise NotImplementedError()

    def get_objects(self, command: Command, ctx: Context) -> Generator[CT, None, None]:
        """List the proper names assigned to the panel."""
        raise NotImplementedError()

    def _get_base_table(self, **defaults: Any) -> Table:
        if self.table_class is None:
            from rich.table import Table

            self.table_class = Table

        kw: dict[str, Any] = {
            "highlight": self._highlight,
            "show_header": False,
        }

        kw.update(defaults)
        kw.update(self.table_styles)
        if "box" in kw and kw["box"] is not None:
            kw["box"] = self.get_box(kw.pop("box", None))
        return self.table_class(**kw)

    def get_column_types(self, formatter: RichHelpFormatter) -> list[ColT]:
        """List the column types that this panel's table is built from."""
        if self._column_types_attr is NotImplemented:
            raise NotImplementedError()
        return self.column_types or getattr(formatter.config, self._column_types_attr)

    def get_rows(self, command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> list[list[Any]]:
        """Build a row of cells for every object in the panel, one cell per column type."""
        raise NotImplementedError()

    def _render_rows(self, command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> list[list[Any]]:
        """Take the rows the alignment pass measured, rather than building them a second time."""
        if self._rows is not None and self._rows[0] is formatter:
            return self._rows[1]
        return self.get_rows(command, ctx, formatter)

    def kept_column_types(self, rows: list[list[Any]], formatter: RichHelpFormatter) -> list[ColT]:
        """List the column types with something in them, dropping any empty for every row."""
        return [
            t for t, cells in zip(self.get_column_types(formatter), zip(*rows)) if any(map(self._has_content, cells))
        ]

    def _inner_width(self, formatter: RichHelpFormatter) -> int:
        """Measure the room this panel leaves its table, at whatever padding the panel is given."""
        config_default = getattr(formatter.config, f"style_{self._object_attr}_panel_padding")
        return _panel_inner_width(formatter, self.panel_styles.get("padding", config_default))

    def _table_padding_width(self, formatter: RichHelpFormatter) -> int:
        """How much horizontal padding a table column takes on top of its content."""
        from rich.padding import Padding

        config_default = getattr(formatter.config, f"style_{self._object_attr}_table_padding")
        _, right, _, left = Padding.unpack(self.table_styles.get("padding", config_default))
        return left + right

    def _manual_column_widths(self, formatter: RichHelpFormatter) -> bool:
        """Whether the user has sized this panel's columns themselves, leaving nothing to work out."""
        return False

    @staticmethod
    def _has_content(cell: Any) -> bool:
        """Whether a cell renders anything. A `rich.columns.Columns` is truthy even when empty."""
        if cell is None:
            return False
        nested = getattr(cell, "renderables", None)
        if nested is not None:
            return any(RichPanel._has_content(item) for item in nested)
        return len(cell) > 0 if hasattr(cell, "__len__") else True

    def _measure_rows(self, rows: list[list[Any]], columns: int, formatter: RichHelpFormatter) -> list[list[int]]:
        """Measure every cell of every row, at the width a panel leaves for its table."""
        from rich.measure import Measurement

        console = formatter.console
        options = console.options.update_width(self._inner_width(formatter))
        return [
            [0 if cell is None else Measurement.get(console, options, cell).maximum for cell in row[:columns]]
            for row in rows
        ]

    def layout(
        self,
        rows: list[list[Any]],
        kept_types: list[ColT],
        formatter: RichHelpFormatter,
        pinned: list[int] | None = None,
    ) -> tuple[list[list[Any]], set[int], set[int], list[int | None], int]:
        """
        Work out the shape of the panel's table(s) from its rows.

        Returns the rows reduced to `kept_types`, the indices of those whose help text belongs on
        its own line, the indices of those spilling into the empty columns to their right, the
        width to pin each column to (`None` for the flexible last one), and the least room the
        columns before the help need between them.

        A column is sized by the rows that reach past it. A row whose cells stop short of the help
        can run on under the columns it leaves empty, so it has no say in how wide they get: it
        asks instead for room enough across all of them, which is what `minimum` carries. The
        column before the help has nothing on its right to run on under, so every row sizes it.

        `pinned` is the width each column is getting anyway, from aligning them across panels. A
        row that fits in the columns it occupies stays put however low `wrap_long_options` is,
        because moving it would cost a line and reclaim nothing.
        """
        keep = [t in kept_types for t in self.get_column_types(formatter)]
        kept_rows = [[cell for cell, k in zip(row, keep) if k] for row in rows]
        help_index = next((i for i, t in enumerate(kept_types) if t == "help"), -1)
        dropped: set[int] = set()
        spanned: set[int] = set()
        minimum = 0
        if help_index < 1:
            return kept_rows, dropped, spanned, [], minimum

        inner_width = self._inner_width(formatter)
        threshold = _wrap_threshold(formatter.config.wrap_long_options, inner_width)
        # Taking a row out of the columns splits the panel into a stack of tables, and a box is
        # drawn around each one, so a boxed table keeps every row inline whatever its width.
        box = self.table_styles.get("box", getattr(formatter.config, f"style_{self._object_attr}_table_box"))
        spilling = bool(
            kept_rows and threshold > 0 and self.get_box(box) is None and not self._manual_column_widths(formatter)
        )
        measured = self._measure_rows(kept_rows, help_index, formatter)
        padding = self._table_padding_width(formatter)
        trailing: list[int | None] = [None] * (len(kept_types) - help_index)

        def room(widths: list[int], columns: range | list[int]) -> int:
            """Measure the room a cell has across `columns`, the padding between them included."""
            return sum(widths[c] for c in columns) + padding * max(len(columns) - 1, 0)

        def sized_by(skip: set[int], spill: bool) -> list[int]:
            """Measure each column against the rows that have a say in how wide it is."""
            return [
                max(
                    (
                        m[c]
                        for i, m in enumerate(measured)
                        if i not in skip and (not spill or c == help_index - 1 or any(m[c + 1 : help_index]))
                    ),
                    default=0,
                )
                for c in range(help_index)
            ]

        if not spilling:
            return kept_rows, dropped, spanned, [*sized_by(set(), False), *trailing], minimum

        filled_by: dict[int, list[int]] = {}
        needed_by: dict[int, int] = {}
        over: set[int] = set()
        for i, row_widths in enumerate(measured):
            # A row with no help text has nothing to move.
            if not self._has_content(kept_rows[i][help_index]):
                continue
            # Only the columns this row fills take up room in it, so only they need a gap.
            filled = [c for c, width in enumerate(row_widths) if width]
            needed = room(row_widths, filled)
            if not filled:
                continue
            filled_by[i], needed_by[i] = filled, needed
            allowed = max(threshold, room(pinned, filled)) if pinned else threshold
            if allowed < needed:
                over.add(i)

        def plan(spill: bool) -> tuple[set[int], set[int], list[int], int]:
            """Work out which rows leave the columns, and what the columns then have to measure."""
            out: set[int] = set()
            across: set[int] = set()
            available = pinned or sized_by(over, spill)
            for i, filled in filled_by.items():
                if i not in over and needed_by[i] <= room(available, filled):
                    continue
                if needed_by[i] <= room(available, range(filled[0], help_index)) or (
                    spill and needed_by[i] <= threshold
                ):
                    across.add(i)
                else:
                    out.add(i)
            # Room for a spilling row is room for the columns on its left, and then for the row.
            least = max(
                (sum(available[: filled_by[i][0]]) + padding * (filled_by[i][0] + 1) + needed_by[i] for i in across),
                default=0,
            )
            return out, across, sized_by(out | across, spill), least

        widths: list[int]
        dropped, spanned, widths, minimum = plan(True)
        if minimum > _column_budget(inner_width):
            # Making room to spill would leave too little for the help text to be worth reading.
            dropped, spanned, widths, minimum = plan(False)
        return kept_rows, dropped, spanned, [*widths, *trailing], minimum

    def _fold_empty_columns(
        self,
        keep: list[bool],
        widths: list[int | None],
        tracks: list[list[Any]],
        formatter: RichHelpFormatter,
    ) -> tuple[list[int | None], list[list[Any]]]:
        """
        Hand each unkept column's width to its left-hand neighbour, so a long entry can spill right.

        The merged column is as wide as the ones it replaces, so the help text still starts where
        it does in every other row. A leading unkept column is left alone: that one is what indents
        the panel into line with its siblings. `tracks` are lists parallel to `widths` - cells,
        headers, column types - filtered alongside it.
        """
        padding = self._table_padding_width(formatter)
        merged_widths: list[int | None] = []
        merged_tracks: list[list[Any]] = [[] for _ in tracks]
        for kept, width, *values in zip(keep, widths, *tracks):
            neighbour = merged_widths[-1] if merged_widths else None
            if kept or width is None or neighbour is None:
                merged_widths.append(width)
                for merged, value in zip(merged_tracks, values):
                    merged.append(value)
            else:
                merged_widths[-1] = neighbour + width + padding
        return merged_widths, merged_tracks

    def _absorb_unused_columns(
        self, rows: list[list[Any]], kept_types: list[ColT], widths: list[int | None], formatter: RichHelpFormatter
    ) -> tuple[list[ColT], list[int | None]]:
        """
        Hand a column's width to its left-hand neighbour when this panel has nothing to put in it.

        Aligning panels gives every panel in a group the same columns, including ones only its
        siblings fill. An empty column still takes up its width, which is then unreachable by the
        entries that could have used it.

        The same fold as `_merge_empty_columns`, decided for the panel rather than row by row.
        """
        used = self.kept_column_types(rows, formatter)
        if all(t in used for t in kept_types):
            return kept_types, widths

        merged_widths, (merged_types,) = self._fold_empty_columns(
            [t in used for t in kept_types], widths, [kept_types], formatter
        )
        return merged_types, merged_widths

    def _style_columns(self, table: Table, headers: list[str], widths: list[int | None]) -> None:
        if any(width is not None for width in widths) and not table.pad_edge:
            # Rich before 14.3 counts the padding `pad_edge` drops at the table's two edges, so a
            # column sized here comes out a cell wider than it asks for. Moving the left padding
            # into the right leaves the gaps between columns as they were, and nothing at an edge.
            top, right, bottom, left = table.padding
            table.padding = (top, right + left, bottom, 0)
        for col, header in zip(table.columns, headers):
            col.header = header
        for col, width in zip(table.columns, widths):
            if width is None:
                # Absorb all leftover width, instead of Rich spreading it over every column.
                col.ratio = col.ratio or 1
            else:
                col.ratio = None
                col.min_width = width

    def _merge_empty_columns(
        self, row: list[Any], headers: list[str], widths: list[int | None], formatter: RichHelpFormatter
    ) -> tuple[list[Any], list[str], list[int | None]]:
        """
        Hand each of a row's empty columns to the cell on its left, so a long entry spills right.

        The same fold as `_absorb_unused_columns`, decided row by row rather than for the panel.
        """
        merged_widths, (cells, merged_headers) = self._fold_empty_columns(
            [self._has_content(cell) for cell in row], widths, [row, headers], formatter
        )
        return cells, merged_headers, merged_widths

    def _next_line_head(self, table: Table, row: list[Any], help_index: int) -> Any:
        """
        Lay an entry's own columns on one line, to sit above the table holding its help text.

        A cell that fits its column keeps that column's width, so the cells either side of the
        over-wide one still line up with every other row. The cell that does not fit runs on and
        pushes the rest of the line right, as a table row would if Rich could overflow a column.
        """
        from rich.text import Text

        filled = [c for c, cell in enumerate(row) if c != help_index and cell]
        if not filled:
            return Text("")
        gap = table.padding[1] + table.padding[3]
        if all(isinstance(row[c], Text) for c in filled):
            widths = [col.min_width or 0 for col in table.columns]
            parts = []
            for c in range(filled[0], filled[-1] + 1):
                # Columns() would ellipsise the long value this line exists to show in full.
                piece = row[c].copy() if c in filled else Text("")
                if c != filled[-1]:
                    piece.pad_right(max(widths[c] - piece.cell_len, 0))
                parts.append(piece)
            head: Any = Text(" " * gap).join(parts)
        else:
            from rich.columns import Columns

            head = Columns([row[c] for c in filled], padding=(0, gap))
        # The columns this entry leaves empty on its left are what indent every other row of the
        # panel - a required marker, say - so the head has to carry their width to stay in line.
        columns = list(table.columns)[: filled[0] if filled else 0]
        indent = (table.padding[3] if table.pad_edge else 0) + sum((col.min_width or 0) + gap for col in columns)
        if not indent:
            return head

        from rich.padding import Padding

        return Padding(head, (0, 0, 0, indent))

    def _build_table(
        self, rows: list[list[Any]], formatter: RichHelpFormatter, new_table: Callable[[], Table]
    ) -> Table | RenderGroup:
        """
        Lay the rows out, dropping any column that is empty for every row.

        Usually that is one table. A row too wide for the columns it fills spills into the empty
        ones to its right, or, when even that is not enough room, moves its help to the following
        line. Rich has neither column spanning nor per-row widths, so the panel then becomes a
        stack of tables that share one set of column widths.
        """
        kept_types, aligned_widths = self._alignment or (self.kept_column_types(rows, formatter), [])
        if aligned_widths:
            kept_types, aligned_widths = self._absorb_unused_columns(rows, kept_types, aligned_widths, formatter)
        already_pinned = [width for width in aligned_widths if width is not None]
        kept_rows, dropped, spanned, widths, minimum = self.layout(rows, kept_types, formatter, already_pinned)
        headers = [t.replace("_", " ").title() for t in kept_types]
        column_widths = aligned_widths or (widths if dropped or spanned else [])
        if not aligned_widths and column_widths:
            # Sizing itself, a panel has to find the room a spilling row asks for on its own.
            fixed = [width for width in column_widths if width is not None]
            padding = self._table_padding_width(formatter)
            column_widths[len(fixed) - 1] = fixed[-1] + max(minimum - sum(fixed) - len(fixed) * padding, 0)

        def table_at(first: int) -> Table:
            """Start a table at row `first`, so that alternating row styles stay in step across a split."""
            table = new_table()
            styles = list(table.row_styles)
            if styles:
                turn = first % len(styles)
                table.row_styles = styles[turn:] + styles[:turn]
            return table

        def table_for(block: list[list[Any]], first: int) -> Table:
            table = table_at(first)
            for row in block:
                table.add_row(*row)
            self._style_columns(table, headers, column_widths)
            return table

        if not dropped and not spanned:
            return table_for(kept_rows, 0)

        from rich.console import Group as RenderGroup

        help_index = kept_types.index("help")  # type: ignore[arg-type]
        blocks: list[Any] = []
        run: list[list[Any]] = []
        run_from = 0
        for i, row in enumerate(kept_rows):
            if i not in dropped and i not in spanned:
                if not run:
                    run_from = i
                run.append(row)
                continue
            if run:
                blocks.append(table_for(run, run_from))
                run = []
            if i in spanned:
                cells, merged_headers, merged_widths = self._merge_empty_columns(row, headers, column_widths, formatter)
                table = table_at(i)
                table.add_row(*cells)
                self._style_columns(table, merged_headers, merged_widths)
                blocks.append(table)
                continue
            # Blank out everything but the help, so it lands in the help column of the line below.
            # ponytail: the head sits outside the table, so a row style reaches only the help line.
            table = table_for([["" if c != help_index else cell for c, cell in enumerate(row)]], i)
            blocks.append(RenderGroup(self._next_line_head(table, row, help_index), table))
        if run:
            blocks.append(table_for(run, run_from))

        return RenderGroup(*blocks)

    def get_table(
        self,
        command: RichCommand,
        ctx: RichContext,
        formatter: RichHelpFormatter,
    ) -> Table | RenderGroup:
        raise NotImplementedError()

    def _get_base_panel(self, table: Table, **defaults: Any) -> Panel:
        if self.panel_class is None:
            from rich_click.rich_help_rendering import RichClickRichPanel

            self.panel_class = RichClickRichPanel
        kw = defaults
        kw.update(self.panel_styles)
        if "box" in kw:
            if kw["box"] is None:
                kw.pop("box")
                kw["box"] = self.get_box("SIMPLE")
            else:
                kw["box"] = self.get_box(kw.pop("box", None))

        return self.panel_class(table, **kw)

    def render(
        self,
        command: RichCommand,
        ctx: RichContext,
        formatter: RichHelpFormatter,
    ) -> Panel:
        raise NotImplementedError()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"


class RichOptionPanel(RichPanel[Parameter, OptionColumnType]):
    """Panel for parameters."""

    _highlight: ClassVar[bool] = True
    _object_attr: ClassVar[str] = "options"
    _column_types_attr: ClassVar[str] = "options_table_column_types"

    def __init__(
        self,
        name: str,
        options: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a RichOptionPanel."""
        super().__init__(name, **kwargs)
        self.options = options or []

    @classmethod
    def list_all_objects(cls, ctx: Context) -> list[tuple[str, Parameter]]:
        return [
            (i.opts[0] if getattr(i, "flag_value", None) and i.opts else i.name or "", i)
            for i in ctx.command.get_params(ctx)
        ]

    def get_objects(self, command: Command, ctx: Context) -> Generator[Parameter, None, None]:
        """List the objects assigned to the panel."""
        params = command.get_params(ctx)
        for opt in self.options:
            # Get the param
            for param in params:
                if any([opt in [*param.opts, param.name]]):
                    break
            # Skip if option is not listed in this group
            else:
                continue
            yield param

    def get_rows(self, command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> list[list[Any]]:
        """Build a row of cells for every parameter in the panel, one cell per column type."""
        from rich_click.rich_help_rendering import get_parameter_rich_table_row

        return [
            (
                param.get_rich_table_row(ctx, formatter, self)
                if isinstance(param, RichParameter)
                else get_parameter_rich_table_row(param, ctx, formatter, self)  # type: ignore[arg-type]
            )
            for param in self.get_objects(command, ctx)
        ]

    def get_table(
        self,
        command: RichCommand,
        ctx: RichContext,
        formatter: RichHelpFormatter,
    ) -> Table | RenderGroup:
        t_styles = {
            "show_lines": formatter.config.style_options_table_show_lines,
            "leading": formatter.config.style_options_table_leading,
            "box": formatter.config.style_options_table_box,
            "border_style": formatter.config.style_options_table_border_style,
            "row_styles": formatter.config.style_options_table_row_styles,
            "pad_edge": formatter.config.style_options_table_pad_edge,
            "padding": formatter.config.style_options_table_padding,
            "expand": formatter.config.style_options_table_expand,
        }
        rows = self._render_rows(command, ctx, formatter)
        return self._build_table(rows, formatter, lambda: self._get_base_table(**t_styles))

    def render(
        self,
        command: RichCommand,
        ctx: RichContext,
        formatter: RichHelpFormatter,
    ) -> Panel:
        from rich.text import Text

        from rich_click.rich_help_rendering import RichClickRichPanel

        inner: Any = self.get_table(command, ctx, formatter)

        p_styles: dict[str, Any] = {
            "border_style": formatter.config.style_options_panel_border,
            "title_align": formatter.config.align_options_panel,
            "box": formatter.config.style_options_panel_box,
            "padding": formatter.config.style_options_panel_padding,
            "style": formatter.config.style_options_panel_style,
        }
        if self.panel_class is None or issubclass(self.panel_class, RichClickRichPanel):
            p_styles["title_padding"] = formatter.config.panel_title_padding

        if self.title_style is None:
            title_style = formatter.config.style_options_panel_title_style
        else:
            title_style = self.title_style

        title = formatter.config.panel_title_string.format(self.name)

        if self.help:
            if self.help_style is None:
                help_style = formatter.config.style_options_panel_help_style
            else:
                help_style = self.help_style
            if self.inline_help_in_title is None:
                inline_help_in_title = formatter.config.panel_inline_help_in_title
            else:
                inline_help_in_title = self.inline_help_in_title

            if inline_help_in_title:
                p_styles["title"] = Text("", overflow="ellipsis").join(
                    [
                        Text(title, style=title_style),
                        Text(formatter.config.panel_inline_help_delimiter),
                        Text(self.help, style=help_style),
                    ]
                )
            else:
                p_styles["title"] = Text(title, style=title_style)
                from rich.containers import Renderables

                inner = Renderables([formatter.rich_text(self.help, style=help_style), inner])
        else:
            p_styles["title"] = Text(title, style=title_style)
        panel = self._get_base_panel(inner, **p_styles)
        return panel


class RichCommandPanel(RichPanel[Command, CommandColumnType]):
    """Panel for parameters."""

    _object_attr: ClassVar[str] = "commands"
    _column_types_attr: ClassVar[str] = "commands_table_column_types"

    def __init__(
        self,
        name: str,
        commands: list[str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize a RichCommandPanel."""
        super().__init__(name, **kwargs)
        self.commands = commands or []

    def _manual_column_widths(self, formatter: RichHelpFormatter) -> bool:
        return has_command_width_ratio(formatter.config.style_commands_table_column_width_ratio)

    @classmethod
    def list_all_objects(cls, ctx: Context) -> list[tuple[str, Command]]:
        if not isinstance(ctx.command, Group):
            return []
        commands = []
        for cmd_name in ctx.command.list_commands(ctx):
            cmd = ctx.command.get_command(ctx, cmd_name)
            if cmd is not None:
                commands.append((cmd_name, cmd))
        return commands

    def get_objects(self, command: Command, ctx: Context) -> Generator[Command, None, None]:
        """List the objects assigned to the panel."""
        if not isinstance(command, Group):
            return

        commands_list = command.list_commands(ctx)
        callback_names = {c.callback.__name__: c for c in command.commands.values() if c.callback is not None}

        for cmd_name in self.commands:
            if cmd_name in commands_list:
                yield command.get_command(ctx, cmd_name)  # type: ignore[misc]
            elif cmd_name in callback_names:
                yield callback_names[cmd_name]
            else:
                continue

    def get_rows(self, command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> list[list[Any]]:
        """Build a row of cells for every subcommand in the panel, one cell per column type."""
        from rich_click.rich_command import RichCommand
        from rich_click.rich_help_rendering import get_command_rich_table_row

        return [
            (
                cmd.get_rich_table_row(ctx, formatter, self)
                if isinstance(cmd, RichCommand)
                else get_command_rich_table_row(cmd, ctx, formatter, self)
            )
            for cmd in self.get_objects(command, ctx)
        ]

    def get_table(
        self,
        command: RichCommand,
        ctx: RichContext,
        formatter: RichHelpFormatter,
    ) -> Table | RenderGroup:
        t_styles = {
            "show_lines": formatter.config.style_commands_table_show_lines,
            "leading": formatter.config.style_commands_table_leading,
            "box": formatter.config.style_commands_table_box,
            "border_style": formatter.config.style_commands_table_border_style,
            "row_styles": formatter.config.style_commands_table_row_styles,
            "pad_edge": formatter.config.style_commands_table_pad_edge,
            "padding": formatter.config.style_commands_table_padding,
            "expand": formatter.config.style_commands_table_expand,
        }
        # Define formatting in first column, as commands don't match highlighter regex
        # and set column ratio for first and second column, if a ratio has been set
        if formatter.config.style_commands_table_column_width_ratio is None:
            table_column_width_ratio: tuple[None, None] | tuple[int, int] = (None, None)
        else:
            table_column_width_ratio = formatter.config.style_commands_table_column_width_ratio

        def new_table() -> Table:
            table = self._get_base_table(**t_styles)
            table.add_column(style=formatter.config.style_command, no_wrap=True, ratio=table_column_width_ratio[0])
            table.add_column(
                no_wrap=False,
                ratio=table_column_width_ratio[1],
            )
            return table

        if not isinstance(command, Group):
            return new_table()

        return self._build_table(self._render_rows(command, ctx, formatter), formatter, new_table)

    def render(
        self,
        command: RichCommand,
        ctx: RichContext,
        formatter: RichHelpFormatter,
    ) -> Panel:
        from rich.text import Text

        from rich_click.rich_help_rendering import RichClickRichPanel

        inner: Any = self.get_table(command, ctx, formatter)

        p_styles: dict[str, Any] = {
            "border_style": formatter.config.style_commands_panel_border,
            "title_align": formatter.config.align_commands_panel,
            "box": formatter.config.style_commands_panel_box,
            "padding": formatter.config.style_commands_panel_padding,
            "style": formatter.config.style_commands_panel_style,
        }
        if self.panel_class is None or issubclass(self.panel_class, RichClickRichPanel):
            p_styles["title_padding"] = formatter.config.panel_title_padding

        if self.title_style is None:
            title_style = formatter.config.style_commands_panel_title_style
        else:
            title_style = self.title_style

        title = formatter.config.panel_title_string.format(self.name)

        if self.help:
            if self.help_style is None:
                help_style = formatter.config.style_commands_panel_help_style
            else:
                help_style = self.help_style
            if self.inline_help_in_title is None:
                inline_help_in_title = formatter.config.panel_inline_help_in_title
            else:
                inline_help_in_title = self.inline_help_in_title

            if inline_help_in_title:
                p_styles["title"] = Text("", overflow="ellipsis").join(
                    [
                        Text(title, style=title_style),
                        Text(formatter.config.panel_inline_help_delimiter),
                        Text(self.help, style=help_style),
                    ]
                )
            else:
                p_styles["title"] = Text(title, style=title_style)
                from rich.containers import Renderables

                inner = Renderables([formatter.rich_text(self.help, style=help_style), inner])
        else:
            p_styles["title"] = Text(title, style=title_style)

        panel = self._get_base_panel(inner, **p_styles)
        return panel


def align_panel_columns(
    panels: list[RichPanel[Any, Any]],
    command: RichCommand,
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> None:
    """
    Give every panel the same columns at the same widths, so that they line up.

    Panels asking for the same columns form a group: the group keeps a column if any panel in it
    has content there, and pins that column to the widest entry across the group that reaches past
    it. Groups are then padded to a common width, so that the final column - option help and
    command help alike - starts in the same place in every panel, and so that an entry running on
    under the columns it leaves empty has room enough across them.

    A panel the user has sized themselves is left out, and sizes itself as it always did.

    Panels live on the command, so the scratch state from a previous render is cleared first,
    whether or not this render aligns anything.
    """
    for panel in panels:
        panel._alignment = None
        panel._rows = None
    panels = [panel for panel in panels if not panel._manual_column_widths(formatter)]
    # A lone panel has nothing to line up against, and sizes itself the same way either way.
    if not formatter.config.align_columns_across_panels or len(panels) < 2:
        return

    groups: dict[tuple[str, ...], list[tuple[RichPanel[Any, Any], list[Any], list[Any]]]] = {}
    for panel in panels:
        rows = panel.get_rows(command, ctx, formatter)
        panel._rows = (formatter, rows)
        member = (panel, rows, panel.kept_column_types(rows, formatter))
        groups.setdefault((panel._object_attr, *panel.get_column_types(formatter)), []).append(member)

    shared_types: dict[tuple[str, ...], list[Any]] = {}
    widths: dict[tuple[str, ...], list[int]] = {}
    paddings: dict[tuple[str, ...], int] = {}
    minimums: dict[tuple[str, ...], int] = {}

    for key, members in groups.items():
        shared = [t for t in key[1:] if any(t in kept for _, _, kept in members)]
        shared_types[key] = shared
        paddings[key] = members[0][0]._table_padding_width(formatter)
        group_widths: list[int] = []
        minimum = 0
        # Widths and which rows keep their help inline depend on each other: a row too wide to sit
        # beside its help fits once the columns are pinned, and then has a say in how wide they
        # are. A few passes settle that, and the last one stands if they trade places instead.
        for _ in range(len(shared) + 3):
            grown: list[int] = []
            minimum = 0
            # Every row inline means every row had its say, so pinning these widths moves nothing.
            settled = True
            for panel, rows, _ in members:
                if not rows:
                    continue
                _, dropped, spanned, measured, needed = panel.layout(rows, shared, formatter, group_widths or None)
                settled = settled and not dropped and not spanned
                minimum = max(minimum, needed)
                # layout() pads the flexible trailing columns with None; only the leading ones are pinned.
                pinnable = [w for w in measured if w is not None]
                grown = [max(pair) for pair in zip(grown, pinnable)] or pinnable
            if grown == group_widths:
                break
            group_widths = grown
            if settled:
                break
        if group_widths:
            widths[key] = group_widths
            minimums[key] = minimum

    if not widths:
        return

    # The budget has to fit the narrowest panel, since they all line up with each other.
    available = min(panel._inner_width(formatter) for panel in panels)
    target = max(max(sum(w) + len(w) * paddings[key] for key, w in widths.items()), *minimums.values())
    if target > _column_budget(available):
        # Lining everything up would squeeze the help text out. Let each panel size itself instead.
        return

    for key, group_widths in widths.items():
        group_widths[-1] += target - sum(group_widths) - len(group_widths) * paddings[key]
        # Only the columns before the help are pinned; layout() reads the rest as flexible.
        flexible = [None] * (len(shared_types[key]) - len(group_widths))
        for panel, _, _ in groups[key]:
            panel._alignment = (shared_types[key], [*group_widths, *flexible])


# Using config to define panels is silently deprecated.
# We do not intend on removing this for a very long time, possibly ever.


def _resolve_panels_from_config(
    ctx: RichContext,
    formatter: RichHelpFormatter,
    groups: dict[str, list[GroupType]],
    panel_cls: type[RichPanel[CT, ColT]],
) -> list[RichPanel[CT, ColT]]:
    """Logic for resolving the groups."""
    # Step 1: get valid name(s) for the command currently being executed
    assert panel_cls._object_attr is not NotImplemented, "RichPanel must have a defined _object_attr"

    cmd_name = ctx.command.name
    _ctx: RichContext = ctx
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
    final_groups_list: list[GroupType] = []

    # Step 2: Match currently executing command to keys
    # Assign wildcards, but make sure we do not overwrite anything already defined.
    for mtch in reversed(sorted([_ for _ in groups if any(fnmatch(_path, _) for _path in paths)])):
        wildcard_option_groups = groups[mtch]
        for grp in wildcard_option_groups:
            grp = grp.copy()
            opts: list[str] = grp.get(panel_cls._object_attr, [])  # type: ignore[assignment]
            traversed = []
            for opt in grp.get(panel_cls._object_attr, []):  # type: ignore[attr-defined]
                if grp.get("deduplicate", True) and opt in [
                    _opt
                    for _grp in final_groups_list
                    for _opt in _grp.get(panel_cls._object_attr, [])  # type: ignore[attr-defined]
                ]:
                    opts.remove(opt)
                traversed.append(opt)
            grp[panel_cls._object_attr] = opts  # type: ignore[literal-required]
            grp.pop("deduplicate", None)
            final_groups_list.append(grp)

    return [panel_cls(**grp) for grp in final_groups_list]  # type: ignore[misc,arg-type]


def construct_panels(
    command: RichCommand,
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> list[RichPanel[Any, Any]]:
    """Construct panels from the command as well as from the old groups config."""
    _show_arguments = formatter.config.show_arguments

    # If only an options or a commands panel is defined,
    # then we respect intra-type sort order but not inter-type sort order.
    defined_commands = False
    defined_options = False
    # Handling ordering is tricky with the "groups" feature.
    # it's safest to flag and treat specially.
    using_groups_feat = False

    # Start with list of panels already defined.
    defined_panels: dict[tuple[str, str], RichPanel[Any, Any]] = {}

    for p in command.panels:
        defined_panels[(p._object_attr, p.name)] = p
        if p._object_attr == "options":
            defined_options = True
        elif p._object_attr == "commands":
            defined_commands = True

    if formatter.config.option_groups:
        option_groups_from_config = _resolve_panels_from_config(
            ctx, formatter, formatter.config.option_groups, formatter.option_panel_class
        )
        if option_groups_from_config:
            defined_panels.update({(p._object_attr, p.name): p for p in option_groups_from_config})
            using_groups_feat = True

    if isinstance(command, Group):
        if formatter.config.command_groups:
            command_groups_from_config = _resolve_panels_from_config(
                ctx, formatter, formatter.config.command_groups, formatter.command_panel_class
            )
            if command_groups_from_config:
                defined_panels.update({(p._object_attr, p.name): p for p in command_groups_from_config})
                using_groups_feat = True

    # Separate out default panels because we need to sort them properly later.
    # We will reversed() through this so order is flipped.
    # Also-- we have to decouple name from obj because commands can have different names
    # than their mappings to a Group.
    new_panels: dict[tuple[str, str], list[str]] = {}
    pre_default_panels: dict[tuple[str, str], list[str]] = {}
    post_default_panels: dict[tuple[str, str], list[str]]
    if isinstance(command, Group):
        if formatter.config.commands_before_options:
            if defined_commands != defined_options or using_groups_feat:
                pre_default_panels = {
                    ("commands", formatter.config.commands_panel_title): [],
                }
                post_default_panels = {
                    ("options", formatter.config.arguments_panel_title): [],
                    ("options", formatter.config.options_panel_title): [],
                }
            else:
                post_default_panels = {
                    ("commands", formatter.config.commands_panel_title): [],
                    ("options", formatter.config.arguments_panel_title): [],
                    ("options", formatter.config.options_panel_title): [],
                }
        else:
            if defined_commands != defined_options or using_groups_feat:
                pre_default_panels = {
                    ("options", formatter.config.arguments_panel_title): [],
                    ("options", formatter.config.options_panel_title): [],
                }
                post_default_panels = {
                    ("commands", formatter.config.commands_panel_title): [],
                }
            else:
                post_default_panels = {
                    ("options", formatter.config.arguments_panel_title): [],
                    ("options", formatter.config.options_panel_title): [],
                    ("commands", formatter.config.commands_panel_title): [],
                }
    else:
        post_default_panels = {
            ("options", formatter.config.arguments_panel_title): [],
            ("options", formatter.config.options_panel_title): [],
        }

    if ("commands", formatter.config.commands_panel_title) in defined_panels:
        pre_default_panels.pop(("commands", formatter.config.commands_panel_title), None)
        post_default_panels.pop(("commands", formatter.config.commands_panel_title), None)

    if ("options", formatter.config.options_panel_title) in defined_panels:
        pre_default_panels.pop(("options", formatter.config.options_panel_title), None)
        post_default_panels.pop(("options", formatter.config.options_panel_title), None)

    if ("options", formatter.config.arguments_panel_title) in defined_panels:
        pre_default_panels.pop(("options", formatter.config.arguments_panel_title), None)
        post_default_panels.pop(("options", formatter.config.arguments_panel_title), None)

    # Go through objects to see whether they are assigned.
    # Need to do tuples because commands and options can have same name.
    assigned_objects: dict[tuple[str, str], set[str]] = {}
    for p in defined_panels.values():
        for o in p.objects:
            assigned_objects.setdefault((p._object_attr, o), set())
            assigned_objects[(p._object_attr, o)].add(p.name)

    if ("options", formatter.config.arguments_panel_title) in defined_panels:
        _show_arguments = True

    objs: list[tuple[str, str, Parameter | Command]] = [
        ("options", name, o) for name, o in formatter.option_panel_class.list_all_objects(ctx)
    ]
    if isinstance(command, Group):
        objs.extend([("commands", name, o) for name, o in formatter.command_panel_class.list_all_objects(ctx)])

    from rich_click.rich_command import RichGroup

    # Here we are interested in:
    # 1. assigning objs based on panel=...
    # 2. getting unassigned objs
    for typ, name, obj in objs:
        if TYPE_CHECKING:
            assert isinstance(obj.name, str)
        if getattr(obj, "hidden", False):
            continue
        names = {name, obj.name}
        if isinstance(obj, Parameter):
            names.update(obj.opts)
        elif isinstance(obj, Command) and obj.callback is not None:
            names.add(obj.callback.__name__)
        assigned_to = set()
        for n in names:
            _assigned_panels = assigned_objects.get((typ, n), set())
            for ap in _assigned_panels:
                assigned_to.add((typ, ap))
        assigned = bool(assigned_to)
        inferred = False
        panel_list: list[str] = []
        if hasattr(obj, "panel"):
            if isinstance(obj.panel, str):
                panel_list = [obj.panel]
            elif obj.panel is None:
                if assigned:
                    continue
            else:
                panel_list = obj.panel
        elif typ == "commands" and isinstance(command, RichGroup):
            _p = command._panel_command_mapping.get(name)
            if _p:
                panel_list.extend(_p)
        if not panel_list:
            inferred = True
            if typ == "options":
                if not formatter.config.group_arguments_options and isinstance(obj, Argument):
                    if _show_arguments is not False:
                        panel_list = [formatter.config.arguments_panel_title]
                    else:
                        panel_list = []
                else:
                    panel_list = [formatter.config.options_panel_title]
            elif typ == "commands":
                panel_list = [formatter.config.commands_panel_title]
            else:
                panel_list = []
        for panel_name in panel_list:
            # Ensure we don't reassign if already assigned.
            if (typ, panel_name) not in assigned_to:
                if (typ, panel_name) in defined_panels:
                    defined_panels[(typ, panel_name)].add_object(name)
                elif assigned:
                    pass
                elif (typ, panel_name) in pre_default_panels:
                    pre_default_panels[(typ, panel_name)].append(name)
                elif (typ, panel_name) in post_default_panels:
                    post_default_panels[(typ, panel_name)].append(name)
                else:
                    new_panels.setdefault((typ, panel_name), []).append(name)
            if (
                _show_arguments is None
                and panel_name == formatter.config.arguments_panel_title
                and isinstance(obj, RichArgument)
                and (not inferred or obj.help is not None)
            ):
                _show_arguments = True

    if not _show_arguments:
        pre_default_panels.pop(("options", formatter.config.arguments_panel_title), None)
        post_default_panels.pop(("options", formatter.config.arguments_panel_title), None)

    final_panels: list[RichPanel[Any, Any]] = []

    def add_panels_from(
        mappings: list[dict[tuple[str, str], list[str]] | dict[tuple[str, str], RichPanel[Any, Any]]],
        type_filter: str | None = None,
    ) -> None:
        for d in mappings:
            for (typ, panel_name), obj_list in d.items():
                if type_filter is not None and typ != type_filter:
                    continue
                cls: type[RichPanel[Any, Any]]
                if typ == "options":
                    cls = formatter.option_panel_class
                elif typ == "commands":
                    cls = formatter.command_panel_class
                else:
                    continue
                panel: RichPanel[Any, Any]
                if isinstance(obj_list, RichPanel):
                    panel = obj_list
                elif (typ, panel_name) not in defined_panels:
                    panel = cls(panel_name)
                    setattr(panel, panel._object_attr, [i for i in obj_list])
                else:
                    panel = defined_panels[(typ, panel_name)]
                    for _obj in obj_list:
                        panel.add_object(_obj)
                final_panels.append(panel)

    if formatter.config.default_panels_first:
        add_panels_from([pre_default_panels], "options")
        add_panels_from([defined_panels, new_panels], "options")
        add_panels_from([pre_default_panels, post_default_panels], "commands")
        add_panels_from([defined_panels, new_panels], "commands")
    else:
        add_panels_from([pre_default_panels, defined_panels, new_panels, post_default_panels])

    align_panel_columns(final_panels, command, ctx, formatter)
    return final_panels
