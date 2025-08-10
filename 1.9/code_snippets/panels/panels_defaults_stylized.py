# /// script
# dependencies = ["rich-click>=1.9.0dev0"]
# ///
import rich_click as click

# TODO: Some behaviors here need to be fixed up.
#   - defining Arguments needs to render it.
#   - setting panel="Arguments" for argument needs to only
#     render the explicitly defined ones.
@click.command()
@click.argument("src")
@click.argument("dest")
@click.option("--env", help="Environment")
@click.option("--log-level", help="Log level")
@click.option_panel("Arguments")
@click.option_panel("Options",
                    panel_styles={"border_style": "dim blue"})
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
