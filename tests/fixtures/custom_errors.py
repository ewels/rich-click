from click import UsageError

import rich_click as click

# Show custom error messages
click.rich_click.STYLE_ERRORS_SUGGESTION = "magenta italic"
click.rich_click.ERRORS_SUGGESTION = "Try running the '--help' flag for more information."
click.rich_click.ERRORS_EPILOGUE = "To find out more, visit [link=https://mytool.com]https://mytool.com[/link]"


@click.command()
@click.argument("input", type=click.Path(), required=True)
@click.option(
    "--type",
    default="files",
    show_default=True,
    help="Type of file to sync",
)
@click.option("--all", is_flag=True, help="Sync all the things?")
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode")
def cli(input: str, type: str, all: bool, debug: bool) -> None:
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific group subcommands.
    """
    raise UsageError("Invalid usage")


if __name__ == "__main__":
    cli()
