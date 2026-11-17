import re
from collections.abc import Callable
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Literal


if TYPE_CHECKING:
    from rich.style import StyleType

# TODO: Optimize loading themes
#  No need to iterate over everything and store in memory.
#  Behaviors when combining themes is also weird
#  and can allow for more interesting variety.

ThemeType = Literal["color", "format", "combined"]


class RichClickTheme:
    """Rich theme. This sets defaults styling for the CLI."""

    def __init__(
        self,
        name: str,
        *,
        description: str | None = None,
        hidden: bool = False,
        styles: dict[str, Any] | None = None,
        primary_colors: list["StyleType"] | None = None,
        post_combine_callback: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
        light_variant: str | None = None,
    ) -> None:
        """
        Create RichTheme instance.

        Args:
        ----
            name: Name of the theme.
            description: Description for the theme.
            hidden: If true, hide from rich-click --themes.
            styles: Dict of styles that are applied.
            primary_colors: Description of which colors are applied. Does not do anything,
                just serves as documentation.
            post_combine_callback: After combining two themes, function is called which adjusts
                the styles.
            light_variant: Name of a color palette to use instead of this one when the terminal
                has a light background.

        """
        self.name = name
        self.description = description
        self.hidden = hidden
        self.styles = styles or {}
        self.primary_colors = primary_colors or []
        self.post_combine_callback = post_combine_callback
        self.light_variant = light_variant

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}>"

    def combine(self, other: "RichClickTheme") -> "RichClickTheme":
        styles = deepcopy(self.styles)
        styles.update(other.styles)
        if self.post_combine_callback:
            styles.update(self.post_combine_callback(styles))
        if other.post_combine_callback:
            styles.update(other.post_combine_callback(styles))
        return self.__class__(
            name=f"{self.name}-{other.name}",
            styles=styles,
        )

    def __add__(self, other: "RichClickTheme") -> "RichClickTheme":
        return self.combine(other)

    def __radd__(self, other: "RichClickTheme") -> "RichClickTheme":
        if other == 0:  # type: ignore[comparison-overlap]
            return self
        return other.combine(self)


def _spaced_delimiters_callback(d: dict[str, Any]) -> dict[str, Any]:
    return {"delimiter_comma": ", ", "delimiter_slash": " / "}


def _not_dim_title_callback(d: dict[str, Any]) -> dict[str, Any]:
    updates = {}
    for k in ["style_options_panel_title_style", "style_commands_panel_title_style"]:
        v: str | None = d.get(k)
        if k in d and v is not None and "dim" not in v.split(" "):
            updates[k] = f"{v} not dim".strip()
    return updates


