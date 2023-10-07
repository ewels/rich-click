import rich_click as click


@click.command()
@click.rich_config(help_config=click.RichHelpConfiguration(use_markdown=True, width=60))
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets `NAME` for a total of `COUNT` times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")


if __name__ == "__main__":
    hello()
