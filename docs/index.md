---
title: rich-click
hide:
  - title
  - navigation
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

<p align="center">
    <a href="https://ewels.github.io/rich-click">Documentation</a>&nbsp&nbsp·&nbsp&nbsp<a href="https://github.com/ewels/rich-click">Source Code</a>
</p>

---

**rich-click** is a shim around [Click](https://click.palletsprojects.com/) that renders help output nicely using [Rich](https://github.com/Textualize/rich).

- Click is a _"Python package for creating beautiful command line interfaces"_.
- Rich is a _"Python library for rich text and beautiful formatting in the terminal"_.

The intention of `rich-click` is to provide attractive help output from
click, formatted with rich, with minimal customisation required.

## Features

- 🌈 Rich command-line formatting of click help and error messages
- 💫 Nice styles be default, usage is simply `import rich_click as click`
- 💻 CLI tool to run on _other people's_ tools (prefix the command with `rich-click`)
- 📦 Export help text as HTML or SVG
- 🎁 Group commands and options into named panels
- ❌ Well formatted error messages
- 🔢 Easily give custom sort order for options and commands
- 🎨 Extensive customisation of styling and behaviour possible

## Installation

=== "pip"
    ```{.shell, .copy}
    pip install rich-click
    ```

=== "uv"
    ```{.shell, .copy}
    uv pip install rich-click
    ```

=== "Rye"
    ```{.shell, .copy}
    rye add rich-click
    rye sync
    ```

=== "Poetry"
    ```{.shell, .copy}
    poetry add rich-click
    ```

=== "Pipenv"
    ```{.shell, .copy}
    pipenv install rich-click
    ```

=== "conda"
    [**rich-click**](https://anaconda.org/conda-forge/rich-click) is available via the conda-forge channel (see [docs](https://conda-forge.org/docs/user/introduction.html#how-can-i-install-packages-from-conda-forge)).
    ```{.shell, .copy}
    conda install rich-click
    ```

=== "MacPorts"
    This installation method is deprecated.
    ```{.shell, .copy}
    sudo port install py-rich-click
    ```

## Examples

### Simple example

To use rich-click in your code, replace `import click` with `import rich_click as click` in your existing click CLI:

```{ .python .copy }
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

<div class="termy termy-static" static="true" style="width: 100%">

```console
$ python examples/hello_11.py --help

 <span style="color: #808000; text-decoration-color: #808000">Usage:</span> <span style="font-weight: bold">hello_11.py</span> [<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">OPTIONS</span>]

 Simple program that greets <span style="color: #008080; text-decoration-color: #008080; background-color: #000000; font-weight: bold">NAME</span> for a total of <span style="color: #008080; text-decoration-color: #008080; background-color: #000000; font-weight: bold">COUNT</span> times.

<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Options ────────────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--count</span>    <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">INTEGER</span>  Number of greetings.                             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--name</span>     <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">TEXT   </span>  The person to greet.                             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--help</span>     <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">       </span>  Show this message and exit.                      <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
```

</div>

### More complex example

**rich-click** has a ton of customization options that let you compose help text however you'd like.
Below is a more complex example of what **rich-click** is capable of:

<div class="termy termy-static" static="true" style="width: 100%">

```console
$ python examples/03_groups_sorting.py --help

 <span style="color: #808000; text-decoration-color: #808000">Usage:</span> <span style="font-weight: bold">03_groups_sorting.py</span> [<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">OPTIONS</span>] <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">COMMAND</span> [<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">ARGS</span>]...
                                                                        
 My amazing tool does all the things.                                   
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">This is a minimal example based on documentation from the &#x27;click&#x27; </span>     
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">package.</span>                                                               
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">You can try using </span><span style="color: #7fbfbf; text-decoration-color: #7fbfbf; font-weight: bold">--help</span><span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> at the top level and also for specific </span>       
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">subcommands.</span>                                                           
                                                                        
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Options ────────────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #800000; text-decoration-color: #800000">*</span>  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--type</span>                     <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">TEXT</span>  Type of file to sync             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                     <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">[default: files]    </span>             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                     <span style="color: #bf7f7f; text-decoration-color: #bf7f7f">[required]          </span>             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>    <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--debug</span>/<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--no-debug</span>  <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">-d</span>/<span style="color: #008000; text-decoration-color: #008000; font-weight: bold">-n</span>  <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">    </span>  Show the debug log messages      <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                     <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">[default: no-debug]        </span>      <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>    <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--version</span>                  <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">    </span>  Show the version and exit.       <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>    <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--help</span>              <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">-h</span>     <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">    </span>  Show this message and exit.      <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Main usage ─────────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">sync       </span> Synchronise all your files between two places.           <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">download   </span> Pretend to download some files from somewhere.           <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Configuration ──────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">config     </span> Set up the configuration.                                <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">auth       </span> Authenticate the app.                                    <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
```

</div>

"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
Section 1.10.32 of "de Finibus Bonorum et Malorum", written by Cicero in 45 BC

"Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"