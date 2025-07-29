import rich_click as click


@click.command(no_args_is_help=True)
@click.version_option(version="1.2.3")
def cli() -> None:
    """
    My amazing tool does all the things.
    """


if __name__ == "__main__":
    cli()
