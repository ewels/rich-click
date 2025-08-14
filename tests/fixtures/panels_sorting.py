from typing import Any

import rich_click as click

# We assert the correct sort order via manually sorting
# in a way that would break if we did something like
# e.g. sort alphanumerically by name.


@click.group()
@click.command_panel(
    "Custom Command Panel 1",
    # Order should be preserved
    commands=["cmd2", "cmd1"],
)
@click.command_panel(
    "Custom Command Panel 2",
    # Order should be preserved
    commands=["cmd3", "cmd4"],
)
def cli() -> None:
    """CLI help text"""


@cli.command()
@click.option("--a", "-a", panel="Custom 2", help="Help text for A")
@click.option("--b", "-b", panel="Custom 1", help="Help text for B")
@click.option("--c", "-c", panel="Custom 2", help="Help text for C")
@click.option("--f", "-f", panel="Custom 3", help="Help text for F")
@click.option("--e", "-e", panel="Custom 1", help="Help text for E")
@click.option("--d", "-d", panel="Custom 3", help="Help text for E")
def cmd1(*args: Any, **kwargs: Any) -> None:
    """Test order of panels is preserved via panel=..."""


@cli.command()
@click.option("--a", "-a", panel="Custom 1", help="Help text for A")
@click.option("--b", "-b", panel="Custom 1", help="Help text for B")
@click.option("--d", "-d", panel="Custom 2", help="Help text for D")
@click.option("--c", "-c", panel="Custom 2", help="Help text for C")
@click.option("--f", "-f", panel="Custom 3", help="Help text for F")
@click.option("--e", "-e", panel="Custom 3", help="Help text for E")
def cmd2(*args: Any, **kwargs: Any) -> None:
    """Test order of options is preserved via panel..."""


@cli.command()
@click.option("--a", "-a", help="Help text for A")
@click.option("--b", "-b", help="Help text for B")
@click.option("--c", "-c", help="Help text for C")
@click.option("--d", "-d", help="Help text for D")
@click.option("--e", "-e", help="Help text for E")
@click.option("--f", "-f", help="Help text for F")
@click.option_panel("Panel 2", options=["--a", "--b"])
@click.option_panel("Panel 1", options=["--c", "--d"])
@click.option_panel("Panel 3", options=["--e", "--f"])
def cmd3(*args: Any, **kwargs: Any) -> None:
    """Test order of panels is preserved via option_panel()"""


@cli.command()
@click.option("--a", "-a", help="Help text for A")
@click.option("--b", "-b", help="Help text for B")
@click.option("--c", "-c", help="Help text for D")
@click.option("--d", "-d", help="Help text for C")
@click.option("--e", "-f", help="Help text for F")
@click.option("--f", "-e", help="Help text for E")
@click.option_panel("Panel 1", options=["-a", "--b"])
@click.option_panel("Panel 2", options=["--d", "-c"])
@click.option_panel("Panel 3", options=["f", "--e"])
def cmd4(*args: Any, **kwargs: Any) -> None:
    """Test order of options is preserved via option_panel()"""


if __name__ == "__main__":
    cli()
