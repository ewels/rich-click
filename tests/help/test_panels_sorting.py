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
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom Command Panel 2 ─────────────────────────────────────────────────────────────────────────╮
│ cmd2       Test order of options is preserved via panel...                                       │
│ cmd1       Test order of panels is preserved via panel=...                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom Command Panel 1 ─────────────────────────────────────────────────────────────────────────╮
│ cmd3      Test order of panels is preserved via option_panel()                                   │
│ cmd4      Test order of options is preserved via option_panel()                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom Command Panel 3 ─────────────────────────────────────────────────────────────────────────╮
│ cmd5   Test that commands appear above options when explicitly set.                              │
│ cmd6   Test that options appear above commands when explicitly set, ignoring the                 │
│        `commands_before_options` config option.                                                  │
│ cmd7   Test that default order is arguments -> options -> commands.                              │
│ cmd8   Test that default order is commands -> arguments -> options, when commands show above     │
│        options.                                                                                  │
│ cmd9   Test that command and option both having the same name doesn't cause any issues. Also     │
│        test that commands render by assigned name in dict, not by the cmd.name.                  │
│ cmd10  Test that command panel and option panel both having the same name doesn't cause any      │
│        issues.                                                                                   │
│ cmd11  Test add_command(..., panel=...)                                                          │
│ cmd12  Test all three methods of assigning a panel don't cause duplication.                      │
│ cmd13  Test that cmd.panel is ignored but that grp.add_command(panel=...) and                    │
│        command_panel.commands are not ignored.                                                   │
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
│ --help  Show this message and exit.                                                              │
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
│ --help  Show this message and exit.                                                              │
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
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
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
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_panel_order_commands_above_options(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd5 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd5 [OPTIONS] COMMAND [ARGS]...                                                        \n\
                                                                                                    \n\
 Test that commands appear above options when explicitly set.                                       \n\
                                                                                                    \n\
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ dummy                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --a     TEXT                                                                                     │
│ --help        Show this message and exit.                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_panel_order_options_above_commands(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd6 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd6 [OPTIONS] COMMAND [ARGS]...                                                        \n\
                                                                                                    \n\
 Test that options appear above commands when explicitly set, ignoring the                          \n\
 `commands_before_options` config option.                                                           \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --a     TEXT                                                                                     │
│ --help        Show this message and exit.                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ dummy                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_panel_order_options_above_commands_with_arguments(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd7 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd7 [OPTIONS] A COMMAND [ARGS]...                                                      \n\
                                                                                                    \n\
 Test that default order is arguments -> options -> commands.                                       \n\
                                                                                                    \n\
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────╮
│ *  A  TEXT  [required]                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --b     TEXT                                                                                     │
│ --help        Show this message and exit.                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ dummy                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_panel_order_arguments_options_commands(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd8 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd8 [OPTIONS] A COMMAND [ARGS]...                                                      \n\
                                                                                                    \n\
 Test that default order is commands -> arguments -> options, when commands show above options.     \n\
                                                                                                    \n\
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ dummy                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────────╮
│ *  A  TEXT  [required]                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --b     TEXT                                                                                     │
│ --help        Show this message and exit.                                                        │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_panel_option_and_command_same_name(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd9 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd9 [OPTIONS] COMMAND [ARGS]...                                                        \n\
                                                                                                    \n\
 Test that command and option both having the same name doesn't cause any issues. Also test that    \n\
 commands render by assigned name in dict, not by the cmd.name.                                     \n\
                                                                                                    \n\
╭─ Custom Opt Panel ───────────────────────────────────────────────────────────────────────────────╮
│ --samename  TEXT                                                                                 │
│ --dummy     TEXT                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ samename                                                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_panel_different_type_panels_same_name(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd10 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd10 [OPTIONS] COMMAND [ARGS]...                                                       \n\
                                                                                                    \n\
 Test that command panel and option panel both having the same name doesn't cause any issues.       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Generic Panel ──────────────────────────────────────────────────────────────────────────────────╮
│ dummy                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Generic Panel ──────────────────────────────────────────────────────────────────────────────────╮
│ --foo  TEXT                                                                                      │
│ --bar  TEXT                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_add_command_panel_kwarg(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd11 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd11 [OPTIONS] COMMAND [ARGS]...                                                       \n\
                                                                                                    \n\
 Test add_command(..., panel=...)                                                                   \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Some Panel ─────────────────────────────────────────────────────────────────────────────────────╮
│ dummy2                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_no_duplicatio_of_commands(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd12 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd12 [OPTIONS] COMMAND [ARGS]...                                                       \n\
                                                                                                    \n\
 Test all three methods of assigning a panel don't cause duplication.                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Some Panel ─────────────────────────────────────────────────────────────────────────────────────╮
│ dummy2                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_ignore_behavior_duplicate_assignments(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd13 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd13 [OPTIONS] COMMAND [ARGS]...                                                       \n\
                                                                                                    \n\
 Test that cmd.panel is ignored but that grp.add_command(panel=...) and command_panel.commands are  \n\
 not ignored.                                                                                       \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Prioritize me ──────────────────────────────────────────────────────────────────────────────────╮
│ dummy2                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
