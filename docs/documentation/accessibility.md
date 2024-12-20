# Accessibility

This page goes over information relevant to both developers and users relating to accessibility considerations.

Accessibility is very important to consider when developing applications.
Colorblindness impacts roughly 4% of the general population, meaning that if your application gets even a small user base, there is a high probability that it is being used by someone with colorblindness.

Fortunately, there are ways as both developers and users to address these accessibility concerns, as detailed on this page.

## Colorblindness accessibility for users

If you are a user of a **rich-click** CLI, there are a few options you have to improve accessibility for yourself.

### 1. Configure your terminal's 4-bit ANSI colors

The 4-bit ANSI color system is a set of 16 different colors implemented in every terminal. This is the most common way to set colors.
These colors are **not** deterministic; different terminals use slightly different hex values for the ANSI colors. [Wikipedia has a full breakdown of all the variations in these colors](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit)

Most modern terminals have the ability to customize all of these colors in the terminals' settings.
If you are having difficulty distinguishing colors, it is recommended that you adjust these settings.

!!! note
    This will only work for CLIs that utilize the 4-bit ANSI color system.
    CLIs that utilize hex values or other color systems will not be impacted by your terminal's ANSI color settings.

### 2. Use the `NO_COLOR` environment variable

Rich uses the `NO_COLOR` standard ([more information here](https://no-color.org/)), which means it has a built-in capability that allows the user to suppress color.
The Rich docs also go over additional and related console settings [here](https://rich.readthedocs.io/en/latest/console.html).

So, instead of running your CLI like this:

```shell
$ python cli.py
```

You can instead do the following:

```shell
# Set environment variable, then run:
export NO_COLOR=1
python cli.py

# ... Or run as a single line:
NO_COLOR=1 python cli.py
```

And this will disable all colors in **rich-click**.

You can also add `NO_COLOR=1` to your `~/.bashrc` (if using bash) or `~/.zshrc` (if using zsh):

```shell
# If using bash:
echo "NO_COLOR=1" > ~/.bashrc

# If using zsh:
echo "NO_COLOR=1" > ~/.zshrc
```

## Colorblindness accessibility considerations for developers

If you would like to make your CLI more accessible for others, there are a few rules of thumb you can follow:

### 1. Use Rich features over Click features

If you are using colors inside your print statements and interactive elements, you can make your CLI more accessible with the following:

- Replace `click.echo()` with `rich.print()` ([Rich docs](https://rich.readthedocs.io/en/stable/introduction.html#quick-start))
- Replace `click.prompt()` with `rich.prompt.Prompt.ask()` ([Rich docs](https://rich.readthedocs.io/en/stable/prompt.html))
- Replace `click.confirm()` with `rich.prompt.Confirm.ask()` ([Rich docs](https://rich.readthedocs.io/en/stable/prompt.html))

The reason why the Rich features are more accessible than the corresponding Click features is because of the `NO_COLOR` environment variable, which the Rich library uses to disables all color. This environment variable does not work with `click.style()`, however.

!!! info
    `NO_COLOR` is a _de facto_ standard for disabling color across a wide variety of terminal programs and frameworks.
    You can read more [here](https://no-color.org/) about the standard.

So, for example:

- `Confirm.ask("[red]Are you sure?[/]")` is more accessible because it works with `NO_COLOR`.
- `click.confirm(click.echo("Are you sure?", fg="red"))` is less accessible because it cannot be overridden by `NO_COLOR`.

### 2. Use 4-bit ANSI colors

The 4-bit ANSI color system is a set of 16 different colors implemented in effectively every terminal, and they are the most common way to set colors.
These colors are **not** deterministic; different terminals use slightly different hex values for the ANSI colors. [Wikipedia has a full breakdown of all the variations in these colors](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit)

!!! note
    **rich-click**'s logo references the ANSI colors! 😁

There are 16 total ANSI colors: 8 base ANSI colors, with each one having a "bright" variant:

- `black`
- `red`
- `green`
- `yellow`
- `blue`
- `magenta`
- `cyan`
- `white`
- `bright_black`
- `bright_red`
- `bright_green`
- `bright_yellow`
- `bright_blue`
- `bright_magenta`
- `bright_cyan`
- `bright_white`

Additionally, each one of these can be modified with `dim`, which in modern terminals just applies a change to the opacity of the color.
In total, when counting `dim`, this gives developers 32 different colors that can be shown.

Below is a quick script that renders all of these colors:

```python
{!code_snippets/accessibility/colors.py!}
```

<!-- RICH-CODEX
working_dir: docs/code_snippets/accessibility
-->
![`python colors.py`](../images/code_snippets/accessibility/colors.svg){.screenshot}

The fact that the colors are not deterministic is a _benefit_ for accessibility; it means, for example, a user can customize their terminal so that the ANSI "red" is more suitable for them.
Nearly every modern terminal allows for this sort of customization.

This means that developers looking to create a more accessible experience should prefer ANSI colors.

So, for example:

- `RichHelpConfiguration(style_option="red")` is more accessible because users can configure the hex value of this red.
- `RichHelpConfiguration(style_option="#FF0000")` is less accessible because it is not configurable by the end user.
