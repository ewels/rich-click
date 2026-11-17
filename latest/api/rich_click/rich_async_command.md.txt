---
project: "rich-click"
title: "rich_click.rich_async_command"
description: "Rich-formatted command classes for asyncclick."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_async_command/"
---

# rich_click.rich_async_command

*module*

Rich-formatted command classes for asyncclick.

`asyncclick <https://github.com/python-trio/asyncclick>`_ is a fork of click whose
command machinery (``main``/``invoke``/``make_context``/``parse_args``) is asynchronous.
rich-click's formatting behavior lives in baseless mixins (:class:`RichCommandMixin`,
:class:`RichGroupMixin`, :class:`RichContextMixin`), so it composes with asyncclick's
async bases just as it does with click's synchronous ones.

This module is only importable when ``asyncclick`` is installed (``pip install
rich-click[async]``). rich-click's core never imports it, so the dependency stays
optional. Most users do not import these classes directly; instead they call
:func:`rich_click.patch.patch` with ``module=asyncclick`` (see that function), which
installs these classes into the asyncclick namespace so plain ``@asyncclick.command``
CLIs render richly with no further changes.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L1-L1)

## rich_click.rich_async_command.RichAsyncCommand

*class*

```python
class RichAsyncCommand(RichCommandMixin, asyncclick.Command)
```

Bases: `rich_click.rich_command.RichCommandMixin`, `asyncclick.Command`

Richly formatted asyncclick Command.

Combines rich-click's :class:`RichCommandMixin` (help/error formatting) with
asyncclick's asynchronous :class:`asyncclick.Command` (async ``main``/``invoke``).

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L42-L120)

### rich_click.rich_async_command.RichAsyncCommand.context_class

*attribute* · *class attribute* · *instance attribute*

```python
context_class: type[RichAsyncContext] = RichAsyncContext
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L50-L50)

### rich_click.rich_async_command.RichAsyncCommand.aliases

*attribute* · *instance attribute*

```python
aliases: Iterable[str] = aliases or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L84-L84)

### rich_click.rich_async_command.RichAsyncCommand.panel

*attribute* · *instance attribute*

```python
panel: str | list[str] | None = panel
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L82-L82)

### rich_click.rich_async_command.RichAsyncCommand.panels

*attribute* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]] = panels or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L83-L83)

### rich_click.rich_async_command.RichAsyncCommand.console

*property*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Rich Console.

This is a separate instance from the help formatter that allows full control of the
console configuration.

See `rich_config` decorator for how to apply the settings.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L89-L103)

### rich_click.rich_async_command.RichAsyncCommand.help_config

*property*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Rich Help Configuration.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L106-L117)

### rich_click.rich_async_command.RichAsyncCommand.invoke

*method* · *async*

```python
async def invoke(ctx: asyncclick.Context) -> Any
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L99-L101)

### rich_click.rich_async_command.RichAsyncCommand.main

*method* · *async*

```python
async def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, **extra: Any) -> Any
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L79-L91)

### rich_click.rich_async_command.RichAsyncCommand.make_context

*method* · *async*

```python
async def make_context(*args: Any, **kwargs: Any) -> Any
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L95-L97)

### rich_click.rich_async_command.RichAsyncCommand.to_info_dict

*method* · *async*

```python
async def to_info_dict(ctx: asyncclick.Context) -> dict[str, Any]
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L71-L75)

### rich_click.rich_async_command.RichAsyncCommand.add_panel

*method*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Add a RichPanel to the RichCommand.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L222-L224)

### rich_click.rich_async_command.RichAsyncCommand.format_epilog

*method*

```python
def format_epilog(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L206-L209)

### rich_click.rich_async_command.RichAsyncCommand.format_help

*method*

```python
def format_help(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L175-L182)

### rich_click.rich_async_command.RichAsyncCommand.format_help_text

*method*

```python
def format_help_text(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L184-L187)

