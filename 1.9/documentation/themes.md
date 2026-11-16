# Themes

**Themes** are a simple way to customize the style of CLI help text as both an end-user and as a developer.
Themes are one of **rich-click**'s most powerful features.

```shell
export RICH_CLICK_THEME=nord-nu
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_ex1.ansi"
$ python cli.py --help
```
```shell
export RICH_CLICK_THEME=dracula-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_ex2.ansi"
$ python cli.py --help
```
```shell
export RICH_CLICK_THEME=cargo-slim
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_ex3.ansi"
$ python cli.py --help
```
```shell
export RICH_CLICK_THEME=forest-robo
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_ex4.ansi"
$ python cli.py --help
```
```shell
export RICH_CLICK_THEME=solarized-square
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_ex5.ansi"
$ python cli.py --help
```
Themes consist of **Color Palettes** and **Formats**, which can be mixed and matched.
The name of a full theme has the following schema: `{color_palette}-{format}`.

For example, the **forest-slim** theme uses the **forest** color palette and the **slim** format.

<details>
<summary>Code for <code>cli.py</code></summary>

The following CLI code is used throughout this module to show off themes.

```python
cliRaw
```

</details>

## Themes as an end-user

Unless a developer specifies otherwise, every **rich-click** CLI can have a theme applied by an end-user by setting the `RICH_CLICK_THEME` env var.

If you'd like to set a global theme, add the following to your shell's config file (replacing `star-modern` with whatever theme you desire):

```shell
echo "export RICH_CLICK_THEME=star-modern" >> ~/.bashrc
```
```shell
echo "export RICH_CLICK_THEME=star-modern" >> ~/.zshrc
```
Themes will also be used when you wrap a base Click CLI in the `rich-click` CLI, e.g.:

```shell
export RICH_CLICK_THEME=star-modern
rich-click flask --help
```
```shell
export RICH_CLICK_THEME=star-modern
uv run --with=flask --with=rich-click \
    rich-click flask --help
```
```sh runnable.outputFile="../images/code_snippets/themes/flask_themed.ansi"
$ RICH_CLICK_THEME=star-modern rich-click flask --help
```

Alternatively, when using the `rich-click [cmd]` CLI, you can pass a theme via the `--theme`/`-t` option:

```shell
rich-click -t star-slim flask --help
```
```shell
uv run --with=flask --with=rich-click \
    rich-click --theme=star-slim flask --help
```
```sh runnable.outputFile="../images/code_snippets/themes/flask_themed_2.ansi"
$ rich-click -t star-slim flask --help
```

The `RICH_CLICK_THEME` env var can also be a full JSON representation of a config.
For example, let's say you prefer having commands above options. There is a config option for this, `commands_before_options`, and you can place that in the `RICH_CLICK_THEME` env var:

```shell
export RICH_CLICK_THEME='{"commands_before_options": true, "theme": "red1-nu"}'
rich-click flask --help
```
```shell
export RICH_CLICK_THEME='{"commands_before_options": true, "theme": "red1-nu"}'
uv run --with=flask --with=rich-click \
    rich-click flask --help
```
```sh runnable.outputFile="../images/code_snippets/themes/flask_themed_3.ansi"
$ rich-click flask --help
```

## Themes as a developer

You can set a theme for your CLI by setting it in the config:

```python
import rich_click as click

@click.group("cli")
@click.rich_config({"theme": "nord-slim"})
def cli():
    """My CLI help text"""
```
```python
import rich_click as click

@click.group("cli")
@click.rich_config(click.RichHelpConfiguration(theme="nord-slim"))
def cli():
    """My CLI help text"""
```
```python
import rich_click as click

click.rich_click.THEME = "nord-slim"

@click.group("cli")
def cli():
    """My CLI help text"""
```
For more advanced CLIs, with lots of other customization options, there are additional considerations with themes and how they interact with your config that you may want to consider, especially in relation to end users being able to override the theme. For more information on this, read [the **Configuration** docs](../../documentation/configuration/).

## All themes

### Formats

There are currently 6 available **formats**.

**(Default)** Original rich-click format with boxes.

```sh runnable.outputFile="../images/code_snippets/themes/themes_default_box.ansi"
$ python cli.py --help
```
Original rich-click format with square boxes.

```sh runnable.outputFile="../images/code_snippets/themes/themes_default_square.ansi"
$ python cli.py --help
```
Simple, classic, no-fuss CLI format.

```sh runnable.outputFile="../images/code_snippets/themes/themes_default_slim.ansi"
$ python cli.py --help
```
Beautiful modern look.

```sh runnable.outputFile="../images/code_snippets/themes/themes_default_modern.ansi"
$ python cli.py --help
```
Spacious with sharp corners.

```sh runnable.outputFile="../images/code_snippets/themes/themes_default_robo.ansi"
$ python cli.py --help
```
Great balance of compactness, legibility, and style.

```sh runnable.outputFile="../images/code_snippets/themes/themes_default_nu.ansi"
$ python cli.py --help
```
### Color palettes

There are currently over a dozen different **color palettes**.

#### Multi-colored palettes

**Default** Original rich-click colors.

```shell
export RICH_CLICK_THEME=default-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_default_box.ansi"
$ python cli.py --help
```
Bright, colorful, vibrant accents.

```shell
export RICH_CLICK_THEME=solarized-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_solarized_box.ansi"
$ python cli.py --help
```
Many shades of cool colors.

