# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.group()
@click.option("--env", help="Environment")
@click.option("--log-level", help="Log level")
@click.option_panel("Some Additional Options",
                    panel_styles={"border_style": "dim blue"})
@click.command_panel("My Tool's Subcommands",
                     panel_styles={"border_style": "dim magenta"})
@click.rich_config({
    "arguments_panel_title": "Very Important Required Args",
    "options_panel_title": "Some Additional Options",
    "commands_panel_title": "My Tool's Subcommands",
    "show_arguments": True
})
def cli(env, log_level):
    """My CLI"""

@cli.command()
@click.argument("src")
@click.argument("dest")
def move_item(src, dest):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    cli()
