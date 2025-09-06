import pytest
import typer
from inline_snapshot import snapshot
from typer.testing import CliRunner

import rich_click.rich_click as rc
from tests.conftest import load_command_from_module


@pytest.fixture
def cli(patch_typer: None) -> typer.Typer:
    cmd = load_command_from_module("tests.typer_help.fixtures.typer_rich_panels")
    return cmd  # type: ignore[return-value]


def test_typer_rich_panels(typer_cli_runner: CliRunner, cli: typer.Typer) -> None:
    rc.THEME = "nu"
    result = typer_cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
 Usage: root [OPTIONS] COMMAND [ARGS]...                                                            \n\
                                                                                                    \n\
 ═ Options ════════════════════════════════════════════════════════════════════════════════════════ \n\
 --install-completion  Install completion for the current shell.                                    \n\
 --show-completion     Show completion for the current shell, to copy it or customize the           \n\
                       installation.                                                                \n\
 --help                Show this message and exit.                                                  \n\
                                                                                                    \n\
 ═ Utils and Configs ══════════════════════════════════════════════════════════════════════════════ \n\
 config  Configure the system. 🔧                                                                   \n\
 sync    Synchronize the system or something fancy like that. ♻                                     \n\
                                                                                                    \n\
 ═ Help and Others ════════════════════════════════════════════════════════════════════════════════ \n\
 help    Get help with the system. ❓                                                               \n\
 report  Report an issue. 🐛                                                                        \n\
                                                                                                    \n\
 ═ Commands ═══════════════════════════════════════════════════════════════════════════════════════ \n\
 create  Create a new user. ✨                                                                      \n\
 delete  Delete a user. 🔥                                                                          \n\
                                                                                                    \n\
"""
    )
    assert result.stderr == snapshot("")