```shell
export RICH_CLICK_THEME=nord-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_nord_box.ansi"
$ python cli.py --help
```
[Litestar](https://litestar.dev/) official theme.

```shell
export RICH_CLICK_THEME=star-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_star_box.ansi"
$ python cli.py --help
```
Dark and radiant.

```shell
export RICH_CLICK_THEME=quartz-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_quartz_box.ansi"
$ python cli.py --help
```
Remix of 'quartz' with accents.

```shell
export RICH_CLICK_THEME=quartz2-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_quartz2_box.ansi"
$ python cli.py --help
```
Cargo CLI theme; legible and bold.

```shell
export RICH_CLICK_THEME=cargo-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_cargo_box.ansi"
$ python cli.py --help
```
Earthy tones with analogous colors.

```shell
export RICH_CLICK_THEME=forest-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_forest_box.ansi"
$ python cli.py --help
```
Vibrant high-contract dark theme.

```shell
export RICH_CLICK_THEME=dracula-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_dracula_box.ansi"
$ python cli.py --help
```
:::caution[Warning]
The `dracula`, `nord`, and `solarized` themes use hex values,
and **rich-click** currently does not detect background colors for users' terminals.

So although these themes are beautiful and work well as an end-user with `export RICH_CLICK_THEME=`, this also makes these themes risky to use as a developer.

All of the other themes use ANSI colors exclusively, and therefore users' environments are more likely to match these themes well.

The `dracula`, `nord`, and `solarized` all have variants that force dark-backgrounds: `dracula_darkbg`, `nord_darkbg`, and `solarized_darkbg`.
You can apply this with something like [`term-background`](https://pypi.org/project/term-background/):

```python
import rich_click as click
from term_background import is_dark_background

if is_dark_background():
    click.rich_click.THEME = "dracula"
else:
    click.rich_click.THEME = "dracula_darkbg"
```

Some of these themes are riskier than others to apply as a developer. For example, the `solarized` theme is designed for both light and dark backgrounds. The `nord` theme has been tested on light terminals and, in practice, is legible. The `dracula` theme, however, is not user-friendly on a light background terminal.

Additionally, the `solarized` theme in particular is quite legible on both dark and light backgrounds,
so it is a relatively safe theme to use as a developer.

In a later version of **rich-click**, we intend on adding background color detection and styling conditional on background color,
which will make these themes safe to use as a developer.
:::

#### Simple palettes

The following palettes all focus on just a single color.

The below palettes are presented with the `modern` format.

Simple theme with red accents on section headers.

```shell
export RICH_CLICK_THEME=red1-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_red1_modern.ansi"
$ python cli.py --help
```
Simple theme with red accents on object names.

```shell
export RICH_CLICK_THEME=red2-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_red2_modern.ansi"
$ python cli.py --help
```
Simple theme with green accents on section headers.

```shell
export RICH_CLICK_THEME=green1-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_green1_modern.ansi"
$ python cli.py --help
```
Simple theme with green accents on object names.

```shell
export RICH_CLICK_THEME=green2-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_green2_modern.ansi"
$ python cli.py --help
```
Simple theme with yellow accents on section headers.

```shell
export RICH_CLICK_THEME=yellow1-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_yellow1_modern.ansi"
$ python cli.py --help
```
Simple theme with yellow accents on object names.

```shell
export RICH_CLICK_THEME=yellow2-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_yellow2_modern.ansi"
$ python cli.py --help
```
Simple theme with blue accents on section headers.

```shell
export RICH_CLICK_THEME=blue1-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_blue1_modern.ansi"
$ python cli.py --help
```
Simple theme with blue accents on object names.

```shell
export RICH_CLICK_THEME=blue2-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_blue2_modern.ansi"
$ python cli.py --help
```
Simple theme with magenta accents on section headers.

```shell
export RICH_CLICK_THEME=magenta1-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_magenta1_modern.ansi"
$ python cli.py --help
```
Simple theme with magenta accents on object names.

```shell
export RICH_CLICK_THEME=magenta2-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_magenta2_modern.ansi"
$ python cli.py --help
```
Simple theme with cyan accents on section headers.

```shell
export RICH_CLICK_THEME=cyan1-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_cyan1_modern.ansi"
$ python cli.py --help
```
Simple theme with cyan accents on object names.

```shell
export RICH_CLICK_THEME=cyan2-modern
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_cyan2_modern.ansi"
$ python cli.py --help
```
#### Monochromatic palettes

The following palettes have zero color.

Monochromatic theme with no colors.

```shell
export RICH_CLICK_THEME=mono-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_mono_box.ansi"
$ python cli.py --help
```
No style at all.

```shell
export RICH_CLICK_THEME=plain-box
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_plain_box.ansi"
$ python cli.py --help
```
<details>
<summary><code>plain-slim</code></summary>

Of course, the most plain style of them all is `plain-slim`, which renders CLI help text in the most conventional way that **rich-click** can.

For fun, we've included it here!

(Or, maybe you really dislike **rich-click**'s styles and you want to add `export RICH_CLICK_THEME=plain-slim` to your `.zshrc`.
We won't judge!)

```shell
export RICH_CLICK_THEME=plain-slim
python docs/code_snippets/themes/cli.py --help
```

```sh runnable.outputFile="../images/code_snippets/themes/themes_plain_slim.ansi"
$ python cli.py --help
```

</details>

### List all themes in command line

Running `rich-click --themes` will provide help text that lists every theme available to you.
The command will also tell you which theme you currently have enabled.

<details>
<summary>Output of <code>rich-click --themes</code></summary>

```sh runnable.outputFile="../images/code_snippets/themes/all_themes.ansi"
$ rich-click --themes
```

</details>