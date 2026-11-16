# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click


@click.group()
@click.option("--type", required=True, help="Type of file to sync")
@click.option("--debug", is_flag=True, help="Show the debug log messages")
@click.command_panel("Main usage", commands=["sync", "download"])
@click.command_panel("Configuration", commands=["config", "auth"])
def cli(type, debug):
    """Synchronise all your files between two places."""


@cli.command()
def sync():
    """Synchronise all your files."""


@cli.command()
def download():
    """Pretend to download some files."""


@cli.command()
def config():
    """Set up the configuration."""


@cli.command()
def auth():
    """Authenticate the app."""


if __name__ == "__main__":
    cli(prog_name="sync-tool")
