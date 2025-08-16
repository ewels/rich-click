from enum import Enum
from typing import Dict, Union


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


ThemeType = Union[RichClickTheme, "RichClickTheme"]


THEMES: Dict[str, Dict[str, str]] = {
    "default": {},

    "dracula": {
        "style_option": "bold magenta",
        "style_argument": "bold green",
        "style_command": "bold cyan",
        "style_switch": "bold red",
        "style_usage": "bright_blue",
        "style_deprecated": "bright_red",
    },

    "gruvbox": {
        "style_option": "bold yellow",
        "style_argument": "bold red",
        "style_command": "bold bright_yellow",
        "style_switch": "bright_black",
        "style_usage": "bright_magenta",
        "style_deprecated": "red",
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
        "style_commands_panel_box": "SQUARE",
        "style_options_panel_box": "SQUARE",
        "style_errors_panel_box": "SQUARE",
    },

    "monochrome": {
        "style_option": "white",
        "style_argument": "white",
        "style_command": "white",
        "style_switch": "white",
        "style_usage": "dim",
        "style_deprecated": "dim",
    },

    "nord": {
        "style_option": "bold bright_cyan",
        "style_argument": "bold white",
        "style_command": "bold bright_blue",
        "style_switch": "cyan",
        "style_usage": "bright_white",
        "style_deprecated": "bright_magenta",
    },

    "onedark": {
        "style_option": "bold turquoise4",
        "style_argument": "bold orange1",
        "style_command": "bold blue",
        "style_switch": "bold green",
        "style_usage": "gray62",
        "style_deprecated": "red",
    },

    "solarized": {
        "style_option": "bold blue",
        "style_argument": "bold green",
        "style_command": "bold yellow",
        "style_switch": "bold cyan",
        "style_usage": "green",
        "style_deprecated": "bright_red",
    },
}
