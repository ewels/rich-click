import click
import rich_click

####
## Rich-click cli stuff
####
@rich_click.group()
@rich_click.option(
    "--debug/--no-debug", "-d/-n", default=False, help="Enable debug mode"
)
def cli(debug):
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific group subcommands.
    """
    print(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@rich_click.option("--all", is_flag=True, help="Sync all the things?")
def sync(all):
    """Synchronise all your files between two places"""
    print("Syncing")


@cli.command()
@rich_click.option("--all", is_flag=True, help="Get everything")
def download(all):
    """Pretend to download some files from somewhere"""
    print("Downloading")


####
## Vanilla click import cli stuff
####
@click.command()
@click.option("--all", is_flag=True, help="Sync all the things?")
def original(all):
    """Synchronise all your files between two places"""
    print("Syncing")


if __name__ == "__main__":
    cli()  # Use rich-click, should be fancy output
    # original()  # Use vanilla click, should be simple output
