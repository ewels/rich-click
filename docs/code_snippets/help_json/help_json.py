# /// script
# dependencies = ["rich-click>=1.9"]
# ///
# `--help json`, `--help json-full` and `--help carapace` work out of the box on every command.
import rich_click as click


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
def cli(verbose):
    """A demo CLI."""


@cli.command()
@click.option("--count", type=int, default=1, help="Number of greetings.")
@click.argument("name")
def hello(count, name):
    """Greet someone."""


@cli.group()
def db():
    """Manage the database."""


@db.command()
def migrate():
    """Run migrations."""


if __name__ == "__main__":
    cli()
