import rich_click as click


# Use Markdown (bit of a ridiculous example!)
click.rich_click.USE_MARKDOWN = True


@click.command()
@click.option("--input", type=click.Path(), help="Input **file**. _[default: a custom default]_")
@click.option(
    "--type",
    default="files",
    show_default=True,
    help="Type of file to sync",
)
@click.option("--all", is_flag=True, help="Sync\n 1. all\n 2. the\n 3. things?")
@click.option("--debug", is_flag=True, help="# Enable `debug mode`")
def cli(input: str, type: str, all: bool, debug: bool) -> None:
    """
    My amazing tool does _**all the things**_.

    This is a `minimal example` based on documentation from the [_click_ package](https://click.palletsprojects.com/).

    > Remember:
    >  - You can try using --help at the top level
    >  - Also for specific group subcommands.

    """
    print(f"Debug mode is {'on' if debug else 'off'}")


if __name__ == "__main__":
    cli()
