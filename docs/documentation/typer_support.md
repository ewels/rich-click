# Typer Support

!!! warning "Experimental"
    `patch_typer()` does not work with `typer>=0.26.0`. See [Typer 0.26+ Support](#typer-026-support) below.

!!! example "Experimental"
    This feature is still experimental.
    Please report any bugs or issues you run into!

You don't need to use **rich-click** directly to get access to a lot of **rich-click**'s great features.

If you are a fan of Typer and you'd like to use **rich-click**'s themes, you can patch Typer to use **rich-click**
and set the global config's `THEME` (and other config options) to whatever you want.

All you need to do is import `patch_typer()` from `rich_click.patch`.
This does not need to be done at the top of the file, in fact you can do it right before calling `app.run()` or `typer.run(...)`:

```python hl_lines="24-28"
{% include "../code_snippets/typer_support/typer_example.py" %}
```

???+ example "Output"

    Running the above Typer CLI works the same as you would otherwise expect,
    except now with a **rich-click** theme applied:

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/typer_support
    -->
    ![`python typer_example.py --help`](../images/code_snippets/typer_support/typer_example.svg){.screenshot}

## Patching Typer via the `rich-click` CLI

You can also patch Typer as an end-user of any Typer CLI via the `rich-click` CLI.

```shell
rich-click my-typer-cli --help
```

In addition to giving access to **rich-click**'s themes, another benefit of this is being able to generate HTML and SVG help text easily.
Although, do note that Typer and **rich-click** have some minor differences in how they render help text.

More information about usage of the `rich-click` CLI is in [the **rich-click CLI** docs](rich_click_cli.md), or you can run **`rich-click --help`** to view the CLI.

## Typer 0.26+ Support

Starting with `typer==0.26.0`, Typer vendors its own internal fork of Click (`typer._click`) instead of subclassing
the `click` package directly. As a result, `typer.core.TyperCommand`, `TyperGroup`, `TyperOption`, and
`TyperArgument` no longer derive from `click.Command`, `click.Group`, `click.Option`, or `click.Argument` --
they derive from Typer's own private copies of those classes, built with a different metaclass (`abc.ABCMeta`).

`patch_typer()` works by building new classes that inherit from *both* Typer's classes and **rich-click**'s own
`RichCommand` / `RichGroup` / etc. (which are built on the real `click` classes). Since `typer>=0.26`, those two
class hierarchies are unrelated, and their metaclasses conflict, so building the patched subclass raises:

```pycon
TypeError: metaclass conflict: the metaclass of a derived class must be a
(non-strict) subclass of the metaclasses of all its bases
```

Rather than let that exception propagate and crash your CLI, `patch_typer()` builds all of its patched classes
up front, inside a single `try`/`except` block, and only swaps them into Typer's internals if every one of them
built successfully. If any of them fails -- which is currently always the case on `typer>=0.26` -- `patch_typer()`:

1. Emits a short `RuntimeWarning` pointing back to this section.
2. Leaves Typer's own classes completely untouched.
3. Returns without raising, so your program keeps running exactly as it would if `patch_typer()` had never been called.

In practice, this means:

- Your Typer CLI keeps working normally on `typer>=0.26`.
- You won't get **rich-click**'s themes or panels from `patch_typer()` -- Typer falls back to rendering help with
  its own (also Rich-based) formatter.
- You'll see a `RuntimeWarning` at the point where `patch_typer()` is called, which you can silence with the
  standard [`warnings` filters](https://docs.python.org/3/library/warnings.html#warning-filter) if it's expected
  in your environment.

If you need `patch_typer()` to actually apply **rich-click**'s theming, pin `typer<0.26` for now. Patching against
Typer's private, vendored fork of Click would mean re-implementing this logic against internals that could change
again with any future Typer release, so there is no fix planned at this time. Track
[issue #330](https://github.com/ewels/rich-click/issues/330) for updates.
