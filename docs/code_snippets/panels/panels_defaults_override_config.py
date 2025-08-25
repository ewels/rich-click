# /// script
# dependencies = ["rich-click>=1.9.0dev1"]
# ///
import rich_click as click

@click.command()
@click.argument("src", help="Source", panel="Main")
@click.argument("dest", help="Destination", panel="Main")
@click.option("--env", help="Environment", panel="Extra")
@click.option("--log-level", help="Log level", panel="Extra")
@click.help_option(panel="Extra")
@click.version_option("1.2.3", panel="Extra")
@click.option_panel("Main", title_style="u b")
@click.option_panel("Extra",
                    panel_styles={"border_style": "blue"},
                    title_style="u b")
@click.rich_config({
    "style_options_panel_border": "bright_red",
    "style_options_panel_box": "SIMPLE",
    "style_option": "",
    "style_argument": "bright_red",
    "style_usage": "",
    "style_metavar": "dim"
})
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
