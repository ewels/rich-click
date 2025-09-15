# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

# 'Main' panel: uses default title style "bright_red"
# 'Extra' panel: title style is overridden to use "blue"

@click.command()
@click.argument("src", help="Source", panel="Main")
@click.argument("dest", help="Destination", panel="Main")
@click.option("--env", help="Environment", panel="Extra")
@click.option("--log-level", help="Log level", panel="Extra")
@click.help_option(panel="Extra")
@click.option_panel("Main")
@click.option_panel("Extra", title_style="blue")
@click.rich_config({
    "theme": "plain",
    "style_options_panel_title_style": "bright_red"  # <- default title style
})
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
