# Structured help formats

rich-click can return the complete command tree through the existing `--help` option.
The default installation includes three structured formats:

| Value | Output |
| --- | --- |
| `--help markdown` | Markdown with one section for each command. |
| `--help json` | JSON with full parameter data at every command level. |
| `--help compact` | A compact text format for coding agents. |

A bare `--help` still shows the normal terminal help for human users. The format value can follow a space or an equals sign:

```console
mytool --help json
mytool --help=json
```

When structured help is enabled, an unknown format value shows normal terminal help. It does not cause
an error.

## Select or disable formats

The `help_formats` configuration controls which built-in and in-process format names `--help` accepts.
The default value is `["compact", "markdown", "json"]`. The list order controls the order in the help
metavar. Formats from installed plugins (see below) are appended automatically and are not affected by
this list.

Enable only Markdown for one command:

```python
import rich_click as click


@click.command()
@click.rich_config(
    help_config=click.RichHelpConfiguration(help_formats=["markdown"])
)
def cli():
    pass
```

Set `help_formats=[]` to turn off the built-in formats while still allowing any installed plugin to add
its own:

```python
click.rich_click.HELP_FORMATS = []
```

Set `help_formats=False` to disable structured help entirely, plugins included:

```python
click.rich_click.HELP_FORMATS = False
```

This setting restores the help option used before structured formats were added. `--help` becomes a
Boolean flag again. It does not show a format metavar. It does not use agent-specific help. A command
such as `--help=json` returns the old “does not take a value” error.

## Markdown

`--help markdown` returns every command in the tree. Each command has a top-level heading with its full invocation path:

```markdown
# `mytool`

Manage projects.

**Usage:** `mytool [OPTIONS] COMMAND [ARGS]...`

## Options

| Option | Type | Description |
| --- | --- | --- |
| `--verbose` | flag | Show more detail. |

# `mytool create`

Create a project.
```

Markdown parameter tables omit a column when every row in that table has an empty value.

## JSON

`--help json` returns the complete command tree. The root object and each object in `subcommands` use the same shape:

```json
{
  "name": "mytool",
  "path": "mytool",
  "help": "Manage projects.",
  "usage": "mytool [OPTIONS] COMMAND [ARGS]...",
  "params": [],
  "subcommands": {
    "create": {
      "name": "create",
      "path": "mytool create",
      "help": "Create a project.",
      "usage": "mytool create [OPTIONS] NAME",
      "params": []
    }
  }
}
```

Each parameter can contain these fields:

| Field | Meaning |
| --- | --- |
| `name` | Python parameter name. |
| `kind` | `option` or `argument`. |
| `opts` | Option names such as `-v` and `--verbose`. |
| `secondary_opts` | Secondary names such as `--no-debug`. |
| `type` | Click type such as `String`, `Int`, or `Path`. |
| `type_info` | Extra type constraints such as a range. |
| `choices` | Accepted values for a `Choice`. |
| `required` | Present and true for a required parameter. |
| `default` | Present when the default carries useful information. |
| `is_flag` | Present and true for a flag option. |
| `flag_value` | Value assigned by a non-boolean value flag. |
| `count` | Present and true for a counting flag such as `-vvv`. |
| `multiple` | Present and true for a repeatable parameter. |
| `nargs` | Present when the arity is not one. |
| `envvar` | One environment variable or a list of variables. |
| `prompt` | Text shown when the option prompts for input. |
| `hidden` | Present and true when the parameter is hidden from normal help. |
| `help` | Plain parameter help text. |

The `--help` parameter includes a `choices` list. This list contains the built-in formats, config formats, and installed plugin formats.

### Customize the JSON schema

Set `help_json_transform` to change the completed schema before rich-click serializes it:

```python
import rich_click as click


def add_version(schema, command, ctx):
    schema["version"] = "1.2.3"
    return schema


click.rich_click.HELP_JSON_TRANSFORM = add_version
```

You can also override `format_help_json()` on a `RichCommand` subclass.

The schema starts with Click's `to_info_dict()` fields. Custom fields from `RichCommand` subclasses,
plain Click leaf commands, and parameter subclasses pass through when they do not replace a derived
field. Plain Click group subclasses use Click's standard group fields so rich-click can traverse lazy
commands once without triggering Click's second recursive walk. Custom `get_params()`,
`collect_usage_pieces()`, and plain Click leaf `to_info_dict()` implementations must be stable when
Click calls them more than once.

Named JSON, Markdown, and compact formats are introspection interfaces, so they can include declared
defaults that normal terminal help does not show. Set `show_default=False` explicitly to omit a default
from Markdown and compact output. Automatic agent help always follows Click's effective default
visibility. JSON retains defaults as schema data.

