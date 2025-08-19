# ruff: noqa: D101,D103,D401,E501
import sys
from inspect import cleandoc
from pathlib import Path

import pytest

from tests.conftest import WriteScript, run_as_subprocess


@pytest.fixture
def simple_cli(mock_script_writer: WriteScript) -> Path:
    return mock_script_writer(
        """
        import sys
        import rich_click as click

        @click.command()
        def cli():
            rich_detected = False
            rich_click_detected = False
            for k in sys.modules.keys():
                if k.startswith("rich_click."):
                    rich_click_detected = True
                if k.startswith("rich."):
                    rich_detected = True
            print(f"rich_detected={rich_detected}")
            print(f"rich_click_detected={rich_click_detected}")

        if __name__ == "__main__":
            cli()
        """,
        module_name="mymodule.py",
    )


def test_no_rich_imports_during_execution(simple_cli: Path) -> None:
    # During execution, rich modules should never be imported via rich_click.
    res = run_as_subprocess(
        [
            sys.executable,
            str(simple_cli / "mymodule.py"),
        ]
    )
    assert cleandoc(res.stdout.decode()) == cleandoc(
        """
        rich_detected=False
        rich_click_detected=True
        """
    )


def test_no_rich_imports_during_execution_rich_click_cli(simple_cli: Path) -> None:
    # During execution, rich modules should never be imported via rich_click.
    res = run_as_subprocess([sys.executable, "-m", "rich_click", "mymodule:cli"])
    assert cleandoc(res.stdout.decode()) == cleandoc(
        """
        rich_detected=False
        rich_click_detected=True
        """
    )