### rich_click.rich_async_command.RichAsyncCommand.format_options

*method*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L195-L204)

### rich_click.rich_async_command.RichAsyncCommand.get_help_option

*method*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Return the help option object.

Skipped if :attr:`add_help_option` is ``False``.

.. versionchanged:: 8.1.8
    The help option is now cached to avoid creating it multiple times.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L232-L253)

### rich_click.rich_async_command.RichAsyncCommand.get_rich_table_row

*method*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L211-L220)

## rich_click.rich_async_command.RichAsyncCommandCollection

*class*

```python
class RichAsyncCommandCollection(asyncclick.CommandCollection, RichAsyncGroup)
```

Bases: `asyncclick.CommandCollection`, `rich_click.rich_async_command.RichAsyncGroup`

Richly formatted asyncclick CommandCollection.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L136-L137)

### rich_click.rich_async_command.RichAsyncCommandCollection.command_class

*attribute* · *class attribute* · *instance attribute*

```python
command_class: type[RichAsyncCommand] | None = RichAsyncCommand
```

Inherited from: `rich_click.rich_async_command.RichAsyncGroup`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L132-L132)

### rich_click.rich_async_command.RichAsyncCommandCollection.context_class

*attribute* · *class attribute* · *instance attribute*

```python
context_class: type[RichAsyncContext] = RichAsyncContext
```

Inherited from: `rich_click.rich_async_command.RichAsyncGroup`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L131-L131)

### rich_click.rich_async_command.RichAsyncCommandCollection.group_class

*attribute* · *class attribute* · *instance attribute*

```python
group_class: Any | None = type
```

Inherited from: `rich_click.rich_async_command.RichAsyncGroup`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L133-L133)

### rich_click.rich_async_command.RichAsyncCommandCollection.aliases

*attribute* · *instance attribute*

```python
aliases: Iterable[str] = aliases or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L84-L84)

### rich_click.rich_async_command.RichAsyncCommandCollection.panel

*attribute* · *instance attribute*

```python
panel: str | list[str] | None = panel
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L82-L82)

### rich_click.rich_async_command.RichAsyncCommandCollection.panels

*attribute* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]] = panels or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L83-L83)

### rich_click.rich_async_command.RichAsyncCommandCollection.console

*property*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Rich Console.

This is a separate instance from the help formatter that allows full control of the
console configuration.

See `rich_config` decorator for how to apply the settings.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L89-L103)

### rich_click.rich_async_command.RichAsyncCommandCollection.help_config

*property*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Rich Help Configuration.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L106-L117)

### rich_click.rich_async_command.RichAsyncCommandCollection.add_command

*method*

```python
def add_command(cmd: click.Command, name: str | None = None, aliases: Iterable[str] | None = None, panel: str | list[str] | None = None) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

Register another :class:`Command` with this group. If the name
is not provided, the name of the command is used.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L564-L578)

### rich_click.rich_async_command.RichAsyncCommandCollection.add_command_to_panel

*method*

```python
def add_command_to_panel(command: click.Command, panel_name: str | Iterable[str]) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L580-L591)

### rich_click.rich_async_command.RichAsyncCommandCollection.command

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

### rich_click.rich_async_command.RichAsyncCommandCollection.format_commands

*method*

```python
def format_commands(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L404-L406)

### rich_click.rich_async_command.RichAsyncCommandCollection.format_help

*method*

```python
def format_help(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L408-L415)

### rich_click.rich_async_command.RichAsyncCommandCollection.get_command

*method*

```python
def get_command(ctx: click.Context, cmd_name: str) -> click.Command | None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L560-L562)

### rich_click.rich_async_command.RichAsyncCommandCollection.group

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

### rich_click.rich_async_command.RichAsyncCommandCollection.invoke

*method* · *async*

```python
async def invoke(ctx: asyncclick.Context) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L99-L101)

### rich_click.rich_async_command.RichAsyncCommandCollection.main