COLORS: dict[str, RichClickTheme] = {
    "default": RichClickTheme(
        name="default",
        description="[b](Default)[/b] Original rich-click colors",
        primary_colors=["cyan", "yellow", "green"],
        styles={
            "style_option": "bold cyan",
            "style_option_negative": None,
            "style_argument": "bold cyan",
            "style_command": "bold cyan",
            "style_command_aliases": "bold green",
            "style_switch": "bold green",
            "style_switch_negative": None,
            "style_metavar": "bold yellow",
            "style_metavar_append": "dim yellow",
            "style_metavar_separator": "dim",
            "style_range_append": None,
            "style_usage": "yellow",
            "style_usage_command": "bold",
            "style_usage_separator": "",
            "style_options_panel_help_style": "dim",
            "style_commands_panel_help_style": "dim",
            "style_deprecated": "red",
            "style_options_table_border_style": "dim",
            "style_commands_table_border_style": "dim",
            "style_options_panel_border": "dim",
            "style_commands_panel_border": "dim",
            "style_options_panel_title_style": "",
            "style_commands_panel_title_style": "",
            "style_required_long": "dim red",
            "style_required_short": "red",
            "style_option_help": "",
            "style_command_help": "",
            "style_option_default": "dim",
            "style_option_envvar": "dim yellow",
            "style_helptext_first_line": "",
            "style_helptext": "dim",
            "style_header_text": "",
            "style_epilog_text": "",
            "style_footer_text": "",
            "style_options_panel_style": "none",
            "style_commands_panel_style": "none",
            "style_padding_usage": "none",
            "style_padding_helptext": "none",
            "style_padding_epilog": "none",
            "style_padding_errors": "none",
            "style_errors_panel_border": "red",
        },
    ),
    "solarized": RichClickTheme(
        name="solarized",
        description="Bright, colorful, vibrant accents",
        primary_colors=["#2aa198", "#268bd2", "#d33682"],
        styles={
            "style_option": "#2aa198",
            "style_option_negative": None,
            "style_argument": "#d33682",
            "style_command": "#2aa198",
            "style_command_aliases": "#859900",
            "style_switch": "#859900",
            "style_switch_negative": None,
            "style_metavar": "#b58900",
            "style_metavar_append": "#b58900",
            "style_metavar_separator": "",
            "style_range_append": None,
            "style_usage": "#b58900",
            "style_usage_command": "",
            "style_usage_separator": "",
            "style_options_panel_help_style": "dim",
            "style_commands_panel_help_style": "dim",
            "style_deprecated": "#6c71c4",
            "style_options_table_border_style": "dim #268bd2",
            "style_commands_table_border_style": "dim #268bd2",
            "style_options_panel_border": "dim #268bd2",
            "style_commands_panel_border": "dim #268bd2",
            "style_options_panel_title_style": "#268bd2 not dim",
            "style_commands_panel_title_style": "#268bd2 not dim",
            "style_required_long": "#dc322f",
            "style_required_short": "#dc322f",
            "style_option_help": "",
            "style_command_help": "",
            "style_option_default": "#d33682",
            "style_option_envvar": "#d33682",
            "style_helptext_first_line": "",
            "style_helptext": "dim",
            "style_header_text": "",
            "style_epilog_text": "",
            "style_footer_text": "",
            "style_options_panel_style": "none",
            "style_commands_panel_style": "none",
            "style_padding_usage": "none",
            "style_padding_helptext": "none",
            "style_padding_epilog": "none",
            "style_padding_errors": "none",
            "style_errors_panel_border": "#dc322f",
        },
    ),
    "solarized_darkbg": RichClickTheme(
        name="solarized_darkbg",
        hidden=True,
        description="Solarized theme with forced background color",
        primary_colors=["#2aa198", "#268bd2", "#d33682"],
        styles={
            "style_option": "#2aa198",
            "style_option_negative": None,
            "style_argument": "#d33682",
            "style_command": "#2aa198",
            "style_command_aliases": "#859900",
            "style_switch": "#859900",
            "style_switch_negative": None,
            "style_metavar": "#b58900",
            "style_metavar_append": "#b58900",
            "style_metavar_separator": "",
            "style_range_append": None,
            "style_usage": "#b58900",
            "style_usage_command": "",
            "style_usage_separator": "",
            "style_options_panel_help_style": "#839496",
            "style_commands_panel_help_style": "#839496",
            "style_deprecated": "#6c71c4",
            "style_options_table_border_style": "dim #268bd2",
            "style_commands_table_border_style": "dim #268bd2",
            "style_options_panel_border": "dim #268bd2",
            "style_commands_panel_border": "dim #268bd2",
            "style_options_panel_title_style": "#268bd2 not dim",
            "style_commands_panel_title_style": "#268bd2 not dim",
            "style_required_long": "#dc322f",
            "style_required_short": "#dc322f",
            "style_option_help": "",
            "style_command_help": "",
            "style_option_default": "#d33682",
            "style_option_envvar": "#d33682",
            "style_helptext_first_line": "#839496",
            "style_helptext": "#839496",
            "style_header_text": "",
            "style_epilog_text": "",
            "style_footer_text": "",
            "style_options_panel_style": "#839496 on #002b36",
            "style_commands_panel_style": "#839496 on #002b36",
            "style_padding_usage": "#839496 on #002b36",
            "style_padding_helptext": "#839496 on #002b36",
            "style_padding_epilog": "#839496 on #002b36",
            "style_padding_errors": "#839496 on #002b36",
            "style_errors_panel_border": "#dc322f",
        },
    ),
    "nord": RichClickTheme(
        name="nord",
        description="Many shades of cool colors",
        light_variant="nord_light",
        primary_colors=["#5e81ac", "#81a1c1", "#b48ead"],
        styles={
            "style_option": "#5e81ac",
            "style_option_negative": None,
            "style_argument": "#81a1c1",
            "style_command": "#8fbcbb",
            "style_command_aliases": "#b48ead",
            "style_usage_command": "#8fbcbb",
            "style_usage_separator": "",
            "style_switch": "#88c0d0",  #
            "style_switch_negative": None,
            "style_usage": "",
            "style_metavar_append": "#b48ead",
            "style_metavar": "#b48ead",
            "style_metavar_separator": "",
            "style_range_append": None,
            "style_options_panel_help_style": "default",
            "style_commands_panel_help_style": "default",
            "style_deprecated": "#d08770",
            "style_options_table_border_style": "#434c5e",
            "style_commands_table_border_style": "#434c5e",
            "style_options_panel_border": "#434c5e",
            "style_commands_panel_border": "#434c5e",
            "style_options_panel_title_style": "bold default not dim",
            "style_commands_panel_title_style": "bold default not dim",
            "style_required_long": "#bf616a",
            "style_required_short": "#bf616a",
            "style_option_help": "default",
            "style_command_help": "default",
            "style_option_default": "#a3be8c",
            "style_option_envvar": "#ebcb8b",
            "style_helptext_first_line": "#8fbcbb",
            "style_helptext": "default",
            "style_header_text": "default",
            "style_epilog_text": "#88c0d0",
            "style_footer_text": "#88c0d0",
            "style_options_panel_style": "none",
            "style_commands_panel_style": "none",
            "style_padding_usage": "none",
            "style_padding_helptext": "none",
            "style_padding_epilog": "none",
            "style_padding_errors": "none",
            "style_errors_panel_border": "#bf616a",
        },
    ),
    "nord_darkbg": RichClickTheme(
        name="nord_darkbg",
        hidden=True,
        description="Nord theme with forced background color",
        primary_colors=["#5e81ac", "#81a1c1", "#b48ead"],
        styles={
            "style_option": "#5e81ac",
            "style_option_negative": None,
            "style_argument": "#81a1c1",
            "style_command": "#8fbcbb",
            "style_command_aliases": "#b48ead",
            "style_usage_command": "#8fbcbb",
            "style_usage_separator": "",
            "style_switch": "#88c0d0",  #
            "style_switch_negative": None,
            "style_usage": "",
            "style_metavar_append": "#b48ead",
            "style_metavar": "#b48ead",
            "style_metavar_separator": "",
            "style_range_append": None,
            "style_options_panel_help_style": "#eceff4",
            "style_commands_panel_help_style": "#eceff4",
            "style_deprecated": "#d08770",
            "style_options_table_border_style": "#434c5e",
            "style_commands_table_border_style": "#434c5e",
            "style_options_panel_border": "#434c5e",
            "style_commands_panel_border": "#434c5e",
            "style_options_panel_title_style": "bold #eceff4 not dim",
            "style_commands_panel_title_style": "bold #eceff4 not dim",
            "style_required_long": "#bf616a",
            "style_required_short": "#bf616a",
            "style_option_help": "#eceff4",
            "style_command_help": "#eceff4",
            "style_option_default": "#a3be8c",
            "style_option_envvar": "#ebcb8b",
            "style_helptext_first_line": "#8fbcbb",
            "style_helptext": "#eceff4",
            "style_header_text": "#eceff4",
            "style_epilog_text": "#88c0d0",
            "style_footer_text": "#88c0d0",
            "style_options_panel_style": "#eceff4 on #2e3440",
            "style_commands_panel_style": "#eceff4 on #2e3440",
            "style_padding_usage": "#eceff4 on #2e3440",
            "style_padding_helptext": "#eceff4 on #2e3440",
            "style_padding_epilog": "#eceff4 on #2e3440",
            "style_padding_errors": "#eceff4 on #2e3440",
            "style_errors_panel_border": "#bf616a",
        },
    ),
    "dracula": RichClickTheme(
        name="dracula",
        description="Vibrant high-contract dark theme",
        light_variant="dracula_light",
        primary_colors=["magenta", "red", "yellow"],
        styles={
            "style_option": "#FF79C6",  # topink
            "style_option_negative": None,
            "style_argument": "not dim not bold #8BE9FD",
            "style_command": "#F1FA8C",
            "style_command_aliases": "#8BE9FD",
            "style_usage_command": "",
            "style_usage_separator": "bold dim",
            "style_switch": "bold #BD93F9",
            "style_switch_negative": None,
            "style_usage": "bold #50FA7B",
            "style_metavar_append": "#50FA7B",
            "style_metavar": "#50FA7B",
            "style_metavar_separator": "#44475A",
            "style_range_append": None,
            "style_options_panel_help_style": "#44475A not dim",
            "style_commands_panel_help_style": "#44475A not dim",
            "style_deprecated": "#FF5555",
            "style_options_table_border_style": "#6272A4",
            "style_commands_table_border_style": "#6272A4",
            "style_options_panel_border": "#6272A4",
            "style_commands_panel_border": "#6272A4",
            "style_options_panel_title_style": "#6272A4",
            "style_commands_panel_title_style": "#6272A4",
            "style_required_long": "#FF5555",
            "style_required_short": "#FF5555",
            "style_option_help": "",
            "style_command_help": "",
            "style_option_default": "#FFB86C",
            "style_option_envvar": "#8BE9FD",
            "style_helptext_first_line": "#6272A4",
            "style_helptext": "",
            "style_header_text": "",
            "style_epilog_text": "",
            "style_footer_text": "",
            "style_options_panel_style": "",
            "style_commands_panel_style": "",
            "style_padding_usage": "",
            "style_padding_helptext": "",
            "style_padding_epilog": "",
            "style_padding_errors": "none",
            "style_errors_panel_border": "#FF5555",
        },
    ),
    "dracula_darkbg": RichClickTheme(
        name="dracula_darkbg",
        hidden=True,
        description="Dracula theme with forced dark background color",
        primary_colors=["magenta", "red", "yellow"],
        styles={
            "style_option": "#FF79C6",  # topink
            "style_option_negative": None,
            "style_argument": "not dim not bold #8BE9FD",
            "style_command": "#F1FA8C",
            "style_command_aliases": "#8BE9FD",
            "style_usage_command": "#F8F8F2",
            "style_usage_separator": "bold dim",
            "style_switch": "bold #BD93F9",
            "style_switch_negative": None,
            "style_usage": "bold #50FA7B",
            "style_metavar_append": "#50FA7B",
            "style_metavar": "#50FA7B",
            "style_metavar_separator": "#44475A",
            "style_range_append": None,
            "style_options_panel_help_style": "#44475A",
            "style_commands_panel_help_style": "#44475A",
            "style_deprecated": "#FF5555",
            "style_options_table_border_style": "bold #6272A4",
            "style_commands_table_border_style": "bold #6272A4",
            "style_options_panel_border": "#6272A4",
            "style_commands_panel_border": "#6272A4",
            "style_options_panel_title_style": "#6272A4",
            "style_commands_panel_title_style": "#6272A4",
            "style_required_long": "#FF5555",
            "style_required_short": "#FF5555",
            "style_option_help": "#F8F8F2",
            "style_command_help": "#F8F8F2",
            "style_option_default": "#FFB86C",
            "style_option_envvar": "#8BE9FD",
            "style_helptext_first_line": "#6272A4",
            "style_helptext": "",
            "style_header_text": "",
            "style_epilog_text": "",
            "style_footer_text": "",
            "style_options_panel_style": "#F8F8F2 on #282A36",
            "style_commands_panel_style": "#F8F8F2 on #282A36",
            "style_padding_usage": "#F8F8F2 on #282A36",
            "style_padding_helptext": "#F8F8F2 on #282A36",
            "style_padding_epilog": "#F8F8F2 on #282A36",
            "style_padding_errors": "#F8F8F2 on #282A36",
            "style_errors_panel_border": "#FF5555",
        },
    ),
    "star": RichClickTheme(
        name="star",
        description="Litestar official theme",
        primary_colors=["yellow", "blue", "default"],
        styles={
            "style_option": "yellow",
            "style_option_negative": None,
            "style_argument": "bright_blue",
            "style_command": "yellow",
            "style_command_aliases": "yellow",
            "style_usage_command": "yellow",
            "style_usage_separator": "",
            "style_switch": "yellow",
            "style_switch_negative": None,
            "style_usage": "bold yellow",
            "style_metavar_append": "blue",
            "style_metavar": "blue",
            "style_metavar_separator": "",
            "style_range_append": None,
            "style_options_panel_help_style": "dim blue",
            "style_commands_panel_help_style": "dim blue",
            "style_deprecated": "dim red",
            "style_options_table_border_style": "",
            "style_commands_table_border_style": "",
            "style_options_panel_border": "dim",
            "style_commands_panel_border": "dim",
            "style_options_panel_title_style": "default not dim",
            "style_commands_panel_title_style": "default not dim",
            "style_required_long": "dim red",
            "style_required_short": "dim red",
            "style_option_help": "default not bold",
            "style_command_help": "default not bold",
            "style_option_default": "dim default",
            "style_option_envvar": "dim blue",
            "style_helptext_first_line": "default",
            "style_helptext": "default",
            "style_header_text": "",
            "style_epilog_text": "",
            "style_footer_text": "",
            "style_options_panel_style": "none",
            "style_commands_panel_style": "none",
            "style_padding_usage": "none",
            "style_padding_helptext": "none",
            "style_padding_epilog": "none",
            "style_padding_errors": "none",
            "style_errors_panel_border": "yellow",
        },
    ),
    # Dark and unified color scheme, looks great with complex CLIs.
    "quartz": RichClickTheme(
        name="quartz",
        description="Dark and radiant",
        primary_colors=["magenta", "dim magenta", "blue"],
        styles={
            "style_option": "bold magenta",
            "style_option_negative": None,
            "style_argument": "magenta not dim",
            "style_command": "bold blue",
            "style_command_aliases": "blue",
            "style_usage_command": "bright_blue",
            "style_usage_separator": "dim magenta",
            "style_switch": "bold magenta",
            "style_switch_negative": None,
            "style_usage": "bold",
            "style_metavar_append": "dim magenta",
            "style_metavar": "dim",
            "style_metavar_separator": "",
            "style_range_append": None,
            "style_options_panel_help_style": "dim",
            "style_commands_panel_help_style": "dim",
            "style_deprecated": "dim red",
            "style_options_table_border_style": "dim magenta",
            "style_commands_table_border_style": "dim blue",
            "style_options_panel_border": "dim magenta",
            "style_commands_panel_border": "dim blue",
            "style_options_panel_title_style": "",
            "style_commands_panel_title_style": "",
            "style_required_long": "dim red",
            "style_required_short": "dim red",
            "style_option_help": "default not bold",
            "style_command_help": "default not bold",
            "style_option_default": "dim",
            "style_option_envvar": "dim bright_magenta",
            "style_helptext_first_line": "bold",
            "style_helptext": "",
            "style_header_text": "",
            "style_epilog_text": "dim",
            "style_footer_text": "dim",
            "style_options_panel_style": "none",
            "style_commands_panel_style": "none",
            "style_padding_usage": "none",
            "style_padding_helptext": "none",
            "style_padding_epilog": "none",
            "style_padding_errors": "none",
            "style_errors_panel_border": "red",
        },
    ),
    # Remix of quartz with accents
    "quartz2": RichClickTheme(
        name="quartz2",
        description="Remix of 'quartz' with accents",
        primary_colors=["magenta", "blue", "yellow"],
        styles={
            "style_option": "magenta",
            "style_option_negative": None,
            "style_argument": "yellow",
            "style_command": "blue",
            "style_command_aliases": "blue",
            "style_usage_command": "",
            "style_usage_separator": "",
            "style_switch": "bold magenta",
            "style_switch_negative": None,
            "style_usage": "blue",
            "style_metavar_append": "yellow",
            "style_metavar": "yellow",
            "style_metavar_separator": "dim",
            "style_range_append": None,
            "style_options_panel_help_style": "yellow not dim italic",
            "style_commands_panel_help_style": "yellow not dim italic",
            "style_deprecated": "dim",
            "style_options_table_border_style": "dim magenta",
            "style_commands_table_border_style": "dim blue",
            "style_options_panel_border": "dim magenta",
            "style_commands_panel_border": "dim blue",
            "style_options_panel_title_style": "bold not dim",
            "style_commands_panel_title_style": "bold not dim",
            "style_required_long": "dim red",
            "style_required_short": "dim red",
            "style_option_help": "default not bold",
            "style_command_help": "default not bold",
            "style_option_default": "dim",
            "style_option_envvar": "dim yellow",
            "style_helptext_first_line": "",
            "style_helptext": "dim",
            "style_header_text": "blue",
            "style_epilog_text": "dim",
            "style_footer_text": "dim",
            "style_options_panel_style": "none",
            "style_commands_panel_style": "none",
            "style_padding_usage": "none",
            "style_padding_helptext": "none",
            "style_padding_epilog": "none",
            "style_padding_errors": "none",
            "style_errors_panel_border": "red",
        },
    ),
    "forest": RichClickTheme(
        name="forest",
        description="Earthy tones with analogous colors",
        primary_colors=["green", "yellow", "cyan"],
        styles={
            "style_option": "green",
            "style_option_negative": "magenta",
            "style_argument": "yellow",
            "style_command": "green",
            "style_command_aliases": "dim green",
            "style_usage_command": "green",
            "style_usage_separator": "",
            "style_switch": "bold green",
            "style_switch_negative": "bold magenta",
            "style_usage": "bold",
            "style_metavar_append": "yellow",
            "style_metavar": "yellow",
            "style_metavar_separator": "dim yellow",
            "style_range_append": None,
            "style_options_panel_help_style": "italic cyan",
            "style_commands_panel_help_style": "italic cyan",
            "style_deprecated": "dim bright_green",
            "style_options_table_border_style": "dim yellow",
            "style_commands_table_border_style": "dim yellow",
            "style_options_panel_border": "dim yellow",
            "style_commands_panel_border": "dim yellow",
            "style_options_panel_title_style": "yellow not dim",
            "style_commands_panel_title_style": "yellow not dim",
            "style_required_long": "bright_green",
            "style_required_short": "bright_green",
            "style_option_help": "default not bold",
            "style_command_help": "default not bold",
            "style_option_default": "yellow",
            "style_option_envvar": "yellow",
            "style_helptext_first_line": "green",
            "style_helptext": "",
            "style_header_text": "cyan",
            "style_epilog_text": "cyan",
            "style_footer_text": "cyan",
            "style_options_panel_style": "none",
            "style_commands_panel_style": "none",
            "style_padding_usage": "none",
            "style_padding_helptext": "none",
            "style_padding_epilog": "none",
            "style_padding_errors": "none",
            "style_errors_panel_border": "dim red",
        },
    ),
    # Theme based on cargo CLI. Legible and bold style.
    "cargo": RichClickTheme(
        name="cargo",
        description="Cargo CLI theme; legible and bold",
        primary_colors=["green", "cyan", "default"],
        styles={
            "style_option": "bold cyan",
            "style_option_negative": None,
            "style_argument": "cyan",
            "style_command": "bold cyan",
            "style_command_aliases": "bold cyan",
            "style_usage_command": "bold cyan",
            "style_usage_separator": "cyan",
            "style_switch": "bold cyan",
            "style_switch_negative": None,
            "style_usage": "bold green",
            "style_metavar_append": "cyan",
            "style_metavar": "cyan",
            "style_metavar_separator": "",
            "style_range_append": None,
            "style_options_panel_help_style": "default not bold italic",
            "style_commands_panel_help_style": "default not bold italic",
            "style_deprecated": "dim",
            "style_options_table_border_style": "green",
            "style_commands_table_border_style": "green",
            "style_options_panel_border": "green",
            "style_commands_panel_border": "green",
            "style_options_panel_title_style": "bold",
            "style_commands_panel_title_style": "bold",
            "style_required_long": "",
            "style_required_short": "bright_red",
            "style_option_help": "default not bold",
            "style_command_help": "default not bold",
            "style_option_default": "",
            "style_option_envvar": "",
            "style_helptext_first_line": "",
            "style_helptext": "",
            "style_header_text": "",
            "style_epilog_text": "",
            "style_footer_text": "",
            "style_options_panel_style": "none",
            "style_commands_panel_style": "none",
            "style_padding_usage": "none",
            "style_padding_helptext": "none",
            "style_padding_epilog": "none",
            "style_padding_errors": "none",
            "style_errors_panel_border": "red",
        },
    ),
    **{
        f"{c}1": RichClickTheme(
            name=f"{c}1",
            description=f"Simple theme with {c} accents on section headers",
            primary_colors=["default", c, f"dim {c}"],
            styles={
                "style_option": "",
                "style_option_negative": None,
                "style_argument": "",
                "style_command": "",
                "style_command_aliases": "",
                "style_usage_command": "bold",
                "style_usage_separator": "",
                "style_switch": "",
                "style_switch_negative": None,
                "style_usage": f"bold {c}",
                "style_metavar_append": "dim",
                "style_metavar": "dim",
                "style_metavar_separator": "",
                "style_range_append": None,
                "style_options_panel_help_style": f"dim italic bright_{c}",
                "style_commands_panel_help_style": f"dim italic bright_{c}",
                "style_deprecated": f"{c}",
                "style_options_table_border_style": f"dim {c}",
                "style_commands_table_border_style": f"dim {c}",
                "style_options_panel_border": f"dim {c}",
                "style_commands_panel_border": f"dim {c}",
                "style_options_panel_title_style": f"bold {c}",
                "style_commands_panel_title_style": f"bold {c}",
                "style_required_long": f"{c}",
                "style_required_short": f"bold {c}",
                "style_option_help": "default not bold",
                "style_command_help": "default not bold",
                "style_option_default": "dim",
                "style_option_envvar": "dim",
                "style_helptext_first_line": "",
                "style_helptext": "dim",
                "style_header_text": "",
                "style_epilog_text": "",
                "style_footer_text": "",
                "style_options_panel_style": "none",
                "style_commands_panel_style": "none",
                "style_padding_usage": "none",
                "style_padding_helptext": "none",
                "style_padding_epilog": "none",
                "style_padding_errors": "none",
                "style_errors_panel_border": "red",
            },
        )
        for c in ["red", "green", "yellow", "blue", "magenta", "cyan"]
    },
    **{
        f"{c}2": RichClickTheme(
            name=f"{c}2",
            description=f"Simple theme with {c} accents on object names",
            primary_colors=[c, "default", "dim"],
            styles={
                "style_option": f"{c}",
                "style_option_negative": None,
                "style_argument": f"{c}",
                "style_command": f"{c}",
                "style_command_aliases": f"{c}",
                "style_usage_command": "bold",
                "style_usage_separator": "",
                "style_switch": f"bold {c}",
                "style_switch_negative": None,
                "style_usage": f"bold {c}",
                "style_metavar_append": f"dim {c}",
                "style_metavar": f"dim {c}",
                "style_metavar_separator": "",
                "style_range_append": None,
                "style_options_panel_help_style": "dim italic",
                "style_commands_panel_help_style": "dim italic",
                "style_deprecated": f"{c}",
                "style_options_table_border_style": "dim",
                "style_commands_table_border_style": "dim",
                "style_options_panel_border": "dim",
                "style_commands_panel_border": "dim",
                "style_options_panel_title_style": "not dim",
                "style_commands_panel_title_style": "not dim",
                "style_required_long": f"{c}",
                "style_required_short": f"bold {c}",
                "style_option_help": "default not bold",
                "style_command_help": "default not bold",
                "style_option_default": "dim",
                "style_option_envvar": "dim",
                "style_helptext_first_line": "",
                "style_helptext": "dim",
                "style_header_text": "",
                "style_epilog_text": "",
                "style_footer_text": "",
                "style_options_panel_style": "none",
                "style_commands_panel_style": "none",
                "style_padding_usage": "none",
                "style_padding_helptext": "none",
                "style_padding_epilog": "none",
                "style_padding_errors": "none",
                "style_errors_panel_border": "red",
            },
        )
        for c in ["red", "green", "yellow", "blue", "magenta", "cyan"]
    },
    "mono": RichClickTheme(
        name="mono",
        description="Monochromatic theme with no colors",
        primary_colors=["default", "dim"],
        post_combine_callback=_spaced_delimiters_callback,
        styles={
            "style_option": "",
            "style_option_negative": None,
            "style_argument": "",
            "style_command": "",
            "style_command_aliases": "",
            "style_usage_command": "bold default",
            "style_usage_separator": "",
            "style_switch": "",
            "style_switch_negative": None,
            "style_usage": "bold",
            "style_metavar_append": "dim",
            "style_metavar": "dim",
            "style_metavar_separator": "",
            "style_range_append": None,
            "style_options_panel_help_style": "dim italic",
            "style_commands_panel_help_style": "dim italic",
            "style_deprecated": "bold",
            "style_options_table_border_style": "",
            "style_commands_table_border_style": "",
            "style_options_panel_border": "dim",
            "style_commands_panel_border": "dim",
            "style_options_panel_title_style": "bold not dim",
            "style_commands_panel_title_style": "bold not dim",
            "style_required_long": "bold",
            "style_required_short": "dim bold",
            "style_option_help": "default not bold",
            "style_command_help": "default not bold",
            "style_option_default": "dim",
            "style_option_envvar": "dim",
            "style_helptext_first_line": "",
            "style_helptext": "dim",
            "style_header_text": "",
            "style_epilog_text": "",
            "style_footer_text": "",
            "style_options_panel_style": "none",
            "style_commands_panel_style": "none",
            "style_padding_usage": "none",
            "style_padding_helptext": "none",
            "style_padding_epilog": "none",
            "style_padding_errors": "none",
            "style_errors_panel_border": "dim",
        },
    ),
    "plain": RichClickTheme(
        name="plain",
        description="No style at all",
        primary_colors=["default"],
        post_combine_callback=_spaced_delimiters_callback,
        styles={
            "style_option": "default",
            "style_option_negative": None,
            "style_argument": "default",
            "style_command": "default",
            "style_command_aliases": "default",
            "style_usage_command": "default",
            "style_usage_separator": "default",
            "style_switch": "default",
            "style_switch_negative": None,
            "style_usage": "default",
            "style_metavar_append": "default",
            "style_metavar": "default",
            "style_metavar_separator": "default",
            "style_range_append": None,
            "style_options_panel_help_style": "default",
            "style_commands_panel_help_style": "default",
            "style_deprecated": "default",
            "style_options_table_border_style": "default",
            "style_commands_table_border_style": "default",
            "style_options_panel_border": "default",
            "style_commands_panel_border": "default",
            "style_options_panel_title_style": "default",
            "style_commands_panel_title_style": "default",
            "style_required_long": "default",
            "style_required_short": "default",
            "style_option_help": "default",
            "style_command_help": "default",
            "style_option_default": "default",
            "style_option_envvar": "default",
            "style_helptext_first_line": "default",
            "style_helptext": "default",
            "style_header_text": "default",
            "style_epilog_text": "default",
            "style_footer_text": "default",
            "style_options_panel_style": "none",
            "style_commands_panel_style": "none",
            "style_padding_usage": "none",
            "style_padding_helptext": "none",
            "style_padding_epilog": "none",
            "style_padding_errors": "none",
            "style_errors_panel_border": "default",
        },
    ),
}


