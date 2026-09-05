import sys

from tests.conftest import WriteScript, run_as_subprocess


def test_patch_with_ctx_forward(mock_script_writer: WriteScript) -> None:
    scripts = mock_script_writer(
        """
        from rich_click.patch import patch

        patch()

        import click
        import rich_click

        @rich_click.command()
        def rich_click_cli() -> None:
            pass

        @click.command()
        @click.pass_context
        def cli(ctx) -> None:
            ctx.forward(rich_click_cli)
            click.echo("Success!")

        cli()
        """,
    )

    res = run_as_subprocess([sys.executable, (scripts / "mymodule.py").as_posix()])
    assert res.returncode == 0
    assert res.stdout.decode() == "Success!\n"
