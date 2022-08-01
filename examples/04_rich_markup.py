import rich_click as click

# Use Rich markup
click.rich_click.USE_RICH_MARKUP = True


@click.command()
@click.option(
    "--input",
    type=click.Path(),
    help="Input [magenta bold]file[/]. [dim]\[default: a custom default][/]",
)
@click.option(
    "--type",
    default="files",
    show_default=True,
    help="Type of file to sync",
)
@click.option("--all", is_flag=True, help="Sync all the things?")
@click.option(
    "--debug/--no-debug",
    "-d/-n",
    default=False,
    help="Enable :point_right: [yellow]debug mode[/] :point_left:",
)
def cli(input, type, all, debug):
    """
    My amazing tool does [black on blue] all the things [/].

    This is a [u]minimal example[/] based on documentation
    from the [link=https://click.palletsprojects.com/]'click' package[/].

    [i]You can try using --help at the top level and also for
    specific group subcommands.[/]
    """
    print(f"Debug mode is {'on' if debug else 'off'}")


if __name__ == "__main__":
    cli()
