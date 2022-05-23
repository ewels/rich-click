import inspect
from io import StringIO
from typing import Any, Callable, cast, Iterable, Optional, Union

import click
from rich.console import Console

from rich_click.rich_click import _make_rich_rext


def echo(
    message: Optional[Any] = None,
    **kwargs: Any,
) -> None:
    """
    Echo text to the console with rich formatting.

    This is a wrapper around click.echo that supports rich text formatting.

    rich.print cannot be used directly as it doesn't work in all cases with pytest and click.testing.CliRunner()

    Args:
        message: The string or bytes to output. Other objects are converted to strings.
        kwargs: any extra arguments are passed to rich.console.Console.print() and click.echo
            if kwargs contains 'file', 'nl', 'err', 'color', these are passed to click.echo,
            all other values passed to rich.console.Console.print()
    """
    # args for click.echo that may have been passed in kwargs
    echo_args = {}
    for arg in ("file", "nl", "err", "color"):
        val = kwargs.pop(arg, None)
        if val is not None:
            echo_args[arg] = val

    # click.echo will include "\n" so don't add it here unless specified
    end = kwargs.pop("end", "")

    width = kwargs.pop("width", Console().width)
    output = StringIO()
    console = Console(force_terminal=True, file=output, width=width)
    message = _make_rich_rext(message)
    console.print(message, end=end, **kwargs)
    click.echo(output.getvalue(), **echo_args)


def echo_via_pager(
    text_or_generator: Union[Iterable[str], Callable[[], Iterable[str]], str],
    **kwargs,
) -> None:
    """Take a text and show it via an environment specific pager on stdout.

    Args:
        text_or_generator: the text to page, or alternatively, a generator emitting the text to page.
        **kwargs: if "color" in kwargs, works the same as click.echo_via_pager(color=color)
        otherwise any kwargs are passed to rich.Console.print()
    """
    if inspect.isgeneratorfunction(text_or_generator):
        text_or_generator = cast(Callable[[], Iterable[str]], text_or_generator)()
    elif isinstance(text_or_generator, str):
        text_or_generator = [text_or_generator]
    else:
        try:
            text_or_generator = iter(text_or_generator)
        except TypeError:
            text_or_generator = [text_or_generator]

    console = Console()

    color = kwargs.pop("color", None)
    if color is None:
        color = bool(console.color_system)

    with console.pager(styles=color):
        for x in text_or_generator:
            if isinstance(x, str):
                x = _make_rich_rext(x)
            console.print(x, **kwargs)
