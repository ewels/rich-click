---
project: "rich-click"
title: "rich_click.rich_command"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_command/"
---

# rich_click.rich_command

*module* · *Added in 1.3.0*

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L1-L1)

## rich_click.rich_command.C

*attribute* · *Added in 1.9.0* · *module attribute*

```python
C = TypeVar('C', bound=click.Command)
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L27-L27)

## rich_click.rich_command.G

*attribute* · *Added in 1.9.0* · *module attribute*

```python
G = TypeVar('G', bound=click.Group)
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L28-L28)

## rich_click.rich_command.OVERRIDES_GUARD

*attribute* · *Added in 1.8.0* · *module attribute*

```python
OVERRIDES_GUARD: bool = False
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L50-L50)

## rich_click.rich_command.RichCommand

*class* · *Added in 1.3.0*

```python
class RichCommand(RichCommandMixin, Command)
```

Bases: `rich_click.rich_command.RichCommandMixin`, `Command`

Richly formatted click Command.

Inherits click.Command and overrides help and error methods
to print richly formatted output.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L256-L372)

### rich_click.rich_command.RichCommand.aliases

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
aliases: Iterable[str]
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L104-L104)

### rich_click.rich_command.RichCommand.context_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
context_class: type[RichContext] = RichContext
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L264-L264)

### rich_click.rich_command.RichCommand.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel: str | None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L103-L103)

### rich_click.rich_command.RichCommand.panels

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]]
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L102-L102)

### rich_click.rich_command.RichCommand.console

*property* · *Added in 1.7.0*

```python
console: Console | None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L126-L126)

### rich_click.rich_command.RichCommand.help_config

*property* · *Added in 1.7.0*

```python
help_config: RichHelpConfiguration | None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L128-L128)

### rich_click.rich_command.RichCommand.add_panel

*method* · *Added in 1.9.0*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L162-L162)

### rich_click.rich_command.RichCommand.format_epilog

*method* · *Added in 1.8.0*

```python
def format_epilog(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L154-L154)

### rich_click.rich_command.RichCommand.format_help

*method* · *Added in 1.3.0*

```python
def format_help(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L151-L151)

### rich_click.rich_command.RichCommand.format_help_text

*method* · *Added in 1.8.0*

```python
def format_help_text(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L152-L152)

### rich_click.rich_command.RichCommand.format_options

*method* · *Added in 1.8.0*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L153-L153)

### rich_click.rich_command.RichCommand.get_help_option

*method* · *Added in 1.9.0*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L155-L155)

### rich_click.rich_command.RichCommand.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L156-L161)

### rich_click.rich_command.RichCommand.main

*method* · *Added in 1.3.0*

```python
def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, windows_expand_args: bool = True, **extra: Any) -> Any
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L292-L372)

### rich_click.rich_command.RichCommand.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict(ctx: click.Context) -> dict[str, Any]
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L266-L270)

## rich_click.rich_command.RichCommandCollection

*class* · *Added in 1.7.0*

```python
class RichCommandCollection(CommandCollection, RichGroup)
```

Bases: `CommandCollection`, `rich_click.rich_command.RichGroup`

Richly formatted click CommandCollection.

Inherits click.CommandCollection and overrides help and error methods
to print richly formatted output.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L609-L624)

### rich_click.rich_command.RichCommandCollection.command_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
command_class: type[RichCommand] | None = RichCommand
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L602-L602)

### rich_click.rich_command.RichCommandCollection.group_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
group_class: type[Group] | type[type] | None = type
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L603-L603)

### rich_click.rich_command.RichCommandCollection.aliases

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
aliases: Iterable[str]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L104-L104)

### rich_click.rich_command.RichCommandCollection.context_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
context_class: type[RichContext] = RichContext
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L264-L264)

### rich_click.rich_command.RichCommandCollection.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel: str | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L103-L103)

### rich_click.rich_command.RichCommandCollection.panels

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L102-L102)

### rich_click.rich_command.RichCommandCollection.console

*property* · *Added in 1.7.0*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L126-L126)

### rich_click.rich_command.RichCommandCollection.help_config

*property* · *Added in 1.7.0*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L128-L128)

### rich_click.rich_command.RichCommandCollection.format_help

*method* · *Added in 1.8.0*

```python
def format_help(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L617-L624)

