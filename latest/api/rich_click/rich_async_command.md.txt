---
project: "rich-click"
title: "rich_click.rich_async_command"
description: "Rich-formatted command classes for asyncclick."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_async_command/"
---

# rich_click.rich_async_command

*module*

Rich-formatted command classes for asyncclick.

[asyncclick](https://github.com/python-trio/asyncclick) is a fork of click with async command
methods (`main`, `invoke`, `make_context` and `parse_args`). The rich-click mixins
(`RichCommandMixin`, `RichGroupMixin` and `RichContextMixin`) have no click base class, so these
classes combine them with the asyncclick classes.

Most code does not import these classes. Call `rich_click.patch.patch(module=asyncclick)` instead.
It puts these classes into the asyncclick namespace, so `@asyncclick.command` CLIs get rich-click help.

> **Note**
>
> This module needs asyncclick: install `rich-click[async]`. The rest of rich-click never imports it.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L1-L1)

## rich_click.rich_async_command.RichAsyncCommand

*class*

```python
class RichAsyncCommand(RichCommandMixin, asyncclick.Command)
```

Bases: `rich_click.rich_command.RichCommandMixin`, `asyncclick.Command`

Richly formatted asyncclick Command.

Combines the help and error formatting of `RichCommandMixin` with the
asynchronous `asyncclick.Command` (async `main` and `invoke`).

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L40-L118)

### rich_click.rich_async_command.RichAsyncCommand.context_class

*attribute* · *class attribute* · *instance attribute*

```python
context_class: type[RichAsyncContext] = RichAsyncContext
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L48-L48)

### rich_click.rich_async_command.RichAsyncCommand.aliases

*attribute* · *instance attribute*

```python
aliases: Iterable[str] = aliases or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L84-L84)

### rich_click.rich_async_command.RichAsyncCommand.panel

*attribute* · *instance attribute*

```python
panel: str | list[str] | None = panel
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L82-L82)

### rich_click.rich_async_command.RichAsyncCommand.panels

*attribute* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]] = panels or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L83-L83)

### rich_click.rich_async_command.RichAsyncCommand.console

*property*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

**Deprecated**: Since 1.9. Use the console of the context, `ctx.console`.

Rich console of this command. Set it with the `rich_config` decorator.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L89-L101)

### rich_click.rich_async_command.RichAsyncCommand.help_config

*property*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

**Deprecated**: Since 1.8. Use the help configuration of the context, `ctx.help_config`.

Help configuration of this command. Set it with the `rich_config` decorator.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L104-L120)

### rich_click.rich_async_command.RichAsyncCommand.invoke

*method* · *async*

```python
async def invoke(ctx: asyncclick.Context) -> Any
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L97-L99)

### rich_click.rich_async_command.RichAsyncCommand.main

*method* · *async*

```python
async def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, **extra: Any) -> Any
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L77-L89)

### rich_click.rich_async_command.RichAsyncCommand.make_context

*method* · *async*

```python
async def make_context(*args: Any, **kwargs: Any) -> Any
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L93-L95)

### rich_click.rich_async_command.RichAsyncCommand.to_info_dict

*method* · *async*

```python
async def to_info_dict(ctx: asyncclick.Context) -> dict[str, Any]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L69-L73)

### rich_click.rich_async_command.RichAsyncCommand.add_panel

*method*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Add a RichPanel to the RichCommand.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L236-L238)

### rich_click.rich_async_command.RichAsyncCommand.format_epilog

*method*

```python
def format_epilog(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L220-L223)

### rich_click.rich_async_command.RichAsyncCommand.format_help

*method*

```python
def format_help(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Write the help: the usage, the help text, the options and the epilog.

Each part has its own `format_*` method, so a subclass can override one part.

> **Warning**
>
> After `rich_click.patch.patch()`, rich-click ignores overrides of `format_usage`,
> `format_help_text`, `format_options` and `format_epilog` in subclasses of the patched
> click classes. These overrides expect click's plain help formatter, so rich-click
> writes those parts itself.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L178-L196)

### rich_click.rich_async_command.RichAsyncCommand.format_help_text

*method*

```python
def format_help_text(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L198-L201)

### rich_click.rich_async_command.RichAsyncCommand.format_options

*method*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L209-L218)

### rich_click.rich_async_command.RichAsyncCommand.get_help_option

*method*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Return the help option, or `None` if `add_help_option` is false. Every call returns the same object.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L246-L260)

### rich_click.rich_async_command.RichAsyncCommand.get_rich_table_row

*method*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L225-L234)

