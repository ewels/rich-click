# /// script
# dependencies = ["rich-click>=1.9", "typer>=0.15"]
# ///

# This example comes from the Typer docs:
# https://typer.tiangolo.com/tutorial/parameter-types/number/
import typer
from typing_extensions import Annotated

def main(
    id: Annotated[int, typer.Argument(min=0, max=1000)],
    age: Annotated[int, typer.Option(min=18)] = 20,
    score: Annotated[float, typer.Option(max=100)] = 0,
):
    print(f"ID is {id}")
    print(f"--age is {age}")
    print(f"--score is {score}")

if __name__ == "__main__":
    from rich_click.patch import patch_typer
    import rich_click.rich_click as rc

    patch_typer()
    rc.THEME = "star-modern"

    typer.run(main)
