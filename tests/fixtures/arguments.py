import rich_click as click


# click.rich_click.SHOW_ARGUMENTS = True
# click.rich_click.GROUP_ARGUMENTS_OPTIONS = True


@click.command()
@click.argument("input", type=click.Path(), required=True)
@click.argument("output", type=click.Path())
@click.option("--type", default="files", show_default=True, help="Type of file to sync")
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
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
    input: str,
    output: str,
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
    print(f"Input: {input}")
    print(f"Output: {output}")
    print(f"Environment: {environment}")
    print(f"Debug mode is {'on' if debug else 'off'}")
    print(f"Syncing files of type {type}")


if __name__ == "__main__":
    cli()