### rich_click.rich_command.RichCommandCollection.add_command

*method* · *Added in 1.9.0*

```python
def add_command(cmd: click.Command, name: str | None = None, aliases: Iterable[str] | None = None, panel: str | list[str] | None = None) -> None
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L448-L454)

### rich_click.rich_command.RichCommandCollection.format_commands

*method* · *Added in 1.9.0*

```python
def format_commands(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L199-L199)

### rich_click.rich_command.RichCommandCollection.get_command

*method* · *Added in 1.9.0*

```python
def get_command(ctx: click.Context, cmd_name: str) -> click.Command | None
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L447-L447)

### rich_click.rich_command.RichCommandCollection.add_command_to_panel

*method*

```python
def add_command_to_panel(command: click.Command, panel_name: str | Iterable[str]) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L580-L591)

### rich_click.rich_command.RichCommandCollection.command

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

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L430-L474)

### rich_click.rich_command.RichCommandCollection.group

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

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L482-L529)

### rich_click.rich_command.RichCommandCollection.add_panel

*method* · *Added in 1.9.0*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L162-L162)

### rich_click.rich_command.RichCommandCollection.format_epilog

*method* · *Added in 1.8.0*

```python
def format_epilog(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L154-L154)

### rich_click.rich_command.RichCommandCollection.format_help_text

*method* · *Added in 1.8.0*

```python
def format_help_text(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L152-L152)

### rich_click.rich_command.RichCommandCollection.format_options

*method* · *Added in 1.8.0*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L153-L153)

### rich_click.rich_command.RichCommandCollection.get_help_option

*method* · *Added in 1.9.0*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L155-L155)

### rich_click.rich_command.RichCommandCollection.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L156-L161)

### rich_click.rich_command.RichCommandCollection.main

*method* · *Added in 1.3.0*

```python
def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, windows_expand_args: bool = True, **extra: Any) -> Any
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L292-L372)

### rich_click.rich_command.RichCommandCollection.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict(ctx: click.Context) -> dict[str, Any]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L266-L270)

## rich_click.rich_command.RichCommandMixin

*class*

```python
class RichCommandMixin(_CommandMixinBase)
```

Bases: `_CommandMixinBase`

Mixin providing Rich help-formatting behavior for click Commands.

Contains only formatting/help behavior and Rich-specific instance state, with
no click base of its own, so it can be composed with either ``click.Command``
(see :class:`RichCommand`) or a click-compatible fork's Command (e.g.
``asyncclick.Command``) without dragging click's synchronous execution methods
(``main``, ``make_context``, ``scope``, etc.) into the MRO.

Execution-flow methods (``main`` and ``to_info_dict``) deliberately live on the
concrete :class:`RichCommand` instead of here, so that async forks can inherit
their own async equivalents. Help and error formatting, including
:meth:`get_help_option` and :meth:`_error_formatter`, is shared here.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L53-L253)

### rich_click.rich_command.RichCommandMixin.aliases

*attribute* · *instance attribute*

```python
aliases: Iterable[str] = aliases or []
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L84-L84)

### rich_click.rich_command.RichCommandMixin.context_class

*attribute* · *instance attribute*

```python
context_class: type[Any]
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L70-L70)

### rich_click.rich_command.RichCommandMixin.panel

*attribute* · *instance attribute*

```python
panel: str | list[str] | None = panel
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L82-L82)

### rich_click.rich_command.RichCommandMixin.panels

*attribute* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]] = panels or []
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L83-L83)

### rich_click.rich_command.RichCommandMixin.console

*property*

```python
console: Console | None
```

Rich Console.

This is a separate instance from the help formatter that allows full control of the
console configuration.

See `rich_config` decorator for how to apply the settings.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L89-L103)

### rich_click.rich_command.RichCommandMixin.help_config

*property*

