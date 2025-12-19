# /// script
# dependencies = ["rich-click>=1.9", "typer>=0.15"]
# ///

# This example comes from the Typer docs:
# https://typer.tiangolo.com/tutorial/commands/help/#help-panels-for-commands
import typer


cli = typer.Typer(rich_markup_mode="rich", no_args_is_help=True)


@cli.command()
def create(username: str) -> None:
    """[green]Create[/green] a new user. :sparkles:"""
    print(f"Creating user: {username}")


@cli.command()
def delete(username: str) -> None:
    """[red]Delete[/red] a user. :fire:"""
    print(f"Deleting user: {username}")


@cli.command(rich_help_panel="Utils and Configs")
def config(configuration: str) -> None:
    """[blue]Configure[/blue] the system. :wrench:"""
    print(f"Configuring the system with: {configuration}")


@cli.command(rich_help_panel="Utils and Configs")
def sync() -> None:
    """[blue]Synchronize[/blue] the system or something fancy like that. :recycle:"""
    print("Syncing the system")


@cli.command(rich_help_panel="Help and Others")
def help() -> None:
    """Get [yellow]help[/yellow] with the system. :question:"""
    print("Opening help portal...")


@cli.command(rich_help_panel="Help and Others")
def report() -> None:
    """[yellow]Report[/yellow] an issue. :bug:"""
    print("Please open a new issue online, not a direct message")


if __name__ == "__main__":
    cli()
