from typing import Generator

import pytest

from rich_click.rich_click_theme import COLORS, FORMATS, RichClickThemeNotFound, get_theme
from rich_click.rich_help_configuration import FromTheme, RichHelpConfiguration


def all_themes() -> Generator[str, None, None]:
    for c in COLORS:
        yield c
        for f in FORMATS:
            yield f
            yield f"{c}-{f}"


def test_all_themes_available() -> None:
    for theme in all_themes():
        get_theme(theme)
    assert True


def test_bad_theme_raises_err() -> None:
    with pytest.raises(RichClickThemeNotFound):
        get_theme("this-does-not-exist")


def test_all_themes_have_from_theme_objs_replaced_on_resolution() -> None:
    def _no_from_themes(config: RichHelpConfiguration) -> bool:
        for k in config.__dataclass_fields__:
            v = getattr(config, k)
            assert not isinstance(v, FromTheme)
        return True

    for theme in all_themes():
        cfg = RichHelpConfiguration(theme=theme)
        assert _no_from_themes(cfg)
