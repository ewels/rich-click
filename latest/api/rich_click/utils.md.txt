---
project: "rich-click"
title: "rich_click.utils"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/utils/"
---

# rich_click.utils

*module* · *Added in 1.7.0*

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L1-L1)

## rich_click.utils.notset

*attribute* · *Added in 1.9.0* · *module attribute*

```python
notset: Any = object()
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L19-L19)

## rich_click.utils.CommandGroupDict

*class* · *Added in 1.8.0*

```python
class CommandGroupDict(TypedDict)
```

Bases: `TypedDict`

Specification for command groups.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L67-L80)

### rich_click.utils.CommandGroupDict.column_types

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
column_types: NotRequired[list[CommandColumnType] | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L76-L76)

### rich_click.utils.CommandGroupDict.commands

*attribute* · *Added in 1.8.0* · *instance attribute*

```python
commands: NotRequired[list[str]]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L71-L71)

### rich_click.utils.CommandGroupDict.deduplicate

*attribute* · *Added in 1.8.7* · *instance attribute*

```python
deduplicate: NotRequired[bool]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L80-L80)

### rich_click.utils.CommandGroupDict.help

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help: NotRequired[str | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L72-L72)

### rich_click.utils.CommandGroupDict.help_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help_style: NotRequired[StyleType | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L73-L73)

### rich_click.utils.CommandGroupDict.inline_help_in_title

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
inline_help_in_title: NotRequired[bool | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L77-L77)

### rich_click.utils.CommandGroupDict.name

*attribute* · *Added in 1.8.0* · *instance attribute*

```python
name: NotRequired[str]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L70-L70)

### rich_click.utils.CommandGroupDict.panel_styles

*attribute* · *Added in 1.8.0* · *instance attribute*

```python
panel_styles: NotRequired[dict[str, Any] | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L75-L75)

### rich_click.utils.CommandGroupDict.table_styles

*attribute* · *Added in 1.8.0* · *instance attribute*

```python
table_styles: NotRequired[dict[str, Any] | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L74-L74)

### rich_click.utils.CommandGroupDict.title_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
title_style: NotRequired[StyleType | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L78-L78)

## rich_click.utils.OptionGroupDict

*class* · *Added in 1.8.0*

```python
class OptionGroupDict(TypedDict)
```

Bases: `TypedDict`

Specification for option groups.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L83-L96)

### rich_click.utils.OptionGroupDict.column_types

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
column_types: NotRequired[list[OptionColumnType] | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L92-L92)

### rich_click.utils.OptionGroupDict.deduplicate

*attribute* · *Added in 1.8.7* · *instance attribute*

```python
deduplicate: NotRequired[bool]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L96-L96)

### rich_click.utils.OptionGroupDict.help

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help: NotRequired[str | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L88-L88)

### rich_click.utils.OptionGroupDict.help_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
help_style: NotRequired[StyleType | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L89-L89)

### rich_click.utils.OptionGroupDict.inline_help_in_title

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
inline_help_in_title: NotRequired[bool | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L93-L93)

### rich_click.utils.OptionGroupDict.name

*attribute* · *Added in 1.8.0* · *instance attribute*

```python
name: NotRequired[str]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L86-L86)

### rich_click.utils.OptionGroupDict.options

*attribute* · *Added in 1.8.0* · *instance attribute*

```python
options: NotRequired[list[str]]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L87-L87)

### rich_click.utils.OptionGroupDict.panel_styles

*attribute* · *Added in 1.8.0* · *instance attribute*

```python
panel_styles: NotRequired[dict[str, Any] | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L91-L91)

### rich_click.utils.OptionGroupDict.table_styles

*attribute* · *Added in 1.8.0* · *instance attribute*

```python
table_styles: NotRequired[dict[str, Any] | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L90-L90)

### rich_click.utils.OptionGroupDict.title_style

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
title_style: NotRequired[StyleType | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L94-L94)

## rich_click.utils.method_is_from_subclass_of

*function* · *Added in 1.8.0*

```python
def method_is_from_subclass_of(base_cls: type[object], method_name: str) -> bool
```

Check to see whether a class's method comes from a subclass of some base class.

This is used under the hood to see whether we would expect a patched RichCommand's help text
methods to be compatible or incompatible with rich-click or not.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L54-L64)

## rich_click.utils.truthy

*function* · *Added in 1.7.0*

```python
def truthy(o: Any) -> bool | None
```

Check if string or other obj is truthy.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/utils.py#L39-L51)
