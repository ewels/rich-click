---
title: "Testing"
description: >-
  Testing CLIs that use Rich prompts and output with rich-click's CliRunner, a drop-in replacement for Click's.
---

Click's [`CliRunner`](https://click.palletsprojects.com/en/stable/testing/) runs a command in isolation. It feeds
`input` to Click's own prompts and captures what the command prints. It does not know about Rich, so tests of
commands that use Rich prompts can go wrong:

- Password prompts (`Prompt.ask(..., password=True)`) call `getpass`. This reads from the terminal, not from
  the `input` that you give to the runner.
- Rich's global console (used by `rich.print()`) keeps the colour setting it had when it was first created. If it
  was created in a real terminal, ANSI codes get into `result.output`.

`rich_click.testing.CliRunner` is a drop-in replacement that fixes this. Change the import and nothing else:

```python ins={4}
import click
from rich.prompt import Confirm, Prompt

from rich_click.testing import CliRunner


@click.command()
def login() -> None:
    user = Prompt.ask("Username")
    Prompt.ask("Password", password=True)
    if Confirm.ask("Remember me?"):
        click.echo(f"Saved login for {user}")


def test_login() -> None:
    result = CliRunner().invoke(login, input="jane\nhunter2\ny\n")
    assert result.output == "Username: jane\nPassword: \nRemember me? [y/n]: y\nSaved login for jane\n"
```

Prompts on every Rich `Console` read from `input`, and typed text is echoed as with `click.prompt()`, except for
passwords. Use `invoke(..., color=True)` to keep colour codes from Rich's global console. A separate `Console()`
that your app creates keeps the colour setting it detected when it was created. Everything is put back after each
invocation.
