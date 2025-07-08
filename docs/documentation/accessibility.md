# Accessibility

This page goes over information relevant to both developers and users relating to accessibility considerations.

Accessibility is very important to consider when developing applications.
Colorblindness impacts roughly 4% of the general population, meaning that if your application gets even a small user base, there is a high probability that it is being used by someone with colorblindness.

Fortunately, there are ways as both developers and users to address these accessibility concerns, as detailed on this page.

## For users

If you are a user of a **rich-click** CLI, there are a few options you have to improve accessibility for yourself.

### 1. Use the `NO_COLOR` environment variable

Rich uses the `NO_COLOR` standard ([more information here](https://no-color.org/)), giving rich-click built-in capability to allow the user to suppress color.

So, to run any rich-click CLI program without colour, you can do:

```shell
export NO_COLOR=1  # Set environment variable in shell
python cli.py      # Run CLI tool

# ... Or run as a single line:
NO_COLOR=1 python cli.py
```

In order to set this environment variable automatically every time you use the terminal, you can add it to your `~/.bashrc` (if using bash) or `~/.zshrc` (if using zsh):

=== "bash"
    ```shell
    echo "export NO_COLOR=1" >> ~/.bashrc
    ```

=== "zsh"
    ```shell
    echo "export NO_COLOR=1" >> ~/.zshrc
    ```

!!!tip
    Note that other programs may also respect `NO_COLOR`, so it could have other effects!

### 2. Configure your terminal's 4-bit ANSI colors

The 4-bit ANSI color system is a set of 16 different colors implemented in every terminal. This is the most common way to set colors.
These colors are **not** deterministic; different terminals use slightly different hex values for the ANSI colors. [Wikipedia has a full breakdown of all the variations in these colors](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit)

Nearly all modern terminals have the ability to customize these colors in the terminals' settings.
If you are having difficulty distinguishing colors, it is recommended that you adjust these settings.

!!! note
    This will only work for CLIs that utilize the 4-bit ANSI color system.
    CLIs that utilize hex values or other color systems will not be impacted by your terminal's ANSI color settings.

## For developers

If you would like to make your CLI more accessible for others, there are a few rules of thumb you can follow:

### 1. Use Rich features over Click features

There are some Click features that rich-click doesn't override such as print statements and interactive prompts (see [Comparison of Click and rich-click](comparison_of_click_and_rich_click.md#click-features-that-rich-click-does-not-override)).

In these cases, we recommend using native Rich functionality so that your end users can benefit from `NO_COLOR`, which Click does not support.

So, for example:

- `#!python Confirm.ask("[red]Are you sure?[/]")` is more accessible because it works with `NO_COLOR`.
- `#!python click.confirm(click.echo("Are you sure?", fg="red"))` is less accessible because it cannot be overridden by `NO_COLOR`.

### 2. Use 4-bit ANSI colors

The 4-bit ANSI color system is a set of 16 different colors implemented in effectively every terminal, and they are the most common way to set colors.
These colors are **not** deterministic; different terminals use slightly different hex values for the ANSI colors. [Wikipedia has a full breakdown of all the variations in these colors](https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit)

!!! note
    **rich-click**'s logo references the ANSI colors! 😁

There are 16 total ANSI colors: 8 base ANSI colors, with each one having a "bright" variant:

- `black`, `bright_black`
- `red`, `bright_red`
- `green`, `bright_green`
- `yellow`, `bright_yellow`
- `blue`, `bright_blue`
- `magenta`, `bright_magenta`
- `cyan`, `bright_cyan`
- `white`, `bright_white`

Additionally, each one of these can be modified with `dim`, which in modern terminals just applies a change to the opacity of the color, giving developers a total of 32 different colors that can be shown.

Below is a quick script that renders all of these colors:

```python
{!code_snippets/accessibility/colors.py!}
```

<!-- RICH-CODEX
working_dir: docs/code_snippets/accessibility
hide_command: true
terminal_width: 48
-->
![`python colors.py`](../images/code_snippets/accessibility/colors.svg){.screenshot}

(The colors you see when running this locally will differ from the colors in the image.)

The fact that the colors are not deterministic is a _benefit_ for accessibility; it means, for example, a user can customize their terminal so that the ANSI "red" is more suitable for them.
Nearly every modern terminal allows for this sort of customization.

This means that developers looking to create a more accessible experience should prefer ANSI colors.

So, for example:

- `#!python RichHelpConfiguration(style_option="red")` is more accessible because users can configure the hex value of this red.
- `#!python RichHelpConfiguration(style_option="#FF0000")` is less accessible because it is not configurable by the end user.
