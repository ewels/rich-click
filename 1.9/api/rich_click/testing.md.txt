---
project: "rich-click"
title: "rich_click.testing"
description: "Test helpers for CLIs that use Rich for output and prompts."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/testing/"
---

# rich_click.testing

*module*

Test helpers for CLIs that use Rich for output and prompts.

[View source](https://github.com/ewels/rich-click/blob/31048949e2a464cb225175dc0aa84afa990bacb6/src/rich_click/testing.py#L1-L1)

## rich_click.testing.CliRunner

*class*

```python
class CliRunner(click.testing.CliRunner)
```

Bases: `click.testing.CliRunner`

A drop-in replacement for `click.testing.CliRunner` that also isolates Rich.

While a command runs:

- Rich prompts (`rich.prompt.Prompt`, `rich.prompt.Confirm`, and `Console.input()`)
  read from the runner's `input`, including password prompts, which would otherwise call
  `getpass.getpass` and read from the terminal.
- Rich's global console (used by `rich.print()` and prompts without an explicit console) is
  reset in place to follow the runner's `color` setting, and is not interactive.
- Environment variables that change Rich output (`FORCE_COLOR`, `NO_COLOR`, `COLUMNS`, ...)
  are unset or pinned, unless given in `env`.

[View source](https://github.com/ewels/rich-click/blob/31048949e2a464cb225175dc0aa84afa990bacb6/src/rich_click/testing.py#L33-L113)

### rich_click.testing.CliRunner.isolation

*method*

```python
def isolation(input: str | bytes | IO[Any] | None = None, env: Mapping[str, str | None] | None = None, color: bool = False) -> Iterator[Any]
```

[View source](https://github.com/ewels/rich-click/blob/31048949e2a464cb225175dc0aa84afa990bacb6/src/rich_click/testing.py#L48-L113)
