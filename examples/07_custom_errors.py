import rich_click as click

# Show custom error messages
click.rich_click.STYLE_ERRORS_SUGGESTION = "blue italic"
click.rich_click.ERRORS_SUGGESTION = "Try running the '--help' flag for more information."
click.rich_click.ERRORS_EPILOGUE = "To find out more, visit https://mytool.com"


@click.command()
@click.argument("input", type=click.Path(), required=True)
@click.option(
    "--type",
    default="files",
    show_default=True,
    help="Type of file to sync",
)
@click.option("--all", is_flag=True, help="Sync all the things?")
@click.option("--debug/--no-debug", "-d/-n", default=False, help="Enable debug mode")
def cli(input, type, all, debug):
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
