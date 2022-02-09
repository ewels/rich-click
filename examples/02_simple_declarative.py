import click
import rich_click


class RichClickGroup(click.Group):
    def format_help(self, ctx, formatter):
        rich_click.rich_format_help(self, ctx, formatter)


class RichClickCommand(click.Command):
    def format_help(self, ctx, formatter):
        rich_click.rich_format_help(self, ctx, formatter)


@click.group(cls=RichClickGroup)
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific group subcommands.
    """
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command(cls=RichClickCommand)
def sync():
    """Synchronise all your files between two places"""
    click.echo("Syncing")


if __name__ == "__main__":
    cli()
