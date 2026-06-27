# Machine-readable help

CLIs are increasingly driven not just by humans, but by tooling and LLM agents.
Those consumers struggle with the rendered `--help` screen: it is laid out for human reading, wraps to the terminal width, and carries Rich styling that obscures the underlying structure.

**rich-click** already holds all of this information as structured data, and exposes it as **format values on the existing `--help` flag**:

| Invocation                       | Output                                                                                                               |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `--help`                         | The normal human-readable help. **Unchanged** — byte-for-byte identical to before.                                   |
| `--help markdown` (alias `md`)   | LLM-friendly Markdown for the current command, plus a subcommand index (_progressive disclosure_).                   |
| `--help markdown-full` (`md-full`) | LLM-friendly Markdown documenting every command in the tree.                                                        |
| `--help json`                    | Machine-readable JSON for the current command, plus a name-only index of its subcommands (_progressive disclosure_). |
| `--help json-full`               | The whole command tree in one call, with full parameter detail at every node.                                        |
| `--help carapace`                | Output conforming to the [carapace](https://carapace.sh) completion spec.                                            |

This capability is **always available** on every rich-click CLI — there is nothing to enable, and bare `--help` is untouched. The format machinery only engages when a value is given.

!!! note "Pass the format after a space"
    The documented form is a space — `mytool --help json` — though the attached form `mytool --help=json` works too. A bare `--help`, or an unrecognized value (a typo, or `mytool --help install` mistakenly meaning "help for the `install` command"), simply shows the normal human-readable help rather than erroring — exactly as a plain `--help` always ignored anything that followed it. To get a subcommand's help, put `--help` after it: `mytool install --help`.

The example CLI used throughout this page:

```python
{% include "../code_snippets/help_json/help_json.py" %}
```

See the [Configuration](configuration.md) page for how to set config options globally or per-command with the `rich_config` decorator.

## `--help markdown`: Markdown for LLMs

`--help markdown` (alias `--help md`) renders the CLI's structure as Markdown, tuned for dropping into an LLM prompt: headings for hierarchy, each command titled by its **full invocation path** so the section is unambiguous out of context, and parameters laid out as compact tables.

```console
$ mytool hello --help markdown
```

```markdown
# `cli hello`

Greet someone.

**Usage:** `cli hello [OPTIONS] NAME`

## Arguments

| Argument | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `name` | String | yes |  |  |

## Options

| Option | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--count` | Int |  | `1` | Number of greetings. |
```

It is progressive: the current command is documented in full, and subcommands appear as a nested name index. `--help markdown-full` (alias `--help md-full`) instead documents **every** command in the tree, each as its own top-level (`#`) section — a flat, uniform layout that is easy for a model to parse and navigate by path.

## `--help json`: progressive disclosure

Running a command with `--help json` prints that command's help, usage and full parameter detail as JSON, together with a name-only index of its subcommands:

```console
$ mytool --help json
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
    },
    {
      "name": "help",
      "kind": "option",
      "opts": ["--help"],
      "choices": ["markdown", "markdown-full", "json", "json-full", "carapace"],
      "help": "Show this message and exit."
    }
  ],
  "subcommands": {
    "db": {
      "help": "Manage the database.",
      "subcommands": { "migrate": { "help": "Run migrations." } }
    },
    "hello": { "help": "Greet someone." }
  }
}
```

Every command reports its `--help` option too, just as the rendered help screen lists it — with the machine-readable formats it accepts surfaced as `choices`, so an agent reading the schema discovers them. (The remaining examples on this page omit the `--help` entry for brevity.)

The format is **contextual**: it reports the current command in full, but for its descendants lists only their names and a one-line description (not their parameters or usage).
This lets tools and agents discover a CLI one level at a time — they can see what each subcommand does and drill down by name, rather than pulling the whole command tree into context at once.

Running it on a subcommand returns that command's full detail, including positional arguments:

```console
$ mytool hello --help json
```

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

The flag is **eager**, exactly like a bare `--help`, so it works even when required arguments are missing:

```shell
# Prints the schema for `hello`, despite the required NAME argument being absent.
python help_json.py hello --help json
```

## `--help json-full`: the whole tree at once

Where `--help json` discloses one level at a time, `--help json-full` expands **every** descendant to its full detail — parameters, usage and nested subcommands — in a single call.
Each node looks exactly like a direct `--help json` on that command would.

This is aimed at consumers that want the entire surface up front rather than crawling it: code generators, documentation builders, and tools that turn a CLI into an [MCP](https://modelcontextprotocol.io) server.

```console
$ mytool --help json-full
```

```json
{
  "name": "cli",
  "path": "cli",
  "usage": "cli [OPTIONS] COMMAND [ARGS]...",
  "params": [{ "name": "verbose", "kind": "option", "opts": ["--verbose", "-v"], "type": "Bool", "is_flag": true }],
  "subcommands": {
    "hello": {
      "name": "hello",
      "path": "cli hello",
      "usage": "cli hello [OPTIONS] NAME",
      "params": [
        { "name": "count", "kind": "option", "opts": ["--count"], "type": "Int", "default": 1 },
        { "name": "name", "kind": "argument", "type": "String", "required": true }
      ]
    },
    "db": {
      "name": "db",
      "path": "cli db",
      "subcommands": { "migrate": { "name": "migrate", "path": "cli db migrate", "params": [] } }
    }
  }
}
```

## `--help carapace`: completion spec

[carapace](https://carapace.sh) is a multi-shell completion engine. Emitting `--help carapace` produces a document conforming to its [command spec](https://carapace.sh/schemas/command.json), so a rich-click CLI becomes a **producer** for carapace's consumer ecosystem.

The output is **YAML** — the format carapace's spec files use — led by the schema directive that editors use for validation:

```console
$ mytool --help carapace
```

```yaml
# yaml-language-server: $schema=https://carapace.sh/schemas/command.json
name: cli
description: A demo CLI.
parsing: non-interspersed
flags:
  -v, --verbose: Enable verbose output.
  --help=: Show this message and exit.
completion:
  flag:
    help: [markdown, markdown-full, json, json-full, carapace]
commands:
- name: hello
  description: Greet someone.
  flags:
    --count=: Number of greetings.
- name: db
  description: Manage the database.
  parsing: non-interspersed
  commands: [...]
```

!!! note "YAML is optional"
    YAML output needs `pyyaml`; install it with the `rich-click[carapace]` extra. Without it, `--help carapace` falls back to **JSON** — which is itself valid YAML, so carapace still consumes it (you just lose the schema directive comment).

Carapace is a structure-and-completion spec rather than a type/validation one, so the mapping is intentionally lossy. Flag keys use carapace's string syntax (`-s, --long` for a boolean, a trailing `=` when the flag takes a value, `*` when it is repeatable, and the `{description, nargs}` object form for multi-value flags); negation flags such as `--no-debug` become their own entries; and `Choice` values are surfaced as completion candidates. Parameter **types** (`Int`/`Path`/…), **defaults**, **envvars** and per-flag **required** have no home in the carapace schema and are dropped — reach for `--help json-full` if you need those.

## Command examples

LLMs respond well to concrete examples. If you give commands examples with the [`examples=` argument](examples.md) — primarily to enrich the rendered `--help` — they flow into the machine-readable formats too:

- `--help markdown` / `--help markdown-full` — an `## Examples` section.
- `--help json` / `--help json-full` — an `examples` array of `{"command", "description"}` objects.
- `--help carapace` — the spec's `examples` map, keyed by the command line.

!!! note
    The carapace `examples` field is a map keyed by the command line, as the spec requires. If two
    examples share the same command (differing only in their descriptions), they collapse to a single
    entry and the last description wins. The `--help json` formats keep every example as a list, so use
    those if you need to preserve duplicates.

See [Command Examples](examples.md) for how to define them.

## What the JSON schema contains

For every command level, the `json` / `json-full` object contains:

| Key           | Description                                                                                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | The command's name.                                                                                                                                                 |
| `path`        | The full invocation path (e.g. `cli db migrate`).                                                                                                                   |
| `help`        | The command's help text, with Rich markup stripped to plain text. Omitted if the command is undocumented.                                                           |
| `usage`       | The usage string.                                                                                                                                                   |
| `params`      | A list of the command's options and arguments, including the `--help` option (its `choices` list the machine-readable formats it accepts).                            |
| `subcommands` | Present only for groups. In `json` it is a name-only index (one-line `help`, plus `aliases` / nested `subcommands`); in `json-full` each entry is the full schema. |

Each entry in `params` has the following keys when applicable:

| Key              | Description                                                                          |
| ---------------- | ------------------------------------------------------------------------------------ |
| `name`           | The Python-side parameter name.                                                      |
| `kind`           | `"option"` or `"argument"`.                                                          |
| `opts`           | An option's flag(s) as seen on the command line. Omitted for arguments (use `name`). |
| `secondary_opts` | An option's negation flags, e.g. `--no-debug` for `--debug/--no-debug`.              |
| `type`           | The parameter type, e.g. `"Bool"`, `"Int"`, `"String"`, `"Path"`.                    |
| `type_info`      | Extra type constraints (range min/max, `Path` flags, `Choice` case-sensitivity).     |
| `choices`        | The allowed values, for a `Choice` type (and the formats accepted by `--help`).      |
| `required`       | Present and `true` only when the parameter is required.                              |
| `is_flag`        | Present and `true` only for boolean flags.                                           |
| `flag_value`     | The value a value-flag sets (e.g. `--upper`/`--lower` sharing a destination).        |
| `count`          | Present and `true` for counting options (`-v`/`-vv`/`-vvv`).                          |
| `multiple`       | Present and `true` only when the parameter may be repeated.                          |
| `nargs`          | The argument count, when not the default of `1` (e.g. `-1` for variadic).            |
| `envvar`         | The environment variable the parameter reads from, if any.                           |
| `prompt`         | The prompt string shown when the option is requested interactively.                  |
| `hidden`         | Present and `true` for hidden parameters (kept, but flagged).                        |
| `default`        | The default value, for non-flag parameters that have one.                            |
| `help`           | The parameter's help text, as plain text.                                            |

## Adding your own data

The schema is built from each command's `to_info_dict()` — the same Click method that powers introspection elsewhere — so anything you add there flows through automatically.
Custom **command-level** fields are merged onto the top-level object; custom **parameter-level** fields are merged onto the parameter (a custom key never overwrites one rich-click already set):

```python
import rich_click as click


class DocumentedCommand(click.RichCommand):
    def to_info_dict(self, ctx):
        info = super().to_info_dict(ctx)
        info["stability"] = "beta"  # -> top-level "stability"
        return info


class SecretOption(click.RichOption):
    def to_info_dict(self):
        info = super().to_info_dict()
        info["sensitive"] = True  # -> appears on the parameter
        return info
```

rich-click's own [aliases](panels/tips.md) flow through the same way, appearing as a top-level `aliases` key on commands that define them.

### The `help_json_transform` hook

If you would rather not subclass, set `help_json_transform` to a callable that post-processes the JSON schema (both `json` and `json-full`) just before it is printed. It receives `(schema, command, ctx)` and returns the schema to emit:

```python
import rich_click as click

click.rich_click.HELP_JSON_TRANSFORM = lambda schema, cmd, ctx: {**schema, "version": "1.2.3"}
```

### Overriding the format methods

For full control, the serialization mirrors Click's own `get_help` / `format_help` split: each `get_help_*(ctx)` method serializes whatever the matching `format_help_*(ctx, formatter)` returns. Override the `format_help_*` method on a `RichCommand` subclass to reshape the output (it returns the data statelessly rather than writing to the formatter):

| Format             | `get_*` method          | Override this               |
| ------------------ | ----------------------- | --------------------------- |
| `--help markdown`      | `get_help_markdown`     | `format_help_markdown`      |
| `--help markdown-full` | `get_help_markdown_full`| `format_help_markdown_full` |
| `--help json`          | `get_help_json`         | `format_help_json`          |
| `--help json-full`     | `get_help_json_full`    | `format_help_json_full`     |
| `--help carapace`      | `get_help_carapace`     | `format_help_carapace`      |

```python
import rich_click as click


class MyCommand(click.RichCommand):
    def format_help_json(self, ctx, formatter):
        data = super().format_help_json(ctx, formatter)
        data["version"] = "1.2.3"
        return data
```

### Adding a new format

The `--help <format>` dispatch is a registry, `RichCommand.help_formats`, mapping each format name to the method that renders it. Add your own by extending it in a subclass — no need to touch the dispatch:

```python
import rich_click as click


class MyCommand(click.RichCommand):
    help_formats = {**click.RichCommand.help_formats, "yaml": "get_help_yaml"}

    def get_help_yaml(self, ctx):
        import yaml

        return yaml.safe_dump(self.format_help_json(ctx, ctx.make_formatter()))
```
