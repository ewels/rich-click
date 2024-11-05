# This is a fleshed-out application built with Click.
# (Except for the fact that it doesn't do anything!)
#
# Run the command `rich-click app:main --help` to render it with rich-click!
import logging

import click
from rich.logging import RichHandler

logger = logging.getLogger(__name__)
logger.addHandler(RichHandler())
logger.setLevel(logging.INFO)

@click.group("my-app")
@click.option("--environment", "-e",
              type=click.Choice(["production", "staging", "integration"]),
              default="production",
              show_default=True,
              help="Environment to run in.")
@click.version_option(version="1.0.1", prog_name="my-app")
def main(environment):
    """CLI for my-app"""
    logger.debug("Running in environment=%s", environment)


@main.command("deploy")
@click.argument("version")
@click.pass_context
def deploy(ctx, version):
    """Deploy my-app"""
    logger.info("Deploying version=%s in environment=%s", version, ctx.parent.params["environment"])

@main.group("user")
def user_cli():
    """Manage users to my-app"""

@user_cli.command("create")
@click.option("--email", "-e",
              required=True,
              help="User's email")
@click.password_option("--password", "-p",
                       required=True,
                       prompt=True,
                       help="User's password")
@click.option("--admin",
              is_flag=True,
              default=False,
              help="If flag is passed, give admin permissions")
@click.pass_context
def create(ctx, email, password, admin):
    """Create my-app users"""
    if len(password) < 6:
        logger.error("Password must be ≥ 6 characters")
        ctx.exit(1)
    logger.info("Creating user with email=%s admin=%s", email, admin)


@user_cli.command("delete")
@click.argument("user_id",
                type=click.INT)
def delete(user_id):
    """Delete my-app users"""
    click.confirm(click.style(f"Are you sure you want to delete user={user_id!r}?", fg="red"), abort=True)
    logger.info("Deleting user with user_id=%i", user_id)


if __name__ == "__main__":
    main()
