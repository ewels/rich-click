import rich_click as click


class Location(click.ParamType):
    name = "location"


@click.command()
@click.option(
    "--number",
    type=click.IntRange(min=1, max=6),
    help="Pick a number",
    default=4,
    show_default=True,
    required=True,
    show_envvar=True,  # No envvar --> envvar shouldn't show.
)
@click.option(
    "--name",
    help="Provide a name",
    envvar="CHOSEN_NAME",
)
@click.option(
    "--location", help="Provide a name", envvar="CHOSEN_LOCATION", type=Location(), show_envvar=False, deprecated=True
)
@click.option("--flag/--no-flag", is_flag=True, help="Set the flag (or not!).")
@click.password_option("--password", help="Password to login with")
@click.option(
    "--loaded",
    "-l",
    help="This option is loaded with everything (assert preservation of order)",
    default=42,
    type=click.IntRange(min=0),
    show_default="Random number",
    envvar="IS_LOADED",
    show_envvar=True,
    required=True,
)
@click.help_option("--help", "-h", help="Show help.")
@click.version_option("1.2.3", "--version", "-v", message="%(prog)s %(version)s", help="Show version.")
def cli(number: int, name: str, location: str, password: str) -> None:
    """
    My amazing tool does all the things.
    """


if __name__ == "__main__":
    cli()
