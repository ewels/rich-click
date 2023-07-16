from distutils.version import LooseVersion

import click

CLICK_IS_BEFORE_VERSION_8X = LooseVersion(click.__version__) < LooseVersion("8.0.0")
