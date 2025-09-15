# Panels - Overview

**rich-click** lets you configure grouping and sorting of command options and subcommands.
The containers which contain grouped options and subcommands are called panels:

![](../../../images/panels.svg)

By default, `RichCommand`s have a single panel for options named "Options", and `RichGroup`s have an additional panel for commands named "Commands".

**rich-click** allows you to control and customize everything about these panels:

- The default panels can be renamed and stylized.
- Options and commands can be split up across multiple panels.
- Positional arguments can be given a separate panel, or included in options panels.
- The styles of these panels can be modified.

!!! info
    Panels are a replacement of rich-click "groups," which are deprecated as of version 1.9.0.
    We will support the old groups API for the foreseeable future, but its use is discouraged.

    Although groups technically can be combined with panels, doing so can lead to unpredictable sorting behavior.

    You can read the [rich-click v1.8 docs](https://ewels.github.io/rich-click/1.8/documentation/groups_and_sorting/) to learn more about groups API.

## Introduction to API

The high-level API for defining panels is with the `@click.command_panel()` and `@click.option_panel()` decorators.

Under the hood, these decorators create **`RichPanel`** objects that are attached to the command.

### Options

Options panels handle parameters for your command:

```python hl_lines="12-15"
{% include "../../code_snippets/panels/panels_simple_decorators.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_decorators.py --help`](../../images/code_snippets/panels/panels_simple_decorators.svg){.screenshot}

Alternatively, you can configure panels within the option itself.
If the panel is not created in a decorator, then one is created on the fly.

The following code generates the same output as the example above:

```python hl_lines="7-12"
{% include "../../code_snippets/panels/panels_simple_kwargs.py" %}
```

??? example "Output"

    Note that this output is the same as the previous example, even though it was defined differently.
    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_kwargs.py --help`](../../images/code_snippets/panels/panels_simple_kwargs.svg){.screenshot}

### Arguments

Despite the name, options panels handle more than just options; they can also handle positional arguments.

Arguments can be given their own panel with the `show_arguments` config option:

```python hl_lines="11"
{% include "../../code_snippets/panels/panels_simple_arguments.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_arguments.py --help`](../../images/code_snippets/panels/panels_simple_arguments.svg){.screenshot}

Arguments can also be included in the options panel with the `group_arguments_options` config option (the `show_arguments` config option does not need to be set).

```python hl_lines="11"
{% include "../../code_snippets/panels/panels_simple_arguments_combined.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_arguments_combined.py --help`](../../images/code_snippets/panels/panels_simple_arguments_combined.svg){.screenshot}

In **rich-click**, unlike base Click, arguments can have `help` text.
If `help=` if set for arguments, then the argument panel is automatically shown:

```python hl_lines="7-8"
{% include "../../code_snippets/panels/panels_simple_arguments_help.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_arguments_help.py --help`](../../images/code_snippets/panels/panels_simple_arguments_help.svg){.screenshot}

### Commands

Sub-commands also have panels that are defined similarly to option panels:

```python hl_lines="7-11"
{% include "../../code_snippets/panels/panels_commands.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_commands.py --help`](../../images/code_snippets/panels/panels_commands.svg){.screenshot}

## Styles & Panel Help

`RichPanel` objects inherit their base style behaviors from the rich config by default, but this can be set on a per-panel basis.

Panels can also have help text.

The below example shows both of these things:

```python hl_lines="11-18"
{% include "../../code_snippets/panels/panels_extra_kwargs.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_extra_kwargs.py --help`](../../images/code_snippets/panels/panels_extra_kwargs.svg){.screenshot}

The `panel_styles` is passed into the outer `rich.panel.Panel()`, and the `table_styles` dict is pass as kwargs into the inner `rich.table.Table()`.

See the available arguments for the **rich** library `Table` and `Panel` objects for more information:

- [Table options :octicons-link-external-24:](https://rich.readthedocs.io/en/latest/tables.html#table-options)
- [Panel options :octicons-link-external-24:](https://rich.readthedocs.io/en/latest/reference/panel.html#rich.panel.Panel)
  and [Box styles :octicons-link-external-24:](https://rich.readthedocs.io/en/latest/appendix/box.html#appendix-box)

## Overriding defaults

Default panel titles can be overridden with the config.
Renamed panels can still have their panel-level configurations modified.

```python hl_lines="14-16"
{% include "../../code_snippets/panels/panels_defaults_renamed.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_defaults_renamed.py --help`](../../images/code_snippets/panels/panels_defaults_renamed.svg){.screenshot}

Note that the rich config passes to subcommands, but panels are defined at the command level.
So running `move-item --help` from the above example _will_ rename the children's panels (because that's set in the parent's config), but it does _not_ pass the `panel_styles=` to the subcommand:

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_defaults_renamed.py move-item --help`](../../images/code_snippets/panels/panels_defaults_renamed_move_item.svg){.screenshot}

Default panel styles are also handled by the config, and will be overridden when conflicting options are defined at the panel level.

```python hl_lines="6-7 15-16 19"
{% include "../../code_snippets/panels/panels_defaults_override_config.py" %}
```

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_defaults_override_config.py --help`](../../images/code_snippets/panels/panels_defaults_override_config.svg){.screenshot}
