import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.panels_sorting")
    return cmd


def test_command_panel_order(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom Command Panel 1 ─────────────────────────────────────────────────────────────────────────╮
│ cmd2       Test order of options is preserved via panel...                                       │
│ cmd1       Test order of panels is preserved via panel=...                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom Command Panel 2 ─────────────────────────────────────────────────────────────────────────╮
│ cmd3      Test order of panels is preserved via option_panel()                                   │
│ cmd4      Test order of options is preserved via option_panel()                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_panel_order_in_panel_decorator(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd1 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd1 [OPTIONS]                                                                          \n\
                                                                                                    \n\
 Test order of panels is preserved via panel=...                                                    \n\
                                                                                                    \n\
╭─ Custom 2 ───────────────────────────────────────────────────────────────────────────────────────╮
│ --a  -a  TEXT  Help text for A                                                                   │
│ --c  -c  TEXT  Help text for C                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom 1 ───────────────────────────────────────────────────────────────────────────────────────╮
│ --b  -b  TEXT  Help text for B                                                                   │
│ --e  -e  TEXT  Help text for E                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom 3 ───────────────────────────────────────────────────────────────────────────────────────╮
│ --f  -f  TEXT  Help text for F                                                                   │
│ --d  -d  TEXT  Help text for E                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_option_order_with_panel_decorator(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd2 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd2 [OPTIONS]                                                                          \n\
                                                                                                    \n\
 Test order of options is preserved via panel...                                                    \n\
                                                                                                    \n\
╭─ Custom 1 ───────────────────────────────────────────────────────────────────────────────────────╮
│ --a  -a  TEXT  Help text for A                                                                   │
│ --b  -b  TEXT  Help text for B                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom 2 ───────────────────────────────────────────────────────────────────────────────────────╮
│ --d  -d  TEXT  Help text for D                                                                   │
│ --c  -c  TEXT  Help text for C                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom 3 ───────────────────────────────────────────────────────────────────────────────────────╮
│ --f  -f  TEXT  Help text for F                                                                   │
│ --e  -e  TEXT  Help text for E                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_panel_order_with_panel_kwarg(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd3 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd3 [OPTIONS]                                                                          \n\
                                                                                                    \n\
 Test order of panels is preserved via option_panel()                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Panel 2 ────────────────────────────────────────────────────────────────────────────────────────╮
│ --a  -a  TEXT  Help text for A                                                                   │
│ --b  -b  TEXT  Help text for B                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Panel 1 ────────────────────────────────────────────────────────────────────────────────────────╮
│ --c  -c  TEXT  Help text for C                                                                   │
│ --d  -d  TEXT  Help text for D                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Panel 3 ────────────────────────────────────────────────────────────────────────────────────────╮
│ --e  -e  TEXT  Help text for E                                                                   │
│ --f  -f  TEXT  Help text for F                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_option_order_with_panel_kwarg(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd4 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd4 [OPTIONS]                                                                          \n\
                                                                                                    \n\
 Test order of options is preserved via option_panel()                                              \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Panel 1 ────────────────────────────────────────────────────────────────────────────────────────╮
│ --a  -a  TEXT  Help text for A                                                                   │
│ --b  -b  TEXT  Help text for B                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Panel 2 ────────────────────────────────────────────────────────────────────────────────────────╮
│ --d  -d  TEXT  Help text for C                                                                   │
│ --c  -c  TEXT  Help text for D                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Panel 3 ────────────────────────────────────────────────────────────────────────────────────────╮
│ --f  -e  TEXT  Help text for E                                                                   │
│ --e  -f  TEXT  Help text for F                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
