---
project: "rich-click"
title: "rich_click.decorators"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/decorators/"
---

# rich_click.decorators

*module* · *Added in 1.7.0*

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L1-L1)

## rich_click.decorators.argument

*function* · *Added in 1.9.0*

```python
def argument(*param_decls: str, cls: type[click.Argument] | None = None, **attrs: Any) -> Callable[[FC], FC]
```

Add a positional argument to the command.

The same as `click.argument`, but the argument is a `RichArgument` unless you set `cls`.

**Parameters**

- `*param_decls` (`str`) (default: `()`) — Name of the argument.
- `cls` (`type[click.Argument] | None`) (default: `None`) — Argument class. Defaults to `RichArgument`.
- `**attrs` (`Any`) (default: `{}`) — Other arguments for the `cls` constructor, such as `nargs` and `type`. See `click.Argument`.

**Returns**

- (`Callable[[FC], FC]`) — A decorator that adds the argument to a command.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L347-L364)

## rich_click.decorators.command

*function* · *Added in 1.7.0*

```python
def command(name: str | None | _AnyCallable = None, cls: type[CmdType] | None = None, **attrs: Any) -> Command | Callable[[_AnyCallable], RichCommand | CmdType]
```

Create a command.

The same as `click.command`, but the command is a `RichCommand` unless you set `cls`.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L128-L175)

## rich_click.decorators.command_panel

*function* · *Added in 1.9.0*

```python
def command_panel(name: str, cls: type[RichPanel[Command, Any]] = RichCommandPanel, **attrs: Any) -> Callable[[FC], FC]
```

Show a group of subcommands in a panel of its own in the help output.

**Parameters**

- `name` (`str`) — Title of the panel.
- `cls` (`type[RichPanel[Command, Any]]`) (default: `RichCommandPanel`) — Panel class. Defaults to `RichCommandPanel`.
- `**attrs` (`Any`) (default: `{}`) — Other arguments for the panel class, such as `commands` and `help`.

**Returns**

- (`Callable[[FC], FC]`) — A decorator that adds the panel to a group.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L274-L290)

## rich_click.decorators.confirmation_option

*function* · *Added in 1.9.0*

```python
def confirmation_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]
```

Add a `--yes` option. Without it, the command asks the user to confirm, and exits if they decline.

**Parameters**

- `*param_decls` (`str`) (default: `()`) — Option names. Defaults to `--yes`.
- `**kwargs` (`Any`) (default: `{}`) — Other arguments for `option`.

**Returns**

- (`Callable[[FC], FC]`) — A decorator that adds the option to a command.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L387-L399)

## rich_click.decorators.group

*function* · *Added in 1.7.0*

```python
def group(name: str | _AnyCallable | None = None, cls: type[G] | None = None, **attrs: Any) -> Group | Callable[[_AnyCallable], RichGroup | G]
```

Create a group of subcommands.

The same as `click.group`, but the group is a `RichGroup` unless you set `cls`.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L76-L92)

## rich_click.decorators.help_option

*function* · *Added in 1.9.0*

```python
def help_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]
```

Add a `--help` option that prints the help and exits.

**Parameters**

- `*param_decls` (`str`) (default: `()`) — Option names. Defaults to `--help`.
- `**kwargs` (`Any`) (default: `{}`) — Other arguments for `option`.

**Returns**

- (`Callable[[FC], FC]`) — A decorator that adds the option to a command.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L311-L344)

## rich_click.decorators.option

*function* · *Added in 1.9.0*

```python
def option(*param_decls: str, cls: type[click.Option] | None = None, **attrs: Any) -> Callable[[FC], FC]
```

Add an option to the command.

The same as `click.option`, but the option is a `RichOption` unless you set `cls`.

**Parameters**

