# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

# Explicitly define the panels and place --help in Extra:
@click.command()
@click.option("--src", panel="Main")
@click.option("--dest", panel="Main")
@click.option("--env", panel="Extra")
@click.option("--log-level", panel="Extra")
@click.option_panel("Main")
@click.option_panel("Extra", options=["--env", "--log-level", "--help"])
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
