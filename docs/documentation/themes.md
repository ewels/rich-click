# Themes

**Themes** are a simple way to customize the style of CLI help text as both an end-user and as a developer.

=== "`quartz-slim`"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/introduction_to_click
    -->
    ![`RICH_CLICK_THEME=quartz-slim python hello_rich.py --help`](../images/code_snippets/themes/themes_ex1.svg){.screenshot}

=== "`lime-modern`"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/introduction_to_click
    -->
    ![`RICH_CLICK_THEME=lime-modern python hello_rich.py --help`](../images/code_snippets/themes/themes_ex2.svg){.screenshot}

=== "`nord-nu`"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/introduction_to_click
    -->
    ![`RICH_CLICK_THEME=nord-nu python hello_rich.py --help`](../images/code_snippets/themes/themes_ex2.svg){.screenshot}

=== "`cargo-slim`"

    <!-- RICH-CODEX
    working_dir: docs/code_snippets/introduction_to_click
    -->
    ![`RICH_CLICK_THEME=cargo-slim python hello_rich.py --help`](../images/code_snippets/themes/themes_ex2.svg){.screenshot}

Themes consist of **Color Palettes** and **Formats**, which can be mixed and matched.
The name of a full theme has the following schema: `{color_palette}-{format}`.

For example, the **forest-slim** theme uses the **forest** color palette and the **slim** format.

??? info "All themes"
    Running `rich-click --themes` will provide help text that lists every theme available to you:

    ![`rich-click --themes`](../images/code_snippets/themes/all_themes.svg){.screenshot}

## Themes as an end-user

Unless a developer specifies otherwise, every **rich-click** CLI can have a theme applied by an end-user by setting the `RICH_CLICK_THEME` env var.

If you'd like to set a global theme, add the following to your shell's config file (replacing `star-modern` with whatever theme you desire):

=== "bash"
    ```shell
    echo "export RICH_CLICK_THEME=star-modern" >> ~/.bashrc
    ```

=== "zsh"
    ```shell
    echo "export NO_COLOR=1" >> ~/.zshrc
    ```

Themes will also be used when you wrap a base Click CLI in the `rich-click` CLI, e.g.:

![](../images/flask_themed.svg "RICH_CLICK_THEME=star-modern rich-click flask --help"){.screenshot}

Alternatively, when using the `rich-click [cmd]` CLI, you can pass a theme via the `--theme`/`-t` option:

![](../images/flask_themed_2.svg "rich-click -t star-slim flask --help"){.screenshot}

The `RICH_CLICK_THEME` env var can also be a full JSON representation of a config.
For example, let's say you prefer having commands above options. There is a config option for this, `commands_before_options`, and you can place that in the `RICH_CLICK_THEME` env var:

```shell
export RICH_CLICK_THEME='{"commands_before_options": true, "theme": "news-robo"}'
rich-click flask --help
```

![](../images/flask_themed_3.svg "rich-click flask --help"){.screenshot}

## Themes as a developer

You can set a theme for your CLI by setting it in the config:

=== "`{}`"

    ```python
    import rich_click as click
    
    @click.group("cli")
    @click.rich_config({"theme": "nord-slim"})
    def cli():
        """My CLI help text"""
    ```

=== "`RichHelpConfiguration()`"
    ```python
    import rich_click as click
    
    @click.group("cli")
    @click.rich_config(click.RichHelpConfiguration(theme="nord-slim"))
    def cli():
        """My CLI help text"""
    ```

=== "Global config"
    ```python
    import rich_click as click

    click.rich_click.THEME = "nord-slim"

    @click.group("cli")
    def cli():
        """My CLI help text"""
    ```

By default, a theme can still be overridden by a user.
For CLIs which are already highly customized, this may cause unintended stylistic consequences;
you may also just want to enforce your own branding.
You can disable overrides with the `enable_theme_env_var` option:

=== "`{}`"

    ```python
    import rich_click as click
    
    @click.group("cli")
    @click.rich_config({"theme": "nord-slim", "enable_theme_env_var": False})
    def cli():
        """My CLI help text"""
    ```

=== "`RichHelpConfiguration()`"
    ```python
    import rich_click as click
    
    @click.group("cli")
    @click.rich_config(click.RichHelpConfiguration(theme="nord-slim", enable_theme_env_var=False))
    def cli():
        """My CLI help text"""
    ```

=== "Global config"
    ```python
    import rich_click as click

    click.rich_click.THEME = "nord-slim"
    click.rich_click.ENABLE_THEME_ENV_VAR = False

    @click.group("cli")
    def cli():
        """My CLI help text"""
    ```

Note that themes never override existing config options; they are essentially the defaults for a config,
so explicitly set options always take precedence over a theme.
For more information on config resolution order, read [the **Configuration** docs](configuration.md).
