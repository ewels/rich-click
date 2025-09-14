# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.command()
@click.option("--src")
@click.option("--dest")
@click.option("--env")
@click.option("--log-level")
@click.option_panel("Options",
                    help="All of the options available",
                    help_style="green",
                    panel_styles={"box": "DOUBLE"},
                    table_styles={
                        "row_styles": ["dim on rgb(16,16,32)", "on rgb(32,32,72)"],
                        "caption": "The arguments are optional"
                    })
@click.rich_config({"color_system": "truecolor"})
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
