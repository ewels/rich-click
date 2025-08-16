import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.panels_defaults")
    return cmd


def test_panels_defaults_command_panel(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
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
   Command Panel A                                                                                  \n\
  cmd4  Test args assigned to arguments panel when help is defined, and test that arg3 is assigned  \n\
        to default even without help so long as panel shows.                                        \n\
                                                                                                    \n\
╔═ Command Panel B ════════════════════════════════════════════════════════════════════════════════╗
║ cmd5  Test args and options assigned to respective panels.                                       ║
║ cmd6  Test order is preserved and option is still assigned when default panel is explicitly      ║
║       defined and ordered.                                                                       ║
║ cmd7  Test order is preserved and option is still assigned when default panel is explicitly      ║
║       defined and ordered.                                                                       ║
║ cmd8  Test options and arguments are assigned to a renamed default options panel with            ║
║       group_arguments_options=True                                                               ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝
   Custom Default Command Panel                                                                     \n\
  cmd1                             cmd1 help                                                        \n\
  cmd2                             cmd2 help                                                        \n\
  cmd3                             cmd3 help                                                        \n\
                                                                                                    \n\
"""
    )
    assert result.stderr == snapshot("")


def test_panels_defaults_argument_panel(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd4 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd4 [OPTIONS] ARG1 ARG3 ARG2                                                           \n\
                                                                                                    \n\
 Test args assigned to arguments panel when help is defined, and test that arg3 is assigned to      \n\
 default even without help so long as panel shows.                                                  \n\
                                                                                                    \n\
╭─ Custom Args Panel Title ────────────────────────────────────────────────────────────────────────╮
│ *  ARG1    TEXT  arg1 help [required]                                                            │
│ *  ARG3    TEXT  [required]                                                                      │
│ *  ARG2    TEXT  arg2 help [required]                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_panels_defaults_order(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "cmd6 --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli cmd6 [OPTIONS]                                                                          \n\
                                                                                                    \n\
 Test order is preserved and option is still assigned when default panel is explicitly defined and  \n\
 ordered.                                                                                           \n\
                                                                                                    \n\
╭─ Help ───────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Panel 1 ────────────────────────────────────────────────────────────────────────────────────────╮
│ --a    TEXT                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Panel 2 ────────────────────────────────────────────────────────────────────────────────────────╮
│ --c    TEXT                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Custom Options Panel Title ─────────────────────────────────────────────────────────────────────╮
│ --b    TEXT                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Panel 3 ────────────────────────────────────────────────────────────────────────────────────────╮
│ --d    TEXT                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
