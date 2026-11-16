---
project: "rich-click"
title: "Quickstart"
description: "A cheat sheet for getting started with rich-click: install it, swap one import, then pick a theme and group options into panels."
url: "https://ewels.github.io/rich-click/latest/documentation/quickstart/"
---

# Quickstart

## Install

:::code-tabs{sync="pm"}
```sh label="pip"
pip install rich-click
```
```sh label="uv"
uv add rich-click
```
```sh label="Poetry"
poetry add rich-click
```
```sh label="conda"
conda install -c conda-forge rich-click
```
:::

## Swap the import

Replace `import click{:py}` with:

```python
import rich_click as click
```

That's it. Everything else is the same Click API you already use.

If Click is new to you, read the [Introduction to Click](../../documentation/introduction_to_click/) first.

## Cheat sheet

```python
// cli.py
cliRaw
```

```sh runnable.outputFile="../images/code_snippets/quickstart/cli_help.ansi"
$ python cli.py --help
```

## Other ways in

| To...                                             | Use                                                                                                      |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Keep plain `click` and opt in per command         | `@click.command(cls=RichCommand){:py}` or `@click.group(cls=RichGroup){:py}`, imported from `rich_click` |
| Format any Click CLI without changing its code    | `rich-click awesometool --help{:bash}` ([rich-click CLI tool](../../documentation/rich_click_cli/))      |
| Let users choose a theme for every rich-click CLI | `export RICH_CLICK_THEME=dracula-modern{:bash}` ([Themes](../../documentation/themes/))                  |