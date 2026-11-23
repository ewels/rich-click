---
project: "rich-click"
title: "rich_click.patch"
description: "Patch click, Typer or asyncclick so that their commands print help and errors with rich-click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/patch/"
---

# rich_click.patch

*module* · *Added in 1.8.0*

Patch click, Typer or asyncclick so that their commands print help and errors with rich-click.

[View source](https://github.com/ewels/rich-click/blob/31048949e2a464cb225175dc0aa84afa990bacb6/src/rich_click/patch.py#L1-L1)

## rich_click.patch.patch

*function* · *Added in 1.8.0*

```python
def patch(rich_config: RichHelpConfiguration | None = None, *, patch_rich_click: bool = True, patch_typer: bool = False, module: Any | None = None) -> None
```

Patch Click internals to use rich-click types.

**Parameters**

- `rich_config` (`RichHelpConfiguration | None`) (default: `None`) — Help configuration to apply globally.
- `patch_rich_click` (`bool`) (default: `True`) — Also patch the `rich_click` namespace. Ignored when `module` is set.
- `patch_typer` (`bool`) (default: `False`) — Also patch Typer. Ignored when `module` is set.
- `module` (`Any | None`) (default: `None`) — An asynchronous click fork, such as `asyncclick`, to patch instead of click. rich-click then installs its async command classes into the namespace of that module. Requires `rich-click[async]`.

**Raises**

- `TypeError` — `module` is not an asynchronous click fork, such as asyncclick.

[View source](https://github.com/ewels/rich-click/blob/31048949e2a464cb225175dc0aa84afa990bacb6/src/rich_click/patch.py#L340-L415)

## rich_click.patch.patch_typer

*function* · *Added in 1.9.0*

```python
def patch_typer(rich_config: RichHelpConfiguration | None = None) -> None
```

Patch Typer so that its commands print help and errors with rich-click.

**Parameters**

- `rich_config` (`RichHelpConfiguration | None`) (default: `None`) — Help configuration for every command.

> **Warning**
>
> Typer 0.26 and later may not support the patch, so the function always shows a warning on those versions.
> If a Typer class cannot be patched, it shows a second warning and leaves Typer unpatched.
> See [Typer support](https://ewels.github.io/rich-click/latest/documentation/typer_support/#typer-026-support).

[View source](https://github.com/ewels/rich-click/blob/31048949e2a464cb225175dc0aa84afa990bacb6/src/rich_click/patch.py#L421-L502)