*method* · *async*

```python
async def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, **extra: Any) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L79-L91)

### rich_click.rich_async_command.RichAsyncCommandCollection.make_context

*method* · *async*

```python
async def make_context(*args: Any, **kwargs: Any) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L95-L97)

### rich_click.rich_async_command.RichAsyncCommandCollection.to_info_dict

*method* · *async*

```python
async def to_info_dict(ctx: asyncclick.Context) -> dict[str, Any]
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L71-L75)

### rich_click.rich_async_command.RichAsyncCommandCollection.add_panel

*method*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Add a RichPanel to the RichCommand.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L222-L224)

### rich_click.rich_async_command.RichAsyncCommandCollection.format_epilog

*method*

```python
def format_epilog(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L206-L209)

### rich_click.rich_async_command.RichAsyncCommandCollection.format_help_text

*method*

```python
def format_help_text(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L184-L187)

### rich_click.rich_async_command.RichAsyncCommandCollection.format_options

*method*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L195-L204)

### rich_click.rich_async_command.RichAsyncCommandCollection.get_help_option

*method*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Return the help option object.

Skipped if :attr:`add_help_option` is ``False``.

.. versionchanged:: 8.1.8
    The help option is now cached to avoid creating it multiple times.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L232-L253)

### rich_click.rich_async_command.RichAsyncCommandCollection.get_rich_table_row

*method*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L211-L220)

## rich_click.rich_async_command.RichAsyncContext

*class*

```python
class RichAsyncContext(RichContextMixin, asyncclick.Context)
```

Bases: `rich_click.rich_context.RichContextMixin`, `asyncclick.Context`

asyncclick Context endowed with rich-click's Rich help formatting.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L38-L39)

### rich_click.rich_async_command.RichAsyncContext.console

*attribute* · *class attribute* · *instance attribute*

```python
console: Console | None = None
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_context.py#L37-L37)

### rich_click.rich_async_command.RichAsyncContext.errors_in_output_format

*attribute* · *class attribute* · *instance attribute*

```python
errors_in_output_format: bool = False
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_context.py#L39-L39)

### rich_click.rich_async_command.RichAsyncContext.export_console_as

*attribute* · *class attribute* · *instance attribute*

```python
export_console_as: Literal['html', 'svg', 'text'] | None = None
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_context.py#L38-L38)

### rich_click.rich_async_command.RichAsyncContext.formatter_class

*attribute* · *class attribute* · *instance attribute*

```python
formatter_class: type[RichHelpFormatter] = RichHelpFormatter
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_context.py#L36-L36)

### rich_click.rich_async_command.RichAsyncContext.help_config

*attribute* · *instance attribute*

```python
help_config = parent.help_config
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_context.py#L92-L92)

### rich_click.rich_async_command.RichAsyncContext.help_to_stderr

*attribute* · *class attribute* · *instance attribute*

```python
help_to_stderr: bool = False
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_context.py#L40-L40)

### rich_click.rich_async_command.RichAsyncContext.make_formatter

*method*

```python
def make_formatter(error_mode: bool = False) -> RichHelpFormatter
```

Inherited from: `rich_click.rich_context.RichContextMixin`

Create the Rich Help Formatter.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_context.py#L107-L116)

## rich_click.rich_async_command.RichAsyncGroup

*class*

```python
class RichAsyncGroup(RichGroupMixin, RichAsyncCommand, asyncclick.Group)
```

Bases: `rich_click.rich_command.RichGroupMixin`, `rich_click.rich_async_command.RichAsyncCommand`, `asyncclick.Group`

Richly formatted asyncclick Group.

Subcommands and subgroups created from this group inherit the async rich classes
via ``command_class``/``group_class``, so the whole command tree renders richly.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L123-L133)

### rich_click.rich_async_command.RichAsyncGroup.command_class

*attribute* · *class attribute* · *instance attribute*

```python
command_class: type[RichAsyncCommand] | None = RichAsyncCommand
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L132-L132)

