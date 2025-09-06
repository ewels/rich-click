import pytest
import typer
from inline_snapshot import snapshot
from typer.testing import CliRunner

import rich_click.rich_click as rc
from tests.conftest import load_command_from_module


@pytest.fixture
def cli(patch_typer: None) -> typer.Typer:
    cmd = load_command_from_module("tests.typer_help.fixtures.typer_types")
    app = typer.Typer()
    app.command()(cmd)
    return app


def test_typer_types_help(typer_cli_runner: CliRunner, cli: typer.Typer) -> None:
    rc.THEME = "nu"
    result = typer_cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
 Usage: cli [OPTIONS] ID                                                                            \n\
                                                                                                    \n\
 ═ Logging ════════════════════════════════════════════════════════════════════════════════════════ \n\
 --log-level         [debug|info|warn|error] (Default: info)                                        \n\
 --color/--no-color  (Default: color)                                                               \n\
                                                                                                    \n\
 ═ Options ════════════════════════════════════════════════════════════════════════════════════════ \n\
 --age                 [INTEGER RANGE x>=18] (Default: 20)                                          \n\
 --score               [FLOAT RANGE x<=100] (Default: 0)                                            \n\
 --install-completion  Install completion for the current shell.                                    \n\
 --show-completion     Show completion for the current shell, to copy it or customize the           \n\
                       installation.                                                                \n\
 --help                Show this message and exit.                                                  \n\
                                                                                                    \n\
"""
    )
    assert result.stderr == snapshot("")


def test_typer_types_help_renamed_default_panel(typer_cli_runner: CliRunner, cli: typer.Typer) -> None:
    rc.THEME = "nu"
    rc.OPTIONS_PANEL_TITLE = "Custom Panel"
    result = typer_cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
 Usage: cli [OPTIONS] ID                                                                            \n\
                                                                                                    \n\
 ═ Logging ════════════════════════════════════════════════════════════════════════════════════════ \n\
 --log-level         [debug|info|warn|error] (Default: info)                                        \n\
 --color/--no-color  (Default: color)                                                               \n\
                                                                                                    \n\
 ═ Custom Panel ═══════════════════════════════════════════════════════════════════════════════════ \n\
 --age                 [INTEGER RANGE x>=18] (Default: 20)                                          \n\
 --score               [FLOAT RANGE x<=100] (Default: 0)                                            \n\
 --install-completion  Install completion for the current shell.                                    \n\
 --show-completion     Show completion for the current shell, to copy it or customize the           \n\
                       installation.                                                                \n\
 --help                Show this message and exit.                                                  \n\
                                                                                                    \n\
"""
    )
    assert result.stderr == snapshot("")
