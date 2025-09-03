# Typer Support

!!! example "Experimental"
    This feature is still experimental.
    Please report any bugs or issues you run into!

You don't need to use **rich-click** directly to get access to a lot of **rich-click**'s great features.

If you are a fan of Typer and you'd like to use **rich-click**'s themes, you can patch Typer to use **rich-click**
and set the global config's `THEME` (and other config options) to whatever you want.

All you need to do is import `patch_typer()` from `rich_click.patch`.
This does not need to be done at the top of the file, in fact you can do it right before calling `app.run()` or `typer.run(...)`:

```python hl_lines="24-28"
{% include "../code_snippets/typer_support/typer_example.py" %}
```

???+ example "Output"

    Running the above Typer CLI works the same as you would otherwise expect,
    except now with a **rich-click** theme applied:

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/typer_support
    -->
    ![`python typer_example.py --help`](../images/code_snippets/typer_support/typer_example.svg){.screenshot}

## Patching Typer via the `rich-click` CLI

You can also patch Typer as an end-user of any Typer CLI via the `rich-click` CLI.

```shell
rich-click my-typer-cli --help
```

In addition to giving access to **rich-click**'s themes, another benefit of this is being able to generate HTML and SVG help text easily.
Although, do note that Typer and **rich-click** have some minor differences in how they render help text.

More information about usage of the `rich-click` CLI is in [the **rich-click CLI** docs](rich_click_cli.md), or you can run **`rich-click --help`** to view the CLI.