### rich_click.rich_async_command.RichAsyncGroup.context_class

*attribute* · *class attribute* · *instance attribute*

```python
context_class: type[RichAsyncContext] = RichAsyncContext
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L131-L131)

### rich_click.rich_async_command.RichAsyncGroup.group_class

*attribute* · *class attribute* · *instance attribute*

```python
group_class: Any | None = type
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L133-L133)

### rich_click.rich_async_command.RichAsyncGroup.aliases

*attribute* · *instance attribute*

```python
aliases: Iterable[str] = aliases or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L84-L84)

### rich_click.rich_async_command.RichAsyncGroup.panel

*attribute* · *instance attribute*

```python
panel: str | list[str] | None = panel
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L82-L82)

### rich_click.rich_async_command.RichAsyncGroup.panels

*attribute* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]] = panels or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L83-L83)

### rich_click.rich_async_command.RichAsyncGroup.console

*property*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Rich Console.

This is a separate instance from the help formatter that allows full control of the
console configuration.

See `rich_config` decorator for how to apply the settings.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L89-L103)

### rich_click.rich_async_command.RichAsyncGroup.help_config

*property*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Rich Help Configuration.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L106-L117)

### rich_click.rich_async_command.RichAsyncGroup.add_command

*method*

```python
def add_command(cmd: click.Command, name: str | None = None, aliases: Iterable[str] | None = None, panel: str | list[str] | None = None) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

Register another :class:`Command` with this group. If the name
is not provided, the name of the command is used.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L564-L578)

### rich_click.rich_async_command.RichAsyncGroup.add_command_to_panel

*method*

```python
def add_command_to_panel(command: click.Command, panel_name: str | Iterable[str]) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L580-L591)

### rich_click.rich_async_command.RichAsyncGroup.command

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

### rich_click.rich_async_command.RichAsyncGroup.format_commands

*method*

```python
def format_commands(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L404-L406)

### rich_click.rich_async_command.RichAsyncGroup.format_help

*method*

```python
def format_help(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L408-L415)

### rich_click.rich_async_command.RichAsyncGroup.get_command

*method*

```python
def get_command(ctx: click.Context, cmd_name: str) -> click.Command | None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L560-L562)

### rich_click.rich_async_command.RichAsyncGroup.group

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

### rich_click.rich_async_command.RichAsyncGroup.invoke

*method* · *async*

```python
async def invoke(ctx: asyncclick.Context) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L99-L101)

### rich_click.rich_async_command.RichAsyncGroup.main

*method* · *async*

```python
async def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, **extra: Any) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L79-L91)

### rich_click.rich_async_command.RichAsyncGroup.make_context

*method* · *async*

```python
async def make_context(*args: Any, **kwargs: Any) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L95-L97)

### rich_click.rich_async_command.RichAsyncGroup.to_info_dict

*method* · *async*

```python
async def to_info_dict(ctx: asyncclick.Context) -> dict[str, Any]
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_async_command.py#L71-L75)

### rich_click.rich_async_command.RichAsyncGroup.add_panel

*method*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Add a RichPanel to the RichCommand.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L222-L224)

### rich_click.rich_async_command.RichAsyncGroup.format_epilog

*method*

```python
def format_epilog(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L206-L209)

### rich_click.rich_async_command.RichAsyncGroup.format_help_text

*method*

```python
def format_help_text(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L184-L187)

### rich_click.rich_async_command.RichAsyncGroup.format_options

*method*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L195-L204)

### rich_click.rich_async_command.RichAsyncGroup.get_help_option

*method*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Return the help option object.

Skipped if :attr:`add_help_option` is ``False``.

.. versionchanged:: 8.1.8
    The help option is now cached to avoid creating it multiple times.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L232-L253)

### rich_click.rich_async_command.RichAsyncGroup.get_rich_table_row

*method*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_command.py#L211-L220)
