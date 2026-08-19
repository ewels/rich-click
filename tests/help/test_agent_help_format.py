import re
from collections.abc import Callable

import pytest
from click.testing import CliRunner, Result
from inline_snapshot import snapshot

import rich_click as click
import rich_click.rich_click as rc
from rich_click import RichHelpConfiguration, rich_config
from rich_click._agent_detection import _SUPPRESSION_ENV_VARS


#: The `agent_env` fixture from conftest; see there for what it does.
ConfigureEnv = Callable[..., None]


@pytest.fixture
def cli() -> click.RichCommand:
    @click.command()
    @click.option("--name", help="Your name.")
    def cli(name: str) -> None:
        """A demo command."""

    return cli


re_ansi = re.compile(r"\x1b\[[0-9;]*m")


def unstyled(text: str) -> str:
    """
    Strip ANSI styling, so assertions on the rendered help do not depend on the environment.

    A config passed to ``rich_config`` as a ``RichHelpConfiguration`` does not inherit the global
    ``COLOR_SYSTEM = None`` this suite sets, and its ``force_terminal`` default reads ``GITHUB_ACTIONS``
    -- so the very same help output is styled on CI and plain locally.
    """
    return re_ansi.sub("", text)


def assert_regular_help(result: Result) -> None:
    assert result.exit_code == 0
    assert "╭─ Options ─" in unstyled(result.stdout)
    assert "# cli" not in result.stdout


def assert_agent_help(result: Result) -> None:
    """A bare `--help` in agent mode renders `--help compact`: the leanest complete rendering."""
    assert result.exit_code == 0
    assert "╭─ Options ─" not in unstyled(result.stdout)
    assert result.stdout == snapshot(
        """\
# cli — A demo command.
--name TEXT  Your name.

"""
    )


# The truth table for a bare `--help`, one test per row.


def test_no_agent_no_suppression_renders_regular_help(
    cli_runner: CliRunner, cli: click.RichCommand, agent_env: ConfigureEnv
) -> None:
    agent_env()

    assert_regular_help(cli_runner.invoke(cli, "--help"))


def test_no_agent_with_suppression_renders_regular_help(cli_runner: CliRunner, cli: click.RichCommand) -> None:
    # No environment changes at all: the suite runs under pytest, so suppression is already in effect.
    assert_regular_help(cli_runner.invoke(cli, "--help"))


def test_agent_marker_renders_compact(cli_runner: CliRunner, cli: click.RichCommand, agent_env: ConfigureEnv) -> None:
    agent_env(marker=True)

    assert_agent_help(cli_runner.invoke(cli, "--help"))


@pytest.mark.parametrize("suppress", _SUPPRESSION_ENV_VARS)
def test_suppression_beats_agent_marker(
    cli_runner: CliRunner, cli: click.RichCommand, agent_env: ConfigureEnv, suppress: str
) -> None:
    agent_env(marker=True, suppress=suppress)

    assert_regular_help(cli_runner.invoke(cli, "--help"))


@pytest.mark.parametrize("suppress", _SUPPRESSION_ENV_VARS)
def test_override_true_beats_suppression(
    cli_runner: CliRunner, cli: click.RichCommand, agent_env: ConfigureEnv, suppress: str
) -> None:
    agent_env(suppress=suppress, override="true")

    assert_agent_help(cli_runner.invoke(cli, "--help"))


def test_override_false_beats_agent_marker(
    cli_runner: CliRunner, cli: click.RichCommand, agent_env: ConfigureEnv
) -> None:
    agent_env(marker=True, override="false")

    assert_regular_help(cli_runner.invoke(cli, "--help"))


# Interaction with an explicit format, and with the `agent_help_format` option.


def test_explicit_format_is_honoured_in_agent_mode(
    cli_runner: CliRunner, cli: click.RichCommand, agent_env: ConfigureEnv
) -> None:
    agent_env(marker=True)

    result = cli_runner.invoke(cli, ["--help", "json"])

    assert result.exit_code == 0
    assert result.stdout.startswith("{")
    assert '"help": "A demo command."' in result.stdout


