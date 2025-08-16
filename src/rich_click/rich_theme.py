from enum import Enum
from typing import Dict, Union
from typing import Literal


class RichClickTheme(str, Enum):
    """
    Themes available for RichHelpConfiguration.

    Use a a Rich Click theme to quickly apply a predefined set of styles.
    """

    default = "default"         #: The default Rich Click theme.
    dracula = "dracula"         #: Vibrant high-contract dark theme.
    gruvbox = "gruvbox"         #: Warm and earthy color theme.
    material = "material"       #: Google Material inspired theme.
    monochrome = "monochrome"   #: Minimal grayscale theme.
    nord = "nord"               #: Cool blues and soft color theme.
    onedark = "onedark"         #: One Dark syntax based theme.
    solarized = "solarized"     #: Solarized color theme.


COLORS = {
    "default": {},
    "solarized": {
        "style_option": "bold blue",
        "style_argument": "bold green",
        "style_command": "bold yellow",
        "style_switch": "bold cyan",
        "style_usage": "green",
        "style_deprecated": "bright_red",
    },
    "dracula": {
        "style_option": "bold magenta",
        "style_argument": "bold green",
        "style_command": "bold cyan",
        "style_switch": "bold red",
        "style_usage": "bright_blue",
        "style_deprecated": "bright_red",
    },
    "star": {
        "style_option": "bright_yellow",
        "style_command": "bright_yellow",
        "style_usage_command": "bright_yellow",
        "style_header_text": "",
        "style_switch": "yellow",
        "style_argument": "bright_blue",
        "style_usage": "bold bright_yellow",
        "style_metavar_append": "dim blue",
        "style_metavar": "dim blue",
        "style_options_panel_help_style": "dim blue",
        "style_commands_panel_help_style": "dim blue",
        "style_deprecated": "dim red",
        "style_required_short": "dim red",
    },
    "quartz": {
        "style_option": "bold magenta",
        "style_command": "bold blue",
        "style_usage_command": "blue",
        "style_header_text": "",
        "style_switch": "bold magenta",
        "style_argument": "magenta",
        "style_usage": "bold",
        "style_metavar_append": "dim yellow",
        "style_metavar": "dim yellow",
        "style_options_panel_help_style": "dim magenta",
        "style_commands_panel_help_style": "dim blue",
        "style_deprecated": "dim red",
        "style_required_short": "dim red",
        "style_options_panel_border": "dim magenta",
        "style_commands_panel_border": "dim blue",
        "style_options_table_border_style": "dim magenta",
        "style_commands_table_border_style": "dim blue",
    },
    "cargo": {
        "style_option": "bold cyan",
        "style_command": "bold cyan",
        "style_usage_command": "bold cyan",
        "style_switch": "bold cyan",
        "style_argument": "cyan",
        "style_usage": "bold green",
        "style_metavar_append": "cyan",
        "style_metavar": "cyan",
        "style_options_panel_border": "bold green",
        "style_commands_panel_border": "bold green",
        "style_options_panel_help_style": "",
        "style_commands_panel_help_style": "",
        "style_option_envvar": "dim",
        "style_option_default": "dim",
        "style_required_long": "dim bold",
    },
    "material": {
        "style_option": "bold cyan",
        "style_argument": "bold purple3",
        "style_command": "bold light_sky_blue1",
        "style_switch": "medium_purple3",
        "style_usage": "bold sea_green3",
        "style_deprecated": "bright_red",
        "style_options_panel_border": "dim medium_purple3",
        "style_commands_panel_border": "dim medium_purple3",
        "style_helptext_first_line": "sea_green3",
        "style_helptext": "dim sea_green3",
    },
    "monochrome": {
        "style_option": "",
        "style_command": "",
        "style_usage_command": "",
        "style_switch": "",
        "style_argument": "",
        "style_usage": "",
        "style_metavar_append": "",
        "style_metavar": "",
        "style_deprecated": "bold",
        "style_options_panel_border": "dim",
        "style_commands_panel_border": "dim",
        "style_options_panel_help_style": "",
        "style_commands_panel_help_style": "",
        "style_option_envvar": "dim",
        "style_option_default": "dim",
        "style_required_long": "bold",
        "style_required_short": "dim bold",
    },
    "nord": {
        "style_option": "bold bright_cyan",
        "style_argument": "bold white",
        "style_command": "bold bright_blue",
        "style_switch": "cyan",
        "style_usage": "bright_white",
        "style_deprecated": "bright_magenta",
    },
}

