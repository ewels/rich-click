---
project: "rich-click"
title: "rich_click.rich_help_configuration"
description: "Richly rendered command line interfaces in Click."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/rich_help_configuration/"
---

# rich_click.rich_help_configuration

*module* · *Added in 1.7.0*

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L1-L1)

## rich_click.rich_help_configuration.ColumnType

*attribute* · *Added in 1.9.0* · *module attribute*

```python
ColumnType = OptionColumnType | CommandColumnType | str
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L47-L47)

## rich_click.rich_help_configuration.CommandColumnType

*attribute* · *Added in 1.9.0* · *module attribute*

```python
CommandColumnType = Literal['name', 'aliases', 'name_with_aliases', 'help']
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L39-L39)

## rich_click.rich_help_configuration.CommandHelpSectionType

*attribute* · *Added in 1.9.0* · *module attribute*

```python
CommandHelpSectionType = Literal['aliases', 'help', 'deprecated']
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L45-L45)

## rich_click.rich_help_configuration.FROM_THEME

*attribute* · *Added in 1.9.0* · *module attribute*

```python
FROM_THEME: Any = FromTheme(default='default-box')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L68-L68)

## rich_click.rich_help_configuration.OptionColumnType

*attribute* · *Added in 1.9.0* · *module attribute*

```python
OptionColumnType = Literal['required', 'opt_primary', 'opt_secondary', 'opt_long', 'opt_short', 'opt_all', 'opt_all_metavar', 'opt_long_metavar', 'metavar', 'metavar_short', 'help']
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L23-L37)

## rich_click.rich_help_configuration.OptionHelpSectionType

*attribute* · *Added in 1.9.0* · *module attribute*

```python
OptionHelpSectionType = Literal['help', 'required', 'envvar', 'default', 'range', 'metavar', 'metavar_short', 'deprecated']
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L41-L43)

## rich_click.rich_help_configuration.T

*attribute* · *Added in 1.8.0* · *module attribute*

```python
T = TypeVar('T', bound='RichHelpConfiguration')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L21-L21)

## rich_click.rich_help_configuration.FromTheme

*class* · *Added in 1.9.0*

```python
class FromTheme
```

Sentinel value for unset config options.

Initialize a default.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L50-L65)

### rich_click.rich_help_configuration.FromTheme.default

*attribute* · *Added in 1.9.0* · *instance attribute*

```python
default = default
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L55-L55)

### rich_click.rich_help_configuration.FromTheme.get_default

*method* · *Added in 1.9.0*

```python
def get_default(key: str) -> Any
```

Get the default value from the default theme.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L60-L65)

## rich_click.rich_help_configuration.RichHelpConfiguration

*class* · *Added in 1.7.0* · *dataclass*

```python
class RichHelpConfiguration
```

Rich Help Configuration class.

When merging multiple RichHelpConfigurations together, user-defined values always
take precedence over the class's defaults. When there are multiple user-defined values
for a given field, the right-most field is used.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L97-L516)

### rich_click.rich_help_configuration.RichHelpConfiguration.aborted_text

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
aborted_text: str = field(default='Aborted.')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L218-L218)

### rich_click.rich_help_configuration.RichHelpConfiguration.align_commands_panel

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
align_commands_panel: AlignMethod = field(default='left')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L161-L161)

### rich_click.rich_help_configuration.RichHelpConfiguration.align_errors_panel

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
align_errors_panel: AlignMethod = field(default='left')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L175-L175)

### rich_click.rich_help_configuration.RichHelpConfiguration.align_options_panel

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
align_options_panel: AlignMethod = field(default='left')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L144-L144)

### rich_click.rich_help_configuration.RichHelpConfiguration.append_metavars_help

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
append_metavars_help: bool | None = field(default=None)
```

Append metavar (eg. [TEXT]) after the help text

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L240-L240)

### rich_click.rich_help_configuration.RichHelpConfiguration.append_metavars_help_string

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
append_metavars_help_string: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L206-L206)

### rich_click.rich_help_configuration.RichHelpConfiguration.append_range_help_string

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
append_range_help_string: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L207-L207)

### rich_click.rich_help_configuration.RichHelpConfiguration.arguments_panel_title

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
arguments_panel_title: str = field(default='Arguments')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L209-L209)

### rich_click.rich_help_configuration.RichHelpConfiguration.color_system

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
color_system: Literal['auto', 'standard', '256', 'truecolor', 'windows'] | None = field(default='auto')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L187-L187)

### rich_click.rich_help_configuration.RichHelpConfiguration.command_groups

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
command_groups: dict[str, list[CommandGroupDict]] = field(default_factory=lambda : {})
```

