# /// script
# dependencies = ["rich-click>=1.9.0dev0"]
# ///
import rich_click as click

# This will explicitly set commands to be above options
# Merely defining the command panel or option panel alone will not do this.
# They both must be defined, and then commands must be set above options.
@click.group()
@click.command_panel("Commands")
@click.option_panel("Options")
def cli():
    """CLI help text"""
    pass

if __name__ == "__main__":
    cli()