FORMATS = {
    "default": {},
    "fluent": {
        "style_options_panel_box": "HORIZONTALS_TOP",
        "style_commands_panel_box": "HORIZONTALS_TOP",
        # "commands_before_options": True,
        "style_options_panel_border": "dim",
        "style_commands_panel_border": "dim",
        "style_options_table_box": None,
        "style_commands_table_box": None,
        "style_options_panel_padding": 0,
        "style_commands_panel_padding": 0,
        "deprecated_string": "[deprecated]",
        "deprecated_with_reason_string": "[deprecated ({})]",
        "envvar_string": "[env={}]",
        "default_string": "[default={}]",
        "required_short_string": "#"
    },
    "slim": {
        "style_options_panel_box": "BLANK",
        "style_commands_panel_box": "BLANK",
        "style_options_panel_border": "bold",
        "style_commands_panel_border": "bold",
        "style_options_table_box": None,
        "style_commands_table_box": None,
        "style_options_panel_padding": (0, 0, 0, 1),
        "style_commands_panel_padding": (0, 0, 0, 1),
        "padding_header_text": (0, 0, 1, 0),
        "padding_helptext": (0, 0, 1, 1),
        "padding_usage": (0, 0, 1, 0),
        # "show_metavars_column": False,
        "show_required_column": False,
        # "append_metavars_help": True,
        "append_metavars_help_string": "[{}]",
        "envvar_string": "[env: {}=]"
    },
    "modern": {
        "style_options_panel_box": None,
        "style_commands_panel_box": None,
        "style_errors_panel_box": None,
        "style_options_panel_border": "",
        "style_commands_panel_border": "",
        "style_options_table_box": "HORIZONTALS_TOP",
        "style_commands_table_box": "HORIZONTALS_TOP",
        "style_options_panel_padding": (0, 1),
        "style_commands_panel_padding": (0, 1),
        "padding_header_text": (1, 0, 0, 2),
        "padding_helptext": (0, 0, 1, 2),
        "padding_usage": (1, 0, 1, 2),
        # "show_metavars_column": False,
        "show_required_column": False,
        # "append_metavars_help": True,
        "append_metavars_help_string": "[{}]",
        "envvar_string": "[env: {}=]"
    },
    "xp": {
        "style_options_panel_box": "ROUNDED",
        "style_commands_panel_box": "ROUNDED",
        "commands_before_options": True,
        "style_options_panel_border": "dim",
        "style_commands_panel_border": "dim",
        "style_options_table_box": None,
        "style_commands_table_box": None,
        "style_options_panel_padding": (1, 2),
        "style_commands_panel_padding": (1, 2),
        # "show_metavars_column": False,
        "show_required_column": False,
        # "append_metavars_help": True,
        "deprecated_string": "(Deprecated)",
        "deprecated_with_reason_string": "(Deprecated: {})",
        "default_string": "(Default: {})",
        "envvar_string": "(Env: {})",
        "required_short_string": "*",
        "required_long_string": "(Required)",
        "range_string": " {}",
        # deprecated_string: str = "[deprecated]"
        # deprecated_with_reason_string: str = "[deprecated: {}]"
        # default_string: str = "[default: {}]"
        # envvar_string: str = "[env var: {}]"
        # required_short_string: str = "*"
        # required_long_string: str = "[required]"
        # range_string: str = " [{}]"
        # append_metavars_help_string: str = "[{}]"

    }
}


THEMES = {}

for k, v in FORMATS.items():
    THEMES[k] = v

for k, v in COLORS.items():
    THEMES[k] = v

for fk, fv in FORMATS.items():
    for ck, cv in COLORS.items():
        THEMES[f"{ck}-{fk}"] = {**fv, **cv}


ThemeType = str
