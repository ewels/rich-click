"""Tests for rich_click.patch.patch()."""

from __future__ import annotations

import sys

import rich_click
from rich_click.patch import _PatchedRichCommand, _PatchedRichGroup
from tests.conftest import run_as_subprocess


def test_patched_command_isinstance_accepts_rich_command() -> None:
    """RichCommand is a parent of _PatchedRichCommand; isinstance must still match."""

    @rich_click.command()
    def rich_cmd() -> None:
        """Rich command."""

    assert isinstance(rich_cmd, _PatchedRichCommand)
    assert not isinstance("not-a-command", _PatchedRichCommand)


def test_patched_group_isinstance_accepts_rich_group() -> None:
    @rich_click.group()
    def rich_grp() -> None:
        """Rich group."""

    assert isinstance(rich_grp, _PatchedRichGroup)
    assert isinstance(rich_grp, _PatchedRichCommand)
    assert not isinstance(object(), _PatchedRichGroup)


def test_forward_rich_command_after_patch() -> None:
    """ctx.forward(rich_cmd) must work after patch() replaces click.Command (#338)."""
    script = """
import click
import rich_click
from click.testing import CliRunner
from rich_click.patch import patch

@rich_click.command()
@rich_click.option("--name", default="world")
def rich_cmd(name):
    print(f"hello {name}")

patch()

@click.command()
@click.option("--name", default="world")
@click.pass_context
def cli(ctx, name):
    ctx.forward(rich_cmd)

res = CliRunner().invoke(cli, ["--name", "sea"])
assert res.exit_code == 0, repr(res.exception)
assert res.output == "hello sea\\n"
print("OK")
"""
    res = run_as_subprocess([sys.executable, "-c", script])
    assert res.returncode == 0, res.stderr.decode() + res.stdout.decode()
    assert res.stdout.decode().strip() == "OK"


def test_invoke_rich_command_after_patch() -> None:
    """ctx.invoke(rich_cmd) uses the same Command isinstance check as forward."""
    script = """
import click
import rich_click
from click.testing import CliRunner
from rich_click.patch import patch

@rich_click.command()
@rich_click.option("--name", default="world")
def rich_cmd(name):
    print(f"hello {name}")

patch()

@click.command()
@click.pass_context
def cli(ctx):
    ctx.invoke(rich_cmd, name="sea")

res = CliRunner().invoke(cli)
assert res.exit_code == 0, repr(res.exception)
assert res.output == "hello sea\\n"
print("OK")
"""
    res = run_as_subprocess([sys.executable, "-c", script])
    assert res.returncode == 0, res.stderr.decode() + res.stdout.decode()
    assert res.stdout.decode().strip() == "OK"
