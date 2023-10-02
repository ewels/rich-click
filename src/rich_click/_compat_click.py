import click
from packaging import version


CLICK_IS_BEFORE_VERSION_8X = version.parse(click.__version__) < version.parse("8.0.0")
CLICK_IS_VERSION_80 = version.parse("8.1.0") > version.parse(click.__version__) >= version.parse("8.0.0")


if CLICK_IS_BEFORE_VERSION_8X:
    import warnings
    warnings.warn(
        "rich-click support for click 7.x is deprecated and will be removed soon."
        " Please upgrade click to a newer version.",
        DeprecationWarning,
    )
