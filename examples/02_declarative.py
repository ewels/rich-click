import click

from rich_click import RichCommand, RichGroup


@click.group(cls=RichGroup, 
             context_settings={"tree_option_names": ["--tree", "-h"]},)
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific group subcommands.
    """
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command(cls=RichCommand)
def sync():
    """Synchronise all your files between two places."""
    click.echo("Syncing")


if __name__ == "__main__":
    cli()
