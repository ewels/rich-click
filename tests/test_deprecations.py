from importlib import reload
from unittest.mock import patch

import pytest
from click.testing import CliRunner
from rich.console import Console

import rich_click
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_9X


@pytest.mark.skipif(not CLICK_IS_BEFORE_VERSION_9X, reason="Click 9 removes MultiCommand")
def test_deprecation_warning_on_multi_command() -> None:
    reload(rich_click)

    with pytest.warns(DeprecationWarning):
        from rich_click import RichMultiCommand  # noqa: F401


def test_deprecation_warning_on_highlighter(cli_runner: CliRunner) -> None:
    c = Console()

    @rich_click.rich_config({})
    @rich_click.pass_context
    def cli(ctx: rich_click.RichContext) -> None:
        if ctx.console is c:
            print("OK!")
        else:
            print("ERROR!")

    # console should be allowed to be first argument,
    with pytest.warns(DeprecationWarning):
        cli = rich_click.rich_config(c)(cli)  # type: ignore[arg-type]

    cli = rich_click.command()(cli)

    res = cli_runner.invoke(cli)
    assert res.stdout == "OK!\n"


def test_deprecation_cli_patch() -> None:

    with patch("rich_click.cli._patch") as mock_underlying_patch:
        with pytest.warns(DeprecationWarning, match=r"`rich_click\.cli\.patch\(\)` has moved.*"):
            import rich_click.cli

            rich_click.cli.patch(a=1, b=2)

    mock_underlying_patch.assert_called_once_with(a=1, b=2)


def test_deprecation_command_help_config() -> None:

    @rich_click.command()
    def cli1() -> None:
        pass

    with pytest.warns(DeprecationWarning):
        cfg1 = getattr(cli1, "help_config")
    assert cfg1 is None

    @rich_click.command()
    @rich_click.rich_config({})
    def cli2() -> None:
        pass

    with pytest.warns(DeprecationWarning):
        cfg2 = getattr(cli2, "help_config")
    assert isinstance(cfg2, rich_click.RichHelpConfiguration)


def test_deprecation_command_console() -> None:

    @rich_click.command()
    def cli1() -> None:
        pass

    with pytest.warns(DeprecationWarning):
        con1 = getattr(cli1, "console")
    assert con1 is None

    @rich_click.command()
    @rich_click.rich_config(console=Console())
    def cli2() -> None:
        pass

    with pytest.warns(DeprecationWarning):
        con2 = getattr(cli2, "console")
    assert isinstance(con2, Console)


def test_not_implemented_warnings_for_help_formatter() -> None:

    formatter = rich_click.RichHelpFormatter()

    with pytest.warns(RuntimeWarning):
        formatter.indent()
    with pytest.warns(RuntimeWarning):
        formatter.dedent()
    with pytest.warns(RuntimeWarning):
        formatter.write_heading("")
    with pytest.warns(RuntimeWarning):
        formatter.write_paragraph()
    with pytest.warns(RuntimeWarning):
        formatter.write_text("")
    with pytest.warns(RuntimeWarning):
        formatter.write_dl([])
    with pytest.warns(RuntimeWarning):
        with formatter.section(""):
            pass
    with pytest.warns(RuntimeWarning):
        with formatter.indentation():
            pass
