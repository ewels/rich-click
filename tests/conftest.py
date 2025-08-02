import importlib
import re
from importlib import reload
from typing import Any, Protocol, cast

import click
import pytest
from click.testing import CliRunner, Result

import rich_click.rich_click as rc
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_82
from rich_click.rich_command import RichCommand


re_link_ids = re.compile(r"id=[\d.\-]*?;.*?\x1b")


def replace_link_ids(render: str) -> str:
    """
    Link IDs have a random ID and system path which is a problem for
    reproducible tests.

    From: https://github.com/Textualize/rich/blob/master/tests/render.py
    """
    return re_link_ids.sub("id=0;foo\x1b", render)


@pytest.fixture(autouse=True)
def default_config() -> None:
    # Isolate rich_click global config module for each test:
    reload(rc)

    # Default config settings
    # from https://github.com/Textualize/rich/blob/master/tests/render.py
    rc.WIDTH = 100
    rc.COLOR_SYSTEM = None
    rc.FORCE_TERMINAL = True


def load_command_from_module(namespace: str, command_attr: str = "cli") -> RichCommand:
    module = importlib.import_module(namespace)
    reload(module)
    return cast(RichCommand, getattr(module, command_attr))


class InvokeCli(Protocol):
    def __call__(self, cmd: click.Command, *args: Any, **kwargs: Any) -> Result:
        """
        Invoke click command.

        Small convenience fixture to allow invoking a click Command
        without standalone mode.
        """
        ...


@pytest.fixture
def cli_runner() -> CliRunner:
    if CLICK_IS_BEFORE_VERSION_82:
        return CliRunner(mix_stderr=False)  # type: ignore[call-arg]
    else:
        return CliRunner()