def _recolor(base: RichClickTheme, name: str, description: str, colors: dict[str, str]) -> RichClickTheme:
    """Copy a color palette, swapping hex colors using the ``colors`` mapping."""
    mapping = {k.lower(): v for k, v in colors.items()}
    pattern = re.compile(r"#[0-9a-fA-F]{6}")

    def swap(value: Any) -> Any:
        if isinstance(value, str):
            return pattern.sub(lambda m: mapping.get(m.group(0).lower(), m.group(0)), value)
        return value

    return RichClickTheme(
        name=name,
        description=description,
        styles={k: swap(v) for k, v in base.styles.items()},
        primary_colors=[swap(c) for c in base.primary_colors],
        post_combine_callback=base.post_combine_callback,
    )


# Light background versions of palettes that use hex colors designed for dark backgrounds.
# These are used automatically in place of the dark palettes when a light background is detected.
_LIGHT_VARIANTS = {
    # Nord has no official light palette.
    # These keep each Nord color's hue, darkened to at least 4.5:1 contrast on white.
    "nord_light": _recolor(
        COLORS["nord"],
        name="nord_light",
        description="Nord colors darkened for light backgrounds",
        colors={
            "#5e81ac": "#41648f",
            "#81a1c1": "#5079a3",
            "#8fbcbb": "#4c7f7e",
            "#88c0d0": "#3a7e92",
            "#b48ead": "#98658f",
            "#d08770": "#b95b3d",
            "#bf616a": "#bb5660",
            "#a3be8c": "#617e47",
            "#ebcb8b": "#9a6f1a",
            "#434c5e": "#aab4c6",
        },
    ),
    # Dracula's official light palette, Alucard: https://draculatheme.com/spec
    "dracula_light": _recolor(
        COLORS["dracula"],
        name="dracula_light",
        description="Alucard, the official light Dracula palette",
        colors={
            "#FF79C6": "#A3144D",
            "#8BE9FD": "#036A96",
            "#F1FA8C": "#846E15",
            "#BD93F9": "#644AC9",
            "#50FA7B": "#14710A",
            "#44475A": "#6C664B",
            "#6272A4": "#635D97",
            "#FF5555": "#CB3A2A",
            "#FFB86C": "#A34D14",
        },
    ),
}
# Place each light palette right after its dark counterpart.
_colors: dict[str, RichClickTheme] = {}
for _name, _theme in COLORS.items():
    _colors[_name] = _theme
    if _theme.light_variant:
        _colors[_theme.light_variant] = _LIGHT_VARIANTS[_theme.light_variant]
