from typing import Any

import rich_click as click


@click.group()
@click.command_panel(
    "Custom Panel",
    help="This is help text for the command panel.",
    help_style="italic",
    commands=["subcommand"],
    table_styles={"caption": "Additional Commands"},
    panel_styles={"box": "SIMPLE"},
)
@click.command_panel("Ignore me")  # No commands assigned.
def cli() -> None:
    """Test basic styles for command panel."""


@cli.command()
@click.option("--a", "-a", panel="Custom Panel", help="Help text for A")
@click.option("--b", "-b", panel="Custom Panel", help="Help text for B")
@click.option("--c", "-c", panel="Custom Panel", help="Help text for C")
@click.option_panel(
    "Custom Panel",
    help="This is help text for the option panel.",
    help_style="italic",
    table_styles={"caption": "Additional Options"},
    panel_styles={"box": "SIMPLE"},
)
@click.option_panel("Ignore me")  # No commands assigned.
def subcommand(*args: Any, **kwargs: Any) -> None:
    """Test basic styles for option panel."""


if __name__ == "__main__":
    cli()
