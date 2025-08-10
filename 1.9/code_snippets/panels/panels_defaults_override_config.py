# /// script
# dependencies = ["rich-click>=1.9.0dev0"]
# ///
import rich_click as click

@click.command()
@click.argument("src", help="Source", panel="[u b]Main[/]")
@click.argument("dest", help="Destination", panel="[u b]Main[/]")
@click.option("--env", help="Environment", panel="[u b]Extra[/]")
@click.option("--log-level", help="Log level", panel="[u b]Extra[/]")
@click.help_option(panel="[u b]Extra[/]")
@click.version_option("1.2.3", panel="[u b]Extra[/]")
@click.option_panel("[u b]Main[/]")
@click.option_panel("[u b]Extra[/]",
                    panel_styles={"border_style": "blue"})
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
