# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.group()
@click.option("--config", "-c", required=True, type=click.Path(), help="Config file")
@click.option("--verbose", is_flag=True, help="Be loud", panel="Logging")
@click.command_panel("Core", commands=["run", "a-much-longer-name"])
@click.command_panel("Extras", commands=["tidy"])
def cli():
    """Every panel lines up with every other panel"""

@cli.command()
def run():
    """Run the thing"""

@cli.command("a-much-longer-name")
def other():
    """Do something else"""

@cli.command()
def tidy():
    """Tidy up"""

if __name__ == "__main__":
    cli()
