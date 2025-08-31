# Comparison of Click and rich-click

**rich-click** is a thin wrapper around Click. The **rich-click** API is designed to mirror the Click API and intercept some of the calls to slightly different functions.

Everything available via `#!python import click` is also available via `#!python import rich_click as click`.

**rich-click** is designed to keep the additional API surface introduced on top of Click as lightweight as possible.
In other words, **rich-click** does not introduce many additional concepts not already in Click.
If you know Click, you already mostly know **rich-click**!

## Click features that rich-click overrides

The only things that **rich-click** explicitly overrides in the high-level API are the decorators:

- `#!python click.command()`
- `#!python click.group()`
- `#!python click.option()` (+ its variants)
- `#!python click.argument()`

The only change to these decorators is that by default, their `#!python cls=` parameters point to the **rich-click** implementations.

!!! note
    There is also a thin wrapper around `#!python pass_context()` to cast the `#!python click.Context` type in the function signature to `#!python click.RichContext` to assist with static type-checking with MyPy. Aside from different typing, there are no substantive changes to the `#!python pass_context()` decorator.

## Click features that rich-click does _not_ override

### Base Click command classes

You can still access the base Click classes by their original names:

```python
from rich_click import Command, Group, Context
```

The above are the same as importing from `click`.

**rich-click**'s subclasses all have the word Rich in front of them!

```python
from rich_click import RichCommand, RichGroup, RichContext
```

### Echo and interactive elements

**rich-click** deliberately does _not_ enrich certain Click features:

```python
click.echo()
click.echo_via_pager()
click.confirm()
click.prompt()
```

You are free to use these functions and they are available via `#!python import rich_click as click`,
but Rich's markup will not work with these functions because these functions are just the base Click implementations,
without any changes.

This is a deliberate decision that we are unlikely to change in the future.
We do not want to maintain a more spread-out API surface, and we encourage users to become comfortable using Rich directly; it's a great library and it's worth learning a little bit about it!
If you'd like Rich markup for your echos and interactive elements, then you can:

| Click Function                    | Rich Replacement                     | Rich Documentation |
|-----------------------------------|--------------------------------------|---------------|
| `#!python click.echo()`           | `#!python rich.print()`              | [Quick start](https://rich.readthedocs.io/en/stable/introduction.html#quick-start) |
| `#!python click.echo_via_pager()` | `#!python rich.Console().pager()`    | [Console](https://rich.readthedocs.io/en/stable/console.html#paging) |
| `#!python click.confirm()`        | `#!python rich.prompt.Confirm.ask()` | [Prompt](https://rich.readthedocs.io/en/stable/prompt.html) |
| `#!python click.prompt()`         | `#!python rich.prompt.Prompt.ask()`  | [Prompt](https://rich.readthedocs.io/en/stable/prompt.html) |

Below is a side-by-side comparison of Click and Rich implementations of echos and interactive elements in **rich-click**:

=== "Click"

    ```python
    import rich_click as click

    @click.command("greet")
    def greet():
        name = click.prompt(click.style("What is your name?", fg="blue"))

        if not click.confirm(click.style("Are you sure?", fg="blue")):
            click.echo(click.style("Aborting", fg="red"))
            return

        click.echo(click.style(f"Hello, {name}!", fg="green"))

    if __name__ == "__main__":
        greet()
    ```

=== "Rich"

    ```python
    import rich_click as click
    import rich
    from rich.prompt import Confirm, Prompt

    @click.command("greet")
    def greet():
        name = Prompt.ask("[blue]What is your name?[/]")

        if not Confirm.ask("[blue]Are you sure?[/]"):
            rich.print("[red]Aborting[/]")
            return

        rich.print(f"[green]Hello, {name}![/]")

    if __name__ == "__main__":
        greet()
    ```

## Additional rich-click features

- **rich-click** arguments can be given `help=` text:
    ```python
    import rich_click as click

    @click.command()
    @click.argument("src", help="Source location")
    @click.argument("dest", help="Destination location")
    def move_item(src, dest):
        """Move an item from a src location to a dest location"""
        ...
    ```
- **rich-click** commands can be given **aliases**, similar to other Click extensions ([click-aliases](https://github.com/click-contrib/click-aliases/tree/master), [click-extra](https://kdeldycke.github.io/click-extra/), [cloup](https://cloup.readthedocs.io/en/stable/)).
- **rich-click** has **themes** to beautify all CLIs, whether you're an end-user or a CLI developer. More information about this is described in [the **Themes** docs](themes.md). 
- **rich-click** help text is formatted using highly configurable **option panels** and **command panels**:
    ```python
    import rich_click as click

    @click.group()
    @click.option("--environment", help="Environment")
    @click.option("--log-level", help="Log level")
    @click.option_panel("Config",
                        options=["--environment", "--log-level"],
                        help="Global runtime configuration")
    @click.command_panel("Admin Commands",
                         commands=["user", "resource", "self"],
                         help="Commands available to administrators")
    def cli(environment, log_level):
        """My application"""
        ...
    ```
    More information about this is described in [the **Panels** docs](panels.md).
- **rich-click** has a configuration object, **`RichHelpConfiguration()`**, that allows for control over how **rich-click** help text renders, so you are not locked into the defaults. More information about this is described in [the **Configuration** docs](configuration.md).
- **rich-click** comes with a CLI tool that allows you to convert regular Click CLIs into **rich-click** CLIs, and also lets you render your **rich-click** CLI help text as HTML, SVG, JSON, and trees. More information about this is described in [the **rich-click CLI** docs](rich_click_cli.md), or you can run **`rich-click --help`** to view the CLI.
