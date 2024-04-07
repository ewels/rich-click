# Formatting & Styles

## Formatting

There are a large number of customisation options in rich-click.
These can be modified by changing variables in the `click.rich_click` namespace.

Note that most normal click options should still work, such as `show_default=True`, `required=True` and `hidden=True`.

### Using Rich markup

In order to be as widely compatible as possible with a simple import, rich-click does _not_ parse rich formatting markup (eg. `[red]`) by default. You need to opt-in to this behaviour.

Remember that you'll need to escape any regular square brackets using a back slash in your help texts,
for example: `[dim]\[my-default: foo][\]`

=== "`RichHelpConfiguration()`"
    ```python
    help_config = click.RichHelpConfiguration(use_rich_markup=True)
    ```

=== "Global config"
    ```python
    click.rich_click.USE_RICH_MARKUP = True
    ```

![`python ../../examples/04_rich_markup.py --help`](../images/rich_markup.svg "Rich markup example")

> See [`examples/04_rich_markup.py`](examples/04_rich_markup.py) for an example.

### Using Markdown

If you prefer, you can use Markdown text.
You must choose either Markdown or rich markup. If you specify both, Markdown takes precedence.

=== "`RichHelpConfiguration()`"
    ```python
    help_config = click.RichHelpConfiguration(use_markdown=True)
    ```

=== "Global config"
    ```python
    click.rich_click.USE_MARKDOWN = True
    ```

![`python ../../examples/05_markdown.py --help`](../images/markdown.svg "Markdown example")

> See [`examples/05_markdown.py`](examples/05_markdown.py) for an example.

### Positional arguments

The default click behaviour is to only show positional arguments in the top usage string,
and not in the list below with the options.

If you prefer, you can tell rich-click to show arguments with `SHOW_ARGUMENTS`.
By default, they will get their own panel, but you can tell rich-click to bundle them together with `GROUP_ARGUMENTS_OPTIONS`:

=== "`RichHelpConfiguration()`"
    ```python
    help_config = click.RichHelpConfiguration(
        show_arguments=True,
        group_arguments_options=True
    )
    ```

=== "Global config"
    ```python
    click.rich_click.SHOW_ARGUMENTS = True
    click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
    ```

![`python ../../examples/06_arguments.py --help`](../images/arguments.svg "Positional arguments example")

> See [`examples/06_arguments.py`](examples/06_arguments.py) for an example.

### Metavars and option choices

Metavars are click's way of showing expected input types.
For example, if you have an option that must be an integer, the metavar is `INTEGER`.
If you have a choice, the metavar is a list of the possible values.

By default, rich-click shows metavars in their own column.
However, if you have a long list of choices, this column can be quite wide and result in a lot of white space:

![`python ../../examples/08_metavars_default.py --help`](../images/metavars_default.svg "Default metavar display")

It may look better to show metavars appended to the help text, instead of in their own column.
For this, use the following:

=== "`RichHelpConfiguration()`"
    ```python
    help_config = click.RichHelpConfiguration(
        show_metavars_column=False,
        append_metavars_help=True
    )
    ```

=== "Global config"
    ```python
    click.rich_click.SHOW_METAVARS_COLUMN = False
    click.rich_click.APPEND_METAVARS_HELP = True
    ```

![`python ../../examples/08_metavars.py --help`](../images/metavars_appended.svg "Appended metavar")

> See [`examples/08_metavars.py`](examples/08_metavars.py) for an example.

### Error messages

By default, rich-click gives some nice formatting to error messages:

![`python ../../examples/01_simple.py --hep || true`](../images/error.svg "Error message")

You can customise the _Try 'command --help' for help._ message with `ERRORS_SUGGESTION`
using rich-click though, and add some text after the error with `ERRORS_EPILOGUE`.

For example, from [`examples/07_custom_errors.py`](examples/07_custom_errors.py):

=== "`RichHelpConfiguration()`"

    ```python
    help_config = click.RichHelpConfiguration(
        style_errors_suggestion="magenta italic",
        errors_suggestion="Try running the '--help' flag for more information.",
        errors_epilogue="To find out more, visit [link=https://mytool.com]https://mytool.com[/link]"
    )
    ```

=== "Global config"
    ```python
    click.rich_click.STYLE_ERRORS_SUGGESTION = "magenta italic"
    click.rich_click.ERRORS_SUGGESTION = "Try running the '--help' flag for more information."
    click.rich_click.ERRORS_EPILOGUE = "To find out more, visit [link=https://mytool.com]https://mytool.com[/link]"
    ```

![`python ../../examples/07_custom_errors.py --hep || true`](../images/custom_error.svg "Custom error message")

> See [`examples/07_custom_errors.py`](examples/07_custom_errors.py) for an example.

### Help width

The default behaviour of rich-click is to use the full width of the terminal for output.
However, if you've carefully crafted your help texts for the default narrow click output, you may find that you now have a lot of whitespace at the side of the panels.

To limit the maximum width of the help output, regardless of the terminal size, set `WIDTH` in characters as follows:

```python
click.rich_click.WIDTH = 128
```

To still use the full width of the terminal up to a certain limit, set `MAX_WIDTH` in characters as follows:

```python
click.rich_click.MAX_WIDTH = 96
```

Setting `MAX_WIDTH` overrides the effect of `WIDTH`

## Styles

Most aspects of rich-click formatting can be customised, from colours to alignment.

For example, to print the option flags in a different colour, you can use:

```python
click.rich_click.STYLE_OPTION = "magenta"
```

To add a blank line between rows of options, you can use:

```python
click.rich_click.STYLE_OPTIONS_TABLE_LEADING = 1
click.rich_click.STYLE_OPTIONS_TABLE_BOX = "SIMPLE"
```

You can make some really ~horrible~ _colourful_ solutions using these styles if you wish:

<!-- RICH-CODEX
extra_env:
    TERMINAL_WIDTH: 160
-->

![`python ../../examples/10_table_styles.py --help`](../images/style_tables.svg "Rich markup example")

> See [`examples/10_table_styles.py`](examples/10_table_styles.py) for an example.

See the [_Configuration options_](#configuration-options) section below for the full list of available options.

