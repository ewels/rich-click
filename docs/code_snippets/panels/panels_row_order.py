# /// script
# dependencies = ["rich-click>=1.9.0dev0"]
# ///
import rich_click as click

@click.command()
@click.option("--src", panel="Main")
@click.option("--dest", panel="Main")
@click.option("--env")
@click.option("--log-level")
@click.option_panel("Extra", options=["env", "log_level", "help"])
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
