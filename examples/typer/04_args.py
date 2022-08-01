from rich_click import typer

typer.rich_click.SHOW_ARGUMENTS = True


def cli(
    name: str = typer.Argument("World"),
    say_hi: bool = typer.Option(True),
):
    if say_hi:
        print(f"Hello, {name}!")


if __name__ == "__main__":
    typer.run(cli)
