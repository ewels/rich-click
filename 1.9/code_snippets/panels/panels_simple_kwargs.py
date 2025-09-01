# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.command()
@click.option("--src", panel="Main", help="Source")
@click.option("--dest", panel="Main", help="Destination")
@click.option("--env", panel="Extra", help="Environment")
@click.option("--log-level", panel="Extra", help="Log level")
@click.help_option(panel="Extra")
@click.version_option("1.2.3", panel="Extra")
@click.rich_config({"style_options_panel_border": "dim blue"})
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
