# Panels - Advanced

!!! danger "Advanced"
    This document contains information that the majority of users will not need.

## Additional details on default order

By default, unless explicitly ordered otherwise, command panels always come after options panels.

```python
{% include "../../code_snippets/panels/panels_panel_order_explicit.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_panel_order_explicit.py --help`](../../images/code_snippets/panels/panels_panel_order_explicit.svg){.screenshot}


There exists a config option `commands_before_options` (default `False`), which changes the default behavior so that commands come before options.
When explicitly defining panels of multiple types with decorators (i.e. both option panels and command panels), this config option is ignored.
So for example, the below code will set options _above_ commands:

```python
{% include "../../code_snippets/panels/panels_panel_order_explicit_override.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_panel_order_explicit_override.py --help`](../../images/code_snippets/panels/panels_panel_order_explicit_override.svg){.screenshot}

If you do not explicitly define panels, then the sort order behavior is more advanced.
The sort order in all situations is deliberate and also thoroughly tested, but it's not worth going into detail about.
In short, if you want to have full control over panel sorting, then you should define each panel!

## Tables & Column Types

RichPanels consist of a `rich.panel.Panel` which contains inside of it a `rich.table.Table`.

For the inner table, the `column_types` are configurable.
The selected column types determine what gets rendered, and the order of the `column_types=[...]` list determines the order in which they show in the table.

Supported **RichOptionPanel** column types:

- `"required"`
- `"opt_primary"`
- `"opt_secondary"`
- `"opt_long"`
- `"opt_short"`
- `"opt_all"`
- `"opt_all_metavar"`
- `"opt_long_metavar"`
- `"metavar"`
- `"metavar_short"`
- `"help"`

Supported **RichCommandPanel** column types:

- `"name"`
- `"aliases"`
- `"name_with_aliases"`
- `"help"`

Below is an example showing how column types can be used:

```python
{% include "../../code_snippets/panels/panels_column_types.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_column_types.py --help`](../../images/code_snippets/panels/panels_column_types.svg){.screenshot}

### Help Text Sections

The `"help"` column type shows information such as deprecations, env var, default value, and the help text itself.

These sections-- whether they render at all, or in which order they render-- are all configurable via the config.
<!-- Note: in a future version of rich-click this will be tied to objects, not just the config. -->

Supported **Option** help section types (configurable via `options_table_help_sections`):

- `"help"`
- `"required"`
- `"envvar"`
- `"default"`
- `"range"`
- `"metavar"`
- `"metavar_short"`
- `"deprecated"`

Supported **Command** help section types (configurable via `commands_table_help_sections`):

- `"help"`
- `"aliases"`
- `"deprecated"`

A popular choice for extremely large CLIs is to remove the metavar column and append it to the help text.
Below is an example that does this, as well as doing some additional reordering of the help text elements.

```python hl_lines="22-23"
{% include "../../code_snippets/panels/panels_help_section_types.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_help_section_types.py --help`](../../images/code_snippets/panels/panels_help_section_types.svg){.screenshot}

## `RichPanel().to_info_dict()`

RichPanel objects support the `.to_info_dict()` method added in Click 8.0.
Additionally, RichGroups will show any panels explicitly assigned when rendering its own info dict.

Note that both default panels and objects assigned by default do not render:

- For a panel to show up in a RichGroup info dict's `panels`, it must be explicitly assigned to the group.
- For an object to show up in a RichPanel info dict, it must be explicitly assigned to the panel.
  In practice what this means is: a panel which is explicitly defined but which acts as a default panel (e.g. `@click.option_panel("Options")`),
  and whose assigned objects are inferred, will not show any assigned objects in its info dict.

## Custom RichPanel Classes

!!! warning
    The `RichPanel` API may be unstable across minor versions, since it is a new concept that we are still trying to find the best API for.
    If you subclass `RichPanel`, you may want to pin your **rich-click** version to `rich-click>=1.9,<1.10`.

RichPanels can be subclassed for additional functionality, if you so choose:

```python
{% include "../../code_snippets/panels/panels_subclass.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_subclass.py --help`](../../images/code_snippets/panels/panels_subclass.svg){.screenshot}