## rich_click.rich_async_command.RichAsyncCommandCollection

*class*

```python
class RichAsyncCommandCollection(asyncclick.CommandCollection, RichAsyncGroup)
```

Bases: `asyncclick.CommandCollection`, `rich_click.rich_async_command.RichAsyncGroup`

Richly formatted asyncclick CommandCollection.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L134-L135)

### rich_click.rich_async_command.RichAsyncCommandCollection.command_class

*attribute* · *class attribute* · *instance attribute*

```python
command_class: type[RichAsyncCommand] | None = RichAsyncCommand
```

Inherited from: `rich_click.rich_async_command.RichAsyncGroup`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L130-L130)

### rich_click.rich_async_command.RichAsyncCommandCollection.context_class

*attribute* · *class attribute* · *instance attribute*

```python
context_class: type[RichAsyncContext] = RichAsyncContext
```

Inherited from: `rich_click.rich_async_command.RichAsyncGroup`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L129-L129)

### rich_click.rich_async_command.RichAsyncCommandCollection.group_class

*attribute* · *class attribute* · *instance attribute*

```python
group_class: Any | None = type
```

Inherited from: `rich_click.rich_async_command.RichAsyncGroup`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L131-L131)

### rich_click.rich_async_command.RichAsyncCommandCollection.aliases

*attribute* · *instance attribute*

```python
aliases: Iterable[str] = aliases or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L84-L84)

### rich_click.rich_async_command.RichAsyncCommandCollection.panel

*attribute* · *instance attribute*

```python
panel: str | list[str] | None = panel
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L82-L82)

### rich_click.rich_async_command.RichAsyncCommandCollection.panels

*attribute* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]] = panels or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L83-L83)

### rich_click.rich_async_command.RichAsyncCommandCollection.console

*property*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

**Deprecated**: Since 1.9. Use the console of the context, `ctx.console`.

Rich console of this command. Set it with the `rich_config` decorator.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L89-L101)

### rich_click.rich_async_command.RichAsyncCommandCollection.help_config

*property*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

**Deprecated**: Since 1.8. Use the help configuration of the context, `ctx.help_config`.

Help configuration of this command. Set it with the `rich_config` decorator.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L104-L120)

### rich_click.rich_async_command.RichAsyncCommandCollection.add_command

*method*

```python
def add_command(cmd: click.Command, name: str | None = None, aliases: Iterable[str] | None = None, panel: str | list[str] | None = None) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

Add a command to this group.

**Parameters**

- `cmd` (`click.Command`) — The command to add.
- `name` (`str | None`) (default: `None`) — Name of the command in this group. Defaults to the name of the command.
- `aliases` (`Iterable[str] | None`) (default: `None`) — Other names that run the command, in addition to the aliases of the command.
- `panel` (`str | list[str] | None`) (default: `None`) — Panel or panels to show the command in, by panel title.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L548-L565)

### rich_click.rich_async_command.RichAsyncCommandCollection.add_command_to_panel

*method*

```python
def add_command_to_panel(command: click.Command, panel_name: str | Iterable[str]) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L567-L577)

### rich_click.rich_async_command.RichAsyncCommandCollection.command

*method*

```python
def command(*args: Any, **kwargs: Any) -> Any
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

Create a command and add it to this group.

Takes the same arguments as the `command` decorator, and works with or without
parentheses. The class of the command is `command_class`, unless you set `cls`.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L432-L467)

### rich_click.rich_async_command.RichAsyncCommandCollection.format_commands

*method*

```python
def format_commands(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L406-L408)

### rich_click.rich_async_command.RichAsyncCommandCollection.format_help

*method*

```python
def format_help(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L410-L417)

### rich_click.rich_async_command.RichAsyncCommandCollection.get_command

*method*

```python
def get_command(ctx: click.Context, cmd_name: str) -> click.Command | None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L544-L546)

### rich_click.rich_async_command.RichAsyncCommandCollection.group

*method*

```python
def group(*args: Any, **kwargs: Any) -> Any
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

Create a subgroup and add it to this group.

Takes the same arguments as the `group` decorator, and works with or without
parentheses. The subgroup has the same class as this group, unless you set `group_class` or `cls`.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L475-L513)

### rich_click.rich_async_command.RichAsyncCommandCollection.invoke

*method* · *async*

```python
async def invoke(ctx: asyncclick.Context) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L97-L99)

### rich_click.rich_async_command.RichAsyncCommandCollection.main

*method* · *async*

