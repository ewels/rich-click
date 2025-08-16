import rich_click as click
from rich.text import Text


# Note: This won't render unless rc.TEXT_MARKUP = "rich"
@click.group()
@click.option("--debug/--no-debug", default=False)
@click.rich_config(help_config={"header_text": "[magenta]Welcome to my CLI![/]", "text_markup": "rich"})
def cli(debug: bool) -> None:
    """My amazing tool does all the things."""
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.rich_config(help_config={"header_text": Text("Welcome to my CLI! (with Text())"), "text_markup": "rich"})
def subcommand() -> None:
    """Subcommand help text"""
    pass


if __name__ == "__main__":
    cli()
