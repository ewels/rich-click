# Introduction to Click

!!! note
    If you know what Click is, you can skip this page.

**rich-click** is a drop-in replacement for [Click](https://click.palletsprojects.com/en/8.1.x/), a Python CLI framework.
This means that if you know Click, you already know **rich-click**.
The docs to Click are the appropriate place to 

## Click 101

### Commands

Click utilizes function decorators as its primary interface for composing a CLI.

For example, the `@click.command` decorator creates a `Command` object that calls the function:

```python
# docs/code_snippets/introduction_to_click/hello.py
{!code_snippets/introduction_to_click/hello.py!}
```

You can run the file like normal, or you can run `--help` to render the function's docstring:

<!-- RICH-CODEX
working_dir: docs/code_snippets/introduction_to_click
-->
![`python hello.py`](../images/introduction_to_click/hello.svg)

<!-- RICH-CODEX
working_dir: docs/code_snippets/introduction_to_click
-->
![`python hello.py --help`](../images/introduction_to_click/hello_help.svg)

### Arguments and Options

Arguments and options are also added with decorators. The difference between arguments and options is:

- Arguments are required, and options are not (unless you specify `required=True`).
- Arguments are positional, and options must be prefixed with one or two dashes.

The below code shows some of the features available with options and arguments:

```python
# docs/code_snippets/introduction_to_click/hello_v2.py
{!code_snippets/introduction_to_click/hello_v2.py!}
```

<!-- RICH-CODEX
working_dir: docs/code_snippets/introduction_to_click
-->
![`python hello_v2.py --say-goodbye --times 3 Edward`](../images/introduction_to_click/hello_v2.svg)

<!-- RICH-CODEX
working_dir: docs/code_snippets/introduction_to_click
-->
![`python hello_v2.py --help`](../images/introduction_to_click/hello_v2_help.svg)

Click is able to parse the new arguments and options, e.g. it knows that `--times [number]` maps to the function argument `times`.
Additionally, Click also knows to render these new arguments in the help text.

### Groups

Last but not least, Click allows for command groups and sub-commands, which allows you to nest commands inside other commands.

```python
# docs/code_snippets/introduction_to_click/hello_v3.py
{!code_snippets/introduction_to_click/hello_v3.py!}
```

Running `python hello.py --help` gives you the help text for the group and lists the subcommands:

<!-- RICH-CODEX
working_dir: docs/code_snippets/introduction_to_click
-->
![`python hello_v3.py --help`](../images/introduction_to_click/hello_v3_help.svg)

And you can run any of the subcommands like so:

<!-- RICH-CODEX
working_dir: docs/code_snippets/introduction_to_click
-->
![`python hello_v3.py french Jennifer`](../images/introduction_to_click/hello_v3_subcommand.svg)

<!-- RICH-CODEX
working_dir: docs/code_snippets/introduction_to_click
-->
![`python hello_v3.py french --help`](../images/introduction_to_click/hello_v3_subcommand_help.svg)

## Next Steps

!!! info
    **There is a lot more to Click than what is covered here.** Read [the official Click docs](https://click.palletsprojects.com/en/8.1.x/) for more information.

So, what does any of this have to do with **rich-click**?
Simply put: **rich-click** is a drop-in replacement for Click.
Let's take the second CLI example above with the `--times` option and add **rich-click** by replacing this:

```python
import click
```

With this:

```python
import rich_click as click
```

That's the **_only_** change needed to use **rich-click**! And now we get the following beautiful help text:

<!-- RICH-CODEX
working_dir: docs/code_snippets/introduction_to_click
-->
![`python hello_rich.py --help`](../images/introduction_to_click/hello_rich.svg)

## Why Click?

Why **rich-click** is obvious. If you're using Click, you may as well use **rich-click** for the beautiful help text!

Why _Click_ is a different question.
The [Why Click?](https://click.palletsprojects.com/en/8.1.x/why) docs are good, but they were written a really long time ago.
The landscape has changed quite a bit since that page was first written.

These days, there are plenty of "competitors" to Click.
In fact, many of them, such as Typer, borrow Click's internals,
since Click got so much right when it comes to the nitty-gritty of parsing arguments and printing text.

So a better way to phrase the question is perhaps: why Click _today_?
I would offer a few reasons:

- **You can do basically anything in Click.** In Click, everything is just a subclass and a method override away. Click is very well abstracted, and as a result, you will likely never feel like you are brushing up against the limitations of what Click is capable of.

- **Click is extremely popular.** It is the most popular third-party CLI tool in Python, even to this day. Tons of libraries use Click. Knowing Click means you are in good company with a tool you'll encounter plenty in the wild.

- **It just works.** Click has been around for more than a decade, it's battle-tested, and you are _very_ unlikely to ever hit a bug or a snag.