COLORS = _colors
del _colors, _name, _theme

_BOX_STYLES: dict[str, Any] = {
    "style_options_panel_box": "ROUNDED",
    "style_commands_panel_box": "ROUNDED",
    "style_errors_panel_box": "ROUNDED",
    "style_options_table_box": None,
    "style_commands_table_box": None,
    "style_options_table_expand": True,
    "style_commands_table_expand": True,
    "style_options_panel_padding": (0, 1),
    "style_commands_panel_padding": (0, 1),
    "panel_inline_help_in_title": False,
    "panel_inline_help_delimiter": " - ",
    "options_table_column_types": ["required", "opt_long", "opt_short", "metavar", "help"],
    "commands_table_column_types": ["name", "aliases", "help"],
    "options_table_help_sections": ["help", "deprecated", "envvar", "default", "required"],
    "commands_table_help_sections": ["help", "deprecated"],
    "panel_title_string": "{}",
    "deprecated_string": "\\[deprecated]",
    "deprecated_with_reason_string": "\\[deprecated: {}]",
    "default_string": "\\[default: {}]",
    "envvar_string": "\\[env var: {}]",
    "required_long_string": "\\[required]",
    "range_string": "[{}]",
    "append_range_help_string": "\\[range: {}]",
    "required_short_string": "*",
    "padding_header_text": (1, 1, 0, 1),
    "padding_helptext": (0, 1, 1, 1),
    "padding_usage": 1,
    "delimiter_comma": ",",
    "delimiter_slash": "/",
    "panel_title_padding": 1,
    "padding_epilog": 1,
    "padding_footer_text": 1,
    "append_metavars_help_string": "({})",
    # "padding_errors_panel": (0, 0, 1, 0),
    # "padding_errors_suggestion": (0, 1, 0, 1),
    # "padding_errors_epilogue": (0, 1, 1, 1),
}


