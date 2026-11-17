---
project: "rich-click"
title: "rich_click.cli"
description: "The command line interface."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/cli/"
---

# rich_click.cli

*module* · *Added in 1.2.0*

The command line interface.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/cli.py#L1-L1)

## rich_click.cli.DISABLE_WARNINGS_NOTE

*attribute* · *Added in 1.9.0* · *module attribute*

```python
DISABLE_WARNINGS_NOTE = '[red]You can pass [b]--suppress-warnings[/b] to the rich-click CLI or set the [b]RICH_CLICK_CLI_SUPPRESS_WARNINGS[/b] environment variable to disable this message.[/red]'
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/cli.py#L32-L36)

## rich_click.cli.list_themes

*function* · *Added in 1.9.0*

```python
def list_themes(ctx: RichContext, param: click.Parameter, value: bool) -> None
```

Print all themes.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/cli.py#L141-L282)

## rich_click.cli.main

*function* · *Added in 1.2.0*

```python
def main(ctx: RichContext, script_and_args: tuple[str, ...], theme: str, output: Literal[None, 'html', 'svg'], errors_in_output_format: bool, suppress_warnings: bool, patch_rich_click: bool, rich_config: dict[str, Any] | None, show_help: bool) -> None
```

The [link=https://github.com/ewels/rich-click]rich-click[/] CLI provides
[#FF6B6B bold]r[/][#FF8E53 bold]i[/][#FFB347 bold]c[/][#4ECDC4 bold]h[/][#45B7D1 bold]l[/][#74B9FF bold]y[/]
formatted help output from any
tool using [link=https://click.palletsprojects.com/]click[/], formatted with
[link=https://github.com/Textualize/rich]rich[/].

Full docs here: [link=https://ewels.github.io/rich-click/latest/documentation/rich_click_cli/]https://ewels.github.io/rich-click/latest/documentation/rich_click_cli/[/]

The rich-click command line tool can be prepended before any Python package
using native click to provide attractive richified click help output.

For example, if you have a package called [argument]my_package[/] that uses click,
you can run:

>>> [command]rich-click[/] [argument]my_package[/] [option]--help[/]

When not rendering help text, the provided command will run normally,
so it is safe to replace calls to the tool with [command]rich-click[/] in front, e.g.:

>>> [command]rich-click[/] [argument]my_package[/] [argument]cmd[/] [option]--foo[/] 3

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/cli.py#L285-L521)

## rich_click.cli.patch

*function* · *Added in 1.3.1*

```python
def patch(*args: Any, **kwargs: Any) -> None
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/cli.py#L39-L50)
