# ruff: noqa: D101,D103,D401,E501
import sys
from inspect import cleandoc
from pathlib import Path

import pytest

from tests.conftest import WriteScript, run_as_subprocess


@pytest.fixture
def check_imports_cli(mock_script_writer: WriteScript) -> Path:
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


@pytest.fixture
def check_imports_render_cli(mock_script_writer: WriteScript) -> Path:
    return mock_script_writer(
        """
        import sys
        import rich_click as click

        @click.command()
        @click.pass_context
        def cli(ctx):
            ctx.get_help()
            rich_detected = False
            rich_click_detected = False
            markdown_it_detected = False
            for k in sys.modules.keys():
                if k.startswith("rich_click."):
                    rich_click_detected = True
                if k.startswith("rich."):
                    rich_detected = True
                if k.startswith("markdown_it."):
                    markdown_it_detected = True
            print(f"rich_detected={rich_detected}")
            print(f"rich_click_detected={rich_click_detected}")
            print(f"markdown_it_detected={markdown_it_detected}")

        if __name__ == "__main__":
            cli()
        """,
        module_name="mymodule.py",
    )


def test_no_rich_imports_during_execution(check_imports_cli: Path) -> None:
    # During execution, rich modules should never be imported via rich_click.
    res = run_as_subprocess(
        [
            sys.executable,
            str(check_imports_cli / "mymodule.py"),
        ]
    )
    assert cleandoc(res.stdout.decode()) == cleandoc(
        """
        rich_detected=False
        rich_click_detected=True
        """
    )


def test_no_rich_imports_during_execution_rich_click_cli(check_imports_cli: Path) -> None:
    # During execution, rich modules should never be imported via rich_click.
    res = run_as_subprocess([sys.executable, "-m", "rich_click", "mymodule:cli"])
    assert cleandoc(res.stdout.decode()) == cleandoc(
        """
        rich_detected=False
        rich_click_detected=True
        """
    )


def test_no_markdown_imports_during_help_rich_click_cli(check_imports_render_cli: Path) -> None:
    # During help rendering, markdown_it should not be imported unless required.
    res = run_as_subprocess([sys.executable, "-m", "rich_click", "mymodule:cli"])
    assert cleandoc(res.stdout.decode()) == cleandoc(
        """
        rich_detected=True
        rich_click_detected=True
        markdown_it_detected=False
        """
    )
