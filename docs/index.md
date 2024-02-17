---
hide:
  - title
---

<style>
  .md-typeset h1,
  .md-content__button {
    display: none;
  }
</style>

<p align="center">
<img src="images/rich-click-logo.png#only-light" align="center">
<img src="images/rich-click-logo-darkmode.png#only-dark" align="center">
</p>
<p align="center">
    <em>Richly rendered command line interfaces in click.</em>
</p>
<p align="center">
    <img src="https://github.com/ewels/rich-click/workflows/Test%20Coverage/badge.svg" alt="Test Coverage badge">
    <img src="https://github.com/ewels/rich-click/workflows/Lint%20code/badge.svg" alt="Lint code badge">
</p>

---

**rich-click** is a shim around [click](https://click.palletsprojects.com/) that renders help output nicely using [Rich](https://github.com/Textualize/rich).

- Click is a _"Python package for creating beautiful command line interfaces"_.
- Rich is a _"Python library for rich text and beautiful formatting in the terminal"_.

The intention of `rich-click` is to provide attractive help output from
click, formatted with rich, with minimal customisation required.

## Installation

```console
pip install rich-click
```

## Examples

### Simple example

To use rich-click in your code, replace `import click` with `import rich_click as click` in your existing click CLI:

```python
import rich_click as click

@click.command()
@click.option("--count", default=1, help="Number of greetings.")
@click.option("--name", prompt="Your name", help="The person to greet.")
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == '__main__':
    hello()
```

<div class="termy">

```console
$ python examples/11_hello.py --help

 <span style="color: #808000; text-decoration-color: #808000">Usage:</span> <span style="font-weight: bold">examples</span> [<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">OPTIONS</span>]

 Simple program that greets <span style="color: #008080; text-decoration-color: #008080; background-color: #000000; font-weight: bold">NAME</span> for a total of <span style="color: #008080; text-decoration-color: #008080; background-color: #000000; font-weight: bold">COUNT</span> times.

<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Options ────────────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--count</span>    <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">INTEGER</span>  Number of greetings.                             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--name</span>     <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">TEXT   </span>  The person to greet.                             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--help</span>     <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">       </span>  Show this message and exit.                      <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>

```

</div>

"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
Section 1.10.32 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC

"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"
