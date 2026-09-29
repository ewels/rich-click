# Asyncclick Support

[Asyncclick](https://github.com/python-trio/asyncclick) is an asynchronous fork of Click. **rich-click** supports
asyncclick 8.2.2.2 and newer on Python 3.11+, and 8.3.0.3 and newer on Python 3.10. Async commands can use the same
help formatting, error rendering, panels, aliases, and configuration as regular Click commands.

Install the optional dependencies with:

```shell
pip install "rich-click[async]"
```

This installs a compatible asyncclick release and AnyIO. Asyncclick remains optional; rich-click does not import it
unless you use the async integration.

## Patching an existing asyncclick CLI

For most applications, call `patch()` before defining any commands:

```python
import asyncclick

from rich_click.patch import patch


patch(module=asyncclick)


@asyncclick.group
async def cli():
    """An asynchronous CLI with rich help output."""


@cli.command
async def status():
    """Show the current status."""


if __name__ == "__main__":
    cli()
```

The patch replaces asyncclick's command classes and its `command` and `group` decorators with rich-click-aware
versions. Both `@asyncclick.command` and `@asyncclick.command()` are supported, as are the equivalent group forms.
The usual asyncclick decorators, such as `option`, `argument`, `pass_context`, and `pass_obj`, continue to work.

Patching changes the imported asyncclick module for the rest of the process and cannot be safely undone. Call it
once during application startup. If a test suite needs both patched and unpatched asyncclick, run the patched CLI
in a separate process.

### Configuration, panels, and aliases

The rich-click decorators and command metadata work with patched async commands:

```python
import asyncclick

from rich_click import command_panel, option_panel, rich_config
from rich_click.patch import patch


patch(module=asyncclick)


@asyncclick.group
@rich_config({"options_panel_title": "Global options"})
@option_panel("Authentication", options=["--token"])
@command_panel("Utilities", commands=["status", "greet"])
@asyncclick.option("--token", help="API token.")
@asyncclick.pass_context
async def cli(ctx, token):
    ctx.obj = {"token": token}


@cli.command
async def status():
    """Show the current status."""


@cli.command(panel="Utilities", aliases=["hi"])
@asyncclick.argument("name")
async def greet(name):
    """Greet NAME."""
    asyncclick.echo(f"Hello {name}")
```

`rich_config`, `option_panel`, and `command_panel` may appear above or below the patched command or group
decorator. Custom async command classes can also override rich-click methods such as `get_rich_table_row()`.

To apply one configuration globally, pass it while patching:

```python
import asyncclick

from rich_click import RichHelpConfiguration
from rich_click.patch import patch


patch(
    module=asyncclick,
    rich_config=RichHelpConfiguration(
        options_panel_title="Arguments and options",
        style_option="bold cyan",
    ),
)
```

Use `@rich_config(...)` instead when the settings should apply only to one command tree. See
[Configuration](configuration.md) for all available settings.

## Using the async classes directly

If you do not want to patch the module, pass the appropriate class to an asyncclick decorator. The async classes
are available from either `rich_click` or `rich_click.rich_async_command`:

```python
import asyncclick

from rich_click import RichAsyncGroup


@asyncclick.group(cls=RichAsyncGroup)
async def cli():
    """An asynchronous CLI with rich help output."""
```

Subcommands and subgroups created through `RichAsyncGroup` use rich async classes automatically. For a standalone
command, use `RichAsyncCommand`:

```python
import asyncclick

from rich_click import RichAsyncCommand


@asyncclick.command(cls=RichAsyncCommand)
async def cli():
    """An asynchronous command with rich help output."""
```

The module also provides `RichAsyncContext` and `RichAsyncCommandCollection`.

## Running and testing

Run an async CLI in the usual way; asyncclick owns the event loop and async backend:

```shell
python app.py --help
python app.py status
```

The repository includes a working example:

```shell
python examples/13_async.py --help
python examples/13_async.py greet World
python examples/13_async.py --token secret greet World --count 3
```

Asyncclick's test runner is asynchronous:

```python
from asyncclick.testing import CliRunner


async def test_help():
    result = await CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
```

For a synchronous test, wrap the invocation with `asyncio.run()`:

```python
import asyncio

from asyncclick.testing import CliRunner


def test_help():
    result = asyncio.run(CliRunner().invoke(cli, ["--help"]))
    assert result.exit_code == 0
```

## Implementation notes

- Async callbacks, context handling, command invocation, and `ctx.obj` are still handled by asyncclick.
- Help honors `context_settings={"help_to_stderr": True}`.
- Usage errors and aborts use rich-click's normal error formatting.
- Use the `RichAsync*` classes for async command trees; the regular `RichCommand` and `RichGroup` classes use
  synchronous Click.
- `RichAsyncCommand.main()` follows asyncclick's execution flow so that rich-click can format exceptions and
  aborts. CI tests both the minimum supported asyncclick release and the latest available release to catch
  compatibility changes.
