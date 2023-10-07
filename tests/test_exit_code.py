import sys

import click
import pytest
from click.testing import CliRunner

from rich_click import command, group, pass_context, RichContext
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_8X

# Don't use the 'invoke' fixture because we want control over the standalone_mode kwarg.


def test_command_exit_code_with_context() -> None:
    for expected_exit_code in range(10):

        @command("cli")
        @pass_context
        def cli(ctx: RichContext) -> None:
            ctx.exit(expected_exit_code)

        runner = CliRunner()
        res = runner.invoke(cli, [])
        assert res.exit_code == expected_exit_code


def test_group_exit_code_with_context() -> None:
    for expected_exit_code in range(10):

        @group("cli")
        @pass_context
        def cli(ctx: RichContext) -> None:
            ctx.exit(expected_exit_code)

        @cli.command("subcommand")
        @pass_context
        def subcommand(ctx: RichContext) -> None:
            ctx.exit(999)

        runner = CliRunner()
        res = runner.invoke(cli, ["subcommand"])
        assert res.exit_code == expected_exit_code


def test_command_exit_code_with_sys_exit() -> None:
    for expected_exit_code in range(10):

        @command("cli")
        def cli() -> None:
            sys.exit(expected_exit_code)

        runner = CliRunner()
        res = runner.invoke(cli, [])
        assert res.exit_code == expected_exit_code


def test_group_exit_code_with_sys_exit() -> None:
    for expected_exit_code in range(10):

        @group("cli")
        def cli() -> None:
            sys.exit(expected_exit_code)

        @cli.command("subcommand")
        def subcommand() -> None:
            sys.exit(999)

        runner = CliRunner()
        res = runner.invoke(cli, ["subcommand"])
        assert res.exit_code == expected_exit_code


def test_command_return_value_does_not_raise_exit_code() -> None:
    @command("cli")
    def cli() -> int:
        return 5

    runner = CliRunner()
    res = runner.invoke(cli, [])
    assert res.exit_code == 0


def test_group_return_value_does_not_raise_exit_code() -> None:
    @group("cli")
    def cli() -> int:
        return 5

    @cli.command("subcommand")
    def subcommand() -> int:
        return 10

    runner = CliRunner()
    res = runner.invoke(cli, [])
    assert res.exit_code == 0


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_8X, reason="Result does not have return_value attribute.")
def test_command_return_value_is_exit_code_when_not_standalone() -> None:
    for expected_exit_code in range(10):

        @command("cli")
        @pass_context
        def cli(ctx: click.Context) -> None:
            ctx.exit(expected_exit_code)

        runner = CliRunner()
        res = runner.invoke(cli, [], standalone_mode=False)
        assert res.return_value == expected_exit_code


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_8X, reason="Result does not have return_value attribute.")
def test_group_return_value_is_exit_code_when_not_standalone() -> None:
    for expected_exit_code in range(10):

        @group("cli")
        @pass_context
        def cli(ctx: RichContext) -> None:
            ctx.exit(expected_exit_code)

        @cli.command("subcommand")
        @pass_context
        def subcommand(ctx: RichContext) -> None:
            # I should not run
            ctx.exit(0)

        runner = CliRunner()
        res = runner.invoke(cli, ["subcommand"], standalone_mode=False)
        assert res.return_value == expected_exit_code
