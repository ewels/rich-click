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

## Aligning columns across panels

`align_columns_across_panels` sizes every panel's columns together, so that the help text starts in
the same place throughout the help screen: a column is kept if any panel has something to put in it,
and is then made wide enough for the widest entry that reaches past it. Turn it off to have each
panel size its own table instead.

```python
{% include "../../code_snippets/panels/panels_align_columns.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_align_columns.py --help`](../../images/code_snippets/panels/panels_align_columns.svg){.screenshot}

A panel that has nothing to put in one of the shared columns hands that column's width to the one on
its left, so the space is still usable by the entries that need it. The leading column is left alone,
since that is what indents each panel's names into line with its siblings.

An entry whose own cells stop short of the help - an option with no short form, say - does the same
row by row: it runs on under the columns it leaves empty rather than widening the one it is in, so
the entries that do use those columns keep them narrow. `wrap_long_options` is the ceiling on how far
the columns will stretch to keep such an entry beside its help.

???+ warning "rich-click ≥2.0.0 deprecation"
    `style_commands_table_column_width_ratio` sizes the first two columns of the commands table by a
    fixed proportion, which truncates a long command name to fit. `wrap_long_options` does that job
    without losing the name, and `align_columns_across_panels` lines the columns up with the rest of
    the help screen, so the ratio is no longer needed and will be removed in a future version.

    Setting it holds command panels out of the alignment pass altogether, so that an explicit ratio
    still decides their column widths. Remove it to opt in to the new layout.

Where the aligned columns would take more than two thirds of the panel, there is too little left for
the help text to be worth reading, and every panel sizes itself instead. A narrow terminal can
therefore show the same CLI unaligned.

## Wrapping long entries

One very long option name sets the width of the whole column, and every other entry's help text pays
for it - a boolean flag and its negative form share a cell, so a pair like
`--reject-output-outside-source/--no-reject-output-outside-source` can stretch the option column
across half the screen on its own. `wrap_long_options` puts a ceiling on that: an entry whose columns
before the help are wider than the given threshold is wrapped instead of widening the column.

```python hl_lines="11"
{% include "../../code_snippets/panels/panels_wrap_long_options.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_wrap_long_options.py --help`](../../images/code_snippets/panels/panels_wrap_long_options.svg){.screenshot}

An over-wide entry first spills into the columns it leaves empty to its right: an option with no
metavar can run on under the metavar column and keep its help beside it. Where that is not room
enough, its help moves to the line below instead - it still starts in the help column, so every
description in the panel lines up.

Either way the entry no longer counts towards the column width, which is what buys the space back.
The threshold also caps how wide the columns will grow to hold an entry that spills across them, and
it applies to command panels too, for subcommands with long names.

If *every* entry in a panel is over the threshold there is no column left to line up with, and that
panel's help text is simply indented instead. An entry wider than the panel itself is left alone,
since no arrangement of columns fits it; rich truncates it with an ellipsis as it did before.

With `align_columns_across_panels` also on, an entry that fits the width its columns get from being
aligned stays put whatever the threshold says - moving it would cost a line and reclaim nothing.

The threshold can be given three ways:

| Value | Meaning |
| --- | --- |
| `float` | A fraction of the room the panel has, so a wide terminal keeps more entries inline than a narrow one. |
| `int` | That many characters, whatever the terminal is doing. |
| callable | Passed the panel's width in characters, returns either of the above. |

The default is `40` characters. A fixed number holds the help text in the same place at every
terminal width, which is what you usually want: a fraction of a 300-column terminal is a threshold so
high that nothing trips it, and the panel goes back to letting one long entry set the column width
for everything. Reach for a `float` or a callable when you want to be gentler on a narrow terminal,
for instance `lambda width: min(width // 2, 40)`.

`0`, a negative number, `False` or `None` turns the whole thing off, leaving every entry to set the
width of its column as it did before. Where spilling would leave the help text less than a third of
the panel, the columns are sized that way too.

Moving the help down is the shape that [clap](https://docs.rs/clap/latest/clap/struct.Arg.html) calls
`next_line_help` and that `argparse` arrives at through a low `max_help_position`.

!!! note

    Rich tables cannot span columns, so a panel containing a wrapped entry is rendered as a stack of
    tables sharing one set of column widths. `RichPanel.get_table()` returns a `rich.console.Group`
    rather than a `Table` in that case. Subclasses that assume a `Table` comes back should either
    turn this option off or handle both.

    A box is drawn around each table in such a stack, so a panel whose `style_options_table_box` or
    `style_commands_table_box` is set keeps all of its entries inline instead, whatever the
    threshold says.

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
