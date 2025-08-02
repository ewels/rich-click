import importlib
import os
import re
import subprocess
import sys
from importlib import reload
from inspect import cleandoc
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol, cast

import click
import pytest
from click.testing import CliRunner, Result
from pytest import MonkeyPatch

import rich_click.rich_click as rc
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_82
from rich_click.rich_command import RichCommand
from rich_click.rich_context import RichContext


class WriteScript(Protocol):
    def __call__(self, script: str, module_name: str = "mymodule.py") -> Path:
        """Write a script to a directory."""
        ...


def run_as_subprocess(args: List[str], env: Optional[Dict[str, str]] = None) -> "subprocess.CompletedProcess[bytes]":
    # Throughout most of this test module,
    # to avoid side effects and to test and uncover potential issues with lazy-loading,
    # we need to use subprocess.run() instead of cli_runner.invoke().

    _env = {**os.environ, "TERMINAL_WIDTH": "100", "FORCE_COLOR": "False"}
    _env.update(env or {})
    res = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=_env,
    )
    return res


@pytest.fixture
def mock_script_writer(tmp_path: Path, monkeypatch: MonkeyPatch) -> WriteScript:
    def write_script(script: str, module_name: str = "mymodule.py") -> Path:
        path = tmp_path / "scripts"
        path.mkdir()
        py_script = path / module_name
        py_script.write_text(cleandoc(script))

        monkeypatch.setattr(sys, "path", [path.as_posix(), *sys.path.copy()])
        monkeypatch.setitem(os.environ, "PYTHONPATH", path.as_posix())
        monkeypatch.setattr(RichContext, "command_path", "mymodule")
        return path

    return write_script


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
