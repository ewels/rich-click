import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
import rich_click.rich_click as rc
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.rich_markup")
    return cmd


def test_rich_markup_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --input    PATH  Input file. [default: a custom default]                                         │
│ --type     TEXT  Type of file to sync [default: files]                                           │
│ --all            Sync all the things?                                                            │
│ --debug          Enable 👉 debug mode 👈                                                         │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_rich_markup_help_turn_off_rich_markup(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.USE_RICH_MARKUP = False
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does [black on blue]all the things[/].                                             \n\
 This is a [u]minimal example[/] based on documentation from the                                    \n\
 [link=https://click.palletsprojects.com/]'click' package[/].                                       \n\
 [i]You can try using --help at the top level and also for specific group subcommands.[/]           \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --input    PATH  Input [magenta bold]file[/]. [dim]\\[default: a custom default][/]               │
│ --type     TEXT  Type of file to sync [default: files]                                           │
│ --all            Sync all the things?                                                            │
│ --debug          Enable :point_right: [yellow]debug mode[/] :point_left:                         │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_markdown_help_text_markup_field(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    # USE_RICH_MARKUP is silently deprecated, and we prefer `text_markup` mode.
    #
    # The previous test ensures that the global works properly when disabled.
    #
    # This test turns off the global, and wraps the code in a help config
    # with `{"text_markup": "rich"}`.
    rc.USE_RICH_MARKUP = False
    cli = rich_click.rich_config(help_config={"text_markup": "rich"})(cli)

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --input    PATH  Input file. [default: a custom default]                                         │
│ --type     TEXT  Type of file to sync [default: files]                                           │
│ --all            Sync all the things?                                                            │
│ --debug          Enable 👉 debug mode 👈                                                         │
│ --help           Show this message and exit.                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
