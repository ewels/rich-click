import sys

import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    return load_command_from_module("tests.help.fixtures.rst")


def test_rst_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    pytest.importorskip("rich_rst")
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things [1].                                                           \n\
                                                                                                    \n\
 This is a minimal example based on documentation from the click package.                           \n\
                                                                                                    \n\
  • You can try using --help at the top level                                                       \n\
  • Also for specific group subcommands.                                                            \n\
                                                                                                    \n\
 Note: Admonitions are rendered compactly.                                                          \n\
                                                                                                    \n\
 Example:                                                                                           \n\
 ┌────────────────────────────────────── console (default) ───────────────────────────────────────┐ \n\
 │ $ cli --all --debug                                                                            │ \n\
 └────────────────────────────────────────────────────────────────────────────────────────────────┘ \n\
 Click no-rewrap                                                                                    \n\
 lines stay apart                                                                                   \n\
 ┌──────────────────────────────────────────── Footer ────────────────────────────────────────────┐ \n\
 │ 1: Footnotes resolve across paragraphs.                                                        │ \n\
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


def test_rst_edge_cases(cli_runner: CliRunner) -> None:
    pytest.importorskip("rich_rst")

    @rich_click.group(context_settings={"help_option_names": ["-h"]})
    @rich_click.rich_config(help_config={"text_markup": "rst", "text_kwargs": {"style": "italic"}})
    def cli() -> None:
        """
        Example usage::

            $ cli run

        \b
        Commands:
          foo     Do the foo
        After the block.
        """

    @cli.command()
    @rich_click.option("--opt", help="\b\nline a\n  line b\n\nAfter.")
    def nowrap(opt: str) -> None:
        """
        \b
        First line
        Second line

        Rest.
        """

    @cli.command()
    def refs() -> None:
        """
        Uses a footnote [#f1]_ and a `link`_.

        .. [#f1] Footnote.
        .. _link: https://example.com
        """

    result = cli_runner.invoke(cli, "-h")
    assert result.exit_code == 0
    assert "│ nowrap  First line   " in result.stdout
    assert "│         Second line   " in result.stdout
    assert "│ refs    Uses a footnote and a link.   " in result.stdout
    assert "\n Commands:   " in result.stdout and "\n   foo     Do the foo   " in result.stdout

    result = cli_runner.invoke(cli, ["nowrap", "-h"])
    assert " line a   " in result.stdout
    assert "   line b   " in result.stdout
    assert " After.   " in result.stdout


def test_rst_styles() -> None:
    pytest.importorskip("rich_rst")
    from rich.console import Console

    from rich_click._rst import RichClickRST

    console = Console(force_terminal=True, color_system="standard", width=40)
    with console.capture() as capture:
        console.print(RichClickRST("Example::\n\n    code\n\nMore *here*.\n\n- item", "red", "green bold"))
    out = capture.get()
    assert "\x1b[1;32mExample:" in out
    assert "\x1b[31;3mhere" in out or "\x1b[3;31mhere" in out
    assert "\x1b[31mMore " in out
    assert "\x1b[31mitem" in out
