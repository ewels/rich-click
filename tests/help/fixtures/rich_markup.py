import rich_click as click


# Use Rich markup
click.rich_click.USE_RICH_MARKUP = True


@click.command
@click.option(
    "--input",
    type=click.Path(),
    help=r"Input [magenta bold]file[/]. [dim]\[default: a custom default][/]",
)
@click.option(
    "--type",
    default="files",
    show_default=True,
    help="Type of file to sync",
)
@click.option("--all", is_flag=True, help="Sync all the things?")
@click.option("--debug", is_flag=True, help="Enable :point_right: [yellow]debug mode[/] :point_left:")
def cli(input: str, type: str, all: bool, debug: bool) -> None:
    """
    My amazing tool does [black on blue]all the things[/].

    This is a [u]minimal example[/] based on documentation
    from the [link=https://click.palletsprojects.com/]'click' package[/].

    [i]You can try using --help at the top level and also for
    specific group subcommands.[/]
    """
    print(f"Debug mode is {'on' if debug else 'off'}")


if __name__ == "__main__":
    cli()
