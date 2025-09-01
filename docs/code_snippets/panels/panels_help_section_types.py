# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.command()
@click.argument("src")
@click.argument("dest")
@click.option("--env",
              help="Environment",
              default="dev", show_default=True,
              envvar="ENV", show_envvar=True,
              required=True)
@click.option("--log-level",
              help="Log level",
              default="INFO", show_default=True,
              envvar="LOG_LEVEL", show_envvar=True,
              deprecated=True)
@click.option_panel("Arguments")
@click.option_panel("Options")
@click.rich_config({
    "options_table_column_types": ["opt_long", "opt_short", "help"],
    "options_table_help_sections": ["metavar", "required", "help", "default", "envvar"]
})
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
