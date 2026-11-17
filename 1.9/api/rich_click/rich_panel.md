---
project: "rich-click"
title: "rich_click.rich_panel"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_panel/"
---

# rich_click.rich_panel

*module* · *Added in 1.9.0*

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L1-L1)

## rich_click.rich_panel.CT

*attribute* · *Added in 1.9.0* · *module attribute*

```python
CT = TypeVar('CT', Command, Parameter)
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L33-L33)

## rich_click.rich_panel.ColT

*attribute* · *Added in 1.9.0* · *module attribute*

```python
ColT = TypeVar('ColT', bound=ColumnType)
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L32-L32)

## rich_click.rich_panel.GroupType

*attribute* · *Added in 1.9.0* · *module attribute*

```python
GroupType = TypeVar('GroupType', OptionGroupDict, CommandGroupDict)
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L34-L34)

## rich_click.rich_panel.RichCommandPanel

*class* · *Added in 1.9.0*

```python
class RichCommandPanel(RichPanel[Command, CommandColumnType])
```

Bases: ``

Panel for parameters.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L293-L456)

### rich_click.rich_panel.RichCommandPanel.commands

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
commands = commands or []
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L306-L306)

### rich_click.rich_panel.RichCommandPanel.get_objects

*method* · *Added in 1.9.0*

```python
def get_objects(command: Command, ctx: Context) -> Generator[Command, None, None]
```

List the objects assigned to the panel.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L319-L333)

### rich_click.rich_panel.RichCommandPanel.get_table

*method* · *Added in 1.9.0*

```python
def get_table(command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> Table
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L335-L398)

### rich_click.rich_panel.RichCommandPanel.list_all_objects

*method* · *Added in 1.9.0* · *classmethod*

```python
def list_all_objects(ctx: Context) -> list[tuple[str, Command]]
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L308-L317)

### rich_click.rich_panel.RichCommandPanel.render

*method* · *Added in 1.9.0*

```python
def render(command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> Panel
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L400-L456)

## rich_click.rich_panel.RichOptionPanel

*class* · *Added in 1.9.0*

```python
class RichOptionPanel(RichPanel[Parameter, OptionColumnType])
```

Bases: ``

Panel for parameters.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L157-L290)

### rich_click.rich_panel.RichOptionPanel.options

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
options = options or []
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L171-L171)

### rich_click.rich_panel.RichOptionPanel.get_objects

*method* · *Added in 1.9.0*

```python
def get_objects(command: Command, ctx: Context) -> Generator[Parameter, None, None]
```

List the objects assigned to the panel.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L180-L190)

### rich_click.rich_panel.RichOptionPanel.get_table

*method* · *Added in 1.9.0*

```python
def get_table(command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> Table
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L192-L233)

### rich_click.rich_panel.RichOptionPanel.list_all_objects

*method* · *Added in 1.9.0* · *classmethod*

```python
def list_all_objects(ctx: Context) -> list[tuple[str, Parameter]]
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L173-L178)

### rich_click.rich_panel.RichOptionPanel.render

*method* · *Added in 1.9.0*

```python
def render(command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> Panel
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L235-L290)

## rich_click.rich_panel.RichPanel

*class* · *Added in 1.9.0*

```python
class RichPanel(Generic[CT, ColT])
```

Bases: ``

RichPanel base class.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L37-L154)

### rich_click.rich_panel.RichPanel.column_types

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
column_types = column_types
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L63-L63)

### rich_click.rich_panel.RichPanel.help

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help = help
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L59-L59)

### rich_click.rich_panel.RichPanel.help_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help_style = help_style
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L60-L60)

### rich_click.rich_panel.RichPanel.inline_help_in_title

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
inline_help_in_title = inline_help_in_title
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L64-L64)

### rich_click.rich_panel.RichPanel.name

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
name = name
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L58-L58)

### rich_click.rich_panel.RichPanel.panel_class

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
panel_class: type[Panel] | None = None
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L40-L40)

### rich_click.rich_panel.RichPanel.panel_styles

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
panel_styles = panel_styles or {}
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L62-L62)

### rich_click.rich_panel.RichPanel.table_class

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
table_class: type[Table] | None = None
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L41-L41)

### rich_click.rich_panel.RichPanel.table_styles

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
table_styles = table_styles or {}
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L61-L61)

### rich_click.rich_panel.RichPanel.title_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
title_style = title_style
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L65-L65)

### rich_click.rich_panel.RichPanel.objects

*property* · *Added in 1.9.0*

```python
objects: list[str]
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L68-L71)

### rich_click.rich_panel.RichPanel.add_object

*method* · *Added in 1.9.0*

```python
def add_object(o: str) -> None
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L73-L76)

### rich_click.rich_panel.RichPanel.get_box

*method* · *Added in 1.9.0*

```python
def get_box(box: str | Box | None) -> Box | None
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L78-L83)

### rich_click.rich_panel.RichPanel.get_objects

*method* · *Added in 1.9.0*

```python
def get_objects(command: Command, ctx: Context) -> Generator[CT, None, None]
```

List the proper names assigned to the panel.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L100-L102)

### rich_click.rich_panel.RichPanel.get_table

*method* · *Added in 1.9.0*

```python
def get_table(command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> Table
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L121-L127)

### rich_click.rich_panel.RichPanel.list_all_objects

*method* · *Added in 1.9.0* · *classmethod*

```python
def list_all_objects(ctx: Context) -> list[tuple[str, CT]]
```

List all objects of the command that this panel type works with.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L95-L98)

### rich_click.rich_panel.RichPanel.render

*method* · *Added in 1.9.0*

```python
def render(command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> Panel
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L145-L151)

### rich_click.rich_panel.RichPanel.to_info_dict

*method* · *Added in 1.9.0*

```python
def to_info_dict(ctx: Context) -> dict[str, Any]
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L85-L93)

## rich_click.rich_panel.construct_panels

*function* · *Added in 1.9.0*

```python
def construct_panels(command: RichCommand, ctx: RichContext, formatter: RichHelpFormatter) -> list[RichPanel[Any, Any]]
```

Construct panels from the command as well as from the old groups config.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/rich_panel.py#L513-L740)
