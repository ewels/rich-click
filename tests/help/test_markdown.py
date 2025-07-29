from importlib.metadata import version

import packaging.version
import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
import rich_click.rich_click as rc
from tests.conftest import load_command_from_module


rich_version = packaging.version.parse(version("rich"))


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.markdown")
    return cmd


@pytest.mark.skipif(rich_version >= packaging.version.parse("13.0.0"), reason="Rich <13 has different table styles")
def test_markdown_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the click package.                           \n\
                                                                                                    \n\
 ▌ Remember:                                                                                        \n\
 ▌  • You can try using --help at the top level                                                     \n\
 ▌  • Also for specific group subcommands.                                                          \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --input    PATH  Input file. [default: a custom default]                                         │
│ --type     TEXT  Type of file to sync                                                            │
│                  [default: files]                                                                │
│ --all            Sync                                                                            │
│                                                                                                  │
│                   1 all                                                                          │
│                   2 the                                                                          │
│                   3 things?                                                                      │
│ --debug          ╔═════════════════════════════════════════════════════════════════════════════╗ │
│                  ║                              Enable debug mode                              ║ │
│                  ╚═════════════════════════════════════════════════════════════════════════════╝ │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_markdown_help_turn_off_markdown(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.USE_MARKDOWN = False
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does _**all the things**_.                                                         \n\
 This is a `minimal example` based on documentation from the [_click_                               \n\
 package](https://click.palletsprojects.com/).                                                      \n\
 > Remember: >  - You can try using --help at the top level >  - Also for specific group            \n\
 subcommands.                                                                                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --input    PATH  Input **file**. _[default: a custom default]_                                   │
│ --type     TEXT  Type of file to sync [default: files]                                           │
│ --all            Sync 1. all 2. the 3. things?                                                   │
│ --debug          # Enable `debug mode`                                                           │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


@pytest.mark.skipif(rich_version >= packaging.version.parse("13.0.0"), reason="Rich <13 has different table styles")
def test_markdown_help_text_markup_field(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    # USE_MARKDOWN is silently deprecated, and we prefer `text_markup` mode.
    #
    # The previous test ensures that the global works properly when disabled.
    #
    # This test turns off the global, and wraps the code in a help config
    # with `{"text_markup": "markdown"}`.
    rc.USE_MARKDOWN = False
    cli = rich_click.rich_config(help_config={"text_markup": "markdown"})(cli)

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the click package.                           \n\
                                                                                                    \n\
 ▌ Remember:                                                                                        \n\
 ▌  • You can try using --help at the top level                                                     \n\
 ▌  • Also for specific group subcommands.                                                          \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --input    PATH  Input file. [default: a custom default]                                         │
│ --type     TEXT  Type of file to sync                                                            │
│                  [default: files]                                                                │
│ --all            Sync                                                                            │
│                                                                                                  │
│                   1 all                                                                          │
│                   2 the                                                                          │
│                   3 things?                                                                      │
│ --debug          ╔═════════════════════════════════════════════════════════════════════════════╗ │
│                  ║                              Enable debug mode                              ║ │
│                  ╚═════════════════════════════════════════════════════════════════════════════╝ │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


@pytest.mark.skipif(rich_version < packaging.version.parse("13.0.0"), reason="Rich <13 has different table styles")
def test_markdown_help_rich_12(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the click package.                           \n\
                                                                                                    \n\
 ▌ Remember:                                                                                        \n\
 ▌  • You can try using --help at the top level                                                     \n\
 ▌  • Also for specific group subcommands.                                                          \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --input    PATH  Input file. [default: a custom default]                                         │
│ --type     TEXT  Type of file to sync                                                            │
│                  [default: files]                                                                │
│ --all            Sync                                                                            │
│                                                                                                  │
│                   1 all                                                                          │
│                   2 the                                                                          │
│                   3 things?                                                                      │
│ --debug          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│                  ┃                              Enable debug mode                              ┃ │
│                  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


@pytest.mark.skipif(rich_version < packaging.version.parse("13.0.0"), reason="Rich <13 has different table styles")
def test_markdown_help_text_markup_field_rich_12(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    # USE_MARKDOWN is silently deprecated, and we prefer `text_markup` mode.
    #
    # The previous test ensures that the global works properly when disabled.
    #
    # This test turns off the global, and wraps the code in a help config
    # with `{"text_markup": "markdown"}`.
    rc.USE_MARKDOWN = False
    cli = rich_click.rich_config(help_config={"text_markup": "markdown"})(cli)

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the click package.                           \n\
                                                                                                    \n\
 ▌ Remember:                                                                                        \n\
 ▌  • You can try using --help at the top level                                                     \n\
 ▌  • Also for specific group subcommands.                                                          \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --input    PATH  Input file. [default: a custom default]                                         │
│ --type     TEXT  Type of file to sync                                                            │
│                  [default: files]                                                                │
│ --all            Sync                                                                            │
│                                                                                                  │
│                   1 all                                                                          │
│                   2 the                                                                          │
│                   3 things?                                                                      │
│ --debug          ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ │
│                  ┃                              Enable debug mode                              ┃ │
│                  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
