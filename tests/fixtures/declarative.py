import click

from rich_click import RichCommand, RichContext, RichGroup, pass_context


@click.group(cls=RichGroup)
@click.option("--debug/--no-debug", default=False)
def cli(debug: bool) -> None:
    """My amazing tool does all the things."""
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@cli.command(cls=RichCommand)
@pass_context
def check(ctx: RichContext) -> None:
    """Check the context type."""
    click.echo(f"Ctx is {type(ctx).__name__}")
    if not isinstance(ctx, RichContext):
        ctx.exit(1)


if __name__ == "__main__":
    cli()
