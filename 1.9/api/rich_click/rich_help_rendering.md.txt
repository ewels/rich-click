# rich_click.rich_help_rendering

*module* · *Added in 1.8.0*

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L1-L1)

## rich_click.rich_help_rendering.RichPanelRow

*attribute* · *Added in 1.9.0* · *module attribute*

```python
RichPanelRow = list[RenderableType | None]
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L37-L37)

## rich_click.rich_help_rendering.RichClickRichPanel

*class* · *Added in 1.9.0*

```python
class RichClickRichPanel(Panel)
```

Bases: `Panel`

A console renderable that draws a border around its contents.

This is a patched version of rich.panel.Panel that has additional features useful
for rendering help text with rich-click.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L40-L75)

### rich_click.rich_help_rendering.RichClickRichPanel.title_padding

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
title_padding = title_padding
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L60-L60)

## rich_click.rich_help_rendering.get_command_rich_table_row

*function* · *Added in 1.9.0*

```python
def get_command_rich_table_row(command: click.Command, ctx: RichContext, formatter: RichHelpFormatter, panel: RichCommandPanel | None) -> RichPanelRow
```

Create a row for the rich table corresponding with this command.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L877-L903)

## rich_click.rich_help_rendering.get_help_parameter

*function* · *Added in 1.9.0*

```python
def get_help_parameter(param: click.Argument | click.Option | RichParameter, ctx: RichContext, formatter: RichHelpFormatter) -> Columns
```

Build primary help text for a click option or argument.
Returns the prose help text for an option or argument, rendered either
as a Rich Text object or as Markdown.
Additional elements are appended to show the default and required status if applicable.

----
    param (click.Argument or click.Option): Parameter to build help text for.
    ctx (click.Context): Click Context object.
    formatter (RichHelpFormatter): formatter object.

-------
    Columns: A columns element with multiple styled objects (help, default, required)

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L655-L709)

## rich_click.rich_help_rendering.get_parameter_rich_table_row

*function* · *Added in 1.9.0*

```python
def get_parameter_rich_table_row(param: click.Argument | click.Option | RichParameter, ctx: RichContext, formatter: RichHelpFormatter, panel: RichOptionPanel | None) -> RichPanelRow
```

Create a row for the rich table corresponding with this parameter.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L712-L825)

## rich_click.rich_help_rendering.get_rich_epilog

*function* · *Added in 1.8.0*

```python
def get_rich_epilog(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Richly render a click Command's epilog if it exists.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L1008-L1036)

## rich_click.rich_help_rendering.get_rich_help_text

*function* · *Added in 1.8.0*

```python
def get_rich_help_text(ctx: RichContext, formatter: RichHelpFormatter) -> None
```

Write rich help text to the formatter if it exists.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L994-L1005)

## rich_click.rich_help_rendering.get_rich_usage

*function* · *Added in 1.8.0*

```python
def get_rich_usage(formatter: RichHelpFormatter, prog: str, args: str = '', prefix: str | None = None) -> None
```

Richly render usage text.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L953-L991)

## rich_click.rich_help_rendering.rich_format_error

*function* · *Added in 1.8.0*

```python
def rich_format_error(formatter: RichHelpFormatter, export_console_as: Literal[None, 'html', 'svg'] = None) -> None
```

Print richly formatted click errors.

Called by custom exception handler to print richly formatted click errors.
Mimics original click.ClickException.echo() function but with rich formatting.

----
    self (click.ClickException): Click exception to format.
    formatter: formatter object.
    export_console_as: If set, outputs error message as HTML or SVG.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_rendering.py#L1039-L1121)
