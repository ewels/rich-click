---
project: "rich-click"
title: "rich_click.decorators"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/decorators/"
---

# rich_click.decorators

*module* · *Added in 1.7.0*

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L1-L1)

## rich_click.decorators.argument

*function* · *Added in 1.9.0*

```python
def argument(*param_decls: str, cls: type[click.Argument] | None = None, **attrs: Any) -> Callable[[FC], FC]
```

Attaches an argument to the command.  All positional arguments are
passed as parameter declarations to :class:`Argument`; all keyword
arguments are forwarded unchanged (except ``cls``).
This is equivalent to creating an :class:`Argument` instance manually
and attaching it to the :attr:`Command.params` list.

For the default argument class, refer to :class:`Argument` and
:class:`Parameter` for descriptions of parameters.

:param cls: the argument class to instantiate.  This defaults to
            :class:`Argument`.
:param param_decls: Passed as positional arguments to the constructor of
    ``cls``.
:param attrs: Passed as keyword arguments to the constructor of ``cls``.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L345-L365)

## rich_click.decorators.command

*function* · *Added in 1.7.0*

```python
def command(name: str | None | _AnyCallable = None, cls: type[CmdType] | None = None, **attrs: Any) -> Command | Callable[[_AnyCallable], RichCommand | CmdType]
```

Command decorator function.

Defines the command() function so that it uses the RichCommand class by default.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L128-L175)

## rich_click.decorators.command_panel

*function* · *Added in 1.9.0*

```python
def command_panel(name: str, cls: type[RichPanel[Command, Any]] = RichCommandPanel, **attrs: Any) -> Callable[[FC], FC]
```

Use decorator to create a RichCommandPanel.

----
    name: Name of the RichCommandPanel instance being created.
    cls: The class of the RichPanel; defaults to RichCommandPanel.
    attrs: Additional attributes to pass to the RichCommandPanel.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L274-L289)

## rich_click.decorators.confirmation_option

*function* · *Added in 1.9.0*

```python
def confirmation_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]
```

Add a ``--yes`` option which shows a prompt before continuing if
not passed. If the prompt is declined, the program will exit.

:param param_decls: One or more option names. Defaults to the single
    value ``"--yes"``.
:param kwargs: Extra arguments are passed to :func:`option`.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L391-L401)

## rich_click.decorators.group

*function* · *Added in 1.7.0*

```python
def group(name: str | _AnyCallable | None = None, cls: type[G] | None = None, **attrs: Any) -> Group | Callable[[_AnyCallable], RichGroup | G]
```

Group decorator function.

Defines the group() function so that it uses the RichGroup class by default.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L76-L92)

## rich_click.decorators.help_option

*function* · *Added in 1.9.0*

```python
def help_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]
```

Pre-configured ``--help`` option which immediately prints the help page
and exits the program.

:param param_decls: One or more option names. Defaults to the single
    value ``"--help"``.
:param kwargs: Extra arguments are passed to :func:`option`.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L311-L342)

## rich_click.decorators.option

*function* · *Added in 1.9.0*

```python
def option(*param_decls: str, cls: type[click.Option] | None = None, **attrs: Any) -> Callable[[FC], FC]
```

Attaches an option to the command.  All positional arguments are
passed as parameter declarations to :class:`Option`; all keyword
arguments are forwarded unchanged (except ``cls``).
This is equivalent to creating an :class:`Option` instance manually
and attaching it to the :attr:`Command.params` list.

For the default option class, refer to :class:`Option` and
:class:`Parameter` for descriptions of parameters.

:param cls: the option class to instantiate.  This defaults to
            :class:`Option`.
:param param_decls: Passed as positional arguments to the constructor of
    ``cls``.
:param attrs: Passed as keyword arguments to the constructor of ``cls``.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L368-L388)

## rich_click.decorators.option_panel

*function* · *Added in 1.9.0*

```python
def option_panel(name: str, cls: type[RichPanel[Parameter, Any]] = RichOptionPanel, **attrs: Any) -> Callable[[FC], FC]
```

Use decorator to create a RichOptionPanel.

----
    name: Name of the RichOptionPanel instance being created.
    cls: The class of the RichPanel; defaults to RichOptionPanel.
    attrs: Additional attributes to pass to the RichOptionPanel.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L256-L271)

## rich_click.decorators.pass_context

*function* · *Added in 1.7.0*

```python
def pass_context(f: Callable[Concatenate[RichContext, PSpec], R]) -> Callable[PSpec, R]
```

Marks a callback as wanting to receive the current context object as first argument.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L305-L308)

## rich_click.decorators.password_option

*function* · *Added in 1.9.0*

```python
def password_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]
```

Add a ``--password`` option which prompts for a password, hiding
input and asking to enter the value again for confirmation.

:param param_decls: One or more option names. Defaults to the single
    value ``"--password"``.
:param kwargs: Extra arguments are passed to :func:`option`.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L404-L420)

## rich_click.decorators.rich_config

*function* · *Added in 1.7.0*

```python
def rich_config(help_config: dict[str, Any] | RichHelpConfiguration | None = None, *, console: Console | None = None) -> Callable[[FC], FC]
```

Use decorator to configure Rich Click settings.

----
    help_config: Rich help configuration that is used internally to format help messages and exceptions
        Defaults to None.
    console: A Rich Console that will be accessible from the `RichContext`, `RichCommand`, and `RichGroup` instances
        Defaults to None.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L198-L238)

## rich_click.decorators.version_option

*function* · *Added in 1.9.0*

```python
def version_option(version: str | None = None, *param_decls: str, package_name: str | None = None, prog_name: str | None = None, message: str | None = None, **kwargs: Any) -> Callable[[FC], FC]
```

Add a ``--version`` option which immediately prints the version
number and exits the program.

If ``version`` is not provided, Click will try to detect it using
:func:`importlib.metadata.version` to get the version for the
``package_name``. On Python < 3.8, the ``importlib_metadata``
backport must be installed.

If ``package_name`` is not provided, Click will try to detect it by
inspecting the stack frames. This will be used to detect the
version, so it must match the name of the installed package.

:param version: The version number to show. If not provided, Click
    will try to detect it.
:param param_decls: One or more option names. Defaults to the single
    value ``"--version"``.
:param package_name: The package name to detect the version from. If
    not provided, Click will try to detect it.
:param prog_name: The name of the CLI to show in the message. If not
    provided, it will be detected from the command.
:param message: The message to show. The values ``%(prog)s``,
    ``%(package)s``, and ``%(version)s`` are available. Defaults to
    ``"%(prog)s, version %(version)s"``.
:param kwargs: Extra arguments are passed to :func:`option`.
:raise RuntimeError: ``version`` could not be detected.

[View source](https://github.com/ewels/rich-click/blob/356c2764769a2bcd92aa67c3ed8f18b42bf9f5ed/src/rich_click/decorators.py#L423-L461)
