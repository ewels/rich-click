"""
Async CLI support via asyncclick.

asyncclick (https://github.com/python-trio/asyncclick) is a fork of click whose
command machinery is async, so command callbacks can be coroutines. rich-click can
format an asyncclick CLI the same way it formats a click CLI: call
``patch(module=asyncclick)`` once, then write a completely vanilla asyncclick CLI.
There is no rich-click-specific code below the patch call: plain @asyncclick.group
and @asyncclick.command decorators produce Rich help and Rich error panels.

Requires the optional dependency, installed with: pip install rich-click[async]
"""

import sys


try:
    import asyncclick
except ModuleNotFoundError:
    print("This example requires asyncclick. Install it with: pip install rich-click[async]")
    sys.exit(0)

import rich_click
from rich_click.patch import patch


rich_click.rich_click.USE_RICH_MARKUP = True
patch(module=asyncclick)


@asyncclick.group()
@asyncclick.option("--token", help="Shared API token passed to every subcommand.")
@asyncclick.pass_context
async def cli(ctx, token):
    """A vanilla async CLI that renders with [bold]rich-click[/] after patching."""
    ctx.obj = {"token": token}


@cli.command()
@asyncclick.argument("name")
@asyncclick.option("--count", default=1, show_default=True, help="Number of greetings.")
async def greet(name, count):
    """Greet [yellow]NAME[/] one or more times, asynchronously."""
    for i in range(count):
        asyncclick.echo(f"[{i + 1}/{count}] Hello {name}!")


if __name__ == "__main__":
    cli()