```python
async def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, **extra: Any) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L77-L89)

### rich_click.rich_async_command.RichAsyncCommandCollection.make_context

*method* · *async*

```python
async def make_context(*args: Any, **kwargs: Any) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L93-L95)

### rich_click.rich_async_command.RichAsyncCommandCollection.to_info_dict

*method* · *async*

```python
async def to_info_dict(ctx: asyncclick.Context) -> dict[str, Any]
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L69-L73)

### rich_click.rich_async_command.RichAsyncCommandCollection.add_panel

*method*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Add a RichPanel to the RichCommand.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L236-L238)

### rich_click.rich_async_command.RichAsyncCommandCollection.format_epilog

*method*

```python
def format_epilog(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L220-L223)

### rich_click.rich_async_command.RichAsyncCommandCollection.format_help_text

*method*

```python
def format_help_text(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L198-L201)

### rich_click.rich_async_command.RichAsyncCommandCollection.format_options

*method*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L209-L218)

### rich_click.rich_async_command.RichAsyncCommandCollection.get_help_option

*method*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Return the help option, or `None` if `add_help_option` is false. Every call returns the same object.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L246-L260)

### rich_click.rich_async_command.RichAsyncCommandCollection.get_rich_table_row

*method*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L225-L234)

## rich_click.rich_async_command.RichAsyncContext

*class*

```python
class RichAsyncContext(RichContextMixin, asyncclick.Context)
```

Bases: `rich_click.rich_context.RichContextMixin`, `asyncclick.Context`

An asyncclick Context that formats help and errors with Rich.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L36-L37)

### rich_click.rich_async_command.RichAsyncContext.console

*attribute* · *class attribute* · *instance attribute*

```python
console: Console | None = None
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L39-L39)

### rich_click.rich_async_command.RichAsyncContext.errors_in_output_format

*attribute* · *class attribute* · *instance attribute*

```python
errors_in_output_format: bool = False
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L41-L41)

### rich_click.rich_async_command.RichAsyncContext.export_console_as

*attribute* · *class attribute* · *instance attribute*

```python
export_console_as: Literal['html', 'svg', 'text'] | None = None
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L40-L40)

### rich_click.rich_async_command.RichAsyncContext.formatter_class

*attribute* · *class attribute* · *instance attribute*

```python
formatter_class: type[RichHelpFormatter] = RichHelpFormatter
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L38-L38)

### rich_click.rich_async_command.RichAsyncContext.help_config

*attribute* · *instance attribute*

```python
help_config = parent.help_config
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L93-L93)

### rich_click.rich_async_command.RichAsyncContext.help_to_stderr

*attribute* · *class attribute* · *instance attribute*

```python
help_to_stderr: bool = False
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L42-L42)

### rich_click.rich_async_command.RichAsyncContext.make_formatter

*method*

```python
def make_formatter(error_mode: bool = False) -> RichHelpFormatter
```

Inherited from: `rich_click.rich_context.RichContextMixin`

Create the Rich Help Formatter.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L108-L117)

## rich_click.rich_async_command.RichAsyncGroup

*class*

```python
class RichAsyncGroup(RichGroupMixin, RichAsyncCommand, asyncclick.Group)
```

Bases: `rich_click.rich_command.RichGroupMixin`, `rich_click.rich_async_command.RichAsyncCommand`, `asyncclick.Group`

Richly formatted asyncclick Group.

Subcommands and subgroups created from this group inherit the async rich classes
via `command_class` and `group_class`, so the whole command tree renders richly.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L121-L131)

### rich_click.rich_async_command.RichAsyncGroup.command_class

*attribute* · *class attribute* · *instance attribute*

```python
command_class: type[RichAsyncCommand] | None = RichAsyncCommand
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L130-L130)

### rich_click.rich_async_command.RichAsyncGroup.context_class

*attribute* · *class attribute* · *instance attribute*

```python
context_class: type[RichAsyncContext] = RichAsyncContext
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L129-L129)

### rich_click.rich_async_command.RichAsyncGroup.group_class

*attribute* · *class attribute* · *instance attribute*

```python
group_class: Any | None = type
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L131-L131)

### rich_click.rich_async_command.RichAsyncGroup.aliases

*attribute* · *instance attribute*

```python
aliases: Iterable[str] = aliases or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L84-L84)

### rich_click.rich_async_command.RichAsyncGroup.panel

*attribute* · *instance attribute*

```python
panel: str | list[str] | None = panel
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L82-L82)

### rich_click.rich_async_command.RichAsyncGroup.panels

*attribute* · *instance attribute*

