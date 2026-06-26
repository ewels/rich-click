# Command examples

Good `--help` output often includes a few concrete invocations. Pass `examples=` to a command or group — a list of `(description, command)` tuples — and **rich-click** renders them in a dedicated **Examples** panel, right after the options and commands:

```python
import rich_click as click


@click.command(
    examples=[
        ("Deploy to production", "mytool deploy prod"),
        ("Preview a staging deploy", "mytool deploy --dry-run staging"),
    ],
)
@click.option("--dry-run", is_flag=True, help="Preview only.")
@click.argument("target")
def deploy(dry_run, target):
    """Deploy a service."""
```

```console
$ mytool deploy --help
```

```text
 Usage: deploy [OPTIONS] TARGET

 Deploy a service.

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --dry-run  Preview only.                                                     │
│ --help     Show this message and exit.                                       │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Examples ───────────────────────────────────────────────────────────────────╮
│ - Deploy to production:                                                      │
│     mytool deploy prod                                                       │
│                                                                              │
│ - Preview a staging deploy:                                                  │
│     mytool deploy --dry-run staging                                          │
╰──────────────────────────────────────────────────────────────────────────────╯
```

Each example is laid out [`tldr`](https://github.com/tldr-pages/tldr)-style: the description is the heading, with the command indented beneath. The panel only appears when a command defines examples, so commands without them are unchanged. Commands and groups both accept `examples=`.

## Placeholder highlighting

rich-click colours the parts of each example command using what it already knows about the command's structure — so the bits a user must fill in stand out. Because it knows the invocation path and every flag (and which flags take a value), it can tell that:

- the **command path** (`mytool deploy`) is the invocation,
- `--dry-run` is a known **flag**,
- and `prod` (a bare positional) or the value after a value-taking flag is a **placeholder**.

No special syntax is needed — you write the command exactly as you'd type it, and placeholders are detected and highlighted automatically.

## Specifying examples

Every example is a `(description, command)` tuple — **description first, command second**. The description is required: an example is only useful with a short explanation of what it does, so rich-click does not accept a bare command string.

```python
examples=[
    ("Deploy to production", "mytool deploy prod"),
    ("Preview a staging deploy", "mytool deploy --dry-run staging"),
]
```

## Writing good examples

A few conventions keep examples useful — both to people skimming `--help` and to LLM agents reading it as a reference. These are suggestions, not rules.

### Descriptions

- Use the **imperative mood** with a concrete action verb — "Deploy to production", "List installed modules", "Remove a cached file" — rather than gerunds ("Deploying…") or "This command…".
- **Capitalise** the first word.
- **Don't add a trailing `.` or `:`** — rich-click appends the separator for you (and trims one off if you do, so you never get `::`).
- Keep each example to a **single idea**. If the description needs an "and", it is probably two examples.
- Descriptions are rendered through the same pipeline as the rest of your help text, honouring the [`text_markup`](text_markup_and_formatting.md) setting — so backticks, Rich markup, or Markdown apply here exactly as they do (or don't) elsewhere in your help.

### Commands

- **Prefer long-form flags** (`--output` over `-o`). They are self-documenting and read better; placeholder detection works with either form.
- Use **generic, fill-in-the-blank placeholder values** — `path/to/file`, `path/to/directory`, `"search_pattern"`, `<commit-sha>` — rather than incidental real values. They are highlighted automatically, so a reader sees at a glance exactly what to replace.
- **Quote** string placeholders that might contain spaces: `"search pattern"`.
- Show a **repeatable argument** with a trailing `...`: `path/to/file1 path/to/file2 ...`.
- Separate an option from its value with a **space** (`--output report.txt`) unless the tool requires `=`.

### Choosing what to include

- **Lead with the most common** invocation, then move to more advanced ones. A small handful is plenty.
- **Skip examples that add little over the options list.** A bare single flag like `mytool --verbose` is already documented there; an example earns its place by showing a real combination, an argument shape, or non-obvious usage.

## Styling

The panel reuses your options-panel styling (border, box, padding) so its frame matches the rest of the help screen. Within it, the description is **dim**, and the command line is coloured by role using dedicated, independently configurable styles:

| Config option                   | Styles                          | Default       |
| ------------------------------- | ------------------------------- | ------------- |
| `style_examples_command`        | the command path / program name | `bold`        |
| `style_examples_flag_long`      | long flags (`--dry-run`)        | `bold cyan`   |
| `style_examples_flag_short`     | short flags (`-f`)              | `bold green`  |
| `style_examples_placeholder`    | detected placeholders           | `blue`        |
| `style_examples_operator`       | shell operators (`\|`, `>`, `&&`) | `bold yellow` |

The panel title defaults to `Examples` and is set with `examples_panel_title`:

```python
import rich_click as click

click.rich_click.EXAMPLES_PANEL_TITLE = "Usage examples"
click.rich_click.STYLE_EXAMPLES_PLACEHOLDER = "bold red"
```

…or per-command via the [`rich_config`](configuration.md) decorator.

## Examples in machine-readable help

Examples are not just for humans. The same data flows into every [machine-readable format](machine_readable_help.md), so tooling and LLM agents see them too:

- `--help markdown` / `--help markdown-full` — an `## Examples` section.
- `--help json` / `--help json-full` — an `examples` array of `{"command", "description"}` objects.
- `--help carapace` — the spec's `examples` map, keyed by the command line.

LLMs in particular tend to produce better invocations when a few worked examples are present, which makes `examples=` a cheap, high-value addition for any agent-facing CLI.
