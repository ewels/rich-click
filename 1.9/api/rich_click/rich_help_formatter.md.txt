# rich_click.rich_help_formatter

*module* · *Added in 1.7.0*

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L1-L1)

## rich_click.rich_help_formatter.RP

*attribute* · *Added in 1.9.0* · *module attribute*

```python
RP = TypeVar('RP', bound=RichPanel[Any, Any])
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L30-L30)

## rich_click.rich_help_formatter.RichHelpFormatter

*class* · *Added in 1.7.0*

```python
class RichHelpFormatter(click.HelpFormatter)
```

Bases: `click.HelpFormatter`

Rich Help Formatter.

This class is a container for the help configuration and Rich Console that
are used internally by the help and error printing methods.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L99-L377)

### rich_click.rich_help_formatter.RichHelpFormatter.command_panel_class

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
command_panel_class: type[RichCommandPanel] = RichCommandPanel
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L116-L116)

### rich_click.rich_help_formatter.RichHelpFormatter.config

*attribute* · *Added in 1.7.0* · *instance attribute*

```python
config = config
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L148-L148)

### rich_click.rich_help_formatter.RichHelpFormatter.console

*attribute* · *Added in 1.7.0* · *instance attribute*

```python
console: Console
```

Rich Console created from the help configuration.

This console is meant only for use with the formatter and should
not be created directly

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L107-L107)

### rich_click.rich_help_formatter.RichHelpFormatter.export_console_as

*attribute* · *Added in 1.8.8* · *class attribute* · *instance attribute*

```python
export_console_as: Literal[None, 'html', 'svg', 'text'] = export_console_as
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L172-L172)

### rich_click.rich_help_formatter.RichHelpFormatter.export_kwargs

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
export_kwargs = export_kwargs or {}
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L173-L173)

### rich_click.rich_help_formatter.RichHelpFormatter.option_panel_class

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
option_panel_class: type[RichOptionPanel] = RichOptionPanel
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L115-L115)

### rich_click.rich_help_formatter.RichHelpFormatter.highlighter

*property* · *Added in 1.8.0* · *cached*

```python
highlighter: Highlighter
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L186-L195)

### rich_click.rich_help_formatter.RichHelpFormatter.width

*property* · *Added in 1.9.0* · *writable*

```python
width: int
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L178-L179)

### rich_click.rich_help_formatter.RichHelpFormatter.dedent

*method* · *Added in 1.9.0*

```python
def dedent() -> None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L335-L338)

### rich_click.rich_help_formatter.RichHelpFormatter.getvalue

*method* · *Added in 1.9.0*

```python
def getvalue() -> str
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L271-L328)

### rich_click.rich_help_formatter.RichHelpFormatter.indent

*method* · *Added in 1.9.0*

```python
def indent() -> None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L330-L333)

### rich_click.rich_help_formatter.RichHelpFormatter.indentation

*method* · *Added in 1.9.0*

```python
def indentation() -> Iterator[None]
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L372-L377)

### rich_click.rich_help_formatter.RichHelpFormatter.rich_text

*method* · *Added in 1.9.0*

```python
def rich_text(text: str | Text | Markdown, style: StyleType = '') -> Text | Markdown
```

Take a string, remove indentations, and return styled text.
By default, return the text as a Rich Text with the request style.

This method uses the config options prefixed `text_` to influence how
rendering works.

----
    text (str): Text to style.
    style (StyleType): Rich style to apply.

-------
    MarkdownElement or Text: Styled text object

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L214-L269)

### rich_click.rich_help_formatter.RichHelpFormatter.section

*method* · *Added in 1.9.0*

```python
def section(name: str) -> Iterator[None]
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L365-L370)

### rich_click.rich_help_formatter.RichHelpFormatter.write

*method* · *Added in 1.7.0*

```python
def write(*objects: Any, **kwargs: Any) -> None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L197-L198)

### rich_click.rich_help_formatter.RichHelpFormatter.write_abort

*method* · *Added in 1.8.0*

```python
def write_abort() -> None
```

Print richly formatted abort error.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L210-L212)

### rich_click.rich_help_formatter.RichHelpFormatter.write_dl

*method* · *Added in 1.9.0*

```python
def write_dl(rows: Iterable[tuple[str, str]], col_max: int = 30, col_spacing: int = 2) -> None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L355-L363)

### rich_click.rich_help_formatter.RichHelpFormatter.write_error

*method* · *Added in 1.9.0*

```python
def write_error(e: click.ClickException) -> None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L205-L208)

### rich_click.rich_help_formatter.RichHelpFormatter.write_heading

*method* · *Added in 1.9.0*

```python
def write_heading(heading: str) -> None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L340-L343)

### rich_click.rich_help_formatter.RichHelpFormatter.write_paragraph

*method* · *Added in 1.9.0*

```python
def write_paragraph() -> None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L345-L348)

### rich_click.rich_help_formatter.RichHelpFormatter.write_text

*method* · *Added in 1.9.0*

```python
def write_text(text: str) -> None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L350-L353)

### rich_click.rich_help_formatter.RichHelpFormatter.write_usage

*method* · *Added in 1.8.0*

```python
def write_usage(prog: str, args: str = '', prefix: str | None = None) -> None
```

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L200-L203)

## rich_click.rich_help_formatter.create_console

*function* · *Added in 1.7.0*

```python
def create_console(config: RichHelpConfiguration, file: IO[str] | None = None, width: int | None = None, max_width: int | None = None) -> Console
```

Create a Rich Console configured from Rich Help Configuration.

----
    config: Rich Help Configuration instance
    file: Optional IO stream to write Rich Console output
        Defaults to None.
    width: Width of the Console; overrides config.width if set.
    max_width: Max width of the Console; overrides config.max_width if set.

[View source](https://github.com/ewels/rich-click/blob/51156e20b2c1db867c83444c7bbed1c9dc610580/src/rich_click/rich_help_formatter.py#L50-L96)
