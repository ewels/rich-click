import rich_click as click


@click.group()
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
@click.option(
    "--environment",
    "-e",
    type=click.Choice(["dev", "staging", "prod"]),
    envvar="MY_ENV",
    show_envvar=True,
    help="Sync to what environment",
)
def cli(
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
    print(f"Environment: {environment}")
    print(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.option("--files", default="*", show_default="All files", help="What files to download")
def download(files: str) -> None:
    """Download files"""
    print(f"Downloading {files}")


if __name__ == "__main__":
    cli()
