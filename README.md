# rich-click

**Format [click](https://click.palletsprojects.com/) help output nicely with [Rich](https://github.com/Textualize/rich).**

- Click is a _"Python package for creating beautiful command line interfaces"_.
- Rich is a _"Python library for rich text and beautiful formatting in the terminal"_.

The intention of `rich-click` is to provide attractive help output from
click, formatted with rich, with minimal customisation required.

## Features

- 🌈 Rich command-line formatting of click help and error messages
- 💫 Nice styles be default, usage is simply `import rich_click as click`
- 💻 CLI tool to run on _other people's_ tools (prefix the command with `rich-click`)
- 🎁 Group commands and options into named panels
- ❌ Well formatted error messages
- 🔢 Easily give custom sort order for options and commands
- 🎨 Extensive customisation of styling and behaviour possible

![rich-click](docs/images/command_groups.svg)

_Screenshot from [`examples/03_groups_sorting.py`](examples/03_groups_sorting.py)_

## Installation

You can install `rich-click` from the [Python Package Index (PyPI)](https://pypi.org/project/rich-click/) with `pip` or equivalent.

```bash
python -m pip install rich-click
```

Conda users can find `rich-click` on [conda forge](https://anaconda.org/conda-forge/rich-click).
Just set up conda to use conda-forge (see [docs](https://conda-forge.org/docs/user/introduction.html#how-can-i-install-packages-from-conda-forge)) then run:

```bash
conda install rich-click
```

Users on macOS can install `rich-click` via [MacPorts](https://ports.macports.org/port/py-rich-click/).

```bash
sudo port install py-rich-click
```

Note that rich-click requires `click>=7` but formatted subcommands (groups) only work with `click>=8`. With v7 the output simply reverts to default click output.

## Usage

### Import as click

To use `rich-click`, switch out your normal `click` import with `rich-click`, using the same namespace:

```python
import rich_click as click
```

That's it ✨ Then continue to use `click` as you would normally.

> See [`examples/01_simple.py`](examples/01_simple.py) for an example.

The intention is to maintain most / all of the normal click functionality and arguments.
If you spot something that breaks or is missing once you start using the plugin, please create an issue about it.

### Declarative

If you prefer, you can `RichGroup` or `RichCommand` with the `cls` argument in your click usage instead.
This means that you can continue to use the unmodified `click` package in parallel.

> See [`examples/02_declarative.py`](examples/02_declarative.py) for an example.

### Command-line usage

`rich-click` comes with a CLI tool that allows you to format the click help output from _any_ package.
As long as that tool is using click and isn't already passing custom `cls` objects, it should work.
However, please consider it an experimental feature at this point.

To use, simply prefix to your normal command.
For example, to get richified click help text from a package called `awesometool`, you could run:

```console
$ rich-click awesometool --help

Usage: awesometool [OPTIONS]
..more richified output below..
```

### Patching

In some situations, you might be registering a command from another Click CLI that does not use Rich-Click:

```python
import rich_click as click
from some_library import another_cli

@click.group("my-cli")
def cli():
    pass

# `another_cli` will NOT have Rich-Click markup. :(
cli.add_command(another_cli)
```

In this situation, `another_cli` retains its original behavior. In order to make `another_cli` work with Rich-Click, you need to patch `click` before you import `another_cli`. You can patch Click with `rich_click.cli.patch` like this:

```python
import rich_click as click
from rich_click.cli import patch

patch()

from some_library import another_cli  # noqa: E402

@click.group("my-cli")
def cli():
    pass

# `another_cli` will have Rich-Click markup. :)
cli.add_command(another_cli)
```

## Customisation

There are a large number of customisation options in rich-click.
These can be modified by changing variables in the `click.rich_click` namespace.

Note that most normal click options should still work, such as `show_default=True`, `required=True` and `hidden=True`.

> Note: All images below are auto-generated using another side-project of mine: [rich-codex](https://github.com/ewels/rich-codex). Pretty cool!

### Using rich markup

In order to be as widely compatible as possible with a simple import, rich-click does _not_ parse rich formatting markup (eg. `[red]`) by default. You need to opt-in to this behaviour.

To use rich markup in your help texts, add the following:

```python
click.rich_click.USE_RICH_MARKUP = True
```

Remember that you'll need to escape any regular square brackets using a back slash in your help texts,
for example: `[dim]\[my-default: foo][\]`

![`python examples/04_rich_markup.py --help`](docs/images/rich_markup.svg "Rich markup example")

> See [`examples/04_rich_markup.py`](examples/04_rich_markup.py) for an example.

### Using Markdown

If you prefer, you can use Markdown text.
You must choose either Markdown or rich markup. If you specify both, Markdown takes preference.

```python
click.rich_click.USE_MARKDOWN = True
```

![`python examples/05_markdown.py --help`](docs/images/markdown.svg "Markdown example")

> See [`examples/05_markdown.py`](examples/05_markdown.py) for an example.

### Positional arguments

The default click behaviour is to only show positional arguments in the top usage string,
and not in the list below with the options.

If you prefer, you can tell rich-click to show arguments with `SHOW_ARGUMENTS`.
By default, they will get their own panel but you can tell rich-click to bundle them together with `GROUP_ARGUMENTS_OPTIONS`:

```python
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
```

![`python examples/06_arguments.py --help`](docs/images/arguments.svg "Positional arguments example")

> See [`examples/06_arguments.py`](examples/06_arguments.py) for an example.

### Metavars and option choices

Metavars are click's way of showing expected input types.
For example, if you have an option that must be an integer, the metavar is `INTEGER`.
If you have a choice, the metavar is a list of the possible values.

By default, rich-click shows metavars in their own column.
However, if you have a long list of choices, this column can be quite wide and result in a lot of white space:

![`python examples/08_metavars_default.py --help`](docs/images/metavars_default.svg "Default metavar display")

It may look better to show metavars appended to the help text, instead of in their own column.
For this, use the following:

```python
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True
```

![`python examples/08_metavars.py --help`](docs/images/metavars_appended.svg "Appended metavar")

> See [`examples/08_metavars.py`](examples/08_metavars.py) for an example.

### Error messages

By default, rich-click gives some nice formatting to error messages:

![`python examples/01_simple.py --hep`](docs/images/error.svg "Error message")

You can customise the _Try 'command --help' for help._ message with `ERRORS_SUGGESTION`
using rich-click though, and add some text after the error with `ERRORS_EPILOGUE`.

For example, from [`examples/07_custom_errors.py`](examples/07_custom_errors.py):

```python
click.rich_click.STYLE_ERRORS_SUGGESTION = "magenta italic"
click.rich_click.ERRORS_SUGGESTION = "Try running the '--help' flag for more information."
click.rich_click.ERRORS_EPILOGUE = "To find out more, visit [link=https://mytool.com]https://mytool.com[/link]"
```

![`python examples/07_custom_errors.py --hep`](docs/images/custom_error.svg "Custom error message")

> See [`examples/07_custom_errors.py`](examples/07_custom_errors.py) for an example.

### Help width

The default behaviour of rich-click is to use the full width of the terminal for output.
However, if you've carefully crafted your help texts for the default narrow click output, you may find that you now have a lot of whitespace at the side of the panels.

To limit the maximum width of the help output, set `MAX_WIDTH` in characters, as follows:

```python
click.rich_click.MAX_WIDTH = 100
```

### Styling

Most aspects of rich-click formatting can be customised, from colours to alignment.

For example, to print the option flags in a different colour, you can use:

```python
click.rich_click.STYLE_OPTION = "magenta"
```

To add a blank line between rows of options, you can use:

```python
click.rich_click.STYLE_OPTIONS_TABLE_LEADING = 1
click.rich_click.STYLE_OPTIONS_TABLE_BOX = "SIMPLE"
```

You can make some really ~horrible~ _colourful_ solutions using these styles if you wish:

<!-- RICH-CODEX
extra_env:
    TERMINAL_WIDTH: 160
-->

![`python examples/10_table_styles.py --help`](docs/images/style_tables.svg "Rich markup example")

> See [`examples/10_table_styles.py`](examples/10_table_styles.py) for an example.

See the [_Configuration options_](#configuration-options) section below for the full list of available options.

## Groups and sorting

`rich-click` gives functionality to list options and subcommands in groups, printed as separate panels.
It accepts a list of options / commands which means you can also choose a custom sorting order.

- For options (flags), set `click.rich_click.OPTION_GROUPS`
- For subcommands (groups), set `click.rich_click.COMMAND_GROUPS`

![`python examples/03_groups_sorting.py --help`](docs/images/command_groups.svg "Command groups")

When grouping subcommands into more than one group (in above example: 'Main usage' and 'Configuration'), you can also enforce the alignment of the help text across these groups by setting `click.rich_click.STYLE_COMMANDS_TABLE_COLUMN_WIDTH_RATIO = (1, 2)`. This results in a fixed ratio of 1:2 for the width of command name and help text column. 

> See [`examples/03_groups_sorting.py`](examples/03_groups_sorting.py) for a full example.

### Options

To group option flags into two sections with custom names, see the following example:

```python
click.rich_click.OPTION_GROUPS = {
    "mytool": [
        {
            "name": "Simple options",
            "options": ["--name", "--description", "--version", "--help"],
        },
        {
            "name": "Advanced options",
            "options": ["--force", "--yes", "--delete"],
        },
    ]
}
```

If you omit `name` it will use `Commands` (can be configured with `OPTIONS_PANEL_TITLE`).

### Commands

Here we create two groups of commands for the base command of `mytool`.
Any subcommands not listed will automatically be printed in a panel at the end labelled "Commands" as usual.

```python
click.rich_click.COMMAND_GROUPS = {
    "mytool": [
        {
            "name": "Commands for uploading",
            "commands": ["sync", "upload"],
        },
        {
            "name": "Download data",
            "commands": ["get", "fetch", "download"],
        },
    ]
}
```

If you omit `name` it will use `Commands` (can be configured with `COMMANDS_PANEL_TITLE`).

### Multiple commands

If you use multiple nested subcommands, you can specify their commands using the top-level dictionary keys:

```python
click.rich_click.COMMAND_GROUPS = {
    "mytool": [{"commands": ["sync", "auth"]}],
    "mytool sync": [
        {
            "name": "Commands for uploading",
            "commands": ["sync", "upload"],
        },
        {
            "name": "Download data",
            "commands": ["get", "fetch", "download"],
        },
    ],
    "mytool auth":[{"commands": ["login", "logout"]}],
}
```

### Table styling

Typically you would style the option / command tables using the global config options.
However, if you wish you may style tables on a per-group basis using the `table_styles` key:

```python
click.rich_click.COMMAND_GROUPS = {
    "mytool": [
        {
            "commands": ["sync", "auth"],
            "table_styles": {
                "show_lines": True,
                "row_styles": ["magenta", "yellow", "cyan", "green"],
                "border_style": "red",
                "box": "DOUBLE",
            },
        },
    ],
}
```

The available keys are: `show_lines`, `leading`, `box`, `border_style`, `row_styles`, `pad_edge`, `padding`.

## Configuration options

Here is the full list of config options:

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
STYLE_COMMANDS_TABLE_COLUMN_WIDTH_RATIO = None  # Set to a tuple[int, int] to define a column width ratio
STYLE_ERRORS_PANEL_BORDER = "red"
ALIGN_ERRORS_PANEL = "left"
STYLE_ERRORS_SUGGESTION = "dim"
STYLE_ABORTED = "red"
MAX_WIDTH = None  # Set to an int to limit to that many characters
COLOR_SYSTEM = "auto"  # Set to None to disable colors

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
USE_MARKDOWN = False  # Parse help strings as markdown
USE_MARKDOWN_EMOJI = True  # Parse emoji codes in markdown :smile:
USE_RICH_MARKUP = False  # Parse help strings for rich markup (eg. [red]my text[/])
COMMAND_GROUPS = {}  # Define sorted groups of panels to display subcommands
OPTION_GROUPS = {}  # Define sorted groups of panels to display options and arguments
USE_CLICK_SHORT_HELP = False  # Use click's default function to truncate help text
```

## Contributing

Contributions and suggestions for new features are welcome, as are bug reports!
Please create a new [issue](https://github.com/ewels/rich-click/issues)
or better still, dive right in with a pull-request.

### Local setup

1. Create a new venv with a python3.7+ interpreter using `python3 -m venv venv`
2. Activate the venv with `source venv/bin/activate`
3. Install our the package as an editable including all dev dependencies with `pip3 install -e ."[dev]"`
4. Install pre-commit with `pre-commit install`

#### Pre-commit

Our pre-commit hooks contain the following hooks:

- [Prettier](https://prettier.io/): formats our markdown and yaml files nicely.
- no relative imports: prevents you from using relative imports.
- [iSort](https://pycqa.github.io/isort/): will automatically sort the imports alphabetically.
- [black](https://black.readthedocs.io/): will automatically format your code to be according to standardized python format.
- [flake8](https://flake8.pycqa.org/): will do linting checks to make sure all your code is correctly styled and used.
- [mypy](http://mypy-lang.org/): static type checker which verifies you are not using objects incorrectly.

As mentioned, some of these tools automatically fix your code while other only highlight potential issues.
Sometimes it will be enough to try to commit a second time and it will pass, while other times it may require
manual changes to your code.

In rare cases it may be difficult or undesirable to change to code to pass the linting rules.
If this happens, it's ok to add a flake8 `# noqa` or mypy `# type: ignore` comment to skip that line.
For details of how to do this, please see the [flake8 docs](https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html#in-line-ignoring-errors)
and [mypy docs](https://mypy.readthedocs.io/en/stable/common_issues.html#spurious-errors-and-locally-silencing-the-checker).

## Credits

This package was written by Phil Ewels ([@ewels](http://github.com/ewels/)),
based on initial code by Will McGugan ([@willmcgugan](https://github.com/willmcgugan)).

rich-click is co-maintained by [@dwreeves](http://github.com/dwreeves/).

Furthermore, these contributors helped make the package what it is today:

- [@harens](http://github.com/harens/)
- [@fridex](http://github.com/fridex/)
- [@pawamoy](http://github.com/pawamoy/)
- [@jorrick](http://github.com/harens/)