```python
help_config: RichHelpConfiguration | None
```

Rich Help Configuration.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L106-L117)

### rich_click.rich_command.RichCommandMixin.add_panel

*method*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Add a RichPanel to the RichCommand.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L222-L224)

### rich_click.rich_command.RichCommandMixin.format_epilog

*method*

```python
def format_epilog(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L206-L209)

### rich_click.rich_command.RichCommandMixin.format_help

*method*

```python
def format_help(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L175-L182)

### rich_click.rich_command.RichCommandMixin.format_help_text

*method*

```python
def format_help_text(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L184-L187)

### rich_click.rich_command.RichCommandMixin.format_options

*method*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L195-L204)

### rich_click.rich_command.RichCommandMixin.get_help_option

*method*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Return the help option object.

Skipped if :attr:`add_help_option` is ``False``.

.. versionchanged:: 8.1.8
    The help option is now cached to avoid creating it multiple times.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L232-L253)

### rich_click.rich_command.RichCommandMixin.get_rich_table_row

*method*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L211-L220)

## rich_click.rich_command.RichGroup

*class* · *Added in 1.7.0*

```python
class RichGroup(RichGroupMixin, RichCommand, Group)
```

Bases: `rich_click.rich_command.RichGroupMixin`, `rich_click.rich_command.RichCommand`, `Group`

Richly formatted click Group.

Inherits click.Group and overrides help and error methods
to print richly formatted output.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L594-L603)

### rich_click.rich_command.RichGroup.command_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
command_class: type[RichCommand] | None = RichCommand
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L602-L602)

### rich_click.rich_command.RichGroup.group_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
group_class: type[Group] | type[type] | None = type
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L603-L603)

### rich_click.rich_command.RichGroup.aliases

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
aliases: Iterable[str]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L104-L104)

### rich_click.rich_command.RichGroup.context_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
context_class: type[RichContext] = RichContext
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L264-L264)

### rich_click.rich_command.RichGroup.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel: str | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L103-L103)

### rich_click.rich_command.RichGroup.panels

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L102-L102)

### rich_click.rich_command.RichGroup.console

*property* · *Added in 1.7.0*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L126-L126)

### rich_click.rich_command.RichGroup.help_config

*property* · *Added in 1.7.0*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L128-L128)

### rich_click.rich_command.RichGroup.add_command

*method* · *Added in 1.9.0*

```python
def add_command(cmd: click.Command, name: str | None = None, aliases: Iterable[str] | None = None, panel: str | list[str] | None = None) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L448-L454)

### rich_click.rich_command.RichGroup.format_commands

*method* · *Added in 1.9.0*

```python
def format_commands(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L199-L199)

### rich_click.rich_command.RichGroup.format_help

*method* · *Added in 1.8.0*

```python
def format_help(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L200-L200)

### rich_click.rich_command.RichGroup.get_command

*method* · *Added in 1.9.0*

```python
def get_command(ctx: click.Context, cmd_name: str) -> click.Command | None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L447-L447)

### rich_click.rich_command.RichGroup.add_command_to_panel

*method* · *Added in 1.9.0*

```python
def add_command_to_panel(command: click.Command, panel_name: str | Iterable[str]) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L580-L591)

### rich_click.rich_command.RichGroup.command

*method* · *Added in 1.7.0*

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

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L430-L474)

### rich_click.rich_command.RichGroup.group

*method* · *Added in 1.7.0*

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

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L482-L529)

### rich_click.rich_command.RichGroup.add_panel

*method* · *Added in 1.9.0*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L162-L162)

### rich_click.rich_command.RichGroup.format_epilog

*method* · *Added in 1.8.0*

```python
def format_epilog(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L154-L154)

### rich_click.rich_command.RichGroup.format_help_text

*method* · *Added in 1.8.0*

```python
def format_help_text(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L152-L152)

### rich_click.rich_command.RichGroup.format_options

*method* · *Added in 1.8.0*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L153-L153)

### rich_click.rich_command.RichGroup.get_help_option

*method* · *Added in 1.9.0*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L155-L155)

