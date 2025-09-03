# /// script
# dependencies = ["rich-click>=1.9", "typer>=0.15"]
# ///
from enum import Enum
import typer
from typing_extensions import Annotated

class LogLevel(str, Enum):
    debug = "debug"
    info = "info"
    warn = "warn"
    error = "error"

def main(
        id: Annotated[int, typer.Argument(min=0, max=1000)],
        age: Annotated[int, typer.Option(min=18)] = 20,
        score: Annotated[float, typer.Option(max=100)] = 0,
        log_level: Annotated[LogLevel, typer.Option(rich_help_panel="Logging")] = LogLevel.info,
        color: Annotated[bool, typer.Option(rich_help_panel="Logging")] = True,
) -> None:
    pass

if __name__ == "__main__":
    from rich_click.patch import patch_typer
    import rich_click.rich_click as rc

    patch_typer()
    rc.THEME = "star-slim"

    typer.run(main)
