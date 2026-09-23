import rich_click as click


@click.group()
@click.option(
    "--reject-output-outside-source/--no-reject-output-outside-source",
    default=True,
    help="Refuse to write output outside the source tree.",
)
@click.option("--format", "-f", type=click.Choice(["svg", "png"]), help="Output format.")
@click.option("--out", "-o", type=click.Path(), help="Where to write the rendered diagram.")
@click.rich_config({"wrap_long_options": 24})
def cli() -> None:
    """CLI help text"""


@cli.command()
def render() -> None:
    """Render the thing."""


@cli.command("a-command-with-a-very-long-name")
def other() -> None:
    """Long enough to trip the threshold too."""
