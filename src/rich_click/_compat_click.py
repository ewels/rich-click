from distutils.version import LooseVersion

import click

CLICK_IS_BEFORE_VERSION_8X = LooseVersion(click.__version__) < LooseVersion("8.0.0")
CLICK_IS_VERSION_80 = LooseVersion("8.1.0") > LooseVersion(click.__version__) >= LooseVersion("8.0.0")
