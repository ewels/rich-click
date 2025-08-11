# Panels

The containers in help text that contain options and subcommands are defined by objects in the code called `RichPanel`s.

By default, `RichCommand`s have a single panel for options named "Options", and `RichGroup`s have an additional panel for commands named "Commands".

**rich-click** allows you to control and customize everything about these panels:

- The default panels can be renamed and stylized.
- Options and commands can be split up across multiple panels.
- Arguments can be given a separate panel, or included in options panels.
- The styles of these panels can be modified.

!!! note
    Panels are a replacement of "groups," which have been silently deprecated as of version 1.9.0.
    We will support the old groups API indefinitely, although its use is discouraged. Furthermore, although groups can be combined with panels, we cannot guarantee any behavior such as ordering when these two things are combined.

    You can read the 1.8 docs to learn more about groups API [here](https://ewels.github.io/rich-click/1.8/documentation/groups_and_sorting/).

## Introduction to API

The high-level API for defining panels is with the `#!python @click.command_panel()` and `#!python @click.option_panel()` decorators:

```python
{% include "../code_snippets/panels/panels_simple_decorators.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_decorators.py --help`](../images/code_snippets/panels/panels_simple_decorators.svg){.screenshot}

You can also specify what options that panels are associated with in the option itself. If the panel is not created in a decorator, then one is created on the fly.

The below code generates the same output as the above code:

```python
{% include "../code_snippets/panels/panels_simple_kwargs.py" %}
```

??? Output

    Note that this output is the same as the previous example, even though it was defined differently.
    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_kwargs.py --help`](../images/code_snippets/panels/panels_simple_kwargs.svg){.screenshot}


RichPanels inherit their base style behaviors from the rich config, although these can be overridden, as we will see in a moment.

RichPanels accept additional args other than just the name and objects associated with them.

Additionally, a panel can be defined without `options=[]`, and the associations between panels and options can be placed inside the `#!python @click.option()`s.

The below code shows both of these things:

```python
{% include "../code_snippets/panels/panels_extra_kwargs.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_extra_kwargs.py --help`](../images/code_snippets/panels/panels_extra_kwargs.svg){.screenshot}

The `panel_styles` is passed into the outer `rich.panel.Panel()`, and the `table_styles` dict is pass as kwargs into the inner `rich.table.Table()`.

You can view the respective docstrings of the `Table` and `Panel` objects for more information:

- [`rich/table.py`](https://github.com/Textualize/rich/blob/master/rich/table.py)
- [`rich/panel.py`](https://github.com/Textualize/rich/blob/master/rich/panel.py)

## Arguments

Despite the name, options panels handle more than just options; they can also handle arguments.

Arguments can be given their own panel with the `show_arguments` config option:

```python
{% include "../code_snippets/panels/panels_simple_arguments.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_arguments.py --help`](../images/code_snippets/panels/panels_simple_arguments.svg){.screenshot}

Arguments can also be included in the options panel with the `group_arguments_options` config option (the `show_arguments` config option does not need to be set).

```python
{% include "../code_snippets/panels/panels_simple_arguments_combined.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_arguments_combined.py --help`](../images/code_snippets/panels/panels_simple_arguments_combined.svg){.screenshot}

In **rich-click**, unlike base Click, arguments can have `help` text.
If `help=` if set for arguments, then the argument panel is shown:

```python
{% include "../code_snippets/panels/panels_simple_arguments_help.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_arguments_help.py --help`](../images/code_snippets/panels/panels_simple_arguments_help.svg){.screenshot}

Arguments can also be given their own panels, or combined with other panels.

```python
{% include "../code_snippets/panels/panels_simple_arguments_explicit.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_simple_arguments_explicit.py --help`](../images/code_snippets/panels/panels_simple_arguments_explicit.svg){.screenshot}

## Commands

!!! info
    Work in progress

## Overriding defaults

Default panel titles can be overridden with the config.
Renamed panels can still have their panel-level configurations modified.

```python
{% include "../code_snippets/panels/panels_defaults_renamed.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_defaults_renamed.py --help`](../images/code_snippets/panels/panels_defaults_renamed.svg){.screenshot}

