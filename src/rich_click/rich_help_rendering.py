from __future__ import annotations

import inspect
import re
from fnmatch import fnmatch
from gettext import gettext
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Literal, Optional, Union

import click

# Due to how rich_click.cli.patch() works, it is safer to import Command types directly
# rather than use the click module e.g. click.Command
from click import Command, Group
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import RenderableType
from rich.highlighter import RegexHighlighter
from rich.markdown import Markdown
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from rich_click._compat_click import (
    CLICK_IS_BEFORE_VERSION_9X,
    CLICK_IS_BEFORE_VERSION_82,
    CLICK_IS_VERSION_80,
)
from rich_click.rich_context import RichContext
from rich_click.rich_help_formatter import RichHelpFormatter
from rich_click.rich_panel import GroupType
from rich_click.rich_parameter import RichParameter


if TYPE_CHECKING:
    from rich_click.rich_command import RichCommand, RichGroup

# Support rich <= 10.6.0
try:
    from rich.console import group
except ImportError:
    from rich.console import render_group as group  # type: ignore[attr-defined,no-redef]

RichPanelRow = List[RenderableType]


if CLICK_IS_BEFORE_VERSION_9X:
    # We need to load from here to help with patching.
    from rich_click.rich_command import MultiCommand  # type: ignore[attr-defined]
else:
    MultiCommand = Group  # type: ignore[misc,assignment,unused-ignore]


@group()
def _get_help_text(obj: Union[Command, Group], formatter: RichHelpFormatter) -> Iterable[Union[Markdown, Text]]:
    """
    Build primary help text for a click command or group.
    Returns the prose help text for a command or group, rendered either as a
    Rich Text object or as Markdown.
    If the command is marked as depreciated, the depreciated string will be prepended.

    Args:
    ----
        obj (click.Command or click.Group): Command or group to build help text for.
        formatter: formatter object.

    Yields:
    ------
        Text or Markdown: Multiple styled objects (depreciated, usage)

    """
    if TYPE_CHECKING:  # pragma: no cover
        assert isinstance(obj.help, str)
    config = formatter.config
    # Prepend deprecated status
    if obj.deprecated:
        if isinstance(obj.deprecated, str):
            yield Text(
                formatter.config.deprecated_with_reason_string.format(obj.deprecated), style=config.style_deprecated
            )
        else:
            yield Text(config.deprecated_string, style=config.style_deprecated)

    # Fetch and dedent the help text
    help_text = inspect.cleandoc(obj.help)

    # Trim off anything that comes after \f on its own line
    help_text = help_text.partition("\f")[0]

    # Get the first paragraph
    first_line = help_text.split("\n\n")[0]
    # Remove single linebreaks
    if not config.use_markdown and not config.text_markup == "markdown":
        if not first_line.startswith("\b"):
            first_line = first_line.replace("\n", " ")
    yield formatter.rich_text(first_line.strip(), config.style_helptext_first_line)

    # Get remaining lines, remove single line breaks and format as dim
    remaining_paragraphs = help_text.split("\n\n")[1:]
    if len(remaining_paragraphs) > 0:
        if not config.use_markdown and not config.text_markup == "markdown":
            # Remove single linebreaks
            remaining_paragraphs = [
                x.replace("\n", " ").strip() if not x.startswith("\b") else "{}\n".format(x.strip("\b\n"))
                for x in remaining_paragraphs
            ]
            # Join back together
            remaining_lines = "\n".join(remaining_paragraphs)
        else:
            # Join with double linebreaks if markdown
            remaining_lines = "\n\n".join(remaining_paragraphs)

        yield formatter.rich_text(remaining_lines, config.style_helptext)


def _get_deprecated_text(
    deprecated: Union[bool, str],
    formatter: RichHelpFormatter,
) -> Text:
    if isinstance(deprecated, str):
        s = formatter.config.deprecated_with_reason_string.format(deprecated)
    else:
        s = formatter.config.deprecated_string
    return Text(s, style=formatter.config.style_deprecated)


