import rich_click.typer as typer

# import typer

app = typer.Typer()


@app.callback()
def cli(
    debug: bool = typer.Option(False, help="Enable debug mode."),
    envvar_ex: str = typer.Option("baz", "--bar", help="Lorep ipsum.", envvar="FOO"),
):
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific group subcommands.
    """
    print(f"Debug mode is {'on' if debug else 'off'} - {envvar_ex}")


if __name__ == "__main__":
    app()