Define sorted groups of panels to display subcommands

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L259-L259)

### rich_click.rich_help_configuration.RichHelpConfiguration.commands_before_options

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
commands_before_options: bool = field(default=False)
```

If set, the commands panel show above the options panel.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L236-L236)

### rich_click.rich_help_configuration.RichHelpConfiguration.commands_panel_title

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
commands_panel_title: str = field(default='Commands')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L211-L211)

### rich_click.rich_help_configuration.RichHelpConfiguration.commands_table_column_types

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
commands_table_column_types: list[CommandColumnType] = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L191-L191)

### rich_click.rich_help_configuration.RichHelpConfiguration.commands_table_help_sections

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
commands_table_help_sections: list[CommandHelpSectionType] = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L193-L193)

### rich_click.rich_help_configuration.RichHelpConfiguration.default_panels_first

*attribute* · *Added in 1.9.6* · *class attribute* · *instance attribute*

```python
default_panels_first: bool = field(default=False)
```

If set, default panels appear before custom panels of the same type.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L238-L238)

### rich_click.rich_help_configuration.RichHelpConfiguration.default_string

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
default_string: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L201-L201)

### rich_click.rich_help_configuration.RichHelpConfiguration.delimiter_comma

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
delimiter_comma: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L213-L213)

### rich_click.rich_help_configuration.RichHelpConfiguration.delimiter_slash

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
delimiter_slash: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L214-L214)

### rich_click.rich_help_configuration.RichHelpConfiguration.deprecated_string

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
deprecated_string: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L199-L199)

### rich_click.rich_help_configuration.RichHelpConfiguration.deprecated_with_reason_string

*attribute* · *Added in 1.8.9* · *class attribute* · *instance attribute*

```python
deprecated_with_reason_string: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L200-L200)

### rich_click.rich_help_configuration.RichHelpConfiguration.enable_theme_env_var

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
enable_theme_env_var: bool = field(default=True)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L108-L108)

### rich_click.rich_help_configuration.RichHelpConfiguration.envvar_string

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
envvar_string: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L202-L202)

### rich_click.rich_help_configuration.RichHelpConfiguration.errors_epilogue

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
errors_epilogue: str | Text | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L217-L217)

### rich_click.rich_help_configuration.RichHelpConfiguration.errors_panel_title

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
errors_panel_title: str = field(default='Error')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L212-L212)

### rich_click.rich_help_configuration.RichHelpConfiguration.errors_suggestion

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
errors_suggestion: str | Text | None = field(default=None)
```

Defaults to Try 'cmd -h' for help. Set to False to disable.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L215-L215)

### rich_click.rich_help_configuration.RichHelpConfiguration.footer_text

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
footer_text: str | Text | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L197-L197)

### rich_click.rich_help_configuration.RichHelpConfiguration.force_terminal

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
force_terminal: bool | None = field(default_factory=force_terminal_default)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L188-L188)

### rich_click.rich_help_configuration.RichHelpConfiguration.group_arguments_options

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
group_arguments_options: bool = field(default=False)
```

Show arguments with options instead of in own panel

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L242-L242)

### rich_click.rich_help_configuration.RichHelpConfiguration.header_text

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
header_text: str | Text | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L196-L196)

### rich_click.rich_help_configuration.RichHelpConfiguration.helptext_aliases_string

*attribute* · *Added in 1.9.2* · *class attribute* · *instance attribute*

```python
helptext_aliases_string: str = field(default='Aliases: {}')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L208-L208)

### rich_click.rich_help_configuration.RichHelpConfiguration.helptext_show_aliases

*attribute* · *Added in 1.9.2* · *class attribute* · *instance attribute*

```python
helptext_show_aliases: bool = field(default=True)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L265-L265)

### rich_click.rich_help_configuration.RichHelpConfiguration.highlighter

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
highlighter: Highlighter | None = field(default=None, repr=False, compare=False)
```

(Deprecated) Rich regex highlighter for help highlighting

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L266-L266)

### rich_click.rich_help_configuration.RichHelpConfiguration.highlighter_patterns

*attribute* · *Added in 1.8.0* · *class attribute* · *instance attribute*

```python
highlighter_patterns: list[str] = field(default_factory=lambda : ['(^|[^\\w\\-])(?P<switch>-([^\\W0-9][\\w\\-]*\\w|[^\\W0-9]))', '(^|[^\\w\\-])(?P<option>--([^\\W0-9][\\w\\-]*\\w|[^\\W0-9]))', '(?P<metavar><[^>]+>)', '(?P<deprecated>\\(DEPRECATED(?:\\: .*?)?\\))$'])
```

Patterns to use with the option highlighter.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L269-L276)

### rich_click.rich_help_configuration.RichHelpConfiguration.legacy_windows

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
legacy_windows: bool | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L279-L279)

### rich_click.rich_help_configuration.RichHelpConfiguration.max_width

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
max_width: int | None = field(default_factory=terminal_width_default)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L186-L186)

### rich_click.rich_help_configuration.RichHelpConfiguration.option_envvar_first

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
option_envvar_first: bool | None = field(default=None)
```