def _get_parameter_env_var(
    param: Union[click.Argument, click.Option, RichParameter],
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> Optional[Text]:
    if not getattr(param, "show_envvar", None):
        return None

    envvar = getattr(param, "envvar", None)

    # https://github.com/pallets/click/blob/0aec1168ac591e159baf6f61026d6ae322c53aaf/src/click/core.py#L2720-L2726
    if envvar is None:
        if (
            getattr(param, "allow_from_autoenv", None)
            and getattr(ctx, "auto_envvar_prefix", None) is not None
            and param.name is not None
        ):
            envvar = f"{ctx.auto_envvar_prefix}_{param.name.upper()}"
    if envvar is not None:
        envvar = ", ".join(envvar) if isinstance(envvar, list) else envvar

    if envvar is not None:
        return Text(formatter.config.envvar_string.format(envvar), style=formatter.config.style_option_envvar)
    return None


def _get_parameter_deprecated(
    param: Union[click.Argument, click.Option, RichParameter],
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> Optional[Text]:
    if not getattr(param, "deprecated", None):
        return None
    return _get_deprecated_text(getattr(param, "deprecated"), formatter)


def _get_parameter_help(
    param: Union[click.Argument, click.Option, RichParameter],
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> Optional[Union[Markdown, Text]]:
    base_help_txt = getattr(param, "help", None)
    if not base_help_txt:
        return None

    if TYPE_CHECKING:  # pragma: no cover
        assert isinstance(param, click.Option)
        assert hasattr(param, "help")
        assert isinstance(param.help, str)

    paragraphs = base_help_txt.split("\n\n")

    # Remove single linebreaks
    if not formatter.config.use_markdown and not formatter.config.text_markup == "markdown":
        paragraphs = [
            x.replace("\n", " ").strip() if not x.startswith("\b") else "{}\n".format(x.strip("\b\n"))
            for x in paragraphs
        ]
    help_text = "\n".join(paragraphs).strip()

    # `Deprecated` is included in base help text; remove it here.
    if getattr(param, "deprecated", None):
        if isinstance(getattr(param, "deprecated"), str):
            help_text = re.sub(r"\(DEPRECATED: .*?\)$", "", help_text)
        else:
            help_text = re.sub(r"\(DEPRECATED\)$", "", help_text)

    if getattr(param, "help_style", None) is None:
        style = formatter.config.style_option_help
    else:
        style = param.help_style  # type: ignore[attr-defined]
    return formatter.rich_text(help_text, style)


def _get_parameter_metavar(
    param: Union[click.Argument, click.Option, RichParameter],
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> Optional[Text]:
    if formatter.config.append_metavars_help:
        metavar_str = param.make_metavar() if CLICK_IS_BEFORE_VERSION_82 else param.make_metavar(ctx)  # type: ignore
        # Do it ourselves if this is a positional argument
        if (
            isinstance(param, click.core.Argument)
            and param.name is not None
            and re.match(rf"\[?{param.name.upper()}]?", metavar_str)
        ):
            metavar_str = param.type.name.upper()
        # Attach metavar if param is a positional argument, or if it is a non boolean and non flag option
        if isinstance(param, click.core.Argument) or (
            metavar_str != "BOOLEAN" and hasattr(param, "is_flag") and not param.is_flag
        ):
            metavar_str = metavar_str.replace("[", "").replace("]", "")
            return Text(
                formatter.config.append_metavars_help_string.format(metavar_str),
                style=formatter.config.style_metavar_append,
                overflow="fold",
            )
    return None


def _get_parameter_default(
    param: Union[click.Argument, click.Option, RichParameter], ctx: RichContext, formatter: RichHelpFormatter
) -> Optional[Text]:

    if not hasattr(param, "show_default"):
        return None

    show_default = False
    show_default_is_str = False

    resilient = ctx.resilient_parsing
    ctx.resilient_parsing = True
    try:
        default_value = param.get_default(ctx, call=False)
    finally:
        ctx.resilient_parsing = resilient

    if (not CLICK_IS_VERSION_80 and param.show_default is not None) or param.show_default:
        if isinstance(param.show_default, str):
            show_default_is_str = show_default = True
        else:
            show_default = param.show_default
    elif ctx.show_default is not None:
        show_default = ctx.show_default

    default_string: Optional[str] = None

    if show_default_is_str or (show_default and (default_value is not None)):
        if show_default_is_str:
            default_string = f"({param.show_default})"
        elif isinstance(default_value, (list, tuple)):
            default_string = ", ".join(str(d) for d in default_value)
        elif inspect.isfunction(default_value):
            default_string = gettext("(dynamic)")
        elif hasattr(param, "is_bool_flag") and param.is_bool_flag and param.secondary_opts:
            # For boolean flags that have distinct True/False opts,
            # use the opt without prefix instead of the value.
            opt = (param.opts if default_value else param.secondary_opts)[0]
            first = opt[:1]
            if first.isalnum():
                default_string = opt
            if opt[1:2] == first:
                default_string = opt[2:]
            else:
                default_string = opt[1:]
        elif hasattr(param, "is_bool_flag") and param.is_bool_flag and not param.secondary_opts and not default_value:
            if CLICK_IS_VERSION_80:
                default_string = str(param.default)
            else:
                default_string = ""
        elif default_value == "":
            default_string = '""'
        else:
            default_string = str(default_value)

    if default_string:
        return Text(
            formatter.config.default_string.format(default_string),
            style=formatter.config.style_option_default,
        )
    return None


def _get_parameter_required(
    param: Union[click.Argument, click.Option, RichParameter], ctx: RichContext, formatter: RichHelpFormatter
) -> Optional[Text]:
    if param.required:
        return Text(formatter.config.required_long_string, style=formatter.config.style_required_long)
    return None


def get_help_parameter(
    param: Union[click.Argument, click.Option, RichParameter], ctx: RichContext, formatter: RichHelpFormatter
) -> Columns:
    """
    Build primary help text for a click option or argument.
    Returns the prose help text for an option or argument, rendered either
    as a Rich Text object or as Markdown.
    Additional elements are appended to show the default and required status if applicable.

    Args:
    ----
        param (click.Argument or click.Option): Parameter to build help text for.
        ctx (click.Context): Click Context object.
        formatter (RichHelpFormatter): formatter object.

    Returns:
    -------
        Columns: A columns element with multiple styled objects (help, default, required)

    """
    config = formatter.config
    items: List[RenderableType] = []

    if TYPE_CHECKING:  # pragma: no cover
        assert isinstance(param.name, str)

    # Get the environment variable first
    envvar_text = _get_parameter_env_var(param, ctx, formatter)
    help_text = _get_parameter_help(param, ctx, formatter)
    deprecated_text = _get_parameter_deprecated(param, ctx, formatter)
    metavar_text = _get_parameter_metavar(param, ctx, formatter)
    default_text = _get_parameter_default(param, ctx, formatter)
    required_text = _get_parameter_required(param, ctx, formatter)

    if envvar_text is not None and config.option_envvar_first:
        items.append(envvar_text)
    if help_text is not None:
        items.append(help_text)
    if deprecated_text is not None:
        items.append(deprecated_text)
    if metavar_text is not None:
        items.append(metavar_text)
    if envvar_text is not None and not config.option_envvar_first:
        items.append(envvar_text)
    if default_text is not None:
        items.append(default_text)
    if required_text is not None:
        items.append(required_text)

    # Use Columns - this allows us to group different renderable types
    # (Text, Markdown) onto a single line.
    return Columns(items)


def get_rich_table_row(
    param: Union[click.Argument, click.Option, RichParameter],
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> RichPanelRow:
    """Create a row for the rich table corresponding with this parameter."""
    # Short and long form
    opt_long_strs = []
    opt_short_strs = []
    for idx, opt in enumerate(param.opts):
        opt_str = opt
        try:
            opt_str += "/" + param.secondary_opts[idx]
        except IndexError:
            pass

        if isinstance(param, click.core.Argument):
            opt_long_strs.append(opt_str.upper())
        elif "--" in opt:
            opt_long_strs.append(opt_str)
        else:
            opt_short_strs.append(opt_str)

    # Column for a metavar, if we have one
    metavar = Text(style=formatter.config.style_metavar, overflow="fold")
    metavar_str = param.make_metavar() if CLICK_IS_BEFORE_VERSION_82 else param.make_metavar(ctx)  # type: ignore

    if TYPE_CHECKING:  # pragma: no cover
        assert isinstance(param.name, str)
        assert isinstance(param, click.Option)

    # Do it ourselves if this is a positional argument
    if isinstance(param, click.core.Argument) and re.match(rf"\[?{param.name.upper()}]?", metavar_str):
        metavar_str = param.type.name.upper()

    # Attach metavar if param is a positional argument, or if it is a non-boolean and non flag option
    if isinstance(param, click.core.Argument) or (metavar_str != "BOOLEAN" and not getattr(param, "is_flag", None)):
        metavar.append(metavar_str)

    # Range - from
    # https://github.com/pallets/click/blob/c63c70dabd3f86ca68678b4f00951f78f52d0270/src/click/core.py#L2698-L2706  # noqa: E501
    try:
        # skip count with default range type
        if isinstance(param.type, click.types._NumberRangeBase) and not (
            param.count and param.type.min == 0 and param.type.max is None
        ):
            range_str = param.type._describe_range()
            if range_str:
                metavar.append(formatter.config.range_string.format(range_str))
    except AttributeError:
        # click.types._NumberRangeBase is only in Click 8x onwards
        pass

    # Required asterisk
    required: Union[Text, str] = ""
    if param.required:
        required = Text(formatter.config.required_short_string, style=formatter.config.style_required_short)

    # Highlighter to make [ | ] and <> dim
    class MetavarHighlighter(RegexHighlighter):
        highlights = [
            r"^(?P<metavar_sep>(\[|<))",
            r"(?P<metavar_sep>\|)",
            r"(?P<metavar_sep>(\]|>)$)",
        ]

    metavar_highlighter = MetavarHighlighter()

    cols: RichPanelRow = [
        required,
        formatter.highlighter(formatter.highlighter(",".join(opt_long_strs))),
        formatter.highlighter(formatter.highlighter(",".join(opt_short_strs))),
        metavar_highlighter(metavar),
        (
            param.get_rich_help(ctx, formatter)
            if isinstance(param, RichParameter)
            else get_help_parameter(param, ctx, formatter)
        ),
    ]

    # Remove metavar if specified in config
    if not formatter.config.show_metavars_column:
        cols.pop(3)

    return cols


def _make_command_help(
    help_text: str, formatter: RichHelpFormatter, deprecated: Union[bool, str]
) -> Union[Text, Markdown, Columns]:
    """
    Build cli help text for a click group command.
    That is, when calling help on groups with multiple subcommands
    (not the main help text when calling the subcommand help).
    Returns the first paragraph of help text for a command, rendered either as a
    Rich Text object or as Markdown.
    Ignores single newlines as paragraph markers, looks for double only.

    Args:
    ----
        help_text (str): Help text
        formatter: formatter object
        deprecated (bool or string): Object marked by user as deprecated.

    Returns:
    -------
        Text or Markdown: Styled object

    """
    paragraphs = inspect.cleandoc(help_text).split("\n\n")
    # Remove single linebreaks
    if not formatter.config.use_markdown and not paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\n", " ")
    elif paragraphs[0].startswith("\b"):
        paragraphs[0] = paragraphs[0].replace("\b\n", "")
    help_text = paragraphs[0].strip()
    renderable: Union[Text, Markdown, Columns]
    renderable = formatter.rich_text(help_text, formatter.config.style_option_help)
    if deprecated:
        dep_txt = _get_deprecated_text(
            deprecated=deprecated,
            formatter=formatter,
        )
        if isinstance(renderable, Text):
            renderable.append(" ")
            renderable.append(dep_txt)
        else:
            renderable = Columns([renderable, dep_txt])
    return renderable


def get_rich_usage(formatter: RichHelpFormatter, prog: str, args: str = "", prefix: Optional[str] = None) -> None:
    """Richly render usage text."""
    if prefix is None:
        prefix = "Usage:"

    config = formatter.config

    # Header text if we have it
    if config.header_text:
        formatter.write(
            Padding(
                formatter.rich_text(config.header_text, config.style_header_text),
                (1, 1, 0, 1),
            ),
        )

    # Highlighter for options and arguments
    class UsageHighlighter(RegexHighlighter):
        highlights = [
            r"(?P<argument>\w+)",
        ]

    usage_highlighter = UsageHighlighter()

    # Print usage
    formatter.write(
        Padding(
            Columns(
                (
                    Text(prefix, style=config.style_usage),
                    Text(prog, style=config.style_usage_command),
                    usage_highlighter(args),
                )
            ),
            1,
        ),
    )


def get_rich_help_text(self: Command, ctx: RichContext, formatter: RichHelpFormatter) -> None:
    """Write rich help text to the formatter if it exists."""
    # Print command / group help if we have some
    if self.help:
        # Print with some padding
        formatter.write(
            Padding(
                Align(_get_help_text(self, formatter), pad=False),
                (0, 1, 1, 1),
            )
        )


def _resolve_groups(
    ctx: RichContext, groups: Dict[str, List[GroupType]], group_attribute: Literal["commands", "options"]
) -> List[GroupType]:
    """Logic for resolving the groups."""
    # Step 1: get valid name(s) for the command currently being executed
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
    final_groups_list: List[GroupType] = []

    # Assign wildcards, but make sure we do not overwrite anything already defined.
    for _path in paths:
        for mtch in reversed(sorted([_ for _ in groups if fnmatch(_path, _)])):
            wildcard_option_groups = groups[mtch]
            for grp in wildcard_option_groups:
                grp = grp.copy()
                opts = grp.get(group_attribute, []).copy()  # type: ignore[attr-defined]
                traversed = []
                for opt in grp.get(group_attribute, []):  # type: ignore[attr-defined]
                    if grp.get("deduplicate", True) and opt in [
                        _opt
                        for _grp in final_groups_list
                        for _opt in [*traversed, *_grp.get(group_attribute, [])]  # type: ignore[has-type]
                    ]:
                        opts.remove(opt)
                    traversed.append(opt)
                grp[group_attribute] = opts  # type: ignore[typeddict-unknown-key]
                final_groups_list.append(grp)

    final_groups_list.append({group_attribute: []})  # type: ignore[misc]
    return final_groups_list


def get_rich_options(
    obj: "RichCommand",
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> None:
    """Richly render a click Command's options."""
    # Look through config.option_groups for this command
    # stick anything unmatched into a default group at the end
    from rich_click.rich_panel import construct_panels

    panels = construct_panels(
        ctx=ctx,
        command=obj,
        formatter=formatter,
        panel_cls=formatter.option_panel_class,
    )
    for panel in panels:
        p = panel.render(obj, ctx, formatter)
        if not isinstance(p.renderable, Table) or len(p.renderable.rows) > 0:
            formatter.write(p)


def get_rich_commands(
    obj: "RichGroup",
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> None:
    """Richly render a click Command's options."""
    from rich_click.rich_panel import construct_panels

    panels = construct_panels(
        ctx=ctx,
        command=obj,
        formatter=formatter,
        panel_cls=formatter.command_panel_class,
    )
    for panel in panels:
        p = panel.render(obj, ctx, formatter)
        if not isinstance(p.renderable, Table) or len(p.renderable.rows) > 0:
            formatter.write(p)


def get_rich_epilog(
    self: Command,
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> None:
    """Richly render a click Command's epilog if it exists."""
    if self.epilog:
        # Remove single linebreaks, replace double with single
        lines = self.epilog.split("\n\n")
        if isinstance(self.epilog, (Text, Markdown)):
            epilog = self.epilog
        else:
            epilog = "\n".join([x.replace("\n", " ").strip() for x in lines])  # type: ignore[assignment]
            epilog = formatter.rich_text(epilog, formatter.config.style_epilog_text)  # type: ignore[assignment]
        formatter.write(Padding(Align(epilog, pad=False), 1))

    # Footer text if we have it
    if formatter.config.footer_text:
        formatter.write(
            Padding(
                formatter.rich_text(formatter.config.footer_text, formatter.config.style_footer_text),
                (1, 1, 0, 1),
            )
        )


def rich_format_error(
    self: click.ClickException, formatter: RichHelpFormatter, export_console_as: Literal[None, "html", "svg"] = None
) -> None:
    """
    Print richly formatted click errors.

    Called by custom exception handler to print richly formatted click errors.
    Mimics original click.ClickException.echo() function but with rich formatting.

    Args:
    ----
        self (click.ClickException): Click exception to format.
        formatter: formatter object.
        export_console_as: If set, outputs error message as HTML or SVG.

    """
    config = formatter.config
    # Print usage
    if getattr(self, "ctx", None) is not None:
        if TYPE_CHECKING:  # pragma: no cover
            assert hasattr(self, "ctx")
        self.ctx.command.format_usage(self.ctx, formatter)
    if config.errors_suggestion:
        formatter.write(
            Padding(
                config.errors_suggestion,
                (0, 1, 0, 1),
            ),
            style=config.style_errors_suggestion,
        )
    elif (
        config.errors_suggestion is None
        and getattr(self, "ctx", None) is not None
        and self.ctx.command.get_help_option(self.ctx) is not None  # type: ignore[attr-defined]
    ):
        cmd_path = self.ctx.command_path  # type: ignore[attr-defined]
        help_option = self.ctx.help_option_names[0]  # type: ignore[attr-defined]
        formatter.write(
            Padding(
                Columns(
                    (
                        Text("Try"),
                        Text(f"'{cmd_path} {help_option}'", style=config.style_errors_suggestion_command),
                        Text("for help"),
                    )
                ),
                (0, 1, 0, 1),
            ),
            style=config.style_errors_suggestion,
        )

    # A major Python library using click (dbt-core) has its own exception
    # logic that subclasses ClickException, but does not use the message
    # attribute. Checking for the 'message' attribute works to make the
    # rich-click CLI compatible.
    if hasattr(self, "message"):

        kw: Dict[str, Any] = {}

        if isinstance(formatter.config.style_errors_panel_box, str):
            box_style = getattr(box, formatter.config.style_errors_panel_box, None)
        else:
            box_style = formatter.config.style_errors_panel_box

        if box_style:
            kw["box"] = box_style

        formatter.write(
            Padding(
                Panel(
                    formatter.highlighter(self.format_message()),
                    border_style=config.style_errors_panel_border,
                    title=config.errors_panel_title,
                    title_align=config.align_errors_panel,
                    **kw,
                ),
                (0, 0, 1, 0),
            )
        )
    if config.errors_epilogue:
        formatter.write(Padding(config.errors_epilogue, (0, 1, 1, 1)))
