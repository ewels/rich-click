import rich_click


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
@rich_click.option(
    "--type",
    required=True,
    default="files",
    show_default=True,
    help="Type of file to sync",
)
@rich_click.option("--all", is_flag=True, help="Sync all the things?")
def sync(type, all):
    """Synchronise all your files between two places"""
    print("Syncing")


@cli.command()
@rich_click.option("--all", is_flag=True, help="Get everything")
def download(all):
    """Pretend to download some files from somewhere"""
    print("Downloading")


if __name__ == "__main__":
    cli()
