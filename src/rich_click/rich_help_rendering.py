from __future__ import annotations

import inspect
import re
from gettext import gettext
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Literal, Optional, Tuple, Union

import click

# Due to how rich_click.cli.patch() works, it is safer to import types
# from click.core rather than use the click module e.g. click.Command
import click.core
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import RenderableType, group
from rich.highlighter import RegexHighlighter
from rich.jupyter import JupyterMixin
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text

from rich_click._compat_click import (
    CLICK_IS_BEFORE_VERSION_9X,
    CLICK_IS_BEFORE_VERSION_82,
    CLICK_IS_VERSION_80,
)
from rich_click.rich_context import RichContext
from rich_click.rich_help_formatter import RichHelpFormatter
from rich_click.rich_parameter import RichParameter


if TYPE_CHECKING:
    from rich.markdown import Markdown

    from rich_click.rich_help_configuration import OptionColumnType


RichPanelRow = List[RenderableType]


if CLICK_IS_BEFORE_VERSION_9X:
    # We need to load from here to help with patching.
    from rich_click.rich_command import MultiCommand  # type: ignore[attr-defined]
else:
    MultiCommand = click.core.Group  # type: ignore[misc,assignment,unused-ignore]


@group()
def _get_help_text(
    obj: Union[click.core.Command, click.core.Group], formatter: RichHelpFormatter
) -> Iterable[Union[Padding, "Markdown", Text]]:
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
            yield Padding(
                Text(
                    formatter.config.deprecated_with_reason_string.format(obj.deprecated), style=config.style_deprecated
                ),
                formatter.config.padding_helptext_deprecated,
            )
        else:
            yield Padding(
                Text(config.deprecated_string, style=config.style_deprecated),
                formatter.config.padding_helptext_deprecated,
            )

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
    yield Padding(
        formatter.rich_text(first_line.strip(), formatter.config.style_helptext_first_line),
        formatter.config.padding_helptext_first_line,
    )
    # Get remaining lines, remove single line breaks and format as dim
    remaining_paragraphs = help_text.split("\n\n")[1:]

    use_markdown = formatter.config.use_markdown or formatter.config.text_markup == "markdown"
    if formatter.config.text_paragraph_linebreaks is None:
        if use_markdown:
            lb = "\n\n"
        else:
            lb = "\n"
    else:
        lb = formatter.config.text_paragraph_linebreaks
    if len(remaining_paragraphs) > 0:
        if not use_markdown:
            # Remove single linebreaks
            remaining_paragraphs = [
                x.replace("\n", " ").strip() if not x.startswith("\b") else "{}\n".format(x.strip("\b\n"))
                for x in remaining_paragraphs
            ]
            # Join back together
            remaining_lines = lb.join(remaining_paragraphs)
        else:
            # Join with double linebreaks if markdown
            remaining_lines = lb.join(remaining_paragraphs)
        yield formatter.rich_text(remaining_lines, formatter.config.style_helptext)


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
) -> Optional[Union["Markdown", Text]]:
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
    append: bool = True,
) -> Optional[Text]:
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
            style=formatter.config.style_metavar_append if append else formatter.config.style_metavar,
            overflow="fold",
        )
    return None


