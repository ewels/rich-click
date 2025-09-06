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


def cli(
    id: Annotated[int, typer.Argument(min=0, max=1000)],
    age: Annotated[int, typer.Option(min=18)] = 20,
    score: Annotated[float, typer.Option(max=100)] = 0,
    log_level: Annotated[LogLevel, typer.Option(rich_help_panel="Logging")] = LogLevel.info,
    color: Annotated[bool, typer.Option(rich_help_panel="Logging")] = True,
) -> None:
    print(f"id={id} age={age} score={score} log_level={log_level} color={color}")


if __name__ == "__main__":
    typer.run(cli)
