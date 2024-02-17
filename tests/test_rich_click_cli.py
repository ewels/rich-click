# ruff: noqa: D101,D103,D401
import sys
from inspect import cleandoc
from pathlib import Path
from typing import List

import pytest
import rich_click.rich_click as rc
from click.testing import CliRunner
from pytest import MonkeyPatch
from rich_click.cli import main
from rich_click.rich_context import RichContext

from tests.conftest import AssertStr


@pytest.fixture(autouse=True)
def default_config(initialize_rich_click: None) -> None:
    # Default config settings from https://github.com/Textualize/rich/blob/master/tests/render.py
    rc.WIDTH = 100
    rc.COLOR_SYSTEM = None
    rc.FORCE_TERMINAL = True


@pytest.fixture
def simple_script(tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    path = tmp_path / "scripts"
    path.mkdir()
    f = cleandoc(
        '''
        import click

        # Test if robust to subclassing
        class CustomClickCommand(click.Command):
            pass

        @click.command(cls=CustomClickCommand)
        def cli():
            """My help text"""
            print('Hello, world!')

        cli()
        '''
    )
    py_script = path / "mymodule.py"
    py_script.write_text(f)

    monkeypatch.setattr(sys, "path", [path.as_posix(), *sys.path.copy()])
    monkeypatch.setattr(RichContext, "command_path", "mymodule")

    return


@pytest.mark.parametrize(
    "command",
    [
        ["mymodule:cli", "--help"],
        ["--", "mymodule:cli", "--help"],
    ],
)
def test_simple_rich_click_cli(
    simple_script: None, cli_runner: CliRunner, assert_str: AssertStr, command: List[str]
) -> None:
    res = cli_runner.invoke(main, command)

    expected_output = """
 Usage: mymodule [OPTIONS]

 My help text

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""

    assert_str(actual=res.stdout, expectation=expected_output)


@pytest.mark.parametrize(
    "command",
    [
        ["mymodule:cli"],
        ["--", "mymodule:cli"],
        ["mymodule:cli", "--"],
    ],
)
def test_simple_rich_click_cli_execute_command(
    simple_script: None, cli_runner: CliRunner, assert_str: AssertStr, command: List[str]
) -> None:
    res = cli_runner.invoke(main, command)

    assert res.stdout == "Hello, world!\n"


def test_custom_config_rich_click_cli(simple_script: None, cli_runner: CliRunner, assert_str: AssertStr) -> None:
    res = cli_runner.invoke(main, ["--rich-config", '{"options_panel_title": "Custom Name"}', "mymodule:cli", "--help"])

    expected_output = """
 Usage: mymodule [OPTIONS]

 My help text

╭─ Custom Name ────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""

    assert_str(actual=res.stdout, expectation=expected_output)