def _get_parameter_help_metavar_col(
    param: Union[click.Argument, click.Option, RichParameter],
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> Optional[Text]:
    # Column for a metavar, if we have one
    metavar = Text(style=formatter.config.style_metavar, overflow="fold")
    metavar_str = param.make_metavar() if CLICK_IS_BEFORE_VERSION_82 else param.make_metavar(ctx)  # type: ignore

    if TYPE_CHECKING:  # pragma: no cover
        assert isinstance(param.name, str)
        assert isinstance(param, click.core.Option)

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
                metavar.append(" " + formatter.config.range_string.format(range_str))
    except AttributeError:
        # click.types._NumberRangeBase is only in Click 8x onwards
        pass

    # Highlighter to make [ | ] and <> dim
    class MetavarHighlighter(RegexHighlighter):
        highlights = [
            r"^(?P<metavar_sep>(\[|<))",
            r"(?P<metavar_sep>\|)",
            r"(?P<metavar_sep>(\]|>)$)",
        ]

    if "".join(metavar._text) == "":
        return None

    metavar_highlighter = MetavarHighlighter()
    return metavar_highlighter(metavar)


def _get_parameter_help_opt(
    param: Union[click.Argument, click.Option, RichParameter],
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> Tuple[
    Optional[Text],
    Optional[Text],
    Optional[Text],
    Optional[Text],
    Optional[Text],
]:
    # This may seem convoluted to return tuples with widths instead of just renderables,
    # but there are two things we want to do that are impossible otherwise:
    # 1. Prevent splitting of options. If we just use Text() and allow wrapping,
    #    then something like --foo/--bar may split in the middle of an option
    #    instead of at the "/".
    # 2. Make it so the table doesn't expand. We solve the first problem by using
    #    Columns(), but the issue is there is no way to prevent the expansion of
    #    the outer table column other than to explicitly set the width.
    # Attempting to solve both of those problems simultaneously leads to this mess.

    opt_long_primary = []
    opt_short_primary = []
    opt_long_secondary = []
    opt_short_secondary = []

    for opt in param.opts:
        if isinstance(param, click.core.Argument):
            opt_long_primary.append(opt.upper())
        elif "--" in opt:
            opt_long_primary.append(opt)
        else:
            opt_short_primary.append(opt)
    for opt in param.secondary_opts:
        if isinstance(param, click.core.Argument):
            opt_long_secondary.append(opt.upper())
        elif "--" in opt:
            opt_long_secondary.append(opt)
        else:
            opt_short_secondary.append(opt)

    from rich.text import Text

    # opt_long_primary_len = len("".join(opt_long_primary)) + len(opt_long_primary) - 1
    # opt_short_primary_len = len("".join(opt_short_primary)) + len(opt_short_primary) - 1
    # opt_long_secondary_len = len("".join(opt_long_secondary)) + len(opt_long_secondary) - 1
    # opt_short_secondary_len = len("".join(opt_short_secondary)) + len(opt_short_secondary) - 1

    primary_cols = []
    secondary_cols = []
    long_cols = []
    short_cols = []

    comma = Text(formatter.config.option_delimiter_comma, style=formatter.config.style_option_help)
    slash = Text(formatter.config.option_delimiter_slash, style=formatter.config.style_option_help)

    for o in opt_short_primary:
        oh = Text(o.strip(), style=formatter.config.style_switch)
        primary_cols.append(oh)
        primary_cols.append(comma)
        short_cols.append(oh)
        short_cols.append(comma)

    for o in opt_long_primary:
        oh = Text(o.strip(), style=formatter.config.style_option)
        primary_cols.append(oh)
        primary_cols.append(comma)
        long_cols.append(oh)
        long_cols.append(comma)

    if opt_short_secondary:
        short_cols = short_cols[:-1]
        short_cols.append(slash)
        for o in opt_short_secondary:
            oh = Text(
                o.strip(),
                style=(
                    formatter.config.style_switch_negative
                    if formatter.config.style_switch_negative is not None
                    else formatter.config.style_switch
                ),
            )
            secondary_cols.append(oh)
            secondary_cols.append(comma)
            short_cols.append(oh)
            short_cols.append(comma)

    if opt_long_secondary:
        long_cols = long_cols[:-1]
        long_cols.append(slash)
        for o in opt_long_secondary:
            oh = Text(
                o.strip(),
                style=(
                    formatter.config.style_option_negative
                    if formatter.config.style_option_negative is not None
                    else formatter.config.style_option
                ),
            )
            secondary_cols.append(oh)
            secondary_cols.append(comma)
            long_cols.append(oh)
            long_cols.append(comma)

    all_cols = primary_cols
    if secondary_cols:
        all_cols = [*primary_cols[:-1], slash, *secondary_cols]

    def _renderable(cols: List[Text]) -> Optional[Text]:
        if not cols:
            return None
        if len(cols) == 1:
            return cols[0]
        # Todo - make the text fold at the slashes without adding whitespace.
        #   this is very tricky.
        t = Text("", overflow="fold").join(cols)
        return t

    primary_final = _renderable(primary_cols[:-1])
    secondary_final = _renderable(secondary_cols[:-1])
    long_final = _renderable(long_cols[:-1])
    short_final = _renderable(short_cols[:-1])
    all_final = _renderable(all_cols[:-1])

    return primary_final, secondary_final, long_final, short_final, all_final


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


def _get_parameter_help_required_short(
    param: Union[click.Argument, click.Option, RichParameter], ctx: RichContext, formatter: RichHelpFormatter
) -> Optional[Text]:
    if param.required:
        return Text(formatter.config.required_short_string, style=formatter.config.style_required_short)
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
    if formatter.config.append_metavars_help:
        metavar_text = _get_parameter_metavar(param, ctx, formatter)
    else:
        metavar_text = None
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
    columns: Optional[List["OptionColumnType"]] = None,
) -> RichPanelRow:
    """Create a row for the rich table corresponding with this parameter."""
    # Short and long form
    columns = columns or formatter.config.options_table_columns

    opt_long_strs = []
    opt_short_strs = []
    for idx, opt in enumerate(param.opts):
        opt_str = opt
        secondary = None
        try:
            secondary = param.secondary_opts[idx]
        except IndexError:
            pass

        if isinstance(param, click.core.Argument):
            opt_long_strs.append(Text.from_markup(opt_str.upper(), style=formatter.config.style_option))
        elif "--" in opt:
            if secondary:
                opt_long_strs.append(
                    Text("/", style=formatter.config.style_option_help).join(
                        [
                            Text(opt_str, style=formatter.config.style_option),
                            Text(
                                secondary,
                                style=(
                                    formatter.config.style_option_negative
                                    if formatter.config.style_option_negative is not None
                                    else formatter.config.style_option
                                ),
                            ),
                        ]
                    )
                )
            else:
                opt_long_strs.append(Text.from_markup(opt_str, style=formatter.config.style_option))
        else:
            if secondary:
                opt_short_strs.append(
                    Text("/", style=formatter.config.style_option_help).join(
                        [
                            Text(opt_str, style=formatter.config.style_option),
                            Text(
                                secondary,
                                style=(
                                    formatter.config.style_option_negative
                                    if formatter.config.style_option_negative is not None
                                    else formatter.config.style_option
                                ),
                            ),
                        ]
                    )
                )
            else:
                opt_short_strs.append(Text.from_markup(opt_str, style=formatter.config.style_option))

    if TYPE_CHECKING:  # pragma: no cover
        assert isinstance(param.name, str)
        assert isinstance(param, click.core.Option)

    _primary, _secondary, _long, _short, _all = _get_parameter_help_opt(param, ctx, formatter)

    _metavar_padded = None
    if any(i in columns for i in ["opt_all_metavar", "opt_long_metavar"]):
        _metavar_padded = _get_parameter_metavar(param, ctx, formatter, append=False)

    def _opt_all_metavar() -> Optional[RenderableType]:
        if _metavar_padded is None:
            return _all
        if _all is None:
            return _metavar_padded
        return Text(" ", style=formatter.config.style_option_help).join([_all, _metavar_padded])

    def _opt_long_metavar() -> Optional[RenderableType]:
        if _metavar_padded is None:
            return _long
        if _long is None:
            return _metavar_padded
        return Text(" ", style=formatter.config.style_option_help).join([_long, _metavar_padded])

    column_callbacks: Dict["OptionColumnType", Callable[..., Any]] = {
        "required": _get_parameter_help_required_short,
        "opt_long": lambda *args, **kwargs: _long,
        "opt_short": lambda *args, **kwargs: _short,
        "opt_primary": lambda *args, **kwargs: _primary,
        "opt_secondary": lambda *args, **kwargs: _secondary,
        "opt_all": lambda *args, **kwargs: _all,
        "metavar": _get_parameter_help_metavar_col,
        "opt_all_metavar": lambda *args, **kwargs: _opt_all_metavar(),
        "opt_long_metavar": lambda *args, **kwargs: _opt_long_metavar(),
        "help": lambda *args, **kwargs: (
            param.get_rich_help(ctx, formatter)
            if isinstance(param, RichParameter)
            else get_help_parameter(param, ctx, formatter)
        ),
        "default": lambda *args, **kwargs: None,
        "envvar": lambda *args, **kwargs: None,
    }

    cols: RichPanelRow = []
    for col in columns:
        cols.append(column_callbacks[col](param, ctx, formatter))

    return cols


def _make_command_help(
    help_text: str, formatter: RichHelpFormatter, deprecated: Union[bool, str]
) -> Union[Text, "Markdown", Columns]:
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
    renderable: Union[Text, "Markdown", Columns]
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
                config.padding_header_text,
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
            formatter.config.padding_usage,
        ),
    )


