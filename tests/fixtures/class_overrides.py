from typing import Any

import rich_click as click


@click.group()
@click.command_panel(
    "Rich Click Panel",
    commands=["click_command", "click_options"],
)
def cli() -> None:
    """
    Test that command is assigned to panel even if it's not a RichCommand.

    (Also test that callback name identifies a command, not just the name of the command.)
    """


@cli.command("click-command", cls=click.Command)
@click.argument("rich-click-arg", help="Arg help text here", panel="Panel Assignment")
@click.option("--rich-click-option", panel="Panel Assignment")
@click.help_option()
def click_command() -> None:
    """Test that RichParameters can be used with base click Commands."""


@cli.command()
@click.argument("click-arg", cls=click.Argument)
@click.option(
    "--click-option",
    cls=click.Option,
    help="This is help text for a click.Option().",
    default="foo",
    required=True,
    show_default=True,
    envvar="CLICK_OPTION",
    show_envvar=True,
)
@click.option_panel("Rich Click Panel", options=["click-arg", "--click-option"])
def click_options(*args: Any, **kwargs: Any) -> None:
    """Test that options+arguments are assigned to the panel even if they're not RichParameters."""


if __name__ == "__main__":
    cli()