- `*param_decls` (`str`) (default: `()`) — Names of the option, such as `"--count"` and `"-c"`.
- `cls` (`type[click.Option] | None`) (default: `None`) — Option class. Defaults to `RichOption`.
- `**attrs` (`Any`) (default: `{}`) — Other arguments for the `cls` constructor, such as `default` and `help`. See `click.Option`.

**Returns**

- (`Callable[[FC], FC]`) — A decorator that adds the option to a command.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L367-L384)

## rich_click.decorators.option_panel

*function* · *Added in 1.9.0*

```python
def option_panel(name: str, cls: type[RichPanel[Parameter, Any]] = RichOptionPanel, **attrs: Any) -> Callable[[FC], FC]
```

Show a group of options in a panel of its own in the help output.

**Parameters**

- `name` (`str`) — Title of the panel.
- `cls` (`type[RichPanel[Parameter, Any]]`) (default: `RichOptionPanel`) — Panel class. Defaults to `RichOptionPanel`.
- `**attrs` (`Any`) (default: `{}`) — Other arguments for the panel class, such as `options` and `help`.

**Returns**

- (`Callable[[FC], FC]`) — A decorator that adds the panel to a command or group.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L255-L271)

## rich_click.decorators.pass_context

*function* · *Added in 1.7.0*

```python
def pass_context(f: Callable[Concatenate[RichContext, PSpec], R]) -> Callable[PSpec, R]
```

Marks a callback as wanting to receive the current context object as first argument.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L306-L308)

## rich_click.decorators.password_option

*function* · *Added in 1.9.0*

```python
def password_option(*param_decls: str, **kwargs: Any) -> Callable[[FC], FC]
```

Add a `--password` option that prompts for the password two times and hides the input.

**Parameters**

- `*param_decls` (`str`) (default: `()`) — Option names. Defaults to `--password`.
- `**kwargs` (`Any`) (default: `{}`) — Other arguments for `option`.

**Returns**

- (`Callable[[FC], FC]`) — A decorator that adds the option to a command.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L402-L420)

## rich_click.decorators.rich_config

*function* · *Added in 1.7.0*

```python
def rich_config(help_config: dict[str, Any] | RichHelpConfiguration | None = None, *, console: Console | None = None) -> Callable[[FC], FC]
```

Set the help configuration and the Rich console of one command or group.

**Parameters**

- `help_config` (`dict[str, Any] | RichHelpConfiguration | None`) (default: `None`) — How to format help and errors, as a `RichHelpConfiguration` or a dict of its fields.
- `console` (`Console | None`) (default: `None`) — Rich console to print help and errors with. The context makes it available as `ctx.console`.

**Returns**

- (`Callable[[FC], FC]`) — A decorator that applies the settings to a command or group.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L198-L237)

## rich_click.decorators.version_option

*function* · *Added in 1.9.0*

```python
def version_option(version: str | None = None, *param_decls: str, package_name: str | None = None, prog_name: str | None = None, message: str | None = None, **kwargs: Any) -> Callable[[FC], FC]
```

Add a `--version` option that prints the version and exits.

**Parameters**

- `version` (`str | None`) (default: `None`) — Version to print. If not set, Click reads it from the metadata of the installed `package_name`. If Click cannot find the version, `--version` raises a `RuntimeError`.
- `*param_decls` (`str`) (default: `()`) — Option names. Defaults to `--version`.
- `package_name` (`str | None`) (default: `None`) — Installed package to read the version from. If not set, it is the top-level package of the module that calls `version_option`.
- `prog_name` (`str | None`) (default: `None`) — Name of the CLI in the message. If not set, Click uses the name of the command.
- `message` (`str | None`) (default: `None`) — Message to print. It can use `%(prog)s`, `%(package)s` and `%(version)s`. Defaults to `"%(prog)s, version %(version)s"`.
- `**kwargs` (`Any`) (default: `{}`) — Other arguments for `option`.

**Returns**

- (`Callable[[FC], FC]`) — A decorator that adds the option to a command.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/decorators.py#L423-L459)
