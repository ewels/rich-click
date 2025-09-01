# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.command(epilog="[blue]For more information, read the docs[/blue]")
@click.option("--foo", "-f", help="[green]foo[/]")
@click.option("--bar", "-b", help="[default on green]bar[/]")
@click.option_panel("Options",
                    help="[magenta not dim]These are [bold]all[/b] the options available.[/]")
@click.rich_config({"text_markup": "rich"})
def cli():
    """CLI for my [red]app[/red].

    This is a demonstration of
    [#FF6B6B bold]r[/][#FF8E53 bold]i[/][#FFB347 bold]c[/][#4ECDC4 bold]h[/]
    markup in CLI help text.
    """

if __name__ == "__main__":
    cli()