def test_agent_help_format_none_disables_the_switch(cli_runner: CliRunner, agent_env: ConfigureEnv) -> None:
    agent_env(marker=True)

    @click.command()
    @rich_config(help_config=RichHelpConfiguration(agent_help_format=None))
    @click.option("--name", help="Your name.")
    def cli(name: str) -> None:
        """A demo command."""

    assert_regular_help(cli_runner.invoke(cli, "--help"))


def test_agent_help_format_is_configurable(cli_runner: CliRunner, agent_env: ConfigureEnv) -> None:
    agent_env(marker=True)

    @click.command()
    @rich_config(help_config=RichHelpConfiguration(agent_help_format="json"))
    @click.option("--name", help="Your name.")
    def cli(name: str) -> None:
        """A demo command."""

    result = cli_runner.invoke(cli, "--help")

    assert result.exit_code == 0
    assert result.stdout.startswith("{")


def test_agent_help_format_global(cli_runner: CliRunner, cli: click.RichCommand, agent_env: ConfigureEnv) -> None:
    agent_env(marker=True)
    rc.AGENT_HELP_FORMAT = None

    assert_regular_help(cli_runner.invoke(cli, "--help"))


def test_unregistered_agent_help_format_falls_back_to_regular_help(
    cli_runner: CliRunner, agent_env: ConfigureEnv
) -> None:
    agent_env(marker=True)

    @click.command()
    @rich_config(help_config=RichHelpConfiguration(agent_help_format="not-a-format"))
    @click.option("--name", help="Your name.")
    def cli(name: str) -> None:
        """A demo command."""

    assert_regular_help(cli_runner.invoke(cli, "--help"))


def test_agent_mode_switches_subcommand_help(cli_runner: CliRunner, agent_env: ConfigureEnv) -> None:
    agent_env(marker=True)

    @click.group()
    def cli() -> None:
        """A demo group."""

    @cli.command()
    def subcommand() -> None:
        """A demo subcommand."""

    result = cli_runner.invoke(cli, "subcommand --help")

    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
# subcommand — A demo subcommand.

"""
    )


# The compact format behaves differently depending on *how* it was asked for: named explicitly it is a
# whole-tree format, while as the agent default it adapts to the character ceiling. Both are the same
# renderer; only the ceiling differs.


def _tree(**config: object) -> click.RichCommand:
    """A group with three subcommands, each carrying enough help to be worth abbreviating."""

    @click.group()
    @rich_config(help_config=RichHelpConfiguration(**config))  # type: ignore[arg-type]
    def cli() -> None:
        """A demo group."""

    for index in range(3):

        @cli.command(name=f"run{index}")
        @click.option("--mode", help="How to run the operation, end to end, in detail.")
        def run(mode: str) -> None:
            """Run the thing against a target."""

    return cli


def test_explicit_compact_ignores_the_ceiling(cli_runner: CliRunner, agent_env: ConfigureEnv) -> None:
    # Naming the format is a request for the whole tree: every command's block, ceiling or no ceiling.
    agent_env(marker=True)

    result = cli_runner.invoke(_tree(agent_help_max_chars=1), ["--help", "compact"])

    assert result.exit_code == 0
    for index in range(3):
        assert f"# run{index} — Run the thing against a target." in result.stdout
        assert "--mode TEXT  How to run the operation, end to end, in detail." in result.stdout


def test_agent_default_compact_adapts_to_the_ceiling(cli_runner: CliRunner, agent_env: ConfigureEnv) -> None:
    # Reached through agent detection instead, the same format degrades under the ceiling rather than
    # letting the harness truncate it -- but still names every command.
    agent_env(marker=True)

    result = cli_runner.invoke(_tree(agent_help_max_chars=300), "--help")

    assert result.exit_code == 0
    assert len(result.stdout.strip()) <= 300
    assert "# cli — A demo group." in result.stdout
    for index in range(3):
        assert f"run{index}  Run the thing against a target." in result.stdout
    assert "How to run the operation" not in result.stdout
    assert "size-limited" in result.stdout


def test_agent_default_markdown_is_still_available(cli_runner: CliRunner, agent_env: ConfigureEnv) -> None:
    # Compact is the default, not the only option: the Markdown formats are unchanged and one config
    # value away.
    agent_env(marker=True)

    result = cli_runner.invoke(_tree(agent_help_format="markdown"), "--help")

    assert result.exit_code == 0
    assert "# `cli`" in result.stdout
    assert "| Option | Type | Description |" in result.stdout
