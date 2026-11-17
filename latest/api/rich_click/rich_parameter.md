---
project: "rich-click"
title: "rich_click.rich_parameter"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_parameter/"
---

# rich_click.rich_parameter

*module* · *Added in 1.9.0*

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L1-L1)

## rich_click.rich_parameter.RichArgument

*class* · *Added in 1.9.0*

```python
class RichArgument(RichParameter, click.Argument)
```

Bases: `rich_click.rich_parameter.RichParameter`, `click.Argument`

Arguments are positional parameters to a command.  They generally
provide fewer features than options but can have infinite ``nargs``
and are required by default.

All parameters are passed onwards to the constructor of :class:`Parameter`.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L81-L88)

### rich_click.rich_parameter.RichArgument.help

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help = help
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L47-L47)

### rich_click.rich_parameter.RichArgument.help_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help_style = help_style
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L49-L49)

### rich_click.rich_parameter.RichArgument.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel = panel
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L37-L37)

### rich_click.rich_parameter.RichArgument.get_rich_help

*method* · *Added in 1.9.0*

```python
def get_rich_help(ctx: RichContext, formatter: RichHelpFormatter) -> Columns
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Get the rich help text for this parameter.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L63-L67)

### rich_click.rich_parameter.RichArgument.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichOptionPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L69-L78)

### rich_click.rich_parameter.RichArgument.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict() -> dict[str, Any]
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Gather information that could be useful for a tool generating
user-facing documentation.

Use :meth:`click.Context.to_info_dict` to traverse the entire
CLI structure.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L51-L61)

## rich_click.rich_parameter.RichOption

*class* · *Added in 1.9.0*

```python
class RichOption(RichParameter, click.Option)
```

Bases: `rich_click.rich_parameter.RichParameter`, `click.Option`

Options are usually optional values on the command line and
have some extra features that arguments don't have.

All other parameters are passed onwards to the parameter constructor.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L91-L97)

### rich_click.rich_parameter.RichOption.help

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help = help
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L47-L47)

### rich_click.rich_parameter.RichOption.help_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help_style = help_style
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L49-L49)

### rich_click.rich_parameter.RichOption.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel = panel
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L37-L37)

### rich_click.rich_parameter.RichOption.get_rich_help

*method* · *Added in 1.9.0*

```python
def get_rich_help(ctx: RichContext, formatter: RichHelpFormatter) -> Columns
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Get the rich help text for this parameter.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L63-L67)

### rich_click.rich_parameter.RichOption.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichOptionPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L69-L78)

### rich_click.rich_parameter.RichOption.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict() -> dict[str, Any]
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Gather information that could be useful for a tool generating
user-facing documentation.

Use :meth:`click.Context.to_info_dict` to traverse the entire
CLI structure.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L51-L61)

## rich_click.rich_parameter.RichParameter

*class* · *Added in 1.9.0*

```python
class RichParameter(click.Parameter)
```

Bases: `click.Parameter`

A parameter to a command comes in two versions: they are either
:class:`Option`\s or :class:`Argument`\s.  Other subclasses are currently
not supported by design as some of the internals for parsing are
intentionally not finalized.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L19-L78)

### rich_click.rich_parameter.RichParameter.help

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help = help
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L47-L47)

### rich_click.rich_parameter.RichParameter.help_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help_style = help_style
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L49-L49)

### rich_click.rich_parameter.RichParameter.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel = panel
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L37-L37)

### rich_click.rich_parameter.RichParameter.get_rich_help

*method* · *Added in 1.9.0*

```python
def get_rich_help(ctx: RichContext, formatter: RichHelpFormatter) -> Columns
```

Get the rich help text for this parameter.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L63-L67)

### rich_click.rich_parameter.RichParameter.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichOptionPanel | None = None) -> RichPanelRow
```

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L69-L78)

### rich_click.rich_parameter.RichParameter.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict() -> dict[str, Any]
```

Gather information that could be useful for a tool generating
user-facing documentation.

Use :meth:`click.Context.to_info_dict` to traverse the entire
CLI structure.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_parameter.py#L51-L61)
