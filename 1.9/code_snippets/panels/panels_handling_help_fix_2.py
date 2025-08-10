# /// script
# dependencies = ["rich-click>=1.9.0dev0"]
# ///
import rich_click as click

# Explicitly define the help_option() and set its panel.
@click.command()
@click.option("--src", panel="Main")
@click.option("--dest", panel="Main")
@click.option("--env", panel="Extra")
@click.option("--log-level", panel="Extra")
@click.help_option(panel="Extra")
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
