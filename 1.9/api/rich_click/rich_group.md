---
project: "rich-click"
title: "rich_click.rich_group"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_group/"
---

# rich_click.rich_group

*module* · *Added in 1.3.0*

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_group.py#L1-L1)

## rich_click.rich_group.RichGroup

*class* · *Added in 1.3.0*

```python
class RichGroup(RichGroupMixin, RichCommand, Group)
```

Bases: `rich_click.rich_command.RichGroupMixin`, `rich_click.rich_command.RichCommand`, `Group`

Re-exported from: `rich_click.rich_command`

Richly formatted click Group.

Inherits click.Group and overrides help and error methods
to print richly formatted output.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L594-L603)

### rich_click.rich_group.RichGroup.command_class

*attribute* · *Added in 1.3.0* · *class attribute* · *instance attribute*

```python
command_class: type[RichCommand] | None = RichCommand
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L602-L602)

### rich_click.rich_group.RichGroup.group_class

*attribute* · *Added in 1.3.0* · *class attribute* · *instance attribute*

```python
group_class: type[Group] | type[type] | None = type
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L603-L603)

### rich_click.rich_group.RichGroup.aliases

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
aliases: Iterable[str]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L104-L104)

### rich_click.rich_group.RichGroup.context_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
context_class: type[RichContext] = RichContext
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L264-L264)

### rich_click.rich_group.RichGroup.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel: str | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L103-L103)

### rich_click.rich_group.RichGroup.panels

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L102-L102)

### rich_click.rich_group.RichGroup.console

*property* · *Added in 1.7.0*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L126-L126)

### rich_click.rich_group.RichGroup.help_config

*property* · *Added in 1.7.0*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L128-L128)

### rich_click.rich_group.RichGroup.add_command

*method* · *Added in 1.9.0*

```python
def add_command(cmd: click.Command, name: str | None = None, aliases: Iterable[str] | None = None, panel: str | list[str] | None = None) -> None
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L448-L454)

### rich_click.rich_group.RichGroup.format_commands

*method* · *Added in 1.9.0*

```python
def format_commands(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L199-L199)

### rich_click.rich_group.RichGroup.format_help

*method* · *Added in 1.3.0*

```python
def format_help(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L200-L200)

### rich_click.rich_group.RichGroup.get_command

*method* · *Added in 1.9.0*

```python
def get_command(ctx: click.Context, cmd_name: str) -> click.Command | None
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L447-L447)

### rich_click.rich_group.RichGroup.add_command_to_panel

*method*

```python
def add_command_to_panel(command: click.Command, panel_name: str | Iterable[str]) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L580-L591)

### rich_click.rich_group.RichGroup.command

*method*

```python
def command(*args: Any, **kwargs: Any) -> Any
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

A shortcut decorator for declaring and attaching a command to
the group. This takes the same arguments as :func:`command` and
immediately registers the created command with this group by
calling :meth:`add_command`.

To customize the command class used, set the
:attr:`command_class` attribute.

.. versionchanged:: 8.1
    This decorator can be applied without parentheses.

.. versionchanged:: 8.0
    Added the :attr:`command_class` attribute.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L430-L474)

### rich_click.rich_group.RichGroup.group

*method*

```python
def group(*args: Any, **kwargs: Any) -> Any
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

A shortcut decorator for declaring and attaching a group to
the group. This takes the same arguments as :func:`group` and
immediately registers the created group with this group by
calling :meth:`add_command`.

To customize the group class used, set the :attr:`group_class`
attribute.

.. versionchanged:: 8.1
    This decorator can be applied without parentheses.

.. versionchanged:: 8.0
    Added the :attr:`group_class` attribute.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L482-L529)

### rich_click.rich_group.RichGroup.add_panel

*method* · *Added in 1.9.0*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L162-L162)

### rich_click.rich_group.RichGroup.format_epilog

*method* · *Added in 1.8.0*

```python
def format_epilog(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L154-L154)

### rich_click.rich_group.RichGroup.format_help_text

*method* · *Added in 1.8.0*

```python
def format_help_text(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L152-L152)

### rich_click.rich_group.RichGroup.format_options

*method* · *Added in 1.8.0*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L153-L153)

### rich_click.rich_group.RichGroup.get_help_option

*method* · *Added in 1.9.0*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L155-L155)

### rich_click.rich_group.RichGroup.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L156-L161)

### rich_click.rich_group.RichGroup.main

*method* · *Added in 1.3.0*

```python
def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, windows_expand_args: bool = True, **extra: Any) -> Any
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L292-L372)

### rich_click.rich_group.RichGroup.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict(ctx: click.Context) -> dict[str, Any]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L266-L270)
