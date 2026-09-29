import errno
import inspect
import io
from unittest.mock import Mock

import click
import pytest
from click import Abort
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
import rich_click.rich_click as rc
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_821
from rich_click.rich_command import RichCommand
from rich_click.rich_context import RichContext
from rich_click.rich_help_rendering import _make_param_metavar
from rich_click.utils import _PacifyFlushWrapper, truthy


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_821, reason="CliRunner's stderr capture doesn't work before 8.2.1.")
def test_abort(cli_runner: CliRunner) -> None:
    rc.COLOR_SYSTEM = "truecolor"

    @rich_click.command
    def cli() -> None:
        raise Abort()

    res = cli_runner.invoke(cli)

    assert res.stdout == snapshot("")
    assert res.stderr == snapshot("""\
\x1b[31mAborted.\x1b[0m
""")


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
    assert res.stderr == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


def test_pacify_flush_wrapper() -> None:
    class Stream(io.StringIO):
        def __init__(self, err: int) -> None:
            super().__init__()
            self.err = err

        def flush(self) -> None:
            raise OSError(self.err, "boom")

    _PacifyFlushWrapper(Stream(errno.EPIPE)).flush()

    with pytest.raises(OSError):
        _PacifyFlushWrapper(Stream(errno.EACCES)).flush()

    stream = io.StringIO()
    wrapper = _PacifyFlushWrapper(stream)
    wrapper.write("hello")
    assert stream.getvalue() == "hello"


def test_error_formatter_with_plain_click_context() -> None:
    command = RichCommand("rich")
    plain_context = click.Context(click.Command("plain"))

    with plain_context:
        formatter = command._error_formatter()

    assert formatter.config is not None


def test_rich_command_info_dict_includes_metadata() -> None:
    command = RichCommand("rich", aliases=["r"])
    panel = Mock()
    panel.to_info_dict.return_value = {"name": "Panel"}
    command.panels = [panel]
    context = RichContext(command)

    info = command.to_info_dict(context)

    assert info["panels"] == [{"name": "Panel"}]
    assert info["aliases"] == ["r"]
    panel.to_info_dict.assert_called_once_with(context)


@pytest.mark.parametrize(("click_is_before_82", "expected_args"), [(False, ("ctx",)), (True, ())])
def test_make_param_metavar_signature_fallback(
    monkeypatch: pytest.MonkeyPatch,
    click_is_before_82: bool,
    expected_args: tuple[str, ...],
) -> None:
    import rich_click.rich_help_rendering as rendering

    param = Mock()
    param.make_metavar.return_value = "VALUE"
    monkeypatch.setattr(inspect, "signature", Mock(side_effect=ValueError))
    monkeypatch.setattr(rendering, "CLICK_IS_BEFORE_VERSION_82", click_is_before_82)

    assert _make_param_metavar(param, "ctx") == "VALUE"  # type: ignore[arg-type]
    param.make_metavar.assert_called_once_with(*expected_args)
