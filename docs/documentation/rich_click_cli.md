# `rich-click` CLI tool

## Overview

**rich-click** comes with a CLI tool that allows you to format the Click help output for any CLI that uses Click.

<!-- RICH-CODEX
head: 12
-->
![`rich-click --help`](../images/code_snippets/rich_click_cli/rich_click.svg){.screenshot}

To use, simply prefix `rich-click` to the command. Here are a few real world examples:

=== "`flask`"

    ![](../images/rich_click_cli_examples/flask.svg "flask --help"){.screenshot}

=== "`celery`"

    ![](../images/rich_click_cli_examples/celery.svg "celery --help"){.screenshot}

=== "`dagster`"

    ![](../images/rich_click_cli_examples/dagster.svg "dagster --help"){.screenshot}

If the CLI is not installed as a script, you can also pass the location with:

- `<module_name>:<click_command_name>`
- `<module_name>`
- `<path>`

For example, if you have a file located at `path/to/my/cli.py`, and the Click `Command` object is named `main`, then you can run:

- `rich-click path.to.my.cli:main`
- `rich-click path.to.my.cli`
- `rich-click path/to/my/cli.py`

In the first case, the object will be imported and called, i.e. `from path.to.my.cli import main` then `main()`.
In the other two cases, the file will be run with `__name__` as `"__main__"`.

## Render help text as HTML or SVG

You can also use `rich-click --output=html [command]` to render rich HTML for help text, or `rich-click --output=svg [command]` to generate an SVG.

This works for RichCommands as well as normal click Commands.

SVG example:

<!-- RICH-CODEX
extra_env:
  PYTHONPATH: .
fake_command: rich-click --output svg app:main --help
working_dir: docs/code_snippets/rich_click_cli
head: 12
-->
![`rich-click --output svg app:main --help | grep -Eo '.{1,120}'`](../images/code_snippets/rich_click_cli/output_to_svg.svg){.screenshot}

HTML example:

<!-- RICH-CODEX
extra_env:
  PYTHONPATH: .
fake_command: rich-click --output html app:main --help
working_dir: docs/code_snippets/rich_click_cli
head: 12
-->
![`rich-click --output html app:main --help | grep -Eo '.{1,120}'`](../images/code_snippets/rich_click_cli/output_to_html.svg){.screenshot}

_SVG and HTML generated from [`docs/code_snippets/rich_click_cli/app.py`](https://github.com/ewels/rich-click/blob/main/docs/code_snippets/rich_click_cli/app.py)_

## Typer support

!!! example "Experimental"
    This feature is still experimental.
    Please report any bugs or issues you run into!

As of 1.9.0, the `rich-click` CLI supports patching Typer.

You don't need to do anything special to patch Typer CLIs; it works out of the box.

The main reason to patch Typer CLIs is to get access to **rich-click**'s themes.
Another reason is to print HTML and SVG.

Here is an example of overriding a Typer CLI with a **rich-click** theme:

```python
{% include "../code_snippets/panels/panels_simple_arguments.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/rich_click_cli
    -->
    ![`rich-click --theme magenta1-nu typer_example.py --help`](../images/code_snippets/rich_click_cli/typer_example.svg){.screenshot}

## Notes on how the `rich-click` CLI works

!!! note
    The rest of this document contains technical details most users will not need to know.

Under the hood, the `rich-click` CLI is patching the `click` module, and replacing the Click decorators and `click.Command`, `click.Group`, etc. objects with their equivalent **rich-click** versions.

Sometimes, a subclassed `click.Command` will overwrite one of these methods:

- `click.Command.format_usage`
- `click.Command.format_help_text`
- `click.Command.format_options`
- `click.MultiCommand.format_commands`
- `click.Command.format_epilog`

Patching Click internals can mess with method resolution order,
since by the time the downstream library subclasses the `click.Command`, it will be a `RichCommand`, and the subclass's method will take precedence over the `RichCommand`'s methods.
The problem is that **rich-click**'s methods can be incompatible or at least stylistically incongruous with the base Click help text rendering.

To solve this, `rich-click` checks whether a method comes from a "true" `RichCommand` subclass or if it just looks that way due to patching.
If `RichCommand` is "properly" subclassed, the override is allowed.
If the subclass is only a result of the patching operation, we ignore the aforementioned methods and use the **rich-click** implementation.

Long story short, the `rich-click` CLI is safe to subclassing when it is the user's intent to subclass a **rich-click** object. (This is so that you can use other nifty features of the CLI such as the `--output` option on your own **rich-click** CLIs)
That said, custom, non-**rich-click** implementations are ignored.

Additional hacks are implemented to provide first-class support for Typer.
When a Click object subclass is defined, we detect whether it is a Typer subclass during the call to the metaclass `__init__`.
When Typer is detected, we do additional overrides to resolve differences between Typer's and **rich-click**'s APIs.

### Using `patch()` as an end user

The functionality that `rich-click` uses to patch Click internals is available for use by **rich-click** end users,
and it occasionally comes in handy outside of the `rich-click` CLI.

In some situations, you might be registering a command from another Click CLI that does not use **rich-click**:

```python
import rich_click as click
from some_library import another_cli

@click.group("my-cli")
def cli():
    pass

# `another_cli` will NOT have rich-click markup. :(
cli.add_command(another_cli)
```

In this situation, `another_cli` retains its original help text behavior.
In order to make `another_cli` work with **rich-click**, you need to patch `click` before you import `another_cli`.
You can patch Click with `rich_click.patch.patch` like this:

```python
import rich_click as click
from rich_click.patch import patch

patch()

from some_library import another_cli  # noqa: E402

@click.group("my-cli")
def cli():
    pass

# `another_cli` will have rich-click markup. :)
cli.add_command(another_cli)
```