Show env vars before option help text instead of after

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L244-L244)

### rich_click.rich_help_configuration.RichHelpConfiguration.option_groups

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
option_groups: dict[str, list[OptionGroupDict]] = field(default_factory=lambda : {})
```

Define sorted groups of panels to display options and arguments

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L261-L261)

### rich_click.rich_help_configuration.RichHelpConfiguration.options_panel_title

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
options_panel_title: str = field(default='Options')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L210-L210)

### rich_click.rich_help_configuration.RichHelpConfiguration.options_table_column_types

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
options_table_column_types: list[OptionColumnType] = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L190-L190)

### rich_click.rich_help_configuration.RichHelpConfiguration.options_table_help_sections

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
options_table_help_sections: list[OptionHelpSectionType] = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L192-L192)

### rich_click.rich_help_configuration.RichHelpConfiguration.padding_epilog

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
padding_epilog: PaddingDimensions = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L225-L225)

### rich_click.rich_help_configuration.RichHelpConfiguration.padding_errors_epilogue

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
padding_errors_epilogue: PaddingDimensions = field(default=(0, 1, 1, 1))
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L229-L229)

### rich_click.rich_help_configuration.RichHelpConfiguration.padding_errors_panel

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
padding_errors_panel: PaddingDimensions = field(default=(0, 0, 1, 0))
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L227-L227)

### rich_click.rich_help_configuration.RichHelpConfiguration.padding_errors_suggestion

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
padding_errors_suggestion: PaddingDimensions = field(default=(0, 1, 0, 1))
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L228-L228)

### rich_click.rich_help_configuration.RichHelpConfiguration.padding_footer_text

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
padding_footer_text: PaddingDimensions = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L226-L226)

### rich_click.rich_help_configuration.RichHelpConfiguration.padding_header_text

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
padding_header_text: PaddingDimensions = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L220-L220)

### rich_click.rich_help_configuration.RichHelpConfiguration.padding_helptext

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
padding_helptext: PaddingDimensions = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L222-L222)

### rich_click.rich_help_configuration.RichHelpConfiguration.padding_helptext_deprecated

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
padding_helptext_deprecated: PaddingDimensions = field(default=0)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L223-L223)

### rich_click.rich_help_configuration.RichHelpConfiguration.padding_helptext_first_line

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
padding_helptext_first_line: PaddingDimensions = field(default=0)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L224-L224)

### rich_click.rich_help_configuration.RichHelpConfiguration.padding_usage

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
padding_usage: PaddingDimensions = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L221-L221)

### rich_click.rich_help_configuration.RichHelpConfiguration.panel_inline_help_delimiter

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
panel_inline_help_delimiter: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L155-L155)

### rich_click.rich_help_configuration.RichHelpConfiguration.panel_inline_help_in_title

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
panel_inline_help_in_title: bool = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L154-L154)

### rich_click.rich_help_configuration.RichHelpConfiguration.panel_title_padding

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
panel_title_padding: int = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L184-L184)

### rich_click.rich_help_configuration.RichHelpConfiguration.panel_title_string

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
panel_title_string: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L198-L198)

### rich_click.rich_help_configuration.RichHelpConfiguration.range_string

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
range_string: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L205-L205)

### rich_click.rich_help_configuration.RichHelpConfiguration.required_long_string

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
required_long_string: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L204-L204)

### rich_click.rich_help_configuration.RichHelpConfiguration.required_short_string

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
required_short_string: str = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L203-L203)

### rich_click.rich_help_configuration.RichHelpConfiguration.show_arguments

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
show_arguments: bool | None = field(default=None)
```

Show positional arguments

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L232-L232)

