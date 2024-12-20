# Comparison of Click and rich-click

**rich-click** is a [shim](https://en.wikipedia.org/wiki/Shim_(computing)) around Click,
meaning its API is designed to mirror the Click API and intercept some of the calls to slightly different functions.

Everything available via `import click` is also available via `import rich_click as click`.

**rich-click** is designed to keep the additional API surface introduced on top of Click as lightweight as possible.

## Click features that rich-click overrides

The only things that **rich-click** explicitly overrides in the high-level API are the decorators:

- `click.command()`
- `click.group()`

The only change to these decorators is that by default, their `cls=` parameters point to the **rich-click** implementations of `Command` (i.e. `RichCommand`) and `Group` (i.e. `RichGroup`).

!!! info
    There is also a thin wrapper around `pass_context()` to cast the `click.Context` type in the function signature to `click.RichContext` to assist with static type-checking with MyPy. Aside from different typing, there are no substantive changes to the `pass_context()` decorator.

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

- Replace `#!python click.echo()` with `#!python rich.print()` ([docs](https://rich.readthedocs.io/en/stable/introduction.html#quick-start))
- Replace `#!python click.echo_via_pager()` with `#!python rich.Console().pager()` ([docs](https://rich.readthedocs.io/en/stable/console.html#paging))
- Replace `#!python click.confirm()` with `#!python rich.prompt.Confirm.ask()` ([docs](https://rich.readthedocs.io/en/stable/prompt.html))
- Replace `#!python click.prompt()` with `#!python rich.prompt.Prompt.ask()` ([docs](https://rich.readthedocs.io/en/stable/prompt.html))

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

- **rich-click** has a configuration object, `RichHelpConfiguration()`, that allows for control over how **rich-click** help text renders, so you are not just locked into the defaults. More information about this is described in [the **Configuration** docs](configuration.md).
- **rich-click** comes with a CLI tool that allows you to convert regular Click CLIs into **rich-click** CLIs, and also lets you render your **rich-click** CLI help text as HTML and SVG. More information about this is described in [the **rich-click CLI** docs](rich_click_cli.md).
