# Machine-readable help

CLIs are increasingly driven not just by humans, but by tooling and LLM agents.
Those consumers struggle with the rendered `--help` screen: it is laid out for human reading, wraps to the terminal width, and carries Rich styling that obscures the underlying structure.

**rich-click** already holds all of this information as structured data. The `help_json` config option exposes it directly.

## Enabling `--help-json`

The feature is off by default, so there is no behavioural change unless you opt in.

Set the `help_json` config option to `True`.
This adds a global `--help-json` flag to every command and group:

```python hl_lines="6"
{% include "../code_snippets/help_json/help_json.py" %}
```

See the [Configuration](configuration.md) page for how to set config options globally or per-command with the `rich_config` decorator.

## Example output

Running the top-level command with `--help-json` prints the current command's help, usage and full parameter detail as JSON, together with a recursive index of subcommand names:

```console
$ mytool --help-json
```

```json
{
  "name": "cli",
  "path": "cli",
  "help": "A demo CLI.",
  "usage": "cli [OPTIONS] COMMAND [ARGS]...",
  "params": [
    {
      "name": "verbose",
      "kind": "option",
      "opts": ["--verbose", "-v"],
      "type": "Bool",
      "is_flag": true,
      "help": "Enable verbose output."
    }
  ],
  "subcommands": {
    "db": { "help": "Manage the database.", "subcommands": { "migrate": { "help": "Run migrations." } } },
    "hello": { "help": "Greet someone." }
  }
}
```

The flag also appears in the regular `--help` output, so it is discoverable:

???+ example "Output"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/help_json
    -->
    ![`python help_json.py --help`](../images/code_snippets/help_json/help_json.svg){.screenshot}

## Progressive disclosure

The flag is **contextual**: it reports the current command in full, but for its descendants lists only their names and a one-line description (not their parameters or usage).
This lets tools and agents discover a CLI one level at a time — they can see what each subcommand does and drill down by name, rather than pulling the whole command tree into context at once.

Running it on a subcommand returns that command's full detail, including positional arguments:

```json
{
  "name": "hello",
  "path": "cli hello",
  "help": "Greet someone.",
  "usage": "cli hello [OPTIONS] NAME",
  "params": [
    {
      "name": "count",
      "kind": "option",
      "opts": ["--count"],
      "type": "Int",
      "help": "Number of greetings.",
      "default": 1
    },
    {
      "name": "name",
      "kind": "argument",
      "type": "String",
      "required": true
    }
  ]
}
```

The flag is **eager**, exactly like `--help`, so it works even when required arguments are missing:

```shell
# Prints the schema for `hello`, despite the required NAME argument being absent.
python help_json.py hello --help-json
```

## What the schema contains

For every command level, the JSON object contains:

| Key           | Description                                                                                           |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| `name`        | The command's name.                                                                                   |
| `path`        | The full invocation path (e.g. `cli db migrate`).                                                     |
| `help`        | The command's help text, with Rich markup stripped to plain text. Omitted if the command is undocumented. |
| `usage`       | The usage string.                                                                                     |
| `params`      | A list of the command's options and arguments. The `--help` / `--help-json` meta-options are omitted. |
| `subcommands` | Present only for groups: a recursive index of all descendants. Each entry carries a one-line `help` (plus `aliases` and a nested `subcommands` where present). |

Each entry in `params` has the following keys when applicable:

| Key        | Description                                                       |
| ---------- | ----------------------------------------------------------------- |
| `name`     | The Python-side parameter name.                                   |
| `kind`     | `"option"` or `"argument"`.                                       |
| `opts`     | An option's flag(s) as seen on the command line. Omitted for arguments (use `name`). |
| `type`     | The parameter type, e.g. `"Bool"`, `"Int"`, `"String"`, `"Path"`. |
| `choices`  | The allowed values, for a `Choice` type.                          |
| `required` | Present and `true` only when the parameter is required.           |
| `is_flag`  | Present and `true` only for boolean flags.                        |
| `multiple` | Present and `true` only when the parameter may be repeated.       |
| `hidden`   | Present and `true` for hidden parameters (kept, but flagged).     |
| `default`  | The default value, for non-flag parameters that have one.         |
| `help`     | The parameter's help text, as plain text.                         |

## Adding your own data

The schema is built from each command's `to_info_dict()` — the same Click method that powers introspection elsewhere — so anything you add there flows through automatically.
Custom **command-level** fields are merged onto the top-level object; custom **parameter-level** fields are merged onto the parameter (a custom key never overwrites one rich-click already set):

```python
import rich_click as click


class DocumentedCommand(click.RichCommand):
    def to_info_dict(self, ctx):
        info = super().to_info_dict(ctx)
        info["examples"] = ["cli deploy --token=XXX prod"]  # -> top-level "examples"
        return info


class SecretOption(click.RichOption):
    def to_info_dict(self):
        info = super().to_info_dict()
        info["sensitive"] = True  # -> appears on the parameter
        return info
```

rich-click's own [aliases](panels/tips.md) flow through the same way, appearing as a top-level `aliases` key on commands that define them.

### The `help_json_transform` hook

If you would rather not subclass, set `help_json_transform` to a callable that post-processes the schema just before it is printed. It receives `(schema, command, ctx)` and returns the schema to emit:

```python
import rich_click as click

click.rich_click.HELP_JSON = True
click.rich_click.HELP_JSON_TRANSFORM = lambda schema, cmd, ctx: {**schema, "version": "1.2.3"}
```

## Customizing the flag name

The flag is named `--help-json` by default, rather than `--json`, because many CLIs already define their own `--json` data-output flag.

If `--help-json` clashes with an existing option in your CLI, change it with the `help_json_option_name` config option:

```python
import rich_click as click

click.rich_click.HELP_JSON = True
click.rich_click.HELP_JSON_OPTION_NAME = "--schema"
```
