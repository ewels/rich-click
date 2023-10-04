import sys

from click.testing import CliRunner

from rich_click import command, group, pass_context, RichContext

# Don't use the 'invoke' fixture because we want control over the standalone_mode kwarg.


def test_command_exit_code_with_context():
    for expected_exit_code in range(10):

        @command("cli")
        @pass_context
        def cli(ctx: RichContext):
            ctx.exit(expected_exit_code)

        runner = CliRunner()
        res = runner.invoke(cli, [])
        assert res.exit_code == expected_exit_code


def test_group_exit_code_with_context():
    for expected_exit_code in range(10):

        @group("cli")
        @pass_context
        def cli(ctx: RichContext):
            ctx.exit(expected_exit_code)

        @cli.command("subcommand")
        @pass_context
        def subcommand(ctx: RichContext):
            ctx.exit(999)

        runner = CliRunner()
        res = runner.invoke(cli, ["subcommand"])
        assert res.exit_code == expected_exit_code


def test_command_exit_code_with_sys_exit():
    for expected_exit_code in range(10):

        @command("cli")
        def cli():
            sys.exit(expected_exit_code)

        runner = CliRunner()
        res = runner.invoke(cli, [])
        assert res.exit_code == expected_exit_code


def test_group_exit_code_with_sys_exit():
    for expected_exit_code in range(10):

        @group("cli")
        def cli():
            sys.exit(expected_exit_code)

        @cli.command("subcommand")
        def subcommand():
            sys.exit(999)

        runner = CliRunner()
        res = runner.invoke(cli, ["subcommand"])
        assert res.exit_code == expected_exit_code


def test_command_return_value_does_not_raise_exit_code():
    @command("cli")
    def cli():
        return 5

    runner = CliRunner()
    res = runner.invoke(cli, [])
    assert res.exit_code == 0


def test_group_return_value_does_not_raise_exit_code():
    @group("cli")
    def cli():
        return 5

    @cli.command("subcommand")
    def subcommand():
        return 10

    runner = CliRunner()
    res = runner.invoke(cli, [])
    assert res.exit_code == 0


def test_command_return_value_is_exit_code_when_not_standalone():
    for expected_exit_code in range(10):

        @command("cli")
        @pass_context
        def cli(ctx: RichContext):
            ctx.exit(expected_exit_code)

        runner = CliRunner()
        res = runner.invoke(cli, [], standalone_mode=False)
        assert res.return_value == expected_exit_code


def test_group_return_value_is_exit_code_when_not_standalone():
    for expected_exit_code in range(10):

        @group("cli")
        @pass_context
        def cli(ctx: RichContext):
            ctx.exit(expected_exit_code)

        @cli.command("subcommand")
        @pass_context
        def subcommand(ctx: RichContext):
            # I should not run
            ctx.exit(0)

        runner = CliRunner()
        res = runner.invoke(cli, ["subcommand"], standalone_mode=False)
        assert res.return_value == expected_exit_code
