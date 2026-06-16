import pytest
from click import Abort
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
import rich_click.rich_click as rc
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_821
from rich_click.rich_context import RichContext
from rich_click.utils import truthy


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_821, reason="CliRunner's stderr capture doesn't work before 8.2.1.")
def test_abort(cli_runner: CliRunner) -> None:
    rc.COLOR_SYSTEM = "truecolor"

    @rich_click.command
    def cli() -> None:
        raise Abort()

    res = cli_runner.invoke(cli)

    assert res.stdout == snapshot("")
    assert res.stderr == snapshot(
        """\
\x1b[31mAborted.\x1b[0m
"""
    )


def test_child_context_inherits_errors_in_output_format() -> None:
    # A child context inherits errors_in_output_format from its parent. Locks in the contract:
    # the inheritance guard used to check the wrong attribute name (harmless while both are
    # class-level defaults, but only correct by accident).
    @rich_click.command()
    def cli() -> None:
        """CLI."""

    parent = RichContext(cli, errors_in_output_format=True)
    child = RichContext(cli, parent=parent)
    assert child.errors_in_output_format is True


def test_truthy() -> None:
    assert truthy("true") is True
    assert truthy("1") is True
    assert truthy("false") is False
    assert truthy("0") is False
    assert truthy(None) is None
    assert truthy(10) is True
    assert truthy("a") is None


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_821, reason="CliRunner's stderr capture doesn't work before 8.2.1.")
def test_help_to_stderr(cli_runner: CliRunner) -> None:
    @rich_click.command(context_settings={"help_to_stderr": True})
    def cli() -> None:
        """CLI help text"""

    res = cli_runner.invoke(cli, "--help")

    assert res.exit_code == 0
    assert res.stdout == snapshot("")
    assert res.stderr == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
