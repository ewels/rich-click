# Groups & Sorting

**rich-click** gives functionality to list options and subcommands in groups, printed as separate panels.
It accepts a list of options / commands which means you can also choose a custom sorting order.

- For options / flags, set `click.rich_click.OPTION_GROUPS`
- For subcommands / Click groups, set `click.rich_click.COMMAND_GROUPS`

![](../images/command_groups.svg)

When grouping subcommands into more than one group (in above example: 'Main usage' and 'Configuration') you may find that the automatically calculated widths of different groups do not line up, due to varying option name lengths.

You can avoid this by enforcing the alignment of the help text across groups by setting `click.rich_click.STYLE_COMMANDS_TABLE_COLUMN_WIDTH_RATIO = (1, 2)`. This results in a fixed ratio of 1:2 for the width of command name and help text column.

!!! info
    See [`examples/03_groups_sorting.py`](https://github.com/ewels/rich-click/blob/main/examples/03_groups_sorting.py) for a full example.

## Options

To group option flags into two sections with custom names, see the following example:

```python
click.rich_click.OPTION_GROUPS = {
    "mytool": [
        {
            "name": "Simple options",
            "options": ["--name", "--description", "--version", "--help"],
        },
        {
            "name": "Advanced options",
            "options": ["--force", "--yes", "--delete"],
        },
    ]
}
```

If you omit `name` it will use `Commands` (can be configured with `OPTIONS_PANEL_TITLE`).

## Commands

Here we create two groups of commands for the base command of `mytool`.
Any subcommands not listed will automatically be printed in a panel at the end labelled "Commands" as usual.

```python
click.rich_click.COMMAND_GROUPS = {
    "mytool": [
        {
            "name": "Commands for uploading",
            "commands": ["sync", "upload"],
        },
        {
            "name": "Download data",
            "commands": ["get", "fetch", "download"],
        },
    ]
}
```

If you omit `name` it will use `Commands` (can be configured with `COMMANDS_PANEL_TITLE`).

## Multiple commands

If you use multiple nested subcommands, you can specify their commands using the top-level dictionary keys:

```python
click.rich_click.COMMAND_GROUPS = {
    "mytool": [{"commands": ["sync", "auth"]}],
    "mytool sync": [
        {
            "name": "Commands for uploading",
            "commands": ["sync", "upload"],
        },
        {
            "name": "Download data",
            "commands": ["get", "fetch", "download"],
        },
    ],
    "mytool auth": [{"commands": ["login", "logout"]}],
}
```

## Wildcard options

Instead of defining the group based on the command path, you can use wildcards instead:

```python
click.rich_click.COMMAND_GROUPS = {
    "*": [
        {
            "name": "Commands for uploading",
            "commands": ["sync", "upload"],
        }
    ]
}

click.rich_click.OPTION_GROUPS = {
    "*": [
        {
            "name": "Simple options",
            "options": ["--name", "--description", "--version", "--help"],
        },
    ]
}
```

This will apply the groups to every subcommand of the command group.
If a command or option specified in the wildcard does not exist, then it is ignored.

If an option is specified for both a wildcard and explicitly named command, then the wildcard is ignored;
explicit naming always takes precedence.

## Table styling

Typically you would style the option / command tables using the global config options.
However, if you wish you may style tables on a per-group basis using the `table_styles` key:

```python
click.rich_click.COMMAND_GROUPS = {
    "mytool": [
        {
            "commands": ["sync", "auth"],
            "table_styles": {
                "show_lines": True,
                "row_styles": ["magenta", "yellow", "cyan", "green"],
                "border_style": "red",
                "box": "DOUBLE",
            },
        },
    ],
}
```

The available keys are: `show_lines`, `leading`, `box`, `border_style`, `row_styles`, `pad_edge`, `padding`.
