# /// script
# dependencies = ["rich-click>=1.9.0dev1"]
# ///
import rich_click as click

@click.command()
@click.option("--src", panel="Main")
@click.option("--dest", panel="Main")
@click.option("--env", panel="Extra")
@click.option("--log-level", panel="Extra")
@click.help_option(panel="Extra")
@click.version_option("1.2.3", panel="Extra")
@click.option_panel("Main", table_styles={"row_styles": ["on grey0", "on grey11"]})
@click.option_panel("Extra",
                    help="Extra options available to the user:",
                    help_style="blue",
                    panel_styles={"box": "DOUBLE"},
                    table_styles={"row_styles": ["on grey0", "on grey11"], "caption": "Optional"})
@click.rich_config({"style_options_panel_border": "dim blue"})
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
