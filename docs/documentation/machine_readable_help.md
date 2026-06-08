# Machine-readable help

CLIs are increasingly driven not just by humans, but by tooling and LLM agents.
Those consumers struggle with the rendered `--help` screen: it is laid out for human reading, wraps to the terminal width, and carries Rich styling that obscures the underlying structure.

**rich-click** already holds all of this information as structured data. The `help_json` config option exposes it directly, as a [JSON Schema](https://json-schema.org) document.

## Enabling `--help-json`

The feature is off by default, so there is no behavioural change unless you opt in.

Set the `help_json` config option to `True`.
This adds a global `--help-json` flag to every command and group:

```python hl_lines="6"
{% include "../code_snippets/help_json/help_json.py" %}
```

See the [Configuration](configuration.md) page for how to set config options globally or per-command with the `rich_config` decorator.

## Example output

Running the top-level command with `--help-json` prints the current command's help, usage and full parameter detail as a JSON Schema document, together with a recursive index of subcommand names:

```console
$ mytool --help-json
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "cli",
  "description": "A demo CLI.",
  "x-usage": "cli [OPTIONS] COMMAND [ARGS]...",
  "type": "object",
  "properties": {
    "verbose": {
      "type": "boolean",
      "description": "Enable verbose output.",
      "x-cli": { "opts": ["--verbose", "-v"], "kind": "option", "is_flag": true }
    }
  },
  "x-subcommands": {
    "db": { "migrate": {} },
    "hello": {}
  }
}
```

The flag also appears in the regular `--help` output, so it is discoverable:

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/help_json
    -->
    ![`python help_json.py --help`](../images/code_snippets/help_json/help_json.svg){.screenshot}

## Why JSON Schema?

JSON Schema is a widely understood standard that validators, function-calling frameworks and LLMs already speak.
The standard keywords — `type`, `enum`, `required`, `default`, `description` — are meaningful to those consumers without any rich-click-specific knowledge.

A command-line invocation is not a JSON document, though, so everything JSON Schema has no vocabulary for lives under `x-` [extension keys](https://json-schema.org/blog/posts/custom-annotations-will-continue), which validators ignore by specification:

| Key             | Where        | Description                                                                  |
| --------------- | ------------ | ---------------------------------------------------------------------------- |
| `x-usage`       | top level    | The usage string.                                                            |
| `x-subcommands` | top level    | Present only for groups: a recursive, names-only index of all descendants.   |
| `x-cli`         | per property | CLI-specific facts about a parameter (see below).                            |

This gives a clean two-layer split: a standard layer a generic tool can read and validate, and a CLI layer for consumers that understand the command line.

## Progressive disclosure

The flag is **contextual**: it reports the current command in full, but lists only the _names_ of its descendants under `x-subcommands`.
This lets tools and agents discover a CLI one level at a time, drilling down by subcommand name, rather than pulling the whole command tree into context at once.

Running it on a subcommand returns that command's full detail, including positional arguments and the top-level `required` array:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "cli hello",
  "description": "Greet someone.",
  "x-usage": "cli hello [OPTIONS] NAME",
  "type": "object",
  "properties": {
    "count": {
      "type": "integer",
      "description": "Number of greetings.",
      "default": 1,
      "x-cli": { "opts": ["--count"], "kind": "option" }
    },
    "name": {
      "type": "string",
      "x-cli": { "opts": ["name"], "kind": "argument" }
    }
  },
  "required": ["name"]
}
```

The flag is **eager**, exactly like `--help`, so it works even when required arguments are missing:

```shell
# Prints the schema for `hello`, despite the required NAME argument being absent.
python help_json.py hello --help-json
```

## What the schema contains

For every command level, the top-level JSON object contains:

| Key             | Description                                                                                |
| --------------- | ------------------------------------------------------------------------------------------ |
| `$schema`       | The JSON Schema dialect URI.                                                               |
| `title`         | The full invocation path (e.g. `cli db migrate`).                                          |
| `description`   | The command's help text, with Rich markup stripped to plain text. Omitted if empty.        |
| `type`          | Always `"object"`.                                                                          |
| `properties`    | A map of parameter name → schema. The `--help` / `--help-json` meta-options are omitted.    |
| `required`      | The names of required parameters. Omitted if none.                                          |
| `x-usage`       | The usage string.                                                                           |
| `x-subcommands` | Present only for groups: a recursive, names-only index of all descendants.                  |

Each entry in `properties` is a JSON Schema property. Standard validation facts use JSON Schema keywords:

| Key           | Description                                                                |
| ------------- | -------------------------------------------------------------------------- |
| `type`        | `"integer"`, `"number"`, `"boolean"`, `"string"`, or `"array"` (repeatable). |
| `enum`        | The allowed values, for a `Choice` type.                                   |
| `default`     | The default value, for non-flag parameters that have one.                  |
| `description` | The parameter's help text, as plain text.                                  |

CLI-specific facts that JSON Schema cannot express live under `x-cli`:

| Key              | Description                                                                       |
| ---------------- | --------------------------------------------------------------------------------- |
| `opts`           | The flag(s) or argument name as seen on the command line.                         |
| `kind`           | `"option"` or `"argument"`.                                                       |
| `is_flag`        | Present and `true` only for boolean flags.                                        |
| `hidden`         | Present and `true` for hidden parameters (kept in the schema, but flagged).        |
| `secondary_opts` | The off-switch flag(s), e.g. `--no-foo`, when present.                            |
| `count`          | Present and `true` for counting options (e.g. `-vvv`).                            |
| `nargs`          | Present when not `1` (e.g. `-1` for variadic).                                    |
| `envvar`         | The environment variable(s) the parameter reads, when set.                       |
| `type`           | The precise Click type (e.g. `"Path"`, `"DateTime"`) when it is not a basic type. |

## Adding your own data

The schema is built from each command's `to_info_dict()` — the same Click method that powers introspection elsewhere — so anything you add there flows through automatically.

Custom **command-level** fields appear as `x-<field>` at the top level; custom **parameter-level** fields appear inside that parameter's `x-cli` object:

```python
import rich_click as click


class DocumentedCommand(click.RichCommand):
    def to_info_dict(self, ctx):
        info = super().to_info_dict(ctx)
        info["examples"] = ["cli deploy --token=XXX prod"]  # -> "x-examples"
        return info


class SecretOption(click.RichOption):
    def to_info_dict(self):
        info = super().to_info_dict()
        info["sensitive"] = True  # -> appears inside the parameter's "x-cli"
        return info
```

rich-click's own [panels](panels/index.md) and [aliases](panels/tips.md) flow through the same way, as `x-panels` and `x-aliases`.

### The `help_json_transform` hook

If you would rather not subclass, set `help_json_transform` to a callable that post-processes the schema just before it is printed. It receives `(schema, command, ctx)` and returns the schema to emit:

```python
import rich_click as click

click.rich_click.HELP_JSON = True
click.rich_click.HELP_JSON_TRANSFORM = lambda schema, cmd, ctx: {**schema, "x-version": "1.2.3"}
```

## Customizing the flag name

The flag is named `--help-json` by default, rather than `--json`, because many CLIs already define their own `--json` data-output flag.

If `--help-json` clashes with an existing option in your CLI, change it with the `help_json_option_name` config option:

```python
import rich_click as click

click.rich_click.HELP_JSON = True
click.rich_click.HELP_JSON_OPTION_NAME = "--schema"
```