### rich_click.rich_command.RichGroup.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L156-L161)

### rich_click.rich_command.RichGroup.main

*method* · *Added in 1.3.0*

```python
def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, windows_expand_args: bool = True, **extra: Any) -> Any
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L292-L372)

### rich_click.rich_command.RichGroup.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict(ctx: click.Context) -> dict[str, Any]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L266-L270)

## rich_click.rich_command.RichGroupMixin

*class*

```python
class RichGroupMixin(RichCommandMixin, _GroupMixinBase)
```

Bases: `rich_click.rich_command.RichCommandMixin`, `_GroupMixinBase`

Mixin providing Rich help-formatting behavior for click Groups.

Like :class:`RichCommandMixin`, this has no click base of its own so it can be
composed with either ``click.Group`` (see :class:`RichGroup`) or a fork's Group.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L375-L591)

### rich_click.rich_command.RichGroupMixin.command_class

*attribute* · *instance attribute*

```python
command_class: type[click.Command] | None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L72-L72)

### rich_click.rich_command.RichGroupMixin.group_class

*attribute* · *instance attribute*

```python
group_class: type[click.Group] | type[type] | None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L73-L73)

### rich_click.rich_command.RichGroupMixin.aliases

*attribute* · *instance attribute*

```python
aliases: Iterable[str] = aliases or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L84-L84)

### rich_click.rich_command.RichGroupMixin.context_class

*attribute* · *instance attribute*

```python
context_class: type[Any]
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L70-L70)

### rich_click.rich_command.RichGroupMixin.panel

*attribute* · *instance attribute*

```python
panel: str | list[str] | None = panel
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L82-L82)

### rich_click.rich_command.RichGroupMixin.panels

*attribute* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]] = panels or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L83-L83)

### rich_click.rich_command.RichGroupMixin.console

*property*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Rich Console.

This is a separate instance from the help formatter that allows full control of the
console configuration.

See `rich_config` decorator for how to apply the settings.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L89-L103)

### rich_click.rich_command.RichGroupMixin.help_config

*property*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Rich Help Configuration.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L106-L117)

### rich_click.rich_command.RichGroupMixin.add_command

*method*

```python
def add_command(cmd: click.Command, name: str | None = None, aliases: Iterable[str] | None = None, panel: str | list[str] | None = None) -> None
```

Register another :class:`Command` with this group. If the name
is not provided, the name of the command is used.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L564-L578)

### rich_click.rich_command.RichGroupMixin.add_command_to_panel

*method*

```python
def add_command_to_panel(command: click.Command, panel_name: str | Iterable[str]) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L580-L591)

### rich_click.rich_command.RichGroupMixin.command

*method*

```python
def command(*args: Any, **kwargs: Any) -> Any
```

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

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L430-L474)

### rich_click.rich_command.RichGroupMixin.format_commands

*method*

```python
def format_commands(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L404-L406)

### rich_click.rich_command.RichGroupMixin.format_help

*method*

```python
def format_help(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L408-L415)

### rich_click.rich_command.RichGroupMixin.get_command

*method*

```python
def get_command(ctx: click.Context, cmd_name: str) -> click.Command | None
```

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L560-L562)

### rich_click.rich_command.RichGroupMixin.group

*method*

```python
def group(*args: Any, **kwargs: Any) -> Any
```

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

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L482-L529)

### rich_click.rich_command.RichGroupMixin.add_panel

*method*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Add a RichPanel to the RichCommand.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L222-L224)

### rich_click.rich_command.RichGroupMixin.format_epilog

*method*

```python
def format_epilog(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L206-L209)

### rich_click.rich_command.RichGroupMixin.format_help_text

*method*