FORMATS: dict[str, RichClickTheme] = {
    # Classic rich-click format with boxes
    "box": RichClickTheme(
        name="box",
        description="[b](Default)[/b] Original rich-click format with boxes",
        styles=_BOX_STYLES,
    ),
    # The default box format, with sharp corners
    "square": RichClickTheme(
        name="square",
        description="Original rich-click format with square boxes",
        styles={
            **_BOX_STYLES,
            "style_options_panel_box": "SQUARE",
            "style_commands_panel_box": "SQUARE",
            "style_errors_panel_box": "SQUARE",
        },
    ),
    # Great balance of compactness, legibility, and style
    "nu": RichClickTheme(
        name="nu",
        description="Great balance of compactness, legibility, and style",
        post_combine_callback=_not_dim_title_callback,
        styles={
            "style_options_panel_box": "HORIZONTALS_DOUBLE_TOP",
            "style_commands_panel_box": "HORIZONTALS_DOUBLE_TOP",
            "style_errors_panel_box": "ROUNDED",
            "style_options_table_box": None,
            "style_commands_table_box": None,
            "style_options_table_expand": False,
            "style_commands_table_expand": False,
            "panel_title_string": "{}",
            "style_options_panel_padding": 0,
            "style_commands_panel_padding": 0,
            "deprecated_string": "(Deprecated)",
            "deprecated_with_reason_string": "(Deprecated: {})",
            "default_string": "(Default: {})",
            "envvar_string": "(Env: {})",
            "required_long_string": "(Required)",
            "range_string": "{}",
            "append_range_help_string": "(Range: {})",
            "append_metavars_help_string": "\\[{}]",
            "required_short_string": "#",
            "padding_header_text": (0, 1, 1, 1),
            "padding_helptext": (0, 1, 1, 1),
            "padding_usage": (0, 1, 1, 1),
            "delimiter_comma": ",",
            "delimiter_slash": "/",
            "panel_title_padding": 1,
            "options_table_column_types": ["required", "opt_long", "opt_short", "help"],
            "commands_table_column_types": ["name", "aliases", "help"],
            "options_table_help_sections": ["help", "metavar", "required", "default", "envvar", "deprecated"],
            "commands_table_help_sections": ["help", "deprecated"],
            "panel_inline_help_delimiter": " - ",
            "padding_epilog": (0, 0, 1, 1),
            "padding_footer_text": (0, 0, 1, 1),
            "panel_inline_help_in_title": False,
        },
    ),
    # Simple, classic, no-fuss CLI format
    "slim": RichClickTheme(
        name="slim",
        description="Simple, classic, no-fuss CLI format",
        post_combine_callback=_not_dim_title_callback,
        styles={
            "style_options_panel_box": "BLANK",
            "style_commands_panel_box": "BLANK",
            "style_errors_panel_box": "ROUNDED",
            "style_options_table_box": None,
            "style_commands_table_box": None,
            "style_options_table_expand": False,
            "style_commands_table_expand": False,
            "panel_title_string": "{}:",
            "style_options_panel_padding": (0, 0, 0, 1),
            "style_commands_panel_padding": (0, 0, 0, 1),
            "padding_header_text": (0, 0, 1, 0),
            "padding_helptext": (0, 0, 1, 0),
            "padding_usage": (0, 0, 1, 0),
            "padding_epilog": (0, 0, 1, 0),
            "padding_footer_text": (0, 0, 1, 0),
            "options_table_column_types": ["opt_short", "opt_long_metavar", "help"],
            "commands_table_column_types": ["name_with_aliases", "help"],
            "options_table_help_sections": ["help", "range", "required", "default", "envvar", "deprecated"],
            "commands_table_help_sections": ["help", "deprecated"],
            "append_metavars_help_string": "<{}>",
            "envvar_string": "\\[env: {}=]",
            "delimiter_comma": ", ",
            "delimiter_slash": "/",
            "panel_title_padding": 0,
            "panel_inline_help_in_title": True,
            "panel_inline_help_delimiter": " ",
            "deprecated_string": "\\[deprecated]",
            "deprecated_with_reason_string": "\\[deprecated: {}]",
            "default_string": "\\[default={}]",
            "required_long_string": "\\[required]",
            "range_string": "{}",
            "append_range_help_string": "\\[range: {}]",
            "required_short_string": "*",
        },
    ),
    # Beautiful modern look
    "modern": RichClickTheme(
        name="modern",
        description="Beautiful modern look",
        post_combine_callback=_not_dim_title_callback,
        styles={
            "style_options_panel_box": None,
            "style_commands_panel_box": None,
            "style_errors_panel_box": "ROUNDED",
            "style_options_table_box": "HORIZONTALS_TOP",
            "style_commands_table_box": "HORIZONTALS_TOP",
            "style_options_table_expand": True,
            "style_commands_table_expand": True,
            "panel_title_string": "{}",
            "style_options_panel_padding": 0,
            "style_commands_panel_padding": 0,
            "padding_header_text": (1, 2, 0, 3),
            "padding_helptext": (0, 2, 1, 2),
            "padding_usage": (1, 2, 1, 2),
            "options_table_column_types": ["opt_short", "opt_long", "metavar", "help"],
            "commands_table_column_types": ["name", "aliases", "help"],
            "options_table_help_sections": ["required", "help", "envvar", "default", "deprecated"],
            "commands_table_help_sections": ["help", "deprecated"],
            "deprecated_string": "\\[deprecated]",
            "deprecated_with_reason_string": "\\[deprecated: {}]",
            "envvar_string": "\\[env={}]",
            "default_string": "\\[default={}]",
            "append_metavars_help_string": "\\[{}]",
            "panel_inline_help_in_title": True,
            "delimiter_comma": ", ",
            "delimiter_slash": " / ",
            "panel_title_padding": 0,
            "required_short_string": "*",
            "panel_inline_help_delimiter": " - ",
            "required_long_string": "\\[required]",
            "range_string": "[{}]",
            "append_range_help_string": "\\[{}]",
            "padding_epilog": (0, 2, 1, 2),
            "padding_footer_text": (0, 2, 1, 2),
        },
    ),
    # Spacious with sharp corners
    "robo": RichClickTheme(
        name="robo",
        description="Spacious with sharp corners",
        post_combine_callback=_not_dim_title_callback,
        styles={
            "style_options_panel_box": "SQUARE",
            "style_commands_panel_box": "SQUARE",
            "style_errors_panel_box": "SQUARE",
            "style_options_table_box": None,
            "style_commands_table_box": None,
            "style_options_panel_padding": (1, 2),
            "style_commands_panel_padding": (1, 2),
            "style_options_table_expand": True,
            "style_commands_table_expand": True,
            "padding_header_text": (0, 0, 1, 0),
            "padding_helptext": (0, 0, 1, 0),
            "padding_usage": (0, 0, 1, 0),
            "deprecated_string": "❮[b]DEPRECATED[/b]❯",
            "deprecated_with_reason_string": "❮[b]DEPRECATED:[/b] {}❯",
            "envvar_string": "❮[b]ENV:[/b] {}=❯",
            "default_string": "❮[b]DEFAULT:[/b] {}❯",
            "append_metavars_help_string": "❮{}❯",
            "required_short_string": "*",
            "required_long_string": "❮[b]REQUIRED[/b]❯",
            "range_string": "{}",
            "append_range_help_string": "❮[b]RANGE[/b]: {}❯",
            "options_table_column_types": ["opt_primary", "opt_secondary", "metavar", "help"],
            "commands_table_column_types": ["name", "aliases", "help"],
            "options_table_help_sections": ["required", "help", "deprecated", "default", "envvar"],
            "commands_table_help_sections": ["help", "deprecated"],
            "delimiter_comma": ", ",
            "delimiter_slash": " / ",
            "panel_title_padding": 2,
            "panel_title_string": "{}",
            "panel_inline_help_delimiter": " - ",
            "padding_epilog": (0, 0, 1, 0),
            "padding_footer_text": (0, 0, 1, 0),
            "panel_inline_help_in_title": False,
        },
    ),
}

