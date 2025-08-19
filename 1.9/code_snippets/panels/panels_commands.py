# /// script
# dependencies = ["rich-click>=1.9.0dev1"]
# ///
import rich_click as click

@click.group()
@click.command_panel("Items",
                     commands=["move-item", "update-item"])
@click.command_panel("Users",
                     commands=["create-user", "update-user"],
                     help="User management commands")
def cli():
    """CLI"""
    pass

@cli.command()
def move_item():
    """Move an item"""
    pass

@cli.command()
def update_item():
    """Update an item"""
    pass

@cli.command()
def create_user():
    """Create a user"""
    pass

@cli.command()
def update_user():
    """Update a user"""
    pass

if __name__ == "__main__":
    cli()