Recursive help creates descendant contexts without parsing arguments. This prevents option callbacks
from running during help generation. If a `RichCommand` subclass adds context setup in `make_context()`,
put the equivalent no-parse setup in `make_context_without_parsing()`. A command that only overrides
`make_context()` causes explicit recursive help to fail instead of returning an incomplete schema.

## Compact

`--help compact` returns the complete tree with one line for each record. It omits Markdown tables and the repeated `--help` parameter.

```text
# mytool — Manage projects.

# mytool create — Create a project.
usage: mytool create NAME
--template basic|web  Project template.
```

An explicit `--help compact` has no character limit.

## Help for coding agents

rich-click detects common coding-agent environments. In these environments, a bare `--help` uses the `agent_help_format` setting. Its default value is `compact`.

The agent-facing compact output uses `agent_help_max_chars`, which defaults to 25,000 characters. rich-click always includes the requested command and the name of every descendant. It adds more detail while space remains.

Set global values when you must change this behavior for all commands:

```python
import rich_click as click

click.rich_click.AGENT_HELP_FORMAT = "json"
click.rich_click.AGENT_HELP_MAX_CHARS = 40_000
```

Set `AGENT_HELP_FORMAT` to `None` to keep the normal terminal help in agent environments. Set
`RICH_CLICK_AGENT_MODE=true` or `false` to override environment detection for one process. The selected
agent format must also appear in `HELP_FORMATS`.

An explicit `--help <format>` always uses the requested format when its name is enabled.

## Install help format plugins

Python packages can add renderers through the `rich_click.help_formats` entry-point group. rich-click
discovers these packages automatically and appends them to every command's format list -- an end user
gets the new format on any rich-click CLI just by installing the plugin, with no change to that CLI's
source. This only stops working if the CLI has set `help_formats=False` (see above), which disables
machine-readable help, plugins included.

For example, [`rich-click-help-formats`](https://github.com/ewels/rich-click-help-formats) adds YAML, HTML, and Carapace:

```console
pip install rich-click-help-formats
```

The CLI now accepts:

```console
mytool --help yaml
mytool --help html
mytool --help carapace
```

rich-click reads entry-point metadata when it builds the format list. It imports a plugin renderer only when a caller selects that format.

## Create a help format plugin

A plugin entry point maps a format name to a renderer. The renderer accepts a Click command and context. It returns the complete output as a string.

This renderer emits YAML from rich-click's recursive schema:

```python
# src/my_help_formats/yaml.py
import yaml

from rich_click.help_json import command_schema


def render(command, ctx):
    schema = command_schema(command, ctx, recursive=True)
    return yaml.safe_dump(schema, sort_keys=False)
```

Register the renderer in the plugin package's `pyproject.toml`:

```toml
[project.entry-points."rich_click.help_formats"]
yaml = "my_help_formats.yaml:render"
```

Installing the package in the same Python environment as the target CLI is enough -- rich-click appends
the plugin's format name to every command automatically.

Use one entry point for each format. Use a short, lowercase entry-point name. Keep each renderer in a separate module when a package provides multiple formats.

rich-click checks format sources in this order:

1. Formats on the command class.
2. Formats in the active `help_format_renderers` registry.
3. Installed plugin entry points.

The earlier source wins when two sources use the same name. If two installed plugins use the same normalized name, rich-click raises an error that identifies both entry points.

The public renderer type is `rich_click.help_formats.HelpFormatRenderer`. The entry-point group constant is `rich_click.help_formats.HELP_FORMAT_ENTRY_POINT_GROUP`.

## Register an in-process format

Use `help_format_renderers` when the renderer is part of the CLI application. Add the same name to
`help_formats`:

```python
import rich_click as click


def render_yaml(command, ctx):
    import yaml

    return yaml.safe_dump(command.format_help_json(ctx, ctx.make_formatter()), sort_keys=False)


click.rich_click.HELP_FORMATS.append("yaml")
click.rich_click.HELP_FORMAT_RENDERERS = {"yaml": render_yaml}
```

This changes only the current application process. Use a package entry point when the format must work for unrelated rich-click CLIs.

You can also add a method name to `RichCommand.help_format_methods` in a command subclass. Add the same
name to the `help_formats` configuration list.

## Command examples

Examples declared with the `examples=` command argument flow into structured formats:

- Markdown adds an `Examples` section.
- JSON adds an `examples` array to the matching command.
- Plugin renderers can read the same `examples` field from `command_schema()`.

See [Command Examples](examples.md) for the declaration syntax.
