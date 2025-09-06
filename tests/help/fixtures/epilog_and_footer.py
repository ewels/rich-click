from rich.text import Text

import rich_click as click


# Note: This won't render unless rc.TEXT_MARKUP = "rich"
@click.group(epilog="[bold green]For more information, visit our website.[/]")
@click.option("--debug/--no-debug", default=False)
@click.rich_config(help_config={"footer_text": "And here is some footer text!", "text_markup": "rich"})
def cli(debug: bool) -> None:
    """My amazing tool does all the things."""
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.rich_config(help_config={"footer_text": "This is [b]footer text[/]"})
def no_epilog() -> None:
    """no_epilog help text."""


@cli.command(epilog="This is [b]epilog text[/b]")
@click.rich_config(help_config={"footer_text": None})
def no_footer() -> None:
    """no_footer help text."""


@cli.command(epilog="This is [b]epilog text[/b]")
@click.rich_config(help_config={"footer_text": Text("Rich text footer")})
def footer_is_rich_text() -> None:
    """footer_is_rich_text help text."""


@cli.command(epilog=Text("Rich text epilog"))
@click.rich_config(help_config={"footer_text": None})
def epilog_is_rich_text() -> None:
    """epilog_is_rich_text help text."""


if __name__ == "__main__":
    cli()
