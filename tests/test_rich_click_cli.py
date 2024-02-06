# ruff: noqa: D101,D103,D401
import sys
from inspect import cleandoc
from pathlib import Path

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

        @click.command
        def cli():
            """My help text"""
            ...

        cli()
        '''
    )
    py_script = path / "mymodule.py"
    py_script.write_text(f)

    monkeypatch.setattr(sys, "path", [path.as_posix(), *sys.path.copy()])
    monkeypatch.setattr(RichContext, "command_path", "mymodule")

    return


def test_simple_rich_click_cli(simple_script: None, cli_runner: CliRunner, assert_str: AssertStr) -> None:
    res = cli_runner.invoke(main, ["mymodule:cli", "--help"])

    expected_output = """
 Usage: mymodule [OPTIONS]

 My help text

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""

    assert_str(actual=res.stdout, expectation=expected_output)


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
