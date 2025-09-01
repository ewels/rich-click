# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.command()
@click.argument("src", panel="Required Args")
@click.argument("dest", panel="Required Args")
@click.option("--env", help="Environment")
@click.option("--log-level", help="Log level")
@click.option_panel("Required Args",
                    panel_styles={"border_style": "dim red"})
@click.option_panel("Options")
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
