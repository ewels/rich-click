import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
import rich_click.rich_click as rc
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_82, CLICK_IS_BEFORE_VERSION_821
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.help.fixtures.simple")
    return cmd


def test_simple_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific subcommands.                       \n\
 Here are things you can do:                                                                        \n\
 - sync files                                                                                       \n\
 - download files                                                                                   \n\
 - print help text!                                                                                 \n\
 ... and more!                                                                                      \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug/--no-debug  -d/-n  Enable debug mode. Newlines are removed by default.                   │
│                            Double newlines are preserved.                                        │
│ --help                     Show this message and exit.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ download  Optionally use short-help for the group help text                                      │
│ sync      Synchronise all your files between two places. Example command that doesn't do much    │
│           except print to the terminal.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


def test_simple_help_no_args_is_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    # when raising NoArgsIsHelpError:
    # - exit code is 2 in Click >=8.2
    # - exit code is 0 in Click <8.2
    # - stdout + stderr should be equivalent to using --help.
    result = cli_runner.invoke(cli)
    if CLICK_IS_BEFORE_VERSION_82:
        assert result.exit_code == 0
    else:
        assert result.exit_code == 2
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific subcommands.                       \n\
 Here are things you can do:                                                                        \n\
 - sync files                                                                                       \n\
 - download files                                                                                   \n\
 - print help text!                                                                                 \n\
 ... and more!                                                                                      \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug/--no-debug  -d/-n  Enable debug mode. Newlines are removed by default.                   │
│                            Double newlines are preserved.                                        │
│ --help                     Show this message and exit.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ download  Optionally use short-help for the group help text                                      │
│ sync      Synchronise all your files between two places. Example command that doesn't do much    │
│           except print to the terminal.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")

    result_with_help = cli_runner.invoke(cli, "--help")
    assert result.stdout == result_with_help.stdout
    assert result.stderr == result_with_help.stderr


def test_simple_help_commands_before_options(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.COMMANDS_BEFORE_OPTIONS = True
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific subcommands.                       \n\
 Here are things you can do:                                                                        \n\
 - sync files                                                                                       \n\
 - download files                                                                                   \n\
 - print help text!                                                                                 \n\
 ... and more!                                                                                      \n\
                                                                                                    \n\
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ download  Optionally use short-help for the group help text                                      │
│ sync      Synchronise all your files between two places. Example command that doesn't do much    │
│           except print to the terminal.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug/--no-debug  -d/-n  Enable debug mode. Newlines are removed by default.                   │
│                            Double newlines are preserved.                                        │
│ --help                     Show this message and exit.                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_821, reason="CliRunner's stderr capture doesn't work before 8.2.1.")
def test_simple_help_no_such_command(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "bad-input")
    assert result.exit_code == 2
    assert result.stdout == snapshot("")
    assert result.stderr == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 Try 'cli --help' for help                                                                          \n\
╭─ Error ──────────────────────────────────────────────────────────────────────────────────────────╮
│ No such command 'bad-input'.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
"""
    )


def test_simple_help_nu_theme(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.THEME = "nu"
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific subcommands.                       \n\
 Here are things you can do:                                                                        \n\
 - sync files                                                                                       \n\
 - download files                                                                                   \n\
 - print help text!                                                                                 \n\
 ... and more!                                                                                      \n\
                                                                                                    \n\
 ═ Options ════════════════════════════════════════════════════════════════════════════════════════ \n\
 --debug/--no-debug  -d/-n  Enable debug mode. Newlines are removed by default.                     \n\
                            Double newlines are preserved.                                          \n\
 --help                     Show this message and exit.                                             \n\
                                                                                                    \n\
 ═ Commands ═══════════════════════════════════════════════════════════════════════════════════════ \n\
 download  Optionally use short-help for the group help text                                        \n\
 sync      Synchronise all your files between two places. Example command that doesn't do much      \n\
           except print to the terminal.                                                            \n\
                                                                                                    \n\
"""
    )
    assert result.stderr == snapshot("")


def test_simple_help_slim_theme(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.THEME = "slim"
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Usage: cli [OPTIONS] COMMAND [ARGS]...                                                              \n\
                                                                                                    \n\
My amazing tool does all the things.                                                                \n\
This is a minimal example based on documentation from the 'click' package.                          \n\
You can try using --help at the top level and also for specific subcommands.                        \n\
Here are things you can do:                                                                         \n\
- sync files                                                                                        \n\
- download files                                                                                    \n\
- print help text!                                                                                  \n\
... and more!                                                                                       \n\
                                                                                                    \n\
Options:                                                                                            \n\
  -d/-n  --debug/--no-debug  Enable debug mode. Newlines are removed by default.                    \n\
                             Double newlines are preserved.                                         \n\
         --help              Show this message and exit.                                            \n\
                                                                                                    \n\
Commands:                                                                                           \n\
  download  Optionally use short-help for the group help text                                       \n\
  sync      Synchronise all your files between two places. Example command that doesn't do much     \n\
            except print to the terminal.                                                           \n\
                                                                                                    \n\
"""
    )
    assert result.stderr == snapshot("")


def test_simple_help_modern_theme(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.THEME = "modern"
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
  Usage: cli [OPTIONS] COMMAND [ARGS]...                                                            \n\
                                                                                                    \n\
  My amazing tool does all the things.                                                              \n\
  This is a minimal example based on documentation from the 'click' package.                        \n\
  You can try using --help at the top level and also for specific subcommands.                      \n\
  Here are things you can do:                                                                       \n\
  - sync files                                                                                      \n\
  - download files                                                                                  \n\
  - print help text!                                                                                \n\
  ... and more!                                                                                     \n\
                                                                                                    \n\
  Options                                                                                           \n\
  ────────────────────────────────────────────────────────────────────────────────────────────────  \n\
  -d / -n   --debug / --no-debug   Enable debug mode. Newlines are removed by default.              \n\
                                   Double newlines are preserved.                                   \n\
            --help                 Show this message and exit.                                      \n\
                                                                                                    \n\
                                                                                                    \n\
  Commands                                                                                          \n\
  ────────────────────────────────────────────────────────────────────────────────────────────────  \n\
  download   Optionally use short-help for the group help text                                      \n\
  sync       Synchronise all your files between two places. Example command that doesn't do much    \n\
             except print to the terminal.                                                          \n\
                                                                                                    \n\
                                                                                                    \n\
"""
    )
    assert result.stderr == snapshot("")


def test_simple_help_robo_theme(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    rc.THEME = "robo"
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Usage: cli [OPTIONS] COMMAND [ARGS]...                                                              \n\
                                                                                                    \n\
My amazing tool does all the things.                                                                \n\
This is a minimal example based on documentation from the 'click' package.                          \n\
You can try using --help at the top level and also for specific subcommands.                        \n\
Here are things you can do:                                                                         \n\
- sync files                                                                                        \n\
- download files                                                                                    \n\
- print help text!                                                                                  \n\
... and more!                                                                                       \n\
                                                                                                    \n\
┌─  Options  ──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                  │
│  -d, --debug  -n, --no-debug  Enable debug mode. Newlines are removed by default.                │
│                               Double newlines are preserved.                                     │
│  --help                       Show this message and exit.                                        │
│                                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
┌─  Commands  ─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                                  │
│  download  Optionally use short-help for the group help text                                     │
│  sync      Synchronise all your files between two places. Example command that doesn't do much   │
│            except print to the terminal.                                                         │
│                                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
"""
    )
    assert result.stderr == snapshot("")
