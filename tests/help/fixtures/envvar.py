import rich_click as click


@click.group(context_settings=dict(auto_envvar_prefix="GREETER"))
@click.option("--debug/--no-debug")
def cli(debug: bool) -> None:
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.option("--username", help="This can be set via env var GREETER_GREET_USERNAME", show_envvar=True)
@click.option(
    "--nickname", envvar="NICKNAME", show_envvar=True, show_default=True, help="This can be set via env var NICKNAME"
)
@click.option(
    "--email",
    envvar=["EMAIL", "EMAIL_ADDRESS"],
    show_envvar=True,
    default="foo@bar.com",
    show_default=True,
    help="This can be set via env var EMAIL or EMAIL_ADDRESS",
)
@click.option("--token", "-t", show_envvar=True)
def greet(username: str, nickname: str, email: str, token: str) -> None:
    click.echo(f"Hello {username} ({nickname}) with email {email}!")
    click.echo(f"Using token {token}")


if __name__ == "__main__":
    cli()
