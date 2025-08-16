from typing import Any

import rich_click as click

# We assert the correct sort order via manually sorting
# in a way that would break if we did something like
# e.g. sort alphanumerically by name.


@click.group()
@click.command_panel(
    "Custom Command Panel 2",
    # Order should be preserved
    commands=["cmd2", "cmd1"],
)
@click.command_panel(
    "Custom Command Panel 1",
    # Order should be preserved
    commands=["cmd3", "cmd4"],
)
@click.command_panel(
    "Custom Command Panel 3",
    # Order should be preserved
    commands=["cmd5", "cmd6", "cmd7", "cmd8", "cmd9", "cmd10"],
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


@cli.group()
@click.option("--a")
@click.command_panel("Commands")
@click.option_panel("Options")
def cmd5(*args: Any, **kwargs: Any) -> None:
    """
    Test that commands appear above options when explicitly set.
    """


@cli.group()
@click.option("--a")
@click.option_panel("Options")
@click.command_panel("Commands")
@click.rich_config({"commands_before_options": True})
def cmd6(*args: Any, **kwargs: Any) -> None:
    """
    Test that options appear above commands when explicitly set,
    ignoring the `commands_before_options` config option.
    """


@cli.group()
@click.argument("a")
@click.option("--b")
@click.rich_config({"show_arguments": True})
def cmd7(*args: Any, **kwargs: Any) -> None:
    """
    Test that default order is arguments -> options -> commands.
    """


@cli.group()
@click.argument("a")
@click.option("--b")
@click.rich_config({"commands_before_options": True, "show_arguments": True})
def cmd8(*args: Any, **kwargs: Any) -> None:
    """
    Test that default order is commands -> arguments -> options, when
    commands show above options.
    """


@cli.group()
@click.option("--samename", "samename", panel="Custom Opt Panel")
@click.option("--dummy", panel="Custom Opt Panel")
def cmd9(*args: Any, **kwargs: Any) -> None:
    """
    Test that command and option both having the same name
    doesn't cause any issues. Also test that commands render by
    assigned name in dict, not by the cmd.name.
    """


@cli.group()
@click.option("--foo", panel="Generic Panel")
@click.option("--bar", panel="Generic Panel")
@click.command_panel("Generic Panel", commands=["dummy"])
def cmd10(*args: Any, **kwargs: Any) -> None:
    """
    Test that command panel and option panel both having the same name
    doesn't cause any issues.
    """


@click.command()
def dummy() -> None:
    pass


cmd5.add_command(dummy)
cmd6.add_command(dummy)
cmd7.add_command(dummy)
cmd8.add_command(dummy)
cmd9.add_command(dummy, name="samename")
cmd10.add_command(dummy)


if __name__ == "__main__":
    cli()
