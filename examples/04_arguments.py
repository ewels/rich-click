import rich_click as click

# Show the positional arguments
click.rich_click.SHOW_ARGUMENTS = True

# Uncomment this line to group the arguments together with the options
# click.rich_click.GROUP_ARGUMENTS_OPTIONS = True

# Move the metavars to after the help text
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True


@click.command()
@click.argument("input", required=True)
@click.option(
    "--type",
    default="files",
    show_default=True,
    help="Type of file to sync",
)
@click.option("--all", is_flag=True, help="Sync all the things?")
@click.option("--debug/--no-debug", "-d/-n", default=False, help="Enable debug mode")
def cli(debug):
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific group subcommands.
    """
    print(f"Debug mode is {'on' if debug else 'off'}")


if __name__ == "__main__":
    cli()
