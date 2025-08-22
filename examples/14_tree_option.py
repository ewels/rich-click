import rich_click as click
from rich_click import RichGroup, RichCommand

# click.tree_option()

# Define the CLI as RichGroup with configuration
@click.group(
    cls=RichGroup,
    context_settings={"tree_option_names": ["--tree","-h"]},
    name="demo",
    help="This CLI provides commands to handle various tasks with subcommands for specific actions.",
)
def cli():
    pass

# First subgroup (config propagated automatically)
@click.group(
    cls=RichGroup,
    context_settings={"tree_option_names": ["--tree","-h"]},
    name="user",
    help="Manage user-related operations.",
)
def user():
    pass

cli.add_command(user)

# Sub-subgroup under user
@click.group(
    cls=RichGroup,
    context_settings={"tree_option_names": ["--tree","-h"]},
    name="manage",
    help="Manage user settings and permissions.",
)
def manage():
    pass

user.add_command(manage)

# Subcommand under manage (third layer)
@click.command(name="set-role", cls=RichCommand)
@click.argument("role", type=str)
@click.argument("user_id", type=str)
@click.argument("reason", type=str)
@click.option(
    "--user-id",
    "-u",
    help="User ID to set role for (unspecified if not provided), where the help is really really long to test the wrapping of the lines in the CLI even if the terminal width is really wide it still tests it because it is just so very very long.",
)
@click.option(
    "--reason",
    "-r",
    help="Reason for setting the role",
)
def set_role(role, user_id, reason):
    """Set a role for a user."""
    click.echo(f"Setting role {role} for user ID {user_id or 'unspecified'}")
    if reason:
        click.echo(f"Reason: {reason}")

manage.add_command(set_role)

# Subcommand under manage (third layer)
@click.command(name="remove-role", cls=RichCommand)
@click.argument("role", type=str)
@click.argument("user_id", type=str)
def remove_role(role, user_id):
    """Remove a role from a user."""
    click.echo(f"Removing role {role} for user {user_id}")

manage.add_command(remove_role)

# Subcommand for user group
@click.command(name="add", cls=RichCommand)
@click.argument("name", type=str)
@click.option("--email", "-e", help="Email address of the user")
def add_user(name, email):
    """Add a new user to the system."""
    click.echo(f"Adding user: {name}")
    if email:
        click.echo(f"Email: {email}")

user.add_command(add_user)

# Subcommand for user group
@click.command(name="list", cls=RichCommand)
def list_users():
    """List all users in the system."""
    click.echo("Listing all users...")

user.add_command(list_users)

# Second subgroup (no subcommands to test robustness)
@click.group(
    cls=RichGroup,
    name="project",
    help="Manage project-related operations.",
)
def project():
    pass

cli.add_command(project)

# Standalone command (to test robustness)
@click.command(name="info", cls=RichCommand)
@click.option("--verbose", "-v", is_flag=True, help="Show detailed information.")
def info(verbose):
    """Display CLI information."""
    click.echo("CLI Information")
    if verbose:
        click.echo("Detailed mode enabled.")

cli.add_command(info)

# Define permissions group under manage
@click.group(
    cls=RichGroup,
    context_settings={"tree_option_names": ["--tree","-h"]},
    name="permissions",
    help="Manage user permissions.",
)
def permissions():
    pass

manage.add_command(permissions)

# Define set group under permissions
@click.group(
    cls=RichGroup,
    context_settings={"tree_option_names": ["--tree","-h"]},
    name="set",
    help="Manage user permissions.",
)
def set_permissions():
    pass

permissions.add_command(set_permissions)

# Add command under set
@click.command(name="add", cls=RichCommand)
@click.argument("user_id", type=str)
@click.argument("permission", type=str)
def add_permission(user_id, permission):
    """Add a permission for a user."""
    click.echo(f"Adding permission {permission} for user {user_id}")

set_permissions.add_command(add_permission)

if __name__ == "__main__":
    cli()


