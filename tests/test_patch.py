# ruff: noqa: D103,E501
import sys

from tests.conftest import WriteScript, run_as_subprocess


def test_patch_ctx_forward_to_rich_command(mock_script_writer: WriteScript) -> None:
    # Regression test for https://github.com/ewels/rich-click/issues/338
    #
    # patch() rebinds click.Command to a rich-click subclass, which narrowed the
    # isinstance guard in click's Context.forward/invoke and broke
    # ctx.forward(rich_cmd). Run in a subprocess because patch() mutates global
    # Click state.
    scripts = mock_script_writer(
        """
        import sys

        import click
        from click.testing import CliRunner

        from rich_click.patch import patch

        patch()

        import rich_click


        @rich_click.command()
        @click.option("--name", default="world")
        @click.option("--count", default=1)
        def target(name, count):
            for _ in range(count):
                click.echo(f"hello {name}")


        @click.command()
        @click.option("--name", default="world")
        @click.option("--count", default=1)
        @click.pass_context
        def source(ctx, name, count):
            ctx.forward(target)


        if __name__ == "__main__":
            result = CliRunner().invoke(source, ["--name", "alice", "--count", "2"])
            if result.exception is not None and not isinstance(result.exception, SystemExit):
                raise result.exception
            assert result.exit_code == 0, result.output
            sys.stdout.write(result.output)
        """,
    )

    res = run_as_subprocess([sys.executable, (scripts / "mymodule.py").as_posix()])
    assert res.returncode == 0, res.stderr.decode()
    assert res.stdout.decode() == "hello alice\nhello alice\n"


def test_patch_ctx_forward_to_command_defined_before_patch(mock_script_writer: WriteScript) -> None:
    # Commands created before patch() are genuine click.Command instances and
    # must still be forwardable once patch() runs.
    scripts = mock_script_writer(
        """
        import sys

        import click
        from click.testing import CliRunner


        @click.command()
        @click.option("--name", default="world")
        def target(name):
            click.echo(f"hi {name}")


        from rich_click.patch import patch

        patch()


        @click.command()
        @click.option("--name", default="world")
        @click.pass_context
        def source(ctx, name):
            ctx.forward(target)


        if __name__ == "__main__":
            result = CliRunner().invoke(source, ["--name", "bob"])
            if result.exception is not None and not isinstance(result.exception, SystemExit):
                raise result.exception
            assert result.exit_code == 0, result.output
            sys.stdout.write(result.output)
        """,
    )

    res = run_as_subprocess([sys.executable, (scripts / "mymodule.py").as_posix()])
    assert res.returncode == 0, res.stderr.decode()
    assert res.stdout.decode() == "hi bob\n"
