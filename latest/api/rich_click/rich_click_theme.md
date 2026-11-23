---
project: "rich-click"
title: "rich_click.rich_click_theme"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_click_theme/"
---

# rich_click.rich_click_theme

*module* · *Added in 1.9.0*

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L1-L1)

## rich_click.rich_click_theme.COLORS

*attribute* · *Added in 1.9.0* · *module attribute*

```python
COLORS: dict[str, RichClickTheme] = _colors
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L945-L945)

## rich_click.rich_click_theme.FORMATS

*attribute* · *Added in 1.9.0* · *module attribute*

```python
FORMATS: dict[str, RichClickTheme] = {'box': RichClickTheme(name='box', description='[b](Default)[/b] Original rich-click format with boxes', styles=_BOX_STYLES), 'square': RichClickTheme(name='square', description='Original rich-click format with square boxes', styles={: _BOX_STYLES, 'style_options_panel_box': 'SQUARE', 'style_commands_panel_box': 'SQUARE', 'style_errors_panel_box': 'SQUARE'}), 'nu': RichClickTheme(name='nu', description='Great balance of compactness, legibility, and style', post_combine_callback=_not_dim_title_callback, styles={'style_options_panel_box': 'HORIZONTALS_DOUBLE_TOP', 'style_commands_panel_box': 'HORIZONTALS_DOUBLE_TOP', 'style_errors_panel_box': 'ROUNDED', 'style_options_table_box': None, 'style_commands_table_box': None, 'style_options_table_expand': False, 'style_commands_table_expand': False, 'panel_title_string': '{}', 'style_options_panel_padding': 0, 'style_commands_panel_padding': 0, 'deprecated_string': '(Deprecated)', 'deprecated_with_reason_string': '(Deprecated: {})', 'default_string': '(Default: {})', 'envvar_string': '(Env: {})', 'required_long_string': '(Required)', 'range_string': '{}', 'append_range_help_string': '(Range: {})', 'append_metavars_help_string': '\\[{}]', 'required_short_string': '#', 'padding_header_text': (0, 1, 1, 1), 'padding_helptext': (0, 1, 1, 1), 'padding_usage': (0, 1, 1, 1), 'delimiter_comma': ',', 'delimiter_slash': '/', 'panel_title_padding': 1, 'options_table_column_types': ['required', 'opt_long', 'opt_short', 'help'], 'commands_table_column_types': ['name', 'aliases', 'help'], 'options_table_help_sections': ['help', 'metavar', 'required', 'default', 'envvar', 'deprecated'], 'commands_table_help_sections': ['help', 'deprecated'], 'panel_inline_help_delimiter': ' - ', 'padding_epilog': (0, 0, 1, 1), 'padding_footer_text': (0, 0, 1, 1), 'panel_inline_help_in_title': False}), 'slim': RichClickTheme(name='slim', description='Simple, classic, no-fuss CLI format', post_combine_callback=_not_dim_title_callback, styles={'style_options_panel_box': 'BLANK', 'style_commands_panel_box': 'BLANK', 'style_errors_panel_box': 'ROUNDED', 'style_options_table_box': None, 'style_commands_table_box': None, 'style_options_table_expand': False, 'style_commands_table_expand': False, 'panel_title_string': '{}:', 'style_options_panel_padding': (0, 0, 0, 1), 'style_commands_panel_padding': (0, 0, 0, 1), 'padding_header_text': (0, 0, 1, 0), 'padding_helptext': (0, 0, 1, 0), 'padding_usage': (0, 0, 1, 0), 'padding_epilog': (0, 0, 1, 0), 'padding_footer_text': (0, 0, 1, 0), 'options_table_column_types': ['opt_short', 'opt_long_metavar', 'help'], 'commands_table_column_types': ['name_with_aliases', 'help'], 'options_table_help_sections': ['help', 'range', 'required', 'default', 'envvar', 'deprecated'], 'commands_table_help_sections': ['help', 'deprecated'], 'append_metavars_help_string': '<{}>', 'envvar_string': '\\[env: {}=]', 'delimiter_comma': ', ', 'delimiter_slash': '/', 'panel_title_padding': 0, 'panel_inline_help_in_title': True, 'panel_inline_help_delimiter': ' ', 'deprecated_string': '\\[deprecated]', 'deprecated_with_reason_string': '\\[deprecated: {}]', 'default_string': '\\[default={}]', 'required_long_string': '\\[required]', 'range_string': '{}', 'append_range_help_string': '\\[range: {}]', 'required_short_string': '*'}), 'modern': RichClickTheme(name='modern', description='Beautiful modern look', post_combine_callback=_not_dim_title_callback, styles={'style_options_panel_box': None, 'style_commands_panel_box': None, 'style_errors_panel_box': 'ROUNDED', 'style_options_table_box': 'HORIZONTALS_TOP', 'style_commands_table_box': 'HORIZONTALS_TOP', 'style_options_table_expand': True, 'style_commands_table_expand': True, 'panel_title_string': '{}', 'style_options_panel_padding': 0, 'style_commands_panel_padding': 0, 'padding_header_text': (1, 2, 0, 3), 'padding_helptext': (0, 2, 1, 2), 'padding_usage': (1, 2, 1, 2), 'options_table_column_types': ['opt_short', 'opt_long', 'metavar', 'help'], 'commands_table_column_types': ['name', 'aliases', 'help'], 'options_table_help_sections': ['required', 'help', 'envvar', 'default', 'deprecated'], 'commands_table_help_sections': ['help', 'deprecated'], 'deprecated_string': '\\[deprecated]', 'deprecated_with_reason_string': '\\[deprecated: {}]', 'envvar_string': '\\[env={}]', 'default_string': '\\[default={}]', 'append_metavars_help_string': '\\[{}]', 'panel_inline_help_in_title': True, 'delimiter_comma': ', ', 'delimiter_slash': ' / ', 'panel_title_padding': 0, 'required_short_string': '*', 'panel_inline_help_delimiter': ' - ', 'required_long_string': '\\[required]', 'range_string': '[{}]', 'append_range_help_string': '\\[{}]', 'padding_epilog': (0, 2, 1, 2), 'padding_footer_text': (0, 2, 1, 2)}), 'robo': RichClickTheme(name='robo', description='Spacious with sharp corners', post_combine_callback=_not_dim_title_callback, styles={'style_options_panel_box': 'SQUARE', 'style_commands_panel_box': 'SQUARE', 'style_errors_panel_box': 'SQUARE', 'style_options_table_box': None, 'style_commands_table_box': None, 'style_options_panel_padding': (1, 2), 'style_commands_panel_padding': (1, 2), 'style_options_table_expand': True, 'style_commands_table_expand': True, 'padding_header_text': (0, 0, 1, 0), 'padding_helptext': (0, 0, 1, 0), 'padding_usage': (0, 0, 1, 0), 'deprecated_string': '❮[b]DEPRECATED[/b]❯', 'deprecated_with_reason_string': '❮[b]DEPRECATED:[/b] {}❯', 'envvar_string': '❮[b]ENV:[/b] {}=❯', 'default_string': '❮[b]DEFAULT:[/b] {}❯', 'append_metavars_help_string': '❮{}❯', 'required_short_string': '*', 'required_long_string': '❮[b]REQUIRED[/b]❯', 'range_string': '{}', 'append_range_help_string': '❮[b]RANGE[/b]: {}❯', 'options_table_column_types': ['opt_primary', 'opt_secondary', 'metavar', 'help'], 'commands_table_column_types': ['name', 'aliases', 'help'], 'options_table_help_sections': ['required', 'help', 'deprecated', 'default', 'envvar'], 'commands_table_help_sections': ['help', 'deprecated'], 'delimiter_comma': ', ', 'delimiter_slash': ' / ', 'panel_title_padding': 2, 'panel_title_string': '{}', 'panel_inline_help_delimiter': ' - ', 'padding_epilog': (0, 0, 1, 0), 'padding_footer_text': (0, 0, 1, 0), 'panel_inline_help_in_title': False})}
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L988-L1170)

