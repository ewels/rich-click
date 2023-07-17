import warnings

import click

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=DeprecationWarning)
    # TODO: Remove use of distutils.version.LooseVersion (distutils.version is deprecated).
    from distutils.version import LooseVersion

    CLICK_IS_BEFORE_VERSION_8X = LooseVersion(click.__version__) < LooseVersion("8.0.0")

if CLICK_IS_BEFORE_VERSION_8X:
    warnings.warn(
        "rich-click support for click 7.x is deprecated and will be removed soon."
        " Please upgrade click to a newer version.",
        DeprecationWarning,
    )
