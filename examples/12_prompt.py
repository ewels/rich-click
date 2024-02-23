import rich_click as click


@click.command()
@click.rich_config(help_config=click.RichHelpConfiguration(use_markdown=True, width=60))
@click.option(
    "--count", default=1, prompt="[blue]How manu times[/blue]", show_default=True, help="Number of greetings."
)
@click.option("--name", prompt="[bold magenta]Your name[/]", help="The person to greet.")
@click.option("--yes", is_flag=True, default=False, prompt="Please confirm", help="Confirm printing.")
def hello(count, name, yes):
    """Simple program that greets `NAME` for a total of `COUNT` times."""
    if yes:
        for _ in range(count):
            click.echo(f"Hello, {name}!")


if __name__ == "__main__":
    hello()
