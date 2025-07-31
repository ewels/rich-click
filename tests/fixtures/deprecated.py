import rich_click as click

click.rich_click.USE_MARKDOWN = True


@click.group()
@click.option(
    "--type", default="files", show_default=True, help="Type of file to sync", deprecated="All files will be synced"
)
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode", deprecated=True)
@click.option(
    "--environment",
    "-e",
    type=click.Choice(["dev", "staging", "prod"]),
    show_default="current",
    envvar="MY_ENV",
    show_envvar=True,
    help="Sync to what environment",
)
def cli(
    type: str,
    debug: bool,
    environment: str,
) -> None:
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific group subcommands.
    """


@cli.command(deprecated=True)
@click.option("--all", is_flag=True, help="Get everything")
def download(all: bool) -> None:
    """Pretend to download some files from _somewhere_."""
    print("Downloading")


@cli.command(deprecated="Removing in later version")
@click.option("--all", is_flag=True)
def sync(type: str, all: bool) -> None:
    """Synchronise all your files between two places.
    Example command that doesn't do much except print to the terminal."""
    print("Syncing")


if __name__ == "__main__":
    cli()
