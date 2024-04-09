# Configuration

There are two methods to configure rich-click:

- Decorator: Use the `@rich_config()` decorator (and `RichHelpConfiguration()`).
- Globals: Set the global variables in the `rich_config.rich_config` module.

## Configuration using the `rich_config` decorator

Initializing a new `RichHelpConfiguration` object creates a configuration that you can then pass to your CLIs via the `rich_config` decorator. For example:

```python
import rich_click as click

@click.command()
@click.rich_config(help_config=click.RichHelpConfiguration(style_option="bold red"))
def cli():
    """Help text here."""

cli()
```

`RichHelpConfiguration()` initializes the default configuration, and the user is able to specify any changes to that default configuration that they'd like. Note that `RichHelpConfiguration()` is unaware of the global configuration.

You may also specify custom config as a dict:

```python
import rich_click as click
from rich_click import rich_config

@click.command()
@rich_config(help_config={"style_option": "bold red"})
def cli():
    """Help text here."""

cli()
```

There is a subtle difference between using a `dict` and using a `RichHelpConfiguration`. Initializing a `RichHelpConfiguration` creates a fresh config from the defaults, whereas a `dict` merges to either the parent or (if the parent config does not exist) the global config.

In the below example `subcommand`'s configuration would get "merged" into `my_group`'s configuration, meaning that `subcommand` would inherit the `style_option="bold red"` style from `my_group`:

```python
import rich_click as click
from rich_click import rich_config

@click.group()
@rich_config(help_config={"style_option": "bold red"})
def my_group():
    """Help text here."""

@my_group.command()
@rich_config(help_config={"style_argument": "bold yellow"})
def subcommand():
    """Help text here."""

cli()
```

## Configuration using the global config

The other way to configure rich-click is to use the global configuration inside the `rich_click.rich_click` module:

```python
import rich_click as click
import rich_click.rich_click as rc

rc.STYLE_OPTION = "bold red"

@click.command()
def my_command():
    """Help text here."""

cli()
```

## Compatibility between `RichHelpConfiguration` and global config

You can load the global config into a `RichHelpConfiguration` using the `RichHelpConfiguration.load_from_globals()` classmethod:

```python
import rich_click as click
import rich_click.rich_click as rc

rc.STYLE_OPTION = "bold red"

# The help config will have `style_option = "bold red"`.
help_config = click.RichHelpConfiguration.load_from_globals()

@click.command()
@click.rich_config(help_config=help_config)
def my_command():
    """Help text here."""

cli()
```

You can also dump a help config into the global config using `RichHelpConfiguration().dump_to_globals()`.
You probably do not need this in most cases; this is mostly for **rich-click**'s internal use.

```python
import rich_click as click
import rich_click.rich_click as rc

help_config = click.RichHelpConfiguration(style_option="bold red")
help_config.dump_to_globals()

# The CLI will have `style_option = "bold red"` since it pulls from the globals.
@click.command()
def my_command():
    """Help text here."""

cli()
```



## Configuration options

Here is a full list of configuration options:

```python
# Default styles
STYLE_OPTION = "bold cyan"
STYLE_ARGUMENT = "bold cyan"
STYLE_COMMAND = "bold cyan"
STYLE_SWITCH = "bold green"
STYLE_METAVAR = "bold yellow"
STYLE_METAVAR_APPEND = "dim yellow"
STYLE_METAVAR_SEPARATOR = "dim"
STYLE_HEADER_TEXT = ""
STYLE_EPILOG_TEXT = ""
STYLE_FOOTER_TEXT = ""
STYLE_USAGE = "yellow"
STYLE_USAGE_COMMAND = "bold"
STYLE_DEPRECATED = "red"
STYLE_HELPTEXT_FIRST_LINE = ""
STYLE_HELPTEXT = "dim"
STYLE_OPTION_HELP = ""
STYLE_OPTION_DEFAULT = "dim"
STYLE_OPTION_ENVVAR = "dim yellow"
STYLE_REQUIRED_SHORT = "red"
STYLE_REQUIRED_LONG = "dim red"
STYLE_OPTIONS_PANEL_BORDER = "dim"
ALIGN_OPTIONS_PANEL = "left"
STYLE_OPTIONS_TABLE_SHOW_LINES = False
STYLE_OPTIONS_TABLE_LEADING = 0
STYLE_OPTIONS_TABLE_PAD_EDGE = False
STYLE_OPTIONS_TABLE_PADDING = (0, 1)
STYLE_OPTIONS_TABLE_BOX = ""
STYLE_OPTIONS_TABLE_ROW_STYLES = None
STYLE_OPTIONS_TABLE_BORDER_STYLE = None
STYLE_COMMANDS_PANEL_BORDER = "dim"
ALIGN_COMMANDS_PANEL = "left"
STYLE_COMMANDS_TABLE_SHOW_LINES = False
STYLE_COMMANDS_TABLE_LEADING = 0
STYLE_COMMANDS_TABLE_PAD_EDGE = False
STYLE_COMMANDS_TABLE_PADDING = (0, 1)
STYLE_COMMANDS_TABLE_BOX = ""
STYLE_COMMANDS_TABLE_ROW_STYLES = None
STYLE_COMMANDS_TABLE_BORDER_STYLE = None
STYLE_COMMANDS_TABLE_COLUMN_WIDTH_RATIO = (None, None)
STYLE_ERRORS_PANEL_BORDER = "red"
ALIGN_ERRORS_PANEL = "left"
STYLE_ERRORS_SUGGESTION = "dim"
STYLE_ERRORS_SUGGESTION_COMMAND = "blue"
STYLE_ABORTED = "red"
WIDTH = int(getenv("TERMINAL_WIDTH")) if getenv("TERMINAL_WIDTH") else None
MAX_WIDTH = int(getenv("TERMINAL_WIDTH")) if getenv("TERMINAL_WIDTH") else WIDTH
COLOR_SYSTEM = "auto"  # Set to None to disable colors
FORCE_TERMINAL = True if getenv("GITHUB_ACTIONS") or getenv("FORCE_COLOR") or getenv("PY_COLORS") else None

# Fixed strings
HEADER_TEXT = None
FOOTER_TEXT = None
DEPRECATED_STRING = "(Deprecated) "
DEFAULT_STRING = "[default: {}]"
ENVVAR_STRING = "[env var: {}]"
REQUIRED_SHORT_STRING = "*"
REQUIRED_LONG_STRING = "[required]"
RANGE_STRING = " [{}]"
APPEND_METAVARS_HELP_STRING = "({})"
ARGUMENTS_PANEL_TITLE = "Arguments"
OPTIONS_PANEL_TITLE = "Options"
COMMANDS_PANEL_TITLE = "Commands"
ERRORS_PANEL_TITLE = "Error"
ERRORS_SUGGESTION = None  # Default: Try 'cmd -h' for help. Set to False to disable.
ERRORS_EPILOGUE = None
ABORTED_TEXT = "Aborted."

# Behaviours
SHOW_ARGUMENTS = False  # Show positional arguments
SHOW_METAVARS_COLUMN = True  # Show a column with the option metavar (eg. INTEGER)
APPEND_METAVARS_HELP = False  # Append metavar (eg. [TEXT]) after the help text
GROUP_ARGUMENTS_OPTIONS = False  # Show arguments with options instead of in own panel
OPTION_ENVVAR_FIRST = False  # Show env vars before option help text instead of avert
TEXT_MARKUP = None  # One of: "rich", "markdown", None.
USE_MARKDOWN_EMOJI = True  # Parse emoji codes in markdown :smile:
COMMAND_GROUPS = {} # Define sorted groups of panels to display subcommands
OPTION_GROUPS = {} # Define sorted groups of panels to display options and arguments
USE_CLICK_SHORT_HELP = False  # Use click's default function to truncate help text
```

Full type annotations of these config options are available in `src/rich_click/rich_click.py`.

All of these are available in the `RichHelpConfiguration` object, but as lowercase.

## Config resolution order (advanced)

It probably should not matter for most use cases, but just case it does matter, there is an explicitly defined order of operations for how the configuration gets resolved:

```mermaid
flowchart TD
    A["Did you pass in a @rich_config(help_config=...)?"]
    A --> |Yes| Ayes
    A --> |No| Ano

    Ayes["Was it a dict or a RichHelpConfiguration?"]

    Ayes --> |dict| AyesBdict
    Ayes --> |RichHelpConfiguration| AyesBrhc

    AyesBdict["Is there a 'parent' config?"]
    
    AyesBdict --> |Yes| AyesBdictCyes
    AyesBdict --> |No| AyesBdictCno

    AyesBdictCyes:::StoppingPoint
    AyesBdictCyes["Merge into the parent config,\nand use that"]

    AyesBdictCno:::StoppingPoint
    AyesBdictCno["Merge into the global config,\nand use that"]

    AyesBrhc:::StoppingPoint
    AyesBrhc["Use the RichHelpConfiguration  object.\n\n(Note: RichHelpConfiguration's\ndefaults are independent of the\nglobal config.)"]

    Ano["Is there a 'parent' config?"]

    Ano --> |Yes| AnoByes
    Ano --> |No| AnoBno

    AnoByes:::StoppingPoint
    AnoByes["Use the parent config"]

    AnoBno:::StoppingPoint
    AnoBno["Use the global config"]

    classDef StoppingPoint font-weight: 600;
```