```python
def format_help_text(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L184-L187)

### rich_click.rich_command.RichGroupMixin.format_options

*method*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L195-L204)

### rich_click.rich_command.RichGroupMixin.get_help_option

*method*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Return the help option object.

Skipped if :attr:`add_help_option` is ``False``.

.. versionchanged:: 8.1.8
    The help option is now cached to avoid creating it multiple times.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L232-L253)

### rich_click.rich_command.RichGroupMixin.get_rich_table_row

*method*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L211-L220)

## rich_click.rich_command.RichMultiCommand

*class* · *Added in 1.7.0*

```python
class RichMultiCommand(RichGroup, click.CommandCollection)
```

Bases: `rich_click.rich_command.RichGroup`, `click.CommandCollection`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L463-L464)

### rich_click.rich_command.RichMultiCommand.command_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
command_class: type[RichCommand] | None = RichCommand
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L602-L602)

### rich_click.rich_command.RichMultiCommand.group_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
group_class: type[Group] | type[type] | None = type
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L603-L603)

### rich_click.rich_command.RichMultiCommand.aliases

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
aliases: Iterable[str]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L104-L104)

### rich_click.rich_command.RichMultiCommand.context_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
context_class: type[RichContext] = RichContext
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L264-L264)

### rich_click.rich_command.RichMultiCommand.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel: str | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L103-L103)

### rich_click.rich_command.RichMultiCommand.panels

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L102-L102)

### rich_click.rich_command.RichMultiCommand.console

*property* · *Added in 1.7.0*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L126-L126)

### rich_click.rich_command.RichMultiCommand.help_config

*property* · *Added in 1.7.0*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L128-L128)

### rich_click.rich_command.RichMultiCommand.add_command

*method* · *Added in 1.9.0*

```python
def add_command(cmd: click.Command, name: str | None = None, aliases: Iterable[str] | None = None, panel: str | list[str] | None = None) -> None
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L448-L454)

### rich_click.rich_command.RichMultiCommand.format_commands

*method* · *Added in 1.8.0*

```python
def format_commands(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L199-L199)

### rich_click.rich_command.RichMultiCommand.format_help

*method* · *Added in 1.8.0*

```python
def format_help(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L200-L200)

### rich_click.rich_command.RichMultiCommand.get_command

*method* · *Added in 1.9.0*

```python
def get_command(ctx: click.Context, cmd_name: str) -> click.Command | None
```

Inherited from: `rich_click.rich_command.RichGroup`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L447-L447)

### rich_click.rich_command.RichMultiCommand.add_command_to_panel

*method*

```python
def add_command_to_panel(command: click.Command, panel_name: str | Iterable[str]) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L580-L591)

### rich_click.rich_command.RichMultiCommand.command

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

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L430-L474)

### rich_click.rich_command.RichMultiCommand.group

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

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L482-L529)

### rich_click.rich_command.RichMultiCommand.add_panel

*method* · *Added in 1.9.0*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L162-L162)

### rich_click.rich_command.RichMultiCommand.format_epilog

*method* · *Added in 1.8.0*

```python
def format_epilog(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L154-L154)

### rich_click.rich_command.RichMultiCommand.format_help_text

*method* · *Added in 1.8.0*

```python
def format_help_text(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L152-L152)

### rich_click.rich_command.RichMultiCommand.format_options

*method* · *Added in 1.8.0*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L153-L153)

### rich_click.rich_command.RichMultiCommand.get_help_option

*method* · *Added in 1.9.0*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L155-L155)

### rich_click.rich_command.RichMultiCommand.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L156-L161)

### rich_click.rich_command.RichMultiCommand.main

*method* · *Added in 1.3.0*

```python
def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, windows_expand_args: bool = True, **extra: Any) -> Any
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L292-L372)

### rich_click.rich_command.RichMultiCommand.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict(ctx: click.Context) -> dict[str, Any]
```

Inherited from: `rich_click.rich_command.RichCommand`

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L266-L270)

## rich_click.rich_command.prevent_incompatible_overrides

*function* · *Added in 1.8.0*

```python
def prevent_incompatible_overrides(cmd: RichCommandMixin, class_name: str, ctx: RichContext, formatter: RichHelpFormatter) -> None
```

For use by the rich-click CLI.

[View source](https://github.com/ewels/rich-click/blob/a968231b54ca97b6b99dbd23dfac04a17163557a/src/rich_click/rich_command.py#L627-L640)