## rich_click.rich_click_theme.ThemeType

*attribute* · *Added in 1.9.0* · *module attribute*

```python
ThemeType = Literal['color', 'format', 'combined']
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L15-L15)

## rich_click.rich_click_theme.RichClickTheme

*class* · *Added in 1.9.0*

```python
class RichClickTheme
```

A named set of styles for the help output. Select one with `--theme` or the `theme` setting.

Create RichTheme instance.

**Parameters**

- `name` (`str`) — Name of the theme.
- `description` (`str | None`) (default: `None`) — Description for the theme.
- `hidden` (`bool`) (default: `False`) — If true, hide from rich-click --themes.
- `styles` (`dict[str, Any] | None`) (default: `None`) — Dict of styles that are applied.
- `primary_colors` (`list[StyleType] | None`) (default: `None`) — Description of which colors are applied. Does not do anything, just serves as documentation.
- `post_combine_callback` (`Callable[[dict[str, Any]], dict[str, Any]] | None`) (default: `None`) — After combining two themes, function is called which adjusts the styles.
- `light_variant` (`str | None`) (default: `None`) — Name of a color palette to use instead of this one when the terminal has a light background.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L18-L77)

### rich_click.rich_click_theme.RichClickTheme.description

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
description = description
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L49-L49)

### rich_click.rich_click_theme.RichClickTheme.hidden

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
hidden = hidden
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L50-L50)

### rich_click.rich_click_theme.RichClickTheme.light_variant

*attribute* · *instance attribute*

```python
light_variant = light_variant
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L54-L54)

