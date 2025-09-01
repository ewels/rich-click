# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.command()
@click.argument("src", help="Source")
@click.argument("dest", help="Destination")
@click.option("--env", help="Environment")
@click.option("--log-level", help="Log level")
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