_THEME_CACHE: dict[str, RichClickTheme] = {}


class RichClickThemeNotFound(KeyError):
    """Raise when a theme is not found."""


def parse_background_theme(theme: str) -> dict[str, str] | None:
    """
    Parse a light/dark theme pair such as ``"dark:nord-modern,light:solarized-modern"``.

    Returns None if the string is not a theme pair.
    """
    if ":" not in theme:
        return None
    pair: dict[str, str] = {}
    for part in theme.split(","):
        key, sep, value = part.partition(":")
        key, value = key.strip(), value.strip()
        if not sep or key not in ("dark", "light") or not value or key in pair:
            raise RichClickThemeNotFound(
                f"RichClickTheme '{theme}' not found."
                " Light/dark theme pairs must look like 'dark:<theme>,light:<theme>'"
            )
        pair[key] = value
    if len(pair) != 2:
        raise RichClickThemeNotFound(
            f"RichClickTheme '{theme}' not found. Light/dark theme pairs must set both 'dark:' and 'light:'"
        )
    return pair


def _light_variant(theme: str) -> str | None:
    """Get the light version of a theme name, if its color palette has one."""
    clr, sep, fmt = theme.partition("-")
    palette = COLORS.get(clr)
    if palette is None or palette.light_variant is None or (sep and fmt not in FORMATS):
        return None
    return palette.light_variant + sep + fmt


