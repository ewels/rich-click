# /// script
# dependencies = ["rich-click>=1.9.0dev1"]
# ///
import rich_click as click
from rich_click import RichContext, RichHelpFormatter


class SpecialGrp(click.RichGroup):
    def format_help(self, ctx: RichContext, formatter: RichHelpFormatter) -> None:
        self.format_options(ctx, formatter)

@click.group(cls=SpecialGrp)
@click.option("--env", help="Environment")
@click.option("--log-level", help="Log level")
# @click.option_panel("Additional Options",
#                     panel_styles={"border_style": "dim blue"})
# @click.command_panel("Subcommands",
#                      panel_styles={"border_style": "dim magenta"})
@click.rich_config({
    # "arguments_panel_title": "Required Args",
    # "options_panel_title": "Additional Options",
    # "commands_panel_title": "Subcommands",
    # "show_arguments": True
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
