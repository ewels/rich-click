# ruff: noqa: D101,D103,D401,E501
import builtins
import importlib
from pathlib import Path
from typing import Any, List

import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import WriteScript


# These tests are to assert various optimizations.
# There are certain imports that significantly slow down execution:
#
# - Importing anything from `rich` during execution is unnecessary and should not occur.
# - Importing `markdown_it` except when necessary significantly slows down help text rendering.
# - Calling `importlib.metadata.version()` is slow. Click has made a decision to deprecate `__version__`,
#   and so the latest versions of click call `importlib.metadata.version()` when you access
#   `click.__version__`, which slows things down. During execution, we want to avoid accessing
#   `click.__version__`. A slightly lazy albeit acceptable way to assert that
#   `importlib.metadata.version()` is never called is to just assert that `importlib.metadata`
#   is not imported at all. During --help, however, we accept that this call will be made.


@pytest.fixture
def check_imports_cli(mock_script_writer: WriteScript) -> Path:
    return mock_script_writer(
        """
        import rich_click as click

        @click.command()
        def cli():
            print("Hello, world!")

        if __name__ == "__main__":
            cli()
        """,
        module_name="my_script.py",
    )


@pytest.fixture
def recorded_imports(monkeypatch: pytest.MonkeyPatch) -> List[str]:
    modules: List[str] = []

    _import = builtins.__import__

    def noisy_import(name: str, *args: Any, **kwargs: Any) -> Any:
        modules.append(name)
        return _import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", noisy_import)
    return modules


def test_imports_during_execution(recorded_imports: List[str], cli_runner: CliRunner) -> None:
    importlib.reload(rich_click)

    @rich_click.command()
    def cli() -> None:
        print("Hello, world!")

    res = cli_runner.invoke(cli)
    assert res.exit_code == 0
    assert res.stdout == "Hello, world!\n"

    assert any(m.startswith("click.") or m == "click" for m in recorded_imports)
    assert not any(m.startswith("rich.") or m == "rich" for m in recorded_imports)
    assert not any(m.startswith("markdown_it.") or m == "markdown_it" for m in recorded_imports)
    assert not any(m.startswith("importlib.") or m == "importlib" for m in recorded_imports)


def test_imports_during_help(recorded_imports: List[str], cli_runner: CliRunner) -> None:
    importlib.reload(rich_click)

    @rich_click.command()
    def cli() -> None:
        print("Hello, world!")

    res = cli_runner.invoke(cli, "--help")
    assert res.exit_code == 0
    assert res.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )

    assert any(m.startswith("click.") or m == "click" for m in recorded_imports)
    assert any(m.startswith("rich.") or m == "rich" for m in recorded_imports)
    assert not any(m.startswith("markdown_it.") or m == "markdown_it" for m in recorded_imports)


def test_imports_during_execution_rich_click_cli(
    recorded_imports: List[str],
    cli_runner: CliRunner,
    check_imports_cli: Path,
) -> None:
    importlib.reload(rich_click)
    from rich_click.cli import main

    res = cli_runner.invoke(main, str(check_imports_cli / "my_script.py"))
    assert res.exit_code == 0
    assert res.stdout == "Hello, world!\n"

    assert any(m.startswith("click.") or m == "click" for m in recorded_imports)
    assert not any(m.startswith("rich.") or m == "rich" for m in recorded_imports)
    assert not any(m.startswith("markdown_it.") or m == "markdown_it" for m in recorded_imports)


def test_imports_during_help_rich_click_cli(
    recorded_imports: List[str],
    cli_runner: CliRunner,
    check_imports_cli: Path,
) -> None:
    importlib.reload(rich_click)
    from rich_click.cli import main

    res = cli_runner.invoke(main, f"{check_imports_cli / 'my_script.py'} --help")
    assert res.exit_code == 0
    assert res.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: mymodule [OPTIONS]                                                                          \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )

    assert any(m.startswith("click.") or m == "click" for m in recorded_imports)
    assert any(m.startswith("rich.") or m == "rich" for m in recorded_imports)
    assert not any(m.startswith("markdown_it.") or m == "markdown_it" for m in recorded_imports)
