# /// script
# dependencies = ["rich-click>=1.9", "typer>=0.15"]
# ///

# This example comes from the Typer docs:
# https://typer.tiangolo.com/tutorial/commands/help/#help-panels-for-commands
import typer


cli = typer.Typer(rich_markup_mode="markdown")


@cli.command(rich_help_panel="Utils and Configs")
def config(configuration: str) -> None:
    """`Configure` the system. :wrench:"""
    print(f"Configuring the system with: {configuration}")


@cli.command(rich_help_panel="Utils and Configs")
def sync() -> None:
    """**Synchronize** the system or something fancy like that. :recycle:"""
    print("Syncing the system")


@cli.command(rich_help_panel="Help and Others")
def help() -> None:
    """Get _help_ with the system. :question:"""
    print("Opening help portal...")


@cli.command(rich_help_panel="Help and Others")
def report() -> None:
    """***Report*** an issue. :bug:"""
    print("Please open a new issue online, not a direct message")


if __name__ == "__main__":
    cli()