### rich_click.rich_click_theme.RichClickTheme.name

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
name = name
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L48-L48)

### rich_click.rich_click_theme.RichClickTheme.post_combine_callback

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
post_combine_callback = post_combine_callback
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L53-L53)

### rich_click.rich_click_theme.RichClickTheme.primary_colors

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
primary_colors = primary_colors or []
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L52-L52)

### rich_click.rich_click_theme.RichClickTheme.styles

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
styles = styles or {}
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L51-L51)

### rich_click.rich_click_theme.RichClickTheme.combine

*method* · *Added in 1.9.0*

```python
def combine(other: RichClickTheme) -> RichClickTheme
```

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L59-L69)

## rich_click.rich_click_theme.RichClickThemeNotFound

*class* · *Added in 1.9.0*

```python
class RichClickThemeNotFound(KeyError)
```

Bases: `KeyError`

Raise when a theme is not found.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L1175-L1176)

## rich_click.rich_click_theme.get_theme

*function* · *Added in 1.9.0*

```python
def get_theme(theme: str, raise_key_error: bool = True, resolve_background: bool = True) -> RichClickTheme
```

Get the theme based on the string name.

If ``resolve_background`` is true, the terminal background may be detected
to pick from a light/dark pair, or to use a palette's light variant.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L1242-L1303)

## rich_click.rich_click_theme.parse_background_theme

*function*

```python
def parse_background_theme(theme: str) -> dict[str, str] | None
```

Parse a light/dark theme pair such as ``"dark:nord-modern,light:solarized-modern"``.

Returns None if the string is not a theme pair.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L1179-L1203)

## rich_click.rich_click_theme.resolve_background_theme

*function*

```python
def resolve_background_theme(theme: str) -> str
```

Pick a theme name based on the terminal background.

- Light/dark pairs (``"dark:nord-modern,light:solarized-modern"``) resolve to one of the two themes.
  If the background cannot be detected, the first theme listed is used.
- Palettes with a light variant (e.g. ``nord``) switch to it (``nord_light``) on light backgrounds.
- All other theme names are returned unchanged.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L1220-L1239)

## rich_click.rich_click_theme.theme_needs_background

*function*

```python
def theme_needs_background(theme: str) -> bool
```

Whether picking this theme depends on the terminal background.

[View source](https://github.com/ewels/rich-click/blob/c66e11c798d1341c346cd82fb22834478340726b/src/rich_click/rich_click_theme.py#L1215-L1217)
