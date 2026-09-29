import sys

import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


pytest.importorskip("rich_rst")


@pytest.fixture
def cli() -> rich_click.RichCommand:
    return load_command_from_module("tests.help.fixtures.rst")


def test_rst_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the click package.                           \n\
                                                                                                    \n\
  • You can try using --help at the top level                                                       \n\
  • Also for specific group subcommands.                                                            \n\
                                                                                                    \n\
 Note: Admonitions are rendered compactly.                                                          \n\
                                                                                                    \n\
 Example:                                                                                           \n\
 ┌─────────────────────────────────────── python (default) ───────────────────────────────────────┐ \n\
 │ $ cli --all --debug                                                                            │ \n\
 └────────────────────────────────────────────────────────────────────────────────────────────────┘ \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --input  PATH  Input file. [default: a custom default]                                           │
│ --type   TEXT  Type of file to sync                                                              │
│                [default: files]                                                                  │
│ --all          Sync                                                                              │
│                                                                                                  │
│                 1. all                                                                           │
│                 2. the                                                                           │
│                 3. things?                                                                       │
│ --debug        Enable debug mode                                                                 │
│ --help         Show this message and exit.                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
 See the rich-click docs for more.                                                                  \n\
                                                                                                    \n\
  • Epilog lists                                                                                    \n\
  • stay intact                                                                                     \n\
                                                                                                    \n\
""")
    assert result.stderr == snapshot("")


def test_rst_missing_dependency(
    cli_runner: CliRunner, cli: rich_click.RichCommand, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setitem(sys.modules, "rich_rst", None)
    monkeypatch.delitem(sys.modules, "rich_click._rst", raising=False)
    result = cli_runner.invoke(cli, "--help")
    assert isinstance(result.exception, ImportError)
    assert "pip install 'rich-click[rst]'" in str(result.exception)
