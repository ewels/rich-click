import re
from collections.abc import Callable, Iterator

import pytest
from click.testing import CliRunner, Result
from inline_snapshot import snapshot

import rich_click as click
import rich_click.rich_click as rc
from rich_click import RichHelpConfiguration, rich_config
from rich_click._agent_detection import _AGENT_ENV_VARS, _SUPPRESSION_ENV_VARS, _reset_agent_cache


#: One representative agent marker; the full list is covered in `tests/test_agent_detection.py`.
AGENT_MARKER = "CLAUDECODE"

ConfigureEnv = Callable[..., None]


@pytest.fixture
def agent_env(monkeypatch: pytest.MonkeyPatch) -> Iterator[ConfigureEnv]:
    """
    Set up an agent-detection environment, and reset the cached detection so it takes effect.

    Call this from inside the test body, not from another fixture: pytest re-sets
    ``PYTEST_CURRENT_TEST`` at the start of every test phase, so the suppression markers can only be
    dropped for the duration of the body itself.
    """

    def configure(*, marker: bool = False, suppress: str | None = None, override: str | None = None) -> None:
        for env_var in (
            *_SUPPRESSION_ENV_VARS,
            *_AGENT_ENV_VARS,
            "AI_AGENT",
            "AGENT",
            "CURSOR_EXTENSION_HOST_ROLE",
            "TERM_PROGRAM",
        ):
            monkeypatch.delenv(env_var, raising=False)
        if suppress is not None:
            monkeypatch.setenv(suppress, "1")
        if marker:
            monkeypatch.setenv(AGENT_MARKER, "1")
        if override is not None:
            monkeypatch.setenv("RICH_CLICK_AGENT_MODE", override)
        _reset_agent_cache()

    yield configure
    _reset_agent_cache()


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
    assert "# `cli`" not in result.stdout


def assert_markdown_help(result: Result) -> None:
    assert result.exit_code == 0
    assert "╭─ Options ─" not in unstyled(result.stdout)
    assert result.stdout == snapshot(
        """\
# `cli`

A demo command.

**Usage:** `cli [OPTIONS]`

## Options

| Option | Type | Description |
| --- | --- | --- |
| `--name` | String | Your name. |
| `--help` | choice: markdown / markdown-full / json / json-full / carapace | Show this message and exit. |

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


def test_agent_marker_renders_markdown(cli_runner: CliRunner, cli: click.RichCommand, agent_env: ConfigureEnv) -> None:
    agent_env(marker=True)

    assert_markdown_help(cli_runner.invoke(cli, "--help"))


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

    assert_markdown_help(cli_runner.invoke(cli, "--help"))


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
# `cli subcommand`

A demo subcommand.

**Usage:** `cli subcommand [OPTIONS]`

## Options

| Option | Type | Description |
| --- | --- | --- |
| `--help` | choice: markdown / markdown-full / json / json-full / carapace | Show this message and exit. |

"""
    )
