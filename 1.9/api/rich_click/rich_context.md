# rich_click.rich_context

*module* · *Added in 1.7.0*

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L1-L1)

## rich_click.rich_context.RichContext

*class* · *Added in 1.7.0*

```python
class RichContext(RichContextMixin, click.Context)
```

Bases: `rich_click.rich_context.RichContextMixin`, `click.Context`

Click Context class endowed with Rich superpowers.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L119-L134)

### rich_click.rich_context.RichContext.console

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
console: Console | None = None
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L37-L37)

### rich_click.rich_context.RichContext.errors_in_output_format

*attribute* · *Added in 1.8.8* · *class attribute* · *instance attribute*

```python
errors_in_output_format: bool = False
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L39-L39)

### rich_click.rich_context.RichContext.export_console_as

*attribute* · *Added in 1.8.0* · *class attribute* · *instance attribute*

```python
export_console_as: Literal['html', 'svg', 'text'] | None = None
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L38-L38)

### rich_click.rich_context.RichContext.formatter_class

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
formatter_class: type[RichHelpFormatter] = RichHelpFormatter
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L36-L36)

### rich_click.rich_context.RichContext.help_config

*attribute* · *Added in 1.7.0* · *instance attribute*

```python
help_config = parent.help_config
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L92-L92)

### rich_click.rich_context.RichContext.help_to_stderr

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
help_to_stderr: bool = False
```

Inherited from: `rich_click.rich_context.RichContextMixin`

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L40-L40)

### rich_click.rich_context.RichContext.make_formatter

*method* · *Added in 1.7.0*

```python
def make_formatter(error_mode: bool = False) -> RichHelpFormatter
```

Inherited from: `rich_click.rich_context.RichContextMixin`

Create the Rich Help Formatter.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L107-L116)

## rich_click.rich_context.RichContextMixin

*class*

```python
class RichContextMixin(_ContextBase)
```

Bases: `_ContextBase`

Mixin that endows a click (or click-compatible fork) Context with Rich superpowers.

Contains only Rich help-formatting behavior and state, with no click base of its
own, so it can be composed with either ``click.Context`` (see :class:`RichContext`)
or a fork's Context (e.g. ``asyncclick.Context``) without dragging click's
synchronous methods into the MRO.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L26-L116)

### rich_click.rich_context.RichContextMixin.console

*attribute* · *class attribute* · *instance attribute*

```python
console: Console | None = None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L37-L37)

### rich_click.rich_context.RichContextMixin.errors_in_output_format

*attribute* · *class attribute* · *instance attribute*

```python
errors_in_output_format: bool = False
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L39-L39)

### rich_click.rich_context.RichContextMixin.export_console_as

*attribute* · *class attribute* · *instance attribute*

```python
export_console_as: Literal['html', 'svg', 'text'] | None = None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L38-L38)

### rich_click.rich_context.RichContextMixin.formatter_class

*attribute* · *class attribute* · *instance attribute*

```python
formatter_class: type[RichHelpFormatter] = RichHelpFormatter
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L36-L36)

### rich_click.rich_context.RichContextMixin.help_config

*attribute* · *instance attribute*

```python
help_config = parent.help_config
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L92-L92)

### rich_click.rich_context.RichContextMixin.help_to_stderr

*attribute* · *class attribute* · *instance attribute*

```python
help_to_stderr: bool = False
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L40-L40)

### rich_click.rich_context.RichContextMixin.make_formatter

*method*

```python
def make_formatter(error_mode: bool = False) -> RichHelpFormatter
```

Create the Rich Help Formatter.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L107-L116)

## rich_click.rich_context.get_current_context

*function* · *Added in 1.9.0*

```python
def get_current_context(silent: bool = False) -> RichContext | None
```

Return the current click context.  This can be used as a way to
access the current context object from anywhere.  This is a more implicit
alternative to the :func:`pass_context` decorator.  This function is
primarily useful for helpers such as :func:`echo` which might be
interested in changing its behavior based on the current context.

To push the current context, :meth:`Context.scope` can be used.

.. versionadded:: 5.0

:param silent: if set to `True` the return value is `None` if no context
               is available.  The default behavior is to raise a
               :exc:`RuntimeError`.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_context.py#L137-L153)
