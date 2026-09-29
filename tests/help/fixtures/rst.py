import rich_click as click


@click.command(
    epilog="""
See the `rich-click docs <https://ewels.github.io/rich-click/>`_ for more.

- Epilog lists
- stay intact
""",
)
@click.rich_config(help_config={"text_markup": "rst"})
@click.option("--input", type=click.Path(), help="Input **file**. *[default: a custom default]*")
@click.option(
    "--type",
    default="files",
    show_default=True,
    help="Type of file to sync",
)
@click.option("--all", is_flag=True, help="Sync\n\n1. all\n2. the\n3. things?")
@click.option("--debug", is_flag=True, help="Enable ``debug mode``")
def cli(input: str, type: str, all: bool, debug: bool) -> None:
    """
    My amazing tool does *all the things*.

    This is a ``minimal example`` based on documentation
    from the `click package <https://click.palletsprojects.com/>`_.

    - You can try using ``--help`` at the top level
    - Also for specific group subcommands.

    .. note::
       Admonitions are rendered compactly.

    Example::

        $ cli --all --debug
    """
    print(f"Debug mode is {'on' if debug else 'off'}")


if __name__ == "__main__":
    cli()
