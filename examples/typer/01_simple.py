import rich_click.typer as typer


def main():
    """A CLI that says hello."""
    typer.echo("Hello World")


if __name__ == "__main__":
    typer.run(main)
