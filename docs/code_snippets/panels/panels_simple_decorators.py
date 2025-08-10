# /// script
# dependencies = ["rich-click>=1.9.0dev0"]
# ///
import rich_click as click

@click.command()
@click.option("--src", help="Source")
@click.option("--dest", help="Destination")
@click.option("--env", help="Environment")
@click.option("--log-level", help="Log level")
@click.version_option("1.2.3")
@click.option_panel("Main",
                    options=["--src", "--dest"])
@click.option_panel("Extra",
                    options=["--env", "--log-level", "--help", "--version"])
@click.rich_config({"style_options_panel_border": "dim blue"})
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