Note that the rich config passes to subcommands, but panels are defined at the command level.
So running `move-item --help` from the above example will rename the children's panels (because that's set in the parent's config), but it does not pass the `panel_styles=` to the subcommand:

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_defaults_renamed.py move-item --help`](../images/code_snippets/panels/panels_defaults_renamed_move_item.svg){.screenshot}

Default panel styles are also handled by the config, and will be overridden when conflicting options are defined at the panel level.

In the below example, `Main` does not have any styles set, but `Extra` has the border style overridden.
However, defaults are overridden on an arg-by-arg basis, so the config level `box` is not overridden.
The below example also employs an additional trick to underline the text of the title.

```python
{% include "../code_snippets/panels/panels_defaults_override_config.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_defaults_override_config.py --help`](../images/code_snippets/panels/panels_defaults_override_config.svg){.screenshot}

## Tips & Gotchas

There are a few things to keep in mind when using RichPanels.

### Handling `--help` option

The help option is associated with the default options panel.

If you define all the panels, the `--help` option will be left straggling in the default panel.

This is probably a mistake, and there are two ways to fix it:

=== "Mistake"

    ```python
    {% include "../code_snippets/panels/panels_handling_help_mistake.py" %}
    ```

    ??? Output

        <!-- RICH-CODEX
        working_dir: docs/code_snippets/panels
        -->
        ![`python panels_handling_help_mistake.py --help`](../images/code_snippets/panels/panels_handling_help_mistake.svg){.screenshot}


=== "Fix (method 1)"
    ```python
    {% include "../code_snippets/panels/panels_handling_help_fix_1.py" %}
    ```

    ??? Output

        <!-- RICH-CODEX
        working_dir: docs/code_snippets/panels
        -->
        ![`python panels_handling_help_fix_1.py --help`](../images/code_snippets/panels/panels_handling_help_fix_1.svg){.screenshot}

=== "Fix (method 2)"
    ```python
    {% include "../code_snippets/panels/panels_handling_help_fix_2.py" %}
    ```

    ??? Output

        <!-- RICH-CODEX
        working_dir: docs/code_snippets/panels
        -->
        ![`python panels_handling_help_fix_2.py --help`](../images/code_snippets/panels/panels_handling_help_fix_2.svg){.screenshot}

### Ordering of panels

!!! warning
    **In 1.9.0dev0, options panels always come first and command panels always come after them.**
    In a near future update, before 1.9.0 is fully released, you will be able to mix the order of panels.

    The below text references the **intended** behavior for 1.9.0, but does not reflect the current behavior.

Panels are printed in the order that they are defined, from top to bottom.

If panels are inferred from `#!python @click.option(panel=...)`, rather than defined by `#!python @click.option_panel()`, then they are defined in the order that they appear in parameters from top to bottom.

This means that the simplest way to control the order panels is to define them explicitly.

This also means that you can order options panels to come before command panels, and vice-versa, based on the decorator order.

By default, unless explicitly ordered otherwise, command panels always come after options panels.

```python
{% include "../code_snippets/panels/panels_panel_order_explicit.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_panel_order_explicit.py --help`](../images/code_snippets/panels/panels_panel_order_explicit.svg){.screenshot}


There exists a config option `commands_before_options` (default `False`), which changes the default behavior so that commands come before options.
**When explicitly defining panel order with decorators, this config option is ignored.**
So for example, the below code will set options _above_ commands:

```python
{% include "../code_snippets/panels/panels_panel_order_explicit_override.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_panel_order_explicit_override.py --help`](../images/code_snippets/panels/panels_panel_order_explicit_override.svg){.screenshot}

### Ordering of rows within panels

The easiest way to control the order of elements within a panel is to explicitly define the order within the panel itself.

If you are having trouble with ordering things, set the order within `options=` or `commands=`.

Additionally, it is suggested you set _every_ object you intend on including in the panel.

```python
{% include "../code_snippets/panels/panels_row_order.py" %}
```

??? Output

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/panels
    -->
    ![`python panels_row_order.py --help`](../images/code_snippets/panels/panels_row_order.svg){.screenshot}

That said, the default behavior is also predictable and follows what base Click does for ordering:

- Arguments + options are presented in the order they occur in the decorators, from top to bottom.
- Subcommands are alphanumerically sorted.
