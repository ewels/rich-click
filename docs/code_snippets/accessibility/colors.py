# /// script
# dependencies = [
#   "rich",
# ]
from rich.console import Console
from rich.box import SIMPLE
from rich.table import Table

console = Console(color_system="truecolor")
table = Table(title="ANSI Colors", box=SIMPLE)
colors = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
table.add_column("Color", style="bold")

for variant in ["Normal", "Dim", "Bright", "Dim +\nBright"]:
    table.add_column(variant, style="bold")

for color in colors:
    table.add_row(
        color,
        *[
            f"[{style}{color}]██████[/{style}{color}]"
            for style in ["", "dim ", "bright_", "dim bright_"]
        ]
    )

console.print(table)