def theme_needs_background(theme: str) -> bool:
    """Whether picking this theme depends on the terminal background."""
    return ":" in theme or _light_variant(theme) is not None


def resolve_background_theme(theme: str) -> str:
    """
    Pick a theme name based on the terminal background.

    - Light/dark pairs (``"dark:nord-modern,light:solarized-modern"``) resolve to one of the two themes.
      If the background cannot be detected, the first theme listed is used.
    - Palettes with a light variant (e.g. ``nord``) switch to it (``nord_light``) on light backgrounds.
    - All other theme names are returned unchanged.
    """
    pair = parse_background_theme(theme)
    light = None if pair else _light_variant(theme)
    if pair is None and light is None:
        return theme
    # Imported here so that the detection code is only loaded when it is needed.
    from rich_click.terminal_background import detect_background

    background = detect_background()
    if pair is not None:
        return pair[background] if background else next(iter(pair.values()))
    return light if background == "light" and light else theme


def get_theme(theme: str, raise_key_error: bool = True, resolve_background: bool = True) -> RichClickTheme:
    """
    Get the theme based on the string name.

    If ``resolve_background`` is true, the terminal background may be detected
    to pick from a light/dark pair, or to use a palette's light variant.
    """
    clr: str | None = None
    fmt: str | None = None

    if theme == "random":
        import random

        clr = random.choice(list(COLORS.keys()))
        fmt = random.choice(list(FORMATS.keys()))

        rich_click_theme = _THEME_CACHE[f"{clr}-{fmt}"] = COLORS[clr] + FORMATS[fmt]
        return rich_click_theme
    if resolve_background and theme_needs_background(theme):
        try:
            resolved = resolve_background_theme(theme)
        except RichClickThemeNotFound:
            # Malformed pair: raise, or fall through to the warning below.
            if raise_key_error:
                raise
        else:
            # Themes picked from a pair are used as-is, so e.g. 'dark:nord,light:nord' never switches palettes.
            return get_theme(resolved, raise_key_error=raise_key_error, resolve_background=False)
    if theme in _THEME_CACHE:
        return _THEME_CACHE[theme]
    try:
        if "-" not in theme:
            if theme in COLORS:
                rich_click_theme = _THEME_CACHE[theme] = COLORS[theme] + FORMATS["box"]
                return rich_click_theme
            elif theme in FORMATS:
                rich_click_theme = _THEME_CACHE[theme] = COLORS["default"] + FORMATS[theme]
                return rich_click_theme
            else:
                raise RichClickThemeNotFound(f"RichClickTheme '{theme}' not found")
        clr, fmt, *_ = theme.split("-")
        if _:
            raise RichClickThemeNotFound(f"RichClickTheme '{theme}' not found")
        if clr in COLORS and fmt in FORMATS:
            rich_click_theme = _THEME_CACHE[theme] = COLORS[clr] + FORMATS[fmt]
            return rich_click_theme
        else:
            raise RichClickThemeNotFound(f"RichClickTheme '{theme}' not found")
    except KeyError:
        if raise_key_error:
            raise
        import warnings

        warnings.warn(
            f"RichClickTheme '{theme}' not found.",
            UserWarning,
            stacklevel=2,
        )
        if clr and clr in COLORS:
            return COLORS[clr] + FORMATS["box"]
        elif fmt and fmt in FORMATS:
            return COLORS["default"] + FORMATS[fmt]
        return COLORS["default"] + FORMATS["box"]
