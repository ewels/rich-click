# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.group()
@click.option("--env", help="Environment")
@click.option("--log-level", help="Log level")
def cli(env, log_level):
    """A tool with options and subcommands"""

@cli.command()
def move_item():
    """Move an item from a src location to a dest location"""

if __name__ == "__main__":
    cli()
