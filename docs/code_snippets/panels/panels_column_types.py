# /// script
# dependencies = ["rich-click>=1.9.0dev1"]
# ///
import rich_click as click

@click.command()
@click.option("--src", "-s", help="Source", type=click.STRING, panel="Main")
@click.option("--dest", "-d", help="Destination", type=click.STRING, panel="Main")
@click.option("--env", "-e", help="Environment", panel="Extra")
@click.option("--quiet/--no-quiet", "-q/-Q", help="Quiet logging", panel="Extra")
@click.help_option("--help", "-h", panel="Extra")
@click.option_panel("Main", column_types=["opt_short", "opt_long", "metavar", "help"])
@click.option_panel("Extra", column_types=["opt_primary", "opt_secondary", "metavar", "help"])
@click.rich_config({
    "delimiter_comma": ", ",
    "style_option_negative": "bold magenta",
    "style_switch_negative": "bold blue",
})
def move_item(src, dest, env, quiet):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