def get_rich_help_text(self: click.core.Command, ctx: RichContext, formatter: RichHelpFormatter) -> None:
    """Write rich help text to the formatter if it exists."""
    # Print command / group help if we have some
    if self.help:
        # Print with some padding
        formatter.write(
            Padding(
                Align(_get_help_text(self, formatter), pad=False),
                formatter.config.padding_helptext,
            )
        )


def get_rich_epilog(
    self: click.core.Command,
    ctx: RichContext,
    formatter: RichHelpFormatter,
) -> None:
    """Richly render a click Command's epilog if it exists."""
    if self.epilog:
        # Remove single linebreaks, replace double with single
        lines = self.epilog.split("\n\n")
        if isinstance(self.epilog, JupyterMixin):  # Handles Text and Markdown
            epilog = self.epilog
        else:
            epilog = "\n".join([x.replace("\n", " ").strip() for x in lines])  # type: ignore[assignment]
            epilog = formatter.rich_text(epilog, formatter.config.style_epilog_text)  # type: ignore[assignment]
        formatter.write(Padding(Align(epilog, pad=False), formatter.config.padding_epilog))

    # Footer text if we have it
    if formatter.config.footer_text:
        formatter.write(
            Padding(
                formatter.rich_text(formatter.config.footer_text, formatter.config.style_footer_text),
                formatter.config.padding_footer_text,
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
                config.padding_errors_suggestion,
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
                config.padding_errors_suggestion,
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
                config.padding_errors_panel,
            )
        )
    if config.errors_epilogue:
        formatter.write(Padding(config.errors_epilogue, config.padding_errors_epilogue))
