# Text Markup & Formatting

!!! info
    This page focuses on formatting help text of help text, not styles more generally.

## Markup

**rich-click** supports 4 different values for `text_markup`, which determines how text is rendered:

- `'ansi'`: **(Default)** Rendered as plain text with ANSI escape codes handled.
- `'rich'`: Rendered using Rich's markup syntax.
- `'markdown'`: Rendered with markdown.
- `None`: Rendered as plain text, ANSI escape codes are not handled.

???+ warning "rich-click ≥1.8.0 deprecation"
    Prior to **rich-click** 1.8.0, markup was controlled by the booleans `use_rich_markup` and `use_markdown`.

    These booleans have been silently deprecated (read: they will still be supported for the distant future),
    and users are encouraged to use the `text_markup` config option instead.

### Rich markup

In order to be as widely compatible as possible with a simple import,
**rich-click** does _not_ parse rich formatting markup (eg. `[red]`) by default.
You need to opt-in to this behaviour.

Remember that you'll need to escape any regular square brackets using a back slash in your help texts,
for example: `[dim]\[my-default: foo][\]`

For more information, read the Rich docs on [markup](https://rich.readthedocs.io/en/stable/markup.html) and [styles](https://rich.readthedocs.io/en/stable/style.html).

=== "`{}`"
    ```python
    help_config = {"text_markup": "rich"}
    ```

=== "`RichHelpConfiguration()`"
    ```python
    help_config = click.RichHelpConfiguration(text_markup="rich")
    ```

=== "Global config"
    ```python
    click.rich_click.TEXT_MARKUP = "rich"
    ```

<!-- RICH-CODEX
working_dir: .
-->
![`python examples/04_rich_markup.py --help`](../images/rich_markup.svg "Rich markup example"){.screenshot}

> See [`examples/04_rich_markup.py`](https://github.com/ewels/rich-click/blob/main/examples/04_rich_markup.py) for an example.

### Markdown

If you prefer, you can use Markdown text.

=== "`{}`"
    ```python
    help_config = {"text_markup": "markdown"}
    ```

=== "`RichHelpConfiguration()`"
    ```python
    help_config = click.RichHelpConfiguration(text_markup="markdown")
    ```

=== "Global config"
    ```python
    click.rich_click.TEXT_MARKUP = "markdown"
    ```

<!-- RICH-CODEX
working_dir: .
-->
![`python examples/05_markdown.py --help`](../images/markdown.svg "Markdown example"){.screenshot}

> See [`examples/05_markdown.py`](https://github.com/ewels/rich-click/blob/main/examples/05_markdown.py) for an example.

## Markup in text

The selected `text_markup` is used to render all text in your CLI help that can be set in the high-level API:

- The command's `help`
- Each subcommand's `help`
- Each parameter's `help`
- Each panel's `help`
- Header text, footer text, and epilog text.

```python
{% include "../code_snippets/text_markup_and_formatting/rich_markup.py" %}
```

???+ example Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/text_markup_and_formatting
    -->
    ![`python rich_markup.py --help`](../images/code_snippets/text_markup_and_formatting/rich_markup.svg){.screenshot}

You can also set the styles of `help` for objects in decorators using `help_style=`.
The below code renders the same as the above code:

```python
{% include "../code_snippets/text_markup_and_formatting/markup_with_help_style.py" %}
```

??? example Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/text_markup_and_formatting
    -->
    ![`python markup_with_help_style.py --help`](../images/code_snippets/text_markup_and_formatting/markup_with_help_style.svg){.screenshot}

## Newlines

Handling newlines on **rich-click**'s end involves discretion because in a docstring, newlines can represent a softwrap; they are not necessarily genuine new lines.

For `'markdown'` mode, we send all newline handling directly to `rich.markdown.Markdown()`

For other modes, we implement the following rules:

- Double newlines collapse to single newlines by default.
- Single newlines are not preserved, unless...
- The line starts with `'- '`, `'* '`, `'> '` or <code>'&nbsp;&nbsp;&nbsp;&nbsp;'</code> (4 spaces).

The following code snippet demonstrates this:

```python
{% include "../code_snippets/text_markup_and_formatting/newline_control.py" %}
```

???+ example Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/text_markup_and_formatting
    -->
    ![`python newline_control.py --help`](../images/code_snippets/text_markup_and_formatting/newline_control.svg){.screenshot}

Note that this differs from how base Click handles newlines.
The following is the same CLI help text but using `import click` instead of `import rich_click as click`:

???+ example Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/text_markup_and_formatting
    -->
    ![`python newline_control_base_click.py --help`](../images/code_snippets/text_markup_and_formatting/newline_control_base_click.svg){.screenshot}
