# Machine-readable help

CLIs are increasingly driven not just by humans, but by tooling and LLM agents.
Those consumers struggle with the rendered `--help` screen: it is laid out for human reading, wraps to the terminal width, and carries Rich styling that obscures the underlying structure.

**rich-click** already holds all of this information as structured data, and exposes it as **format values on the existing `--help` flag**:

| Invocation                       | Output                                                                                                               |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `--help`                         | The normal human-readable help — byte-for-byte identical to before, unless [an AI agent is detected](#automatic-agent-detection), where it renders `--help compact` under a [character budget](#adaptive-disclosure). |
| `--help compact`                 | The whole command tree in the leanest complete form: one line per option, one line per subcommand, no tables. What an agent gets from a bare `--help`. |
| `--help markdown` (alias `md`)   | LLM-friendly Markdown: the current command in full, plus as much of the rest of the tree as fits a character budget ([_adaptive disclosure_](#adaptive-disclosure)). |
| `--help markdown-full` (`md-full`) | LLM-friendly Markdown documenting every command in the tree.                                                        |
| `--help json`                    | Machine-readable JSON for the current command, plus a name-only index of its subcommands (_progressive disclosure_). |
| `--help json-full`               | The whole command tree in one call, with full parameter detail at every node.                                        |
| `--help carapace`                | Output conforming to the [carapace](https://carapace.sh) completion spec.                                            |

This capability is **always available** on every rich-click CLI — there is nothing to enable. For a human at a terminal, bare `--help` is untouched: the format machinery only engages when a value is given, or when [an AI agent is detected](#automatic-agent-detection).

!!! note "Pass the format after a space"
    The documented form is a space — `mytool --help json` — though the attached form `mytool --help=json` works too. A bare `--help`, or an unrecognized value (a typo, or `mytool --help install` mistakenly meaning "help for the `install` command"), simply shows the normal human-readable help rather than erroring — exactly as a plain `--help` always ignored anything that followed it. To get a subcommand's help, put `--help` after it: `mytool install --help`.

The example CLI used throughout this page:

```python
{% include "../code_snippets/help_json/help_json.py" %}
```

See the [Configuration](configuration.md) page for how to set config options globally or per-command with the `rich_config` decorator.

## Automatic agent detection

The machine-readable formats are always available, but an LLM driving your CLI has no way of knowing that — `--help markdown` is not something it would think to try, and a hint in the help output only works if the agent notices it and makes a second call.

So rich-click does it for them: when it detects that it is running inside an **AI coding agent**, a bare `--help` renders [`--help compact`](#-help-compact-the-agent-default) instead of the rendered help screen. No configuration, no discovery step, and nothing changes for human users.

Detection is based on the environment variables that coding agents set — `CLAUDECODE`, `CURSOR_AGENT`, `CODEX_SANDBOX`, `GEMINI_CLI` and [many more](https://github.com/vercel/detect-agent), plus the emerging `AI_AGENT` and `AGENT` conventions — and a handful of terminal, `PATH` and filesystem signals.

### What a bare `--help` renders

| `RICH_CLICK_AGENT_MODE` | Suppression variable | Agent detected | Output               |
| ----------------------- | -------------------- | -------------- | -------------------- |
| unset                   | no                   | no             | Human-readable help  |
| unset                   | yes                  | no             | Human-readable help  |
| unset                   | no                   | **yes**        | **`--help compact`** |
| unset                   | yes                  | yes            | Human-readable help  |
| `true`                  | any                  | any            | **`--help compact`** |
| `false`                 | any                  | any            | Human-readable help  |

Only a **bare** `--help` is redirected. An explicit `--help json`, `--help markdown-full` and so on is always honoured exactly as given, in every environment. Error and usage output is never affected.

### Choosing the format, or opting out

The format is the `agent_help_format` config option (`AGENT_HELP_FORMAT` global), which defaults to `"compact"`. Any registered format name works, including [your own](#adding-a-new-format):

```python
import rich_click as click

click.rich_click.AGENT_HELP_FORMAT = "markdown"  # Or "json", "markdown-full", "carapace", ...
click.rich_click.AGENT_HELP_FORMAT = None  # Opt out: bare `--help` is always human-readable.
```

Per-command, via the `rich_config` decorator:

```python
from rich_click import RichHelpConfiguration, rich_config

@click.command()
@rich_config(help_config=RichHelpConfiguration(agent_help_format="json"))
def cli():
    ...
```

### Overriding detection from the shell

Set `RICH_CLICK_AGENT_MODE=true` to force agent mode on, or `RICH_CLICK_AGENT_MODE=false` to force it off. It takes precedence over every other signal, so it is the escape hatch when a guess is wrong in either direction.

### Suppression: tests and screenshots

Detection looks at the whole environment, so a test suite or a docs screenshot run **from** an agent shell would otherwise inherit that shell's markers and capture Markdown where a human-readable help screen is expected. rich-click suppresses detection when any of these variables is present:

| Variable                                | Set by                                                        |
| --------------------------------------- | ------------------------------------------------------------- |
| `PYTEST_CURRENT_TEST`                   | pytest, for each test (all modern versions)                   |
| `PYTEST_VERSION`                        | pytest >= 8.2, for the whole process                          |
| `RICH_CODEX`                            | [rich-codex](https://ewels.github.io/rich-codex/) >= 1.3.1, always, when generating output |

Both cases therefore need no action at all: `--help` snapshots in your pytest suite and screenshots generated by rich-codex (1.3.1 or newer) keep rendering the human-readable help, even when you run them from inside an agent.

Other doc-generation or snapshot tooling can either export `RICH_CLICK_AGENT_MODE=false` for its runs, or — if it always sets an identifying variable of its own — [open an issue](https://github.com/ewels/rich-click/issues) to have it added to the list above.

An explicitly falsy value (e.g. `RICH_CODEX=0`) does not suppress. pytest's own variables carry values that are neither truthy nor falsy (a test ID, a version number), so mere presence is what counts.

## `--help compact`: the agent default

`--help compact` renders the same information as everything else on this page, in the leanest shape that keeps the **whole tree** intact: one line per option, one line per subcommand, no tables and no Markdown scaffolding. It is what a bare `--help` renders when [an AI agent is detected](#automatic-agent-detection).

```console
$ mytool --help compact
```

```
# mytool — A demo CLI.
--verbose, -v  Enable verbose output.

# db — Manage the database.

# db migrate — Run migrations.

# hello — Greet someone.
usage: mytool hello NAME
--count INTEGER  Number of greetings. [default: 1]
```

A block with more to say looks like this:

```
# plarv crell (cl) — Create a record.
*--crull TEXT  Annotation text for the record.
--kolm pelm|crox|zeff  Mode of the record. [default: pelm]
--wover INT  Weight of the record. [default: 7]
--torv TEXT ...  Label to attach; repeat for several.
--murd TEXT  Steward name. [default: veld] [env: QUORV_MURD]
examples:
- quorv plarv crell --crull 'north ledger'
- quorv plarv crell --crull 'north ledger' --kolm crox --wover 12
```

That is 497 characters. The same command as Markdown is 2,025 — and a 132-command CLI is ~80,000 characters of Markdown against ~28,000 compact, which is the difference between a help page an agent reads in one call and one its harness cuts in half.

### Why it is shaped this way

**Characters are the currency.** Agent harnesses truncate a tool's output at a character count (Claude Code at ~30,000). Markdown help is table-heavy, and tables are the most expensive way to say anything: pipes, dashes and padding on every row. What gets truncated does not merely cost tokens — it costs *turns*, because the agent goes back in with `grep` and `tail` to read the half it did not get.

**Conventions, not sigils.** Everything in a block is notation a model has already read a thousand times in rendered help screens, so nothing has to be explained before the page can be used:

| Element | Means |
| ------- | ----- |
| `# <path> (<aliases>) — <summary>` | The start of a command's block. The `#` is the anchor a model greps for and navigates by; the program name is dropped from the path, since it is constant and already in the usage line and examples. |
| `*--crull TEXT` | A **required** option — the same `*` the rendered `--help` screen marks required options with. There is no `[required]` tag; the star replaces it. |
| `--kolm pelm\|crox\|zeff` | A `Choice`, spelled out where the metavar would go. The choice values *are* the vocabulary needed to construct a valid invocation. |
| `--torv TEXT ...` | A **repeatable** option (`multiple=True`). |
| `[default: x]`, `[env: NAME]` | Click's own phrasing, appended to the description verbatim. |
| `usage: <prog> <path> SRC [DEST]` | Only for commands with **positional arguments** — their order is information no other line carries. Option-only commands get no usage line, and `[OPTIONS]` is never printed: the options are listed directly underneath. |
| `examples:` then `- <command line>` | Worked invocations, without their descriptions — next to the option list, a command line describes itself. |
| `<name>  <summary>` | A subcommand that is listed rather than documented (see [adaptive disclosure](#adaptive-disclosure)). |

**Two spaces separate a signature from its description**, on every line. Not one — a single space is ambiguous with the spaces inside a signature. Not aligned columns — padding makes the boundary depend on the widest row in the block, and costs characters on every line to convey nothing. There is no trailing whitespace anywhere in the output.

The `--help` row is omitted throughout. It is the one row identical on every command of every CLI, which makes it the single largest block of repetition in a whole-tree rendering; the other formats still report it.

### Whole tree, or budgeted

Asked for **by name**, `--help compact` renders the invoked command's block followed by every descendant's, depth-first in definition order, with no ceiling — the compact analogue of `--help markdown-full`. A caller who names the format is asking for everything.

Reached as the **agent default** (a bare `--help` with an agent detected), the same renderer runs under [adaptive disclosure](#adaptive-disclosure) instead, so a very large tree degrades gracefully rather than being truncated by the harness. The tiers are the compact ones: a full block, an anchor line plus bare option signatures, or a single listing line.

Metavars come from Click itself, so an explicit `metavar=`, a `Path(file_okay=False)`'s `DIRECTORY`, and any custom `ParamType`'s own rendering all appear exactly as they do in the rendered help.

!!! tip "Prefer Markdown? One line of config"
    `click.rich_click.AGENT_HELP_FORMAT = "markdown"` restores Markdown as what an agent's bare `--help` renders; every format remains available by name in either case. Task success measured flat across formats in benchmarking — what changed was cost, which is why the leanest complete format is the default.

## `--help markdown`: Markdown for LLMs

`--help markdown` (alias `--help md`) renders the CLI's structure as Markdown, tuned for dropping into an LLM prompt: headings for hierarchy, each command titled by its **full invocation path** so the section is unambiguous out of context, and parameters laid out as compact tables. How much of the command tree comes back is [decided by a character budget](#adaptive-disclosure).

```console
$ mytool hello --help markdown
```

```markdown
# `cli hello`

Greet someone.

**Usage:** `cli hello [OPTIONS] NAME`

## Arguments

| Argument | Type | Required |
| --- | --- | --- |
| `name` | String | yes |

## Options

| Option | Type | Default | Description |
| --- | --- | --- | --- |
| `--count` | Int | `1` | Number of greetings. |
```

A column that is empty for **every** row of a table — here Required and Default in the options table, Default and Description in the arguments table — is dropped rather than padded out with empty cells. For a consumer reading the help that costs no information, and an all-empty column is pure token padding.

`--help markdown-full` (alias `--help md-full`) documents **every** command in the tree, each as its own top-level (`#`) section — a flat, uniform layout that is easy for a model to parse and navigate by path.

### Adaptive disclosure

`--help markdown`, and a bare `--help` in an agent environment, do not stop at the invoked command. They render that command in full, and then disclose as much of the rest of the tree as fits a **character ceiling**, promoting commands **nearest the invoked one first**.

Why not just document the invoked command and list its subcommands by name? Because a name and a one-line summary are usually not enough to choose between subcommands: the vocabulary that decides which one is right — the flag that does the thing you need — lives in the option help text. An agent given only names has to guess, descend, read, and backtrack, spending turns on navigation. Given the whole tree up front it does not have to guess at all.

So each command in the tree is rendered at one of three levels of detail:

| Level | Contents |
| ----- | -------- |
| **Full** | Description, usage, examples and every parameter — what the invoked command always gets. |
| **Signature** | Anchor/usage line, one-line description, and the options as bare signatures (`--mode fast\|safe`, `--count INTEGER`) — names, metavars and choice values, with no descriptions. |
| **Pointer** | A single line in the nearest documented ancestor's subcommand listing: name, aliases and a one-line description. |

The invoked command is always Full. Every other command starts as a Pointer and is promoted breadth-first — nearest hop first, in command order within a hop — first to Signature and then to Full, for as long as the whole response stays under the ceiling. Promotion stops at the first step that does not fit, so what gets disclosed is always a contiguous nearest-first slice of the tree, and the same command always renders exactly the same help.

**In practice, most CLIs never hit the ceiling at all**: the default is set well above what a small or mid-size CLI needs, so the entire tree comes back in full detail from a single `--help` — the shape that works best for an agent. Only a genuinely large CLI degrades, and it degrades gracefully rather than falling back to bare names. When anything was abbreviated, the output ends with a note saying so and pointing at the individual commands.

One thing the ceiling never buys: the invoked command's own detail, and a line naming **every** command in the tree, are always emitted. A ceiling below that floor is overshot rather than hiding a command's existence — an agent that cannot see a command cannot run it.

### Tuning the ceiling

The ceiling is the `agent_help_max_chars` config option (`AGENT_HELP_MAX_CHARS` global), in characters:

```python
import rich_click as click

click.rich_click.AGENT_HELP_MAX_CHARS = 50_000  # Disclose more of a large tree.
click.rich_click.AGENT_HELP_MAX_CHARS = None  # Off: current command + a name index, nothing more.
```

**Characters, not tokens**, and the default of 25,000 is not arbitrary. The failure the ceiling exists to prevent is an agent harness truncating the output mid-document — and every harness cap is measured in characters, not tokens (Claude Code cuts a tool result at ~30,000). A help page that gets cut is worse than a short one: the agent goes back in with `grep` and `tail`, spending turns to read what one call should have delivered. 25,000 leaves headroom under that cap.

Characters also need no estimator. `len(text)` is exact, so the rendered document is guaranteed to fit the number you configured; a token ceiling needed a calibrated characters-per-token divisor per format, which is an approximation of the wrong quantity. And a character budget bounds the token cost anyway: help text does not go below ~2.5 characters per token, so 25,000 characters is at most ~10,000 tokens.

An explicit `--help compact`, `--help markdown-full`, `--help json`, `--help json-full` and `--help carapace` are all unaffected by this setting — each is a whole-tree format by definition, and naming one is a request for everything it has.

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
      "type": "String",
      "help": "Show this message and exit.",
      "choices": ["markdown", "markdown-full", "json", "json-full", "carapace", "compact"]
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
  --help?: Show this message and exit.
completion:
  flag:
    help: [markdown, markdown-full, json, json-full, carapace, compact]
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

Carapace is a structure-and-completion spec rather than a type/validation one, so the mapping is intentionally lossy. Flag keys use carapace's string syntax (`-s, --long` for a flag that takes no value — booleans and counters alike, a trailing `=` when the flag requires a value, `?` when the value is optional as it is for `--help`, `*` when it is repeatable, and the `{description, nargs}` object form for multi-value flags); negation flags such as `--no-debug` become their own entries; and `Choice` values are surfaced as completion candidates. Parameter **types** (`Int`/`Path`/…), **defaults**, **envvars** and per-flag **required** have no home in the carapace schema and are dropped — reach for `--help json-full` if you need those.

## Error diagnosis

Getting help right only solves half the problem. The other half is what happens when a caller gets the invocation *wrong*.

Click's usage errors report the symptom: `No such option: --repo`. A human reads that, remembers that `--repo` belongs to the parent group, and moves the flag. An agent frequently cannot — the message says nothing about **why** the option was rejected, so there is nothing to correct against, and it retries variations of the same broken command until it runs out of turns. An error that states the rule it broke is usually fixed on the very next attempt.

So rich-click diagnoses usage errors where it can, and says what it worked out. It derives, when derivable:

- **The violated rule**, stated as a rule — including the parent-group case: `'--repo' is an option of the parent group 'tool', not of 'tool build'. A group's options must be given before its subcommand.`
- **Near matches** by edit distance over the command's *real* option names, or over its subcommand names for an unknown command.
- **The valid values** of a `Choice`, and the requirement behind a missing parameter.
- **A corrected invocation**, copyable as-is, whenever one can be constructed confidently.

### Two renderings

For a human, the diagnosis is a terse addition inside the existing error panel — the rule, the nearest alternatives, the corrected command:

```console
$ tool build --repo ewels/rich-click thing
```

```
 Usage: tool build [OPTIONS] NAME

 Try 'tool build --help' for help
╭─ Error ────────────────────────────────────────────────────────────────────╮
│ No such option '--repo'.                                                   │
│                                                                            │
│ '--repo' is an option of the parent group 'tool', not of 'tool build'. A   │
│ group's options must be given before its subcommand.                       │
│ Try: tool --repo TEXT build ...                                           │
│ See 'tool --help' for help                                                 │
╰────────────────────────────────────────────────────────────────────────────╯
```

Inside a [detected agent environment](#automatic-agent-detection), the same diagnosis is rendered as a plain-text block instead — no panel, no ANSI, one fact per line, and the attempted invocation restated (an agent has no scrollback to look at):

```
Error: No such option '--repo'.

Attempted: tool build --repo ewels/rich-click thing
Rule: '--repo' is an option of the parent group 'tool', not of 'tool build'. A group's options must be given before its subcommand.
Try: tool --repo TEXT build ...
Usage: tool build [OPTIONS] NAME
Help: tool --help
```

This is **strictly additive**. Exit codes are unchanged, and Click's own error message is still the first line, so anything matching on it keeps working. An error rich-click cannot say anything useful about — a `ctx.fail()` from your own callback, which already states its rule — is left exactly as it was, rather than padded out with guesses.

### Turning it off

Set the `error_diagnosis` config option (`ERROR_DIAGNOSIS` global) to `False`, or the `RICH_CLICK_ERROR_DIAGNOSIS` environment variable to a falsy value — which overrides the config option in both directions, so the behaviour can be A/B'd across runs without touching your CLI's source:

```shell
RICH_CLICK_ERROR_DIAGNOSIS=0 mytool build --repo x thing
```

With diagnosis off, errors render exactly as Click and rich-click rendered them before, in every environment.

## Command examples

LLMs respond well to concrete examples. If you give commands examples with the [`examples=` argument](examples.md) — primarily to enrich the rendered `--help` — they flow into the machine-readable formats too:

- `--help markdown` / `--help markdown-full` — an `## Examples` section, placed immediately after the usage line and **before** the parameter tables.
- `--help compact` — an `examples:` label followed by the command lines alone, after the option list.
- `--help json` / `--help json-full` — an `examples` array of `{"command", "description"}` objects.
- `--help carapace` — the spec's `examples` map, keyed by the command line.

!!! note
    The carapace `examples` field is a map keyed by the command line, as the spec requires. If two
    examples share the same command (differing only in their descriptions), they collapse to a single
    entry and the last description wins. The `--help json` formats keep every example as a list, so use
    those if you need to preserve duplicates.

The placement in the Markdown formats is deliberate. An example is a complete, copyable invocation — the highest-value thing a model can read about a command — and models demonstrably copy the ones they are shown, so it goes first, before the reference material. Examples survive [adaptive disclosure](#adaptive-disclosure) there too: a command abbreviated to its signature keeps its examples in full. A compact block puts them last instead — it is short enough to read whole, so they land as the summary of the option lines rather than ahead of them — and drops the descriptions, since a command line sitting under its own option list describes itself.

The rendered human `--help` is laid out the other way round, with the Examples panel *after* the options: someone scanning a terminal wants the reference material first and the worked examples at the end.

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

There are two ways to register a new `--help <format>`, depending on whether you want it on a command subclass or process-wide.

**On a subclass** — extend the `RichCommand.help_formats` registry (format name → method that renders it) and add the method. No need to touch the dispatch:

```python
import rich_click as click


class MyCommand(click.RichCommand):
    help_formats = {**click.RichCommand.help_formats, "yaml": "get_help_yaml"}

    def get_help_yaml(self, ctx):
        import yaml

        return yaml.safe_dump(self.format_help_json(ctx, ctx.make_formatter()))
```

**Without subclassing** — register a renderer on the `help_formats` **config** option (the counterpart to the class registry, mapping a format name to a `(command, ctx) -> str` callable). Set it like any other config option — e.g. process-wide via the globals module — and every rich-click CLI in the process gains the format:

```python
import rich_click as click
import yaml


def render_yaml(command, ctx):
    return yaml.safe_dump(command.format_help_json(ctx, ctx.make_formatter()))


click.rich_click.HELP_FORMATS = {"yaml": render_yaml}
# `mytool --help yaml` now works, with no subclass.
```

Either way the new name is dispatched by `--help`, listed in its metavar, and surfaced in the `--help` option's `choices`.
