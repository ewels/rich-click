import rich_click.typer as typer

app = typer.Typer()


@app.callback()
def cli(debug: bool = typer.Option(False, help="Enable debug mode.")):
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific group subcommands.
    """
    print(f"Debug mode is {'on' if debug else 'off'}")


@app.command()
def sync(
    type: str = typer.Option("files", help="Type of file to sync"),
    all: bool = typer.Option(False, help="Sync all the things?"),
):
    """Synchronise all your files between two places"""
    print("Syncing")


@app.command()
def download(all: bool = typer.Option(False, help="Get everything")):
    """
    Pretend to download some files from
    somewhere. Multi-line help strings are unwrapped
    until you use a double newline.

    Only the first paragraph is used in group help texts.
    Don't forget you can opt-in to rich and markdown formatting!

    \b
    Click escape markers should still work.
      * So you
      * Can keep
      * Your newlines

    And this is a paragraph
    that will be rewrapped again.

    \f
    Also if you want to write function help text that won't
    be rendered to the terminal.
    """
    print("Downloading")


if __name__ == "__main__":
    app()