### rich_click.rich_help_configuration.RichHelpConfiguration.show_metavars_column

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
show_metavars_column: bool | None = field(default=None)
```

Show a column with the option metavar (eg. INTEGER)

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L234-L234)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_aborted

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_aborted: StyleType = field(default='red')
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L179-L179)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_argument

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_argument: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L113-L113)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_command

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_command: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L114-L114)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_command_aliases

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_command_aliases: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L115-L115)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_command_help

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_command_help: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L133-L133)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_panel_border

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_commands_panel_border: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L153-L153)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_panel_box

*attribute* · *Added in 1.8.0* · *class attribute* · *instance attribute*

```python
style_commands_panel_box: str | Box | None = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L156-L156)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_panel_help_style

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_commands_panel_help_style: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L157-L157)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_panel_padding

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_commands_panel_padding: PaddingDimensions = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L159-L159)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_panel_style

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_commands_panel_style: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L160-L160)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_panel_title_style

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_commands_panel_title_style: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L158-L158)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_table_border_style

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_commands_table_border_style: StyleType | None = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L169-L169)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_table_box

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_commands_table_box: str | Box | None = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L167-L167)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_table_column_width_ratio

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_commands_table_column_width_ratio: tuple[None, None] | tuple[int, int] | None = field(default_factory=lambda : (None, None))
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L170-L172)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_table_expand

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_commands_table_expand: bool = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L166-L166)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_table_leading

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_commands_table_leading: int = field(default=0)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L163-L163)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_table_pad_edge

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_commands_table_pad_edge: bool = field(default=False)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L164-L164)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_table_padding

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_commands_table_padding: PaddingDimensions = field(default_factory=lambda : (0, 1))
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L165-L165)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_table_row_styles

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_commands_table_row_styles: list[StyleType] | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L168-L168)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_commands_table_show_lines

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_commands_table_show_lines: bool = field(default=False)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L162-L162)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_deprecated

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_deprecated: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L128-L128)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_epilog_text

*attribute* · *Added in 1.7.2* · *class attribute* · *instance attribute*

```python
style_epilog_text: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L123-L123)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_errors_panel_border

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_errors_panel_border: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L173-L173)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_errors_panel_box

*attribute* · *Added in 1.8.0* · *class attribute* · *instance attribute*

```python
style_errors_panel_box: str | Box | None = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L174-L174)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_errors_suggestion

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_errors_suggestion: StyleType | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L176-L176)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_errors_suggestion_command

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_errors_suggestion_command: StyleType | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L177-L177)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_footer_text

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_footer_text: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L124-L124)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_header_text

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_header_text: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L122-L122)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_helptext

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_helptext: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L130-L130)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_helptext_aliases

*attribute* · *Added in 1.9.2* · *class attribute* · *instance attribute*

```python
style_helptext_aliases: StyleType | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L131-L131)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_helptext_first_line

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_helptext_first_line: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L129-L129)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_metavar

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_metavar: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L118-L118)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_metavar_append

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_metavar_append: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L119-L119)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_metavar_separator

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_metavar_separator: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L120-L120)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_option

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_option: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L111-L111)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_option_default

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_option_default: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L134-L134)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_option_envvar

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_option_envvar: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L135-L135)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_option_help

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_option_help: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L132-L132)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_option_negative

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_option_negative: StyleType | None = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L112-L112)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_panel_border

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_options_panel_border: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L138-L138)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_panel_box

*attribute* · *Added in 1.8.0* · *class attribute* · *instance attribute*

```python
style_options_panel_box: str | Box | None = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L139-L139)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_panel_help_style

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_options_panel_help_style: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L140-L140)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_panel_padding

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_options_panel_padding: PaddingDimensions = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L142-L142)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_panel_style

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_options_panel_style: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L143-L143)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_panel_title_style

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_options_panel_title_style: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L141-L141)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_table_border_style

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_options_table_border_style: StyleType | None = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L152-L152)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_table_box

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_options_table_box: str | Box | None = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L150-L150)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_table_expand

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_options_table_expand: bool = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L149-L149)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_table_leading

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_options_table_leading: int = field(default=0)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L146-L146)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_table_pad_edge

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_options_table_pad_edge: bool = field(default=False)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L147-L147)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_table_padding

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_options_table_padding: PaddingDimensions = field(default_factory=lambda : (0, 1))
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L148-L148)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_table_row_styles

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_options_table_row_styles: list[StyleType] | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L151-L151)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_options_table_show_lines

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_options_table_show_lines: bool = field(default=False)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L145-L145)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_padding_epilog

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_padding_epilog: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L182-L182)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_padding_errors

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_padding_errors: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L178-L178)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_padding_helptext

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_padding_helptext: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L181-L181)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_padding_usage

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_padding_usage: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L180-L180)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_range_append

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_range_append: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L121-L121)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_required_long

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_required_long: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L137-L137)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_required_short

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_required_short: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L136-L136)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_switch

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_switch: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L116-L116)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_switch_negative

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_switch_negative: StyleType | None = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L117-L117)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_usage

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_usage: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L125-L125)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_usage_command

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
style_usage_command: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L126-L126)

