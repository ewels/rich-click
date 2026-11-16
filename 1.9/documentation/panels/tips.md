---
project: "rich-click"
title: "Panels - Tips"
description: "Practical advice for rich-click panels: where the --help option lands, controlling row order, and the mistakes that are easy to make."
url: "https://ewels.github.io/rich-click/latest/documentation/panels/tips/"
---

# Panels - Tips

There are a few things to keep in mind when using RichPanels.

## Handling `--help` option

The help option is associated with the default options panel.

If you define all the panels, the `--help` option will be left straggling in the default panel.

This is probably a mistake, and there are two ways to fix it:

```python
panelsHandlingHelpMistakeRaw
```

<details open>
<summary>Output - Mistake</summary>

```sh runnable.outputFile="../../images/code_snippets/panels/panels_handling_help_mistake.ansi"
$ python panels_handling_help_mistake.py --help
```

</details>
```python
panelsHandlingHelpFix1Raw
```

<details open>
<summary>Output - Fix (method 1)</summary>

```sh runnable.outputFile="../../images/code_snippets/panels/panels_handling_help_fix_1.ansi"
$ python panels_handling_help_fix_1.py --help
```

</details>
```python
panelsHandlingHelpFix2Raw
```

<details open>
<summary>Output - Fix (method 2)</summary>

```sh runnable.outputFile="../../images/code_snippets/panels/panels_handling_help_fix_2.ansi"
$ python panels_handling_help_fix_2.py --help
```

</details>
## Sort order of panels

Panels are printed in the order that they are defined, from top to bottom.

```python
@click.option_panel("first")
@click.command_panel("second")
@click.option_panel("third")
```

If panels are inferred from `@click.option(panel=...)`, rather than defined by `@click.option_panel()`, then they are defined in the order that they appear in parameters from top to bottom.

**The simplest way to control the order panels is to define them explicitly!**

This also means that you can order options panels to come before command panels, and vice-versa, based on the decorator order.

## Ordering of rows within panels

The easiest way to control the order of elements within a panel is to explicitly define the order within the panel itself.

If you are having trouble with ordering things, set the order within `options=` or `commands=`.

Additionally, it is suggested you set _every_ object you intend on including in the panel.

```python
panelsRowOrderRaw
```

<details open>
<summary>Output</summary>

```sh runnable.outputFile="../../images/code_snippets/panels/panels_row_order.ansi"
$ python panels_row_order.py --help
```

</details>

That said, the default behavior is also predictable and follows what base Click does for ordering:

- Arguments + options are presented in the order they occur in the decorators, from top to bottom.
- Subcommands are alphanumerically sorted.