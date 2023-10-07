import rich_click as click


@click.command(context_settings={"show_default": True})
@click.option("--a", default="show me always", help="This works in all supported click versions.")
@click.option("--b", default="show me always", show_default=True, help="This works in all supported click versions.")
@click.option("--c", default="show me in old versions", show_default=False, help="Hide default only in click>=8.1")
@click.option(
    "--d",
    show_default="show me in c8+",
    help="Show 'default: (show me in c8+)' in click>=8.0. In click 7, no default is shown.",
)
def cli(a: str, b: str, c: str, d: str) -> None:
    """
    Test cases for context_settings.

    Note that in click < 8.1, '[default: False]' shows for "--help".
    """
    print("Hello, world!")


if __name__ == "__main__":
    cli()
