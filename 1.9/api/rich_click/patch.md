---
project: "rich-click"
title: "rich_click.patch"
description: "The command line interface."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/patch/"
---

# rich_click.patch

*module* · *Added in 1.8.0*

The command line interface.

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/patch.py#L1-L1)

## rich_click.patch.patch

*function* · *Added in 1.8.0*

```python
def patch(rich_config: RichHelpConfiguration | None = None, *, patch_rich_click: bool = True, patch_typer: bool = False, module: Any | None = None) -> None
```

Patch Click internals to use rich-click types.

----
    rich_config: Rich help configuration to apply globally. Defaults to None.
    patch_rich_click: Also patch the ``rich_click`` namespace. Defaults to True.
    patch_typer: Also patch Typer. Defaults to False.
    module: An async click fork (e.g. ``asyncclick``) to patch instead of ``click``.
        When provided, rich-click's async command classes are installed into that
        module's namespace. Requires ``rich-click[async]``. Defaults to None (click).

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/patch.py#L341-L415)

## rich_click.patch.patch_typer

*function* · *Added in 1.9.0*

```python
def patch_typer(rich_config: RichHelpConfiguration | None = None) -> None
```

[View source](https://github.com/ewels/rich-click/blob/da645c7fb7c3b8823220e33e62ff00a262d994da/src/rich_click/patch.py#L421-L491)
