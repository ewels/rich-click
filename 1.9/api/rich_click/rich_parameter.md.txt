---
project: "rich-click"
title: "rich_click.rich_parameter"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_parameter/"
---

# rich_click.rich_parameter

*module* · *Added in 1.9.0*

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L1-L1)

## rich_click.rich_parameter.RichArgument

*class* · *Added in 1.9.0*

```python
class RichArgument(RichParameter, click.Argument)
```

Bases: `rich_click.rich_parameter.RichParameter`, `click.Argument`

A positional argument of a command, formatted by rich-click. The `argument` decorator creates one.

Arguments are required by default. With `nargs=-1`, an argument takes any number of values.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L76-L81)

### rich_click.rich_parameter.RichArgument.help

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help = help
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L42-L42)

### rich_click.rich_parameter.RichArgument.help_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help_style = help_style
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L44-L44)

### rich_click.rich_parameter.RichArgument.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel = panel
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L32-L32)

### rich_click.rich_parameter.RichArgument.get_rich_help

*method* · *Added in 1.9.0*

```python
def get_rich_help(ctx: RichContext, formatter: RichHelpFormatter) -> Columns
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Get the rich help text for this parameter.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L58-L62)

### rich_click.rich_parameter.RichArgument.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichOptionPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L64-L73)

### rich_click.rich_parameter.RichArgument.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict() -> dict[str, Any]
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Gather information that could be useful for a tool generating
user-facing documentation.

Use `click.Context.to_info_dict` to traverse the entire
CLI structure.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L46-L56)

## rich_click.rich_parameter.RichOption

*class* · *Added in 1.9.0*

```python
class RichOption(RichParameter, click.Option)
```

Bases: `rich_click.rich_parameter.RichParameter`, `click.Option`

An option of a command, formatted by rich-click. The `option` decorator creates one.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L84-L85)

### rich_click.rich_parameter.RichOption.help

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help = help
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L42-L42)

### rich_click.rich_parameter.RichOption.help_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help_style = help_style
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L44-L44)

### rich_click.rich_parameter.RichOption.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel = panel
```

Inherited from: `rich_click.rich_parameter.RichParameter`

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L32-L32)

### rich_click.rich_parameter.RichOption.get_rich_help

*method* · *Added in 1.9.0*

```python
def get_rich_help(ctx: RichContext, formatter: RichHelpFormatter) -> Columns
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Get the rich help text for this parameter.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L58-L62)

### rich_click.rich_parameter.RichOption.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichOptionPanel | None = None) -> RichPanelRow
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L64-L73)

### rich_click.rich_parameter.RichOption.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict() -> dict[str, Any]
```

Inherited from: `rich_click.rich_parameter.RichParameter`

Gather information that could be useful for a tool generating
user-facing documentation.

Use `click.Context.to_info_dict` to traverse the entire
CLI structure.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L46-L56)

## rich_click.rich_parameter.RichParameter

*class* · *Added in 1.9.0*

```python
class RichParameter(click.Parameter)
```

Bases: `click.Parameter`

Base class of `RichOption` and `RichArgument`: a click Parameter that rich-click formats in help.

Create RichParameter instance.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L19-L73)

### rich_click.rich_parameter.RichParameter.help

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help = help
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L42-L42)

### rich_click.rich_parameter.RichParameter.help_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help_style = help_style
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L44-L44)

### rich_click.rich_parameter.RichParameter.panel

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel = panel
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L32-L32)

### rich_click.rich_parameter.RichParameter.get_rich_help

*method* · *Added in 1.9.0*

```python
def get_rich_help(ctx: RichContext, formatter: RichHelpFormatter) -> Columns
```

Get the rich help text for this parameter.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L58-L62)

### rich_click.rich_parameter.RichParameter.get_rich_table_row

*method* · *Added in 1.9.0*

```python
def get_rich_table_row(ctx: RichContext, formatter: RichHelpFormatter, panel: RichOptionPanel | None = None) -> RichPanelRow
```

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L64-L73)

### rich_click.rich_parameter.RichParameter.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict() -> dict[str, Any]
```

Gather information that could be useful for a tool generating
user-facing documentation.

Use `click.Context.to_info_dict` to traverse the entire
CLI structure.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_parameter.py#L46-L56)
