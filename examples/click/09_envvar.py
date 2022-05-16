import rich_click as click

# import click

# Example test usage:
# GREETER_DEBUG=1 GREETER_GREET_USERNAME="test" EMAIL_ADDRESS="foo@bar.com" python examples/click/09_envvar.py greet


@click.group()
@click.option("--debug/--no-debug")
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.option("--username", help="This can be set via env var GREETER_GREET_USERNAME", show_envvar=True)
@click.option(
    "--nickname",
    envvar="NICKNAME",
    show_envvar=True,
    show_default=True,
    help="This can be set via env var NICKNAME",
)
@click.option(
    "--email",
    envvar=["EMAIL", "EMAIL_ADDRESS"],
    show_envvar=True,
    default="foo@bar.com",
    show_default=True,
    help="This can be set via env var EMAIL or EMAIL_ADDRESS",
)
def greet(username, nickname, email):
    click.echo(f"Hello {username} ({nickname}) with email {email}!")


if __name__ == "__main__":
    cli(auto_envvar_prefix="GREETER")
