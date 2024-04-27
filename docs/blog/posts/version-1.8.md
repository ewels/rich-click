---
draft: false
slug: version-1.8
date: 2024-04-30
authors:
  - dwreeves
  - ewels
categories:
  - Release notes
---

# New blog + v1.8 released!

Today we are very happy to release version 1.8 of rich-click,
and along with it - this blog!

<!-- more -->

## New docs website and blog

Until now, **rich-click** has just had a GitHub repo and all documentation has been in the `README`.


## rich-click version 1.8

### Docs + live style editor!

### CLI makeover

The rich-click CLI now has some goodies e.g. `--output svg` and `--output html` to help easily generate outputs for READMEs and docs:

```shell
rich-click --output svg path.to.my.cli:main --help
```

### Improved performance

Rich is now lazy-loaded (it's only loaded when rendering `--help`), which keeps the runtime slimmer and faster.

### Easier decorator API

The `rich_config()` decorator API is now easier to use:
You can pass a `dict` into the `@click.rich_config()` decorator. E.g.:

```python
@click.command
@click.rich_config(help_config={"max_width": 100"})
def my_command():
    ...
```

### Improvements to option and command group API

### More style options

More control over panel styles!

### And more..

Misc. bugfixes and other small internal improvements+refactors, mostly aimed at composability and customizability for advanced use cases. (This does not impact 99% of users.)
