import rich_click as click  # [!annotate] Use in place of `import click`


@click.group()
@click.rich_config({"theme": "dracula-robo"})  # [!annotate] Any colour scheme with any format.
def cli():
    """My amazing tool does all the things."""


@cli.command(panel="Files")  # [!annotate] Group commands and options under headings.
@click.argument("src")
@click.option("--dest", help="Where to copy to.", panel="Main")
@click.option("--verbose", is_flag=True, panel="Extra")
def copy(src, dest, verbose):
    """Copy a file."""


@cli.command(panel="Users")
def login():
    """Log in to the server."""


if __name__ == "__main__":
    cli()
