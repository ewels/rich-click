import rich_click as click


@click.group()
@click.option("--config", "-c", required=True, type=click.Path(), help="Config file.")
@click.option("--verbose", is_flag=True, help="Be loud.", panel="Logging")
@click.command_panel("Core", commands=["run", "a-much-longer-name"])
@click.command_panel("Extras", commands=["tidy"])
@click.rich_config({"align_columns_across_panels": True})
def cli() -> None:
    """CLI help text"""


@cli.command()
def run() -> None:
    """Run the thing."""


@cli.command("a-much-longer-name")
def other() -> None:
    """Do something else."""


@cli.command()
def tidy() -> None:
    """Tidy up."""