```python
panels: list[RichPanel[Any, Any]] = panels or []
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L83-L83)

### rich_click.rich_async_command.RichAsyncGroup.console

*property*

```python
console: Console | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

**Deprecated**: Since 1.9. Use the console of the context, `ctx.console`.

Rich console of this command. Set it with the `rich_config` decorator.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L89-L101)

### rich_click.rich_async_command.RichAsyncGroup.help_config

*property*

```python
help_config: RichHelpConfiguration | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

**Deprecated**: Since 1.8. Use the help configuration of the context, `ctx.help_config`.

Help configuration of this command. Set it with the `rich_config` decorator.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L104-L120)

### rich_click.rich_async_command.RichAsyncGroup.add_command

*method*

```python
def add_command(cmd: click.Command, name: str | None = None, aliases: Iterable[str] | None = None, panel: str | list[str] | None = None) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

Add a command to this group.

**Parameters**

- `cmd` (`click.Command`) — The command to add.
- `name` (`str | None`) (default: `None`) — Name of the command in this group. Defaults to the name of the command.
- `aliases` (`Iterable[str] | None`) (default: `None`) — Other names that run the command, in addition to the aliases of the command.
- `panel` (`str | list[str] | None`) (default: `None`) — Panel or panels to show the command in, by panel title.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L548-L565)

### rich_click.rich_async_command.RichAsyncGroup.add_command_to_panel

*method*

```python
def add_command_to_panel(command: click.Command, panel_name: str | Iterable[str]) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L567-L577)

### rich_click.rich_async_command.RichAsyncGroup.command

*method*

```python
def command(*args: Any, **kwargs: Any) -> Any
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

Create a command and add it to this group.

Takes the same arguments as the `command` decorator, and works with or without
parentheses. The class of the command is `command_class`, unless you set `cls`.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L432-L467)

### rich_click.rich_async_command.RichAsyncGroup.format_commands

*method*

```python
def format_commands(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L406-L408)

### rich_click.rich_async_command.RichAsyncGroup.format_help

*method*

```python
def format_help(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L410-L417)

### rich_click.rich_async_command.RichAsyncGroup.get_command

*method*

```python
def get_command(ctx: click.Context, cmd_name: str) -> click.Command | None
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L544-L546)

### rich_click.rich_async_command.RichAsyncGroup.group

*method*

```python
def group(*args: Any, **kwargs: Any) -> Any
```

Inherited from: `rich_click.rich_command.RichGroupMixin`

Create a subgroup and add it to this group.

Takes the same arguments as the `group` decorator, and works with or without
parentheses. The subgroup has the same class as this group, unless you set `group_class` or `cls`.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L475-L513)

### rich_click.rich_async_command.RichAsyncGroup.invoke

*method* · *async*

```python
async def invoke(ctx: asyncclick.Context) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L97-L99)

### rich_click.rich_async_command.RichAsyncGroup.main

*method* · *async*

```python
async def main(args: Sequence[str] | None = None, prog_name: str | None = None, complete_var: str | None = None, standalone_mode: bool = True, **extra: Any) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L77-L89)

### rich_click.rich_async_command.RichAsyncGroup.make_context

*method* · *async*

```python
async def make_context(*args: Any, **kwargs: Any) -> Any
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L93-L95)

### rich_click.rich_async_command.RichAsyncGroup.to_info_dict

*method* · *async*

```python
async def to_info_dict(ctx: asyncclick.Context) -> dict[str, Any]
```

Inherited from: `rich_click.rich_async_command.RichAsyncCommand`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_async_command.py#L69-L73)

### rich_click.rich_async_command.RichAsyncGroup.add_panel

*method*

```python
def add_panel(panel: RichPanel[Any, Any]) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Add a RichPanel to the RichCommand.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L236-L238)

### rich_click.rich_async_command.RichAsyncGroup.format_epilog

*method*

```python
def format_epilog(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L220-L223)

### rich_click.rich_async_command.RichAsyncGroup.format_help_text

*method*

```python
def format_help_text(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L198-L201)

### rich_click.rich_async_command.RichAsyncGroup.format_options

*method*

```python
def format_options(ctx: click.Context, formatter: click.HelpFormatter) -> None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L209-L218)

### rich_click.rich_async_command.RichAsyncGroup.get_help_option

*method*

```python
def get_help_option(ctx: click.Context) -> click.Option | None
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Return the help option, or `None` if `add_help_option` is false. Every call returns the same object.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L246-L260)

### rich_click.rich_async_command.RichAsyncGroup.get_rich_table_row

*method*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_command.RichCommandMixin`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_command.py#L225-L234)
