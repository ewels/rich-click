from typing import Any

import rich_click as click

# We assert the correct sort order via manually sorting
# in a way that would break if we did something like
# e.g. sort alphanumerically by name.


@click.group()
@click.command_panel("Command Panel A", commands=["cmd4"])
@click.command_panel("Command Panel B", commands=["cmd5", "cmd6", "cmd7"], panel_styles={"box": "DOUBLE"})
# Default panel should sort commands alphanumerically
# Even if commands are defined in different order.
@click.rich_config({"commands_panel_title": "[b]Custom Default Command Panel[/]", "style_commands_panel_box": "SIMPLE"})
def cli() -> None:
    """CLI help text"""


@cli.command()
def cmd2() -> None:
    """cmd2 help"""


@cli.command()
def cmd1() -> None:
    """cmd1 help"""


@cli.command()
def cmd3() -> None:
    """cmd3 help"""


@cli.command()
@click.argument("arg1", help="arg1 help")
@click.argument("arg3")
@click.argument("arg2", help="arg2 help")
@click.rich_config({"arguments_panel_title": "Custom Args Panel Title"})
def cmd4(*args: Any, **kwargs: Any) -> None:
    """
    Test args assigned to arguments panel when help is defined,
    and test that arg3 is assigned to default even without help
    so long as panel shows.
    """


@cli.command()
@click.argument("arg")
@click.option("--a")
@click.option("--b")
@click.option("--c")
@click.rich_config(
    {
        "arguments_panel_title": "Custom Args Panel Title",
        "options_panel_title": "Custom Options Panel Title",
        "show_arguments": True,
    }
)
def cmd5(*args: Any, **kwargs: Any) -> None:
    """
    Test args and options assigned to respective panels.
    """


@cli.command()
@click.option("--a", panel="Panel 1")
@click.option("--b")
@click.option("--c", panel="Panel 2")
@click.option("--d", panel="Panel 3")
@click.help_option(panel="Help")
@click.option_panel("Help")
@click.option_panel("Panel 1")
@click.option_panel("Panel 2")
@click.option_panel("Custom Options Panel Title")
@click.option_panel("Panel 3")
@click.rich_config(
    {
        "options_panel_title": "Custom Options Panel Title",
    }
)
def cmd6(*args: Any, **kwargs: Any) -> None:
    """
    Test order is preserved and option is still assigned
    when default panel is explicitly defined and ordered.
    """


@cli.command()
@click.option("--a", panel="Panel 1")
@click.option("--b")
@click.option("--c", panel="Panel 2")
@click.option("--d", panel="Panel 3")
@click.help_option(panel="Help")
@click.option_panel("Help")
@click.option_panel("Panel 1")
@click.option_panel("Panel 2")
@click.option_panel("Custom Options Panel Title")
@click.option_panel("Panel 3")
@click.rich_config(
    {
        "options_panel_title": "Custom Options Panel Title",
    }
)
def cmd7(*args: Any, **kwargs: Any) -> None:
    """
    Test order is preserved and option is still assigned
    when default panel is explicitly defined and ordered.
    """


if __name__ == "__main__":
    cli()
