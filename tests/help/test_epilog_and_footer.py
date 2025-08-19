import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.epilog_and_footer")
    return cmd


def test_epilog_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug/--no-debug                                                                               │
│ --help              Show this message and exit.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ epilog-is-rich-text                    epilog_is_rich_text help text.                            │
│ footer-is-rich-text                    footer_is_rich_text help text.                            │
│ no-epilog                              no_epilog help text.                                      │
│ no-footer                              no_footer help text.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
 For more information, visit our website.                                                           \n\
                                                                                                    \n\
                                                                                                    \n\
 And here is some footer text!                                                                      \n\
"""
    )
    assert result.stderr == snapshot("")


def test_epilog_help_subcommand_no_footer(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "no-footer --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Usage: cli no-footer [OPTIONS]                                                                     \n\
                                                                                                    \n\
 no_footer help text.                                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
 This is epilog text                                                                                \n\
                                                                                                    \n\
"""
    )
    assert result.stderr == snapshot("")


def test_epilog_help_subcommand_no_epilog(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "no-epilog --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Usage: cli no-epilog [OPTIONS]                                                                     \n\
                                                                                                    \n\
 no_epilog help text.                                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
 This is footer text                                                                                \n\
"""
    )
    assert result.stderr == snapshot("")


def test_epilog_help_subcommand_footer_is_rich_text(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "footer-is-rich-text --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Usage: cli footer-is-rich-text [OPTIONS]                                                           \n\
                                                                                                    \n\
 footer_is_rich_text help text.                                                                     \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
 This is epilog text                                                                                \n\
                                                                                                    \n\
                                                                                                    \n\
 Rich text footer                                                                                   \n\
"""
    )
    assert result.stderr == snapshot("")


def test_epilog_help_subcommand_epilog_is_rich_text(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "epilog-is-rich-text --help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
Debug mode is off
                                                                                                    \n\
 Usage: cli epilog-is-rich-text [OPTIONS]                                                           \n\
                                                                                                    \n\
 epilog_is_rich_text help text.                                                                     \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
 Rich text epilog                                                                                   \n\
                                                                                                    \n\
"""
    )
    assert result.stderr == snapshot("")


def test_epilog_help_turn_off_rich_markup(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    cli.context_settings["rich_help_config"]["text_markup"] = None
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --debug/--no-debug                                                                               │
│ --help              Show this message and exit.                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ epilog-is-rich-text                    epilog_is_rich_text help text.                            │
│ footer-is-rich-text                    footer_is_rich_text help text.                            │
│ no-epilog                              no_epilog help text.                                      │
│ no-footer                              no_footer help text.                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
                                                                                                    \n\
 [bold green]For more information, visit our website.[/]                                            \n\
                                                                                                    \n\
                                                                                                    \n\
 And here is some footer text!                                                                      \n\
"""
    )
    assert result.stderr == snapshot("")
