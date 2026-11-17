---
project: "rich-click"
title: "rich_click.rich_help_rendering"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_help_rendering/"
---

# rich_click.rich_help_rendering

*module* · *Added in 1.8.0*

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L1-L1)

## rich_click.rich_help_rendering.RichPanelRow

*attribute* · *Added in 1.9.0* · *module attribute*

```python
RichPanelRow = list[RenderableType | None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L38-L38)

## rich_click.rich_help_rendering.RichClickRichPanel

*class* · *Added in 1.9.0*

```python
class RichClickRichPanel(Panel)
```

Bases: `Panel`

A console renderable that draws a border around its contents.

This is a patched version of rich.panel.Panel that has additional features useful
for rendering help text with rich-click.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L41-L75)

### rich_click.rich_help_rendering.RichClickRichPanel.title_padding

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
title_padding = title_padding
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L60-L60)

## rich_click.rich_help_rendering.get_command_rich_table_row

*function* · *Added in 1.9.0*

```python
def get_command_rich_table_row(command: click.Command, ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None) -> RichPanelRow
```

Create a row for the rich table corresponding with this command.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L895-L921)

## rich_click.rich_help_rendering.get_help_parameter

*function* · *Added in 1.9.0*

```python
def get_help_parameter(param: click.Argument | click.Option | RichParameter, ctx: RichContext, formatter: RichHelpFormatter) -> Columns
```

Build primary help text for a click option or argument.
Returns the prose help text for an option or argument, rendered either
as a Rich Text object or as Markdown.
Additional elements are appended to show the default and required status if applicable.

**Parameters**

- `param` (`click.Argument | click.Option | RichParameter`) — Parameter to build help text for.
- `ctx` (`RichContext`) — Click Context object.
- `formatter` (`RichHelpFormatter`) — Formatter object.

**Returns**

- `Columns` (`Columns`) — A columns element with multiple styled objects (help, default, required)

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L673-L727)

## rich_click.rich_help_rendering.get_parameter_rich_table_row

*function* · *Added in 1.9.0*

```python
def get_parameter_rich_table_row(param: click.Argument | click.Option | RichParameter, ctx: RichContext, formatter: RichHelpFormatter, panel: RichOptionPanel | None) -> RichPanelRow
```

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L730-L843)

## rich_click.rich_help_rendering.get_rich_epilog

*function* · *Added in 1.8.0*

```python
def get_rich_epilog(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Richly render a click Command's epilog if it exists.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L1035-L1065)

## rich_click.rich_help_rendering.get_rich_help_text

*function* · *Added in 1.8.0*

```python
def get_rich_help_text(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Write rich help text to the formatter if it exists.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L1021-L1032)

## rich_click.rich_help_rendering.get_rich_usage

*function* · *Added in 1.8.0*

```python
def get_rich_usage(formatter: RichHelpFormatter, prog: str, args: str = '', prefix: str | None = None) -> None
```

Richly render usage text.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L980-L1018)

## rich_click.rich_help_rendering.rich_format_error

*function* · *Added in 1.8.0*

```python
def rich_format_error(formatter: RichHelpFormatter, export_console_as: Literal[None, 'html', 'svg'] = None) -> None
```

Print richly formatted click errors.

Called by custom exception handler to print richly formatted click errors.
Mimics original click.ClickException.echo() function but with rich formatting.

**Parameters**

- `self` (`click.ClickException`) — Click exception to format.
- `formatter` (`RichHelpFormatter`) — formatter object.
- `export_console_as` (`Literal[None, 'html', 'svg']`) (default: `None`) — If set, outputs error message as HTML or SVG.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_rendering.py#L1068-L1149)
