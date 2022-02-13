import rich_click as click

# The rest of the code is vanilla click usage
@click.group()
@click.option("--debug/--no-debug", "-d/-n", default=False, help="Enable debug mode")
def cli(debug):
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific group subcommands.
    """
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.option("--all", is_flag=True, help="Sync all the things?")
def sync():
    """Synchronise all your files between two places"""
    click.echo("Syncing")


@cli.command()
@click.option("--all", is_flag=True, help="Get everything")
def download():
    """Pretend to download some files from somewhere"""
    click.echo("Downloading")


if __name__ == "__main__":
    cli()
