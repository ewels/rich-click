# Panels - Tips

There are a few things to keep in mind when using RichPanels.

## Handling `--help` option

The help option is associated with the default options panel.

If you define all the panels, the `--help` option will be left straggling in the default panel.

This is probably a mistake, and there are two ways to fix it:

=== "Mistake"

    ```python
    {% include "../../code_snippets/panels/panels_handling_help_mistake.py" %}
    ```

    ???+ failure "Output - Mistake"

        <!-- RICH-CODEX
        working_dir: docs/code_snippets/panels
        -->
        ![`python panels_handling_help_mistake.py --help`](../../images/code_snippets/panels/panels_handling_help_mistake.svg){.screenshot}


=== "Fix (method 1)"
    ```python hl_lines="13"
    {% include "../../code_snippets/panels/panels_handling_help_fix_1.py" %}
    ```

    ???+ success "Output - Fix (method 1)"

        <!-- RICH-CODEX
        working_dir: docs/code_snippets/panels
        -->
        ![`python panels_handling_help_fix_1.py --help`](../../images/code_snippets/panels/panels_handling_help_fix_1.svg){.screenshot}

=== "Fix (method 2)"
    ```python hl_lines="12"
    {% include "../../code_snippets/panels/panels_handling_help_fix_2.py" %}
    ```

    ???+ success "Output - Fix (method 2)"

        <!-- RICH-CODEX
        working_dir: docs/code_snippets/panels
        -->
        ![`python panels_handling_help_fix_2.py --help`](../../images/code_snippets/panels/panels_handling_help_fix_2.svg){.screenshot}

## Sort order of panels

Panels are printed in the order that they are defined, from top to bottom.

```python
@click.option_panel("first")
@click.command_panel("second")
@click.option_panel("third")
```

If panels are inferred from `@click.option(panel=...)`, rather than defined by `@click.option_panel()`, then they are defined in the order that they appear in parameters from top to bottom.

**The simplest way to control the order panels is to define them explicitly!**

This also means that you can order options panels to come before command panels, and vice-versa, based on the decorator order.

## Ordering of rows within panels

The easiest way to control the order of elements within a panel is to explicitly define the order within the panel itself.

If you are having trouble with ordering things, set the order within `options=` or `commands=`.

Additionally, it is suggested you set _every_ object you intend on including in the panel.

```python
{% include "../../code_snippets/panels/panels_row_order.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_row_order.py --help`](../../images/code_snippets/panels/panels_row_order.svg){.screenshot}

That said, the default behavior is also predictable and follows what base Click does for ordering:

- Arguments + options are presented in the order they occur in the decorators, from top to bottom.
- Subcommands are alphanumerically sorted.
