# /// script
# dependencies = ["rich-click>=1.9.0dev0"]
# ///
import rich_click as click

# Even though `commands_before_options` is True,
# the panel order is being explicitly defined by the decorators,
# and thus the `commands_before_options` config option is ignored.
@click.group()
@click.option_panel("Options")
@click.command_panel("Commands")
@click.rich_config({"commands_before_options": True})
def cli():
    """CLI help text"""
    pass

if __name__ == "__main__":
    cli()
