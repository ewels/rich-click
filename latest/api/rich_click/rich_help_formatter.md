---
project: "rich-click"
title: "rich_click.rich_help_formatter"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_help_formatter/"
---

# rich_click.rich_help_formatter

*module* · *Added in 1.7.0*

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L1-L1)

## rich_click.rich_help_formatter.RP

*attribute* · *Added in 1.9.0* · *module attribute*

```python
RP = TypeVar('RP', bound=RichPanel[Any, Any])
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L32-L32)

## rich_click.rich_help_formatter.RichHelpFormatter

*class* · *Added in 1.7.0*

```python
class RichHelpFormatter(click.HelpFormatter)
```

Bases: `click.HelpFormatter`

Rich Help Formatter.

This class is a container for the help configuration and Rich Console that
are used internally by the help and error printing methods.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L101-L381)

### rich_click.rich_help_formatter.RichHelpFormatter.command_panel_class

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
command_panel_class: type[RichCommandPanel] = RichCommandPanel
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L118-L118)

### rich_click.rich_help_formatter.RichHelpFormatter.config

*attribute* · *Added in 1.7.0* · *instance attribute*

```python
config = config
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L148-L148)

### rich_click.rich_help_formatter.RichHelpFormatter.console

*attribute* · *Added in 1.7.0* · *instance attribute*

```python
console: Console
```

Rich Console created from the help configuration.

This console is meant only for use with the formatter and should
not be created directly

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L109-L109)

### rich_click.rich_help_formatter.RichHelpFormatter.export_console_as

*attribute* · *Added in 1.8.8* · *class attribute* · *instance attribute*

```python
export_console_as: Literal[None, 'html', 'svg', 'text'] = export_console_as
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L172-L172)

### rich_click.rich_help_formatter.RichHelpFormatter.export_kwargs

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
export_kwargs = export_kwargs or {}
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L173-L173)

### rich_click.rich_help_formatter.RichHelpFormatter.option_panel_class

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
option_panel_class: type[RichOptionPanel] = RichOptionPanel
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L117-L117)

### rich_click.rich_help_formatter.RichHelpFormatter.highlighter

*property* · *Added in 1.8.0* · *cached*

```python
highlighter: Highlighter
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L186-L195)

### rich_click.rich_help_formatter.RichHelpFormatter.width

*property* · *Added in 1.9.0* · *writable*

```python
width: int
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L178-L179)

### rich_click.rich_help_formatter.RichHelpFormatter.dedent

*method* · *Added in 1.9.0*

```python
def dedent() -> None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L339-L342)

### rich_click.rich_help_formatter.RichHelpFormatter.getvalue

*method* · *Added in 1.9.0*

```python
def getvalue() -> str
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L275-L332)

### rich_click.rich_help_formatter.RichHelpFormatter.indent

*method* · *Added in 1.9.0*

```python
def indent() -> None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L334-L337)

### rich_click.rich_help_formatter.RichHelpFormatter.indentation

*method* · *Added in 1.9.0*

```python
def indentation() -> Iterator[None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L376-L381)

### rich_click.rich_help_formatter.RichHelpFormatter.rich_text

*method* · *Added in 1.9.0*

```python
def rich_text(text: str | Text | Markdown, style: StyleType = '') -> Text | Markdown | RichClickRST
```

Take a string, remove indentations, and return styled text.
By default, return the text as a Rich Text with the request style.

This method uses the config options prefixed `text_` to influence how
rendering works.

**Parameters**

- `text` (`str | Text | Markdown`) — Text to style.
- `style` (`StyleType`) (default: `''`) — Rich style to apply.

**Returns**

- (`Text | Markdown | RichClickRST`) — Text, Markdown, or RichClickRST: Styled text object

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L214-L273)

### rich_click.rich_help_formatter.RichHelpFormatter.section

*method* · *Added in 1.9.0*

```python
def section(name: str) -> Iterator[None]
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L369-L374)

### rich_click.rich_help_formatter.RichHelpFormatter.write

*method* · *Added in 1.7.0*

```python
def write(*objects: Any, **kwargs: Any) -> None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L197-L198)

### rich_click.rich_help_formatter.RichHelpFormatter.write_abort

*method* · *Added in 1.8.0*

```python
def write_abort() -> None
```

Print richly formatted abort error.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L210-L212)

### rich_click.rich_help_formatter.RichHelpFormatter.write_dl

*method* · *Added in 1.9.0*

```python
def write_dl(rows: Iterable[tuple[str, str]], col_max: int = 30, col_spacing: int = 2) -> None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L359-L367)

### rich_click.rich_help_formatter.RichHelpFormatter.write_error

*method* · *Added in 1.9.0*

```python
def write_error(e: click.ClickException) -> None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L205-L208)

### rich_click.rich_help_formatter.RichHelpFormatter.write_heading

*method* · *Added in 1.9.0*

```python
def write_heading(heading: str) -> None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L344-L347)

### rich_click.rich_help_formatter.RichHelpFormatter.write_paragraph

*method* · *Added in 1.9.0*

```python
def write_paragraph() -> None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L349-L352)

### rich_click.rich_help_formatter.RichHelpFormatter.write_text

*method* · *Added in 1.9.0*

```python
def write_text(text: str) -> None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L354-L357)

### rich_click.rich_help_formatter.RichHelpFormatter.write_usage

*method* · *Added in 1.8.0*

```python
def write_usage(prog: str, args: str = '', prefix: str | None = None) -> None
```

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L200-L203)

## rich_click.rich_help_formatter.create_console

*function* · *Added in 1.7.0*

```python
def create_console(config: RichHelpConfiguration, file: IO[str] | None = None, width: int | None = None, max_width: int | None = None) -> Console
```

Create a Rich console from a help configuration.

**Parameters**

- `config` (`RichHelpConfiguration`) — Help configuration to take the console settings from.
- `file` (`IO[str] | None`) (default: `None`) — Stream to write to. If not set, the console records its output to an in-memory buffer.
- `width` (`int | None`) (default: `None`) — Width of the console. Overrides `config.width`.
- `max_width` (`int | None`) (default: `None`) — Maximum width of the console. Overrides `config.max_width`.

**Returns**

- (`Console`) — The new console.

[View source](https://github.com/ewels/rich-click/blob/4505e60065c35d2ec66a57eb8c768c7b41cc1e3f/src/rich_click/rich_help_formatter.py#L52-L98)
