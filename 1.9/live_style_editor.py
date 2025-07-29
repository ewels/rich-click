import rich_click as click


@click.group("my-command")
@click.argument("foo")
@click.option("--bar", "-b", help="Lorem ipsum", show_default="someval")
@click.option("--baz", required=True, help="Choose wisely", type=click.Choice(["a", "b", "c"]))
def cli(foo, bar, baz):
    """
    Help text for CLI

    Second line of help text.
    """


@cli.command("subcommand")
def subcommand(foo, bar):
    """Help text for subcommand"""


if __name__ == "__main__":
    # TERMINAL_WIDTH=72 rich-click docs.live_style_editor:cli --help
    cli()
