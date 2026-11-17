---
project: "rich-click"
title: "rich_click.rich_context"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_context/"
---

# rich_click.rich_context

*module* · *Added in 1.7.0*

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L1-L1)

## rich_click.rich_context.RichContext

*class* · *Added in 1.7.0*

```python
class RichContext(RichContextMixin, click.Context)
```

Bases: `rich_click.rich_context.RichContextMixin`, `click.Context`

The context of a rich-click command: a click Context that formats help and errors with Rich.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L120-L135)

### rich_click.rich_context.RichContext.console

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
console: Console | None = None
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L39-L39)

### rich_click.rich_context.RichContext.errors_in_output_format

*attribute* · *Added in 1.8.8* · *class attribute* · *instance attribute*

```python
errors_in_output_format: bool = False
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L41-L41)

### rich_click.rich_context.RichContext.export_console_as

*attribute* · *Added in 1.8.0* · *class attribute* · *instance attribute*

```python
export_console_as: Literal['html', 'svg', 'text'] | None = None
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L40-L40)

### rich_click.rich_context.RichContext.formatter_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
formatter_class: type[RichHelpFormatter] = RichHelpFormatter
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L38-L38)

### rich_click.rich_context.RichContext.help_config

*attribute* · *Added in 1.7.0* · *instance attribute*

```python
help_config = parent.help_config
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L93-L93)

### rich_click.rich_context.RichContext.help_to_stderr

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
help_to_stderr: bool = False
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L42-L42)

### rich_click.rich_context.RichContext.make_formatter

*method* · *Added in 1.7.0*

```python
def make_formatter(error_mode: bool = False) -> RichHelpFormatter
```

Inherited from: `rich_click.rich_context.RichContextMixin`

Create the Rich Help Formatter.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L108-L117)

## rich_click.rich_context.RichContextMixin

*class*

```python
class RichContextMixin(_ContextBase)
```

Bases: `_ContextBase`

Rich help formatting for a click Context, as a mixin with no click base class.

`RichContext` combines this mixin with `click.Context`. A click fork combines it
with its own Context class, such as `asyncclick.Context`. Because the mixin has
no click base class, it does not add click's synchronous methods to the fork.

> **Note**
>
> To customize the context of a click CLI, subclass `RichContext`, not this mixin.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L26-L117)

### rich_click.rich_context.RichContextMixin.console

*attribute* · *class attribute* · *instance attribute*

```python
console: Console | None = None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L39-L39)

### rich_click.rich_context.RichContextMixin.errors_in_output_format

*attribute* · *class attribute* · *instance attribute*

```python
errors_in_output_format: bool = False
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L41-L41)

### rich_click.rich_context.RichContextMixin.export_console_as

*attribute* · *class attribute* · *instance attribute*

```python
export_console_as: Literal['html', 'svg', 'text'] | None = None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L40-L40)

### rich_click.rich_context.RichContextMixin.formatter_class

*attribute* · *class attribute* · *instance attribute*

```python
formatter_class: type[RichHelpFormatter] = RichHelpFormatter
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L38-L38)

### rich_click.rich_context.RichContextMixin.help_config

*attribute* · *instance attribute*

```python
help_config = parent.help_config
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L93-L93)

### rich_click.rich_context.RichContextMixin.help_to_stderr

*attribute* · *class attribute* · *instance attribute*

```python
help_to_stderr: bool = False
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L42-L42)

### rich_click.rich_context.RichContextMixin.make_formatter

*method*

```python
def make_formatter(error_mode: bool = False) -> RichHelpFormatter
```

Create the Rich Help Formatter.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L108-L117)

## rich_click.rich_context.get_current_context

*function* · *Added in 1.9.0*

```python
def get_current_context(silent: bool = False) -> RichContext | None
```

Return the context of the command that runs now.

Use it in helper functions that need the context but do not get it from the `pass_context` decorator.

**Parameters**

- `silent` (`bool`) (default: `False`) — If true, return `None` when no command runs. If false, raise a `RuntimeError`.

**Returns**

- (`RichContext | None`) — The context, or `None` if no command runs and `silent` is true.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_context.py#L138-L150)
