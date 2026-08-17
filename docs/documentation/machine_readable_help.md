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

An unknown value shows the normal terminal help. It does not cause an error.

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
| `multiple` | Present and true for a repeatable parameter. |
| `nargs` | Present when the arity is not one. |
| `envvar` | One environment variable or a list of variables. |
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

The schema starts with Click's `to_info_dict()` result. Custom command and parameter fields pass through when they do not replace a derived field.

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

Set `AGENT_HELP_FORMAT` to `None` to keep the normal terminal help in agent environments. Set `RICH_CLICK_AGENT_MODE=true` or `false` to override environment detection for one process.

An explicit `--help <format>` always uses the requested format.

## Install help format plugins

Python packages can add formats through the `rich_click.help_formats` entry-point group. rich-click discovers these packages automatically. A CLI that already uses rich-click does not need a source change.

For example, [`rich-click-help-formats`](https://github.com/ewels/rich-click-help-formats) adds YAML, HTML, and Carapace:

```console
pip install rich-click-help-formats
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

Install the package in the same Python environment as the target CLI. The CLI then accepts `--help yaml` without any code change.

Use one entry point for each format. Use a short, lowercase entry-point name. Keep each renderer in a separate module when a package provides multiple formats.

rich-click checks format sources in this order:

1. Formats on the command class.
2. Formats in the active rich-click configuration.
3. Installed plugin entry points.

The earlier source wins when two sources use the same name. If two installed plugins use the same normalized name, rich-click raises an error that identifies both entry points.

The public renderer type is `rich_click.help_formats.HelpFormatRenderer`. The entry-point group constant is `rich_click.help_formats.HELP_FORMAT_ENTRY_POINT_GROUP`.

## Register an in-process format

Use the `help_formats` configuration when the renderer is part of the CLI application instead of a separately installed package:

```python
import rich_click as click


def render_yaml(command, ctx):
    import yaml

    return yaml.safe_dump(command.format_help_json(ctx, ctx.make_formatter()), sort_keys=False)


click.rich_click.HELP_FORMATS = {"yaml": render_yaml}
```

This changes only the current application process. Use a package entry point when the format must work for unrelated rich-click CLIs.

You can also add a method name to `RichCommand.help_formats` in a command subclass. This option is useful when the output depends on a custom command class.

## Command examples

Examples declared with the `examples=` command argument flow into structured formats:

- Markdown adds an `Examples` section.
- JSON adds an `examples` array to the matching command.
- Plugin renderers can read the same `examples` field from `command_schema()`.

See [Command Examples](examples.md) for the declaration syntax.