### rich_click.rich_help_configuration.RichHelpConfiguration.style_usage_separator

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
style_usage_separator: StyleType = field(default=FROM_THEME)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L127-L127)

### rich_click.rich_help_configuration.RichHelpConfiguration.text_emojis

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
text_emojis: bool = field(default=notset)
```

If set, parse emoji codes and replace with actual emojis, e.g. :smiley_cat: -> 😺

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L251-L251)

### rich_click.rich_help_configuration.RichHelpConfiguration.text_kwargs

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
text_kwargs: dict[str, Any] | None = field(default=None)
```

Additional kwargs to pass to Rich text rendering. Kwargs differ by text_markup chosen.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L248-L248)

### rich_click.rich_help_configuration.RichHelpConfiguration.text_markup

*attribute* · *Added in 1.8.0* · *class attribute* · *instance attribute*

```python
text_markup: Literal['ansi', 'rich', 'markdown', 'rst', None] = field(default=notset)
```

What engine to use to render the text. Default is 'ansi'.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L246-L246)

### rich_click.rich_help_configuration.RichHelpConfiguration.text_paragraph_linebreaks

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
text_paragraph_linebreaks: Literal['\n', '\n\n'] | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L250-L250)

### rich_click.rich_help_configuration.RichHelpConfiguration.theme

*attribute* · *Added in 1.9.0* · *class attribute* · *instance attribute*

```python
theme: str | RichClickTheme | None = field(default=None)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L107-L107)

### rich_click.rich_help_configuration.RichHelpConfiguration.use_click_short_help

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
use_click_short_help: bool = field(default=False)
```

Use click's default function to truncate help text

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L263-L263)

### rich_click.rich_help_configuration.RichHelpConfiguration.use_markdown

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
use_markdown: bool | None = field(default=None)
```

Silently deprecated; use `text_markup` field instead.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L253-L253)

### rich_click.rich_help_configuration.RichHelpConfiguration.use_markdown_emoji

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
use_markdown_emoji: bool | None = field(default=None)
```

Silently deprecated; use `text_emojis` instead.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L255-L255)

### rich_click.rich_help_configuration.RichHelpConfiguration.use_rich_markup

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
use_rich_markup: bool | None = field(default=None)
```

Silently deprecated; use `text_markup` field instead.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L257-L257)

### rich_click.rich_help_configuration.RichHelpConfiguration.width

*attribute* · *Added in 1.7.0* · *class attribute* · *instance attribute*

```python
width: int | None = field(default_factory=terminal_width_default)
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L185-L185)

### rich_click.rich_help_configuration.RichHelpConfiguration.apply_theme

*method* · *Added in 1.9.0*

```python
def apply_theme(force_default: bool = False) -> None
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L411-L496)

### rich_click.rich_help_configuration.RichHelpConfiguration.dump_to_globals

*method* · *Added in 1.8.0*

```python
def dump_to_globals(module: ModuleType | None = None) -> None
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L508-L516)

### rich_click.rich_help_configuration.RichHelpConfiguration.load_from_globals

*method* · *Added in 1.8.0* · *classmethod*

```python
def load_from_globals(module: ModuleType | None = None, **extra: Any) -> RichHelpConfiguration
```

Build a RichHelpConfiguration from globals in rich_click.rich_click.

When building from globals, all fields are treated as having been set by the user,
meaning they will overwrite other fields when "merged".

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L389-L409)

### rich_click.rich_help_configuration.RichHelpConfiguration.to_theme

*method* · *Added in 1.9.0*

```python
def to_theme(**kwargs: Any) -> RichClickTheme
```

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L498-L506)

## rich_click.rich_help_configuration.force_terminal_default

*function* · *Added in 1.7.0*

```python
def force_terminal_default() -> bool | None
```

Use as the default factory for `force_terminal`.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L71-L78)

## rich_click.rich_help_configuration.terminal_width_default

*function* · *Added in 1.7.0*

```python
def terminal_width_default() -> int | None
```

Use as the default factory for `width` and `max_width`.

[View source](https://github.com/ewels/rich-click/blob/022f47e9f25a36a3d4301fed1e2272df54ed4688/src/rich_click/rich_help_configuration.py#L81-L94)
