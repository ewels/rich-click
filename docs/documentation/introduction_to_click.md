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
# hello.py
import click

@click.command()
def hello():
    """Prints 'hello, world!' into the terminal."""
    print("Hello, world!")

if __name__ == "__main__":
    hello()
```

You can run the file like normal, or you can run `--help` to render the function's docstring:

<div class="termy">
```console
$ python hello.py

Hello, world!

$ python hello.py --help

Usage: hello.py [OPTIONS]

  Prints 'hello, world!' into the terminal.

Options:
  --help  Show this message and exit.
```
</div>

### Arguments and Options

Arguments and options are also added with decorators. The difference between arguments and options is:

- Arguments are required, and options are not (unless you specify `required=True`).
- Arguments are positional, and options must be prefixed with one or two dashes.

The below code shows some of the features available with options and arguments:

```python
# hello.py
import click

@click.command()
@click.argument("name")
@click.option("--times", "-t",
              default=1,
              type=click.INT,
              show_default=True,
              help="Number of times to print the greeting.")
@click.option("--say-goodbye",
              is_flag=True,
              default=False,
              help="After saying hello, say goodbye.")
def hello(name, times, say_goodbye):
    """Prints 'hello, [name]!' into the terminal N times."""
    for t in range(times):
        print(f"Hello, {name}!")
    if say_goodbye:
        print("Goodbye!")

if __name__ == "__main__":
    hello()
```

<div class="termy">
```console
$ python hello.py --say-goodbye --times 3 Edward

Hello, Edward!
Hello, Edward!
Hello, Edward!
Goodbye!

$ python hello.py --help

Usage: hello.py [OPTIONS] NAME

  Prints 'hello, [name]!' into the terminal N times.

Options:
  -t, --times INTEGER  Number of times to print the greeting.
                       [default: 1]
  --say-goodbye        After saying hello, say goodbye.
  --help               Show this message and exit.
```
</div>

Click is able to parse the new arguments and options, e.g. it knows that `--times [number]` maps to the function argument `times`.
Additionally, Click also knows to render these new arguments in the help text.

### Groups

Last but not least, Click allows for command groups and sub-commands, which allows you to nest commands inside other commands.

```python
# hello.py
import click

@click.group("greetings")
def greetings_cli():
    """CLI for greetings."""

@greetings_cli.command("english")
@click.argument("name")
def english(name):
    """Greet in English"""
    print(f"Hello, {name}!")

@greetings_cli.command("french")
@click.argument("name")
def french(name):
    """Greet in French"""
    print(f"Bonjour, {name}!")

if __name__ == "__main__":
    greetings_cli()
```

Running `python hello.py --help` gives you the help text for the group and lists the subcommands:

<div class="termy">
```console
$  python hello.py --help
Usage: hello.py [OPTIONS] COMMAND [ARGS]...

  CLI for greetings.

Options:
  --help  Show this message and exit.

Commands:
  english  Greet in English.
  french   Greet in French.
```
</div>

And you can run any of the subcommands like so:

<div class="termy">
```console
$ python hello.py french Jennifer

Bonjour, Jennifer!

$ python hello.py french --help

Usage: hello.py french [OPTIONS] NAME

  Greet in French.

Options:
  --help  Show this message and exit.
```
</div>

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

<div class="termy">
```console
$ python hello.py --help

<span style="color: #808000; text-decoration-color: #808000">Usage:</span> <span style="font-weight: bold">my_file</span> [<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">OPTIONS</span>] <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">NAME</span>

 Prints &#x27;hello, [name]!&#x27; into the terminal N times.

<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Options ────────────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--times</span>        <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">-t</span>  <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">INTEGER</span>  Number of times to print the greeting.   <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">[default: 1]                          </span>   <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--say-goodbye</span>      <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">       </span>  After saying hello, say goodbye.         <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--help</span>             <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">       </span>  Show this message and exit.              <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
```
</div>

## Other CLI libraries

Click has been around for over a decade and is the most popular third-party CLI tool in Python.
It's popularity is for a good reason: you can do basically _anything_ in Click.
Click is very well abstracted, and as a result, you will likely never feel like you are brushing up against the limitations of what Click is capable of.

There are other CLI libraries available.
Of particular note is [Typer](https://typer.tiangolo.com/), which is itself built on top of Click.
Typer is also [able to format help messages with Rich](https://typer.tiangolo.com/tutorial/commands/help/#rich-markdown-and-markup),
functionality that was adapted from **rich-click** - as a result, the output looks remarkably similar!
However, the two libraries have since drifted apart, so note that not all **rich-click** functionality is available within Typer.

!!! tip "Why Click?"
    If you're interested in why people choose to use Click, check out the
    [Why Click? docs](https://click.palletsprojects.com/en/8.1.x/why).
    These are good, but be aware that they were written a really long time ago.
    The landscape has changed quite a bit since that page was first written.
