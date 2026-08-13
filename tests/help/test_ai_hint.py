import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click as click
from rich_click import RichHelpConfiguration, rich_config
from rich_click._agent_detection import _reset_agent_cache


@pytest.fixture
def cli() -> click.RichCommand:
    @click.command()
    @click.option("--name", help="Your name.")
    def cli(name: str) -> None:
        """A demo command."""

    return cli


def test_ai_markdown_hint_hidden_without_agent_environment(cli_runner: CliRunner, cli: click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert "AI-friendly" not in result.stdout


@pytest.mark.parametrize("env_var", ["AGENT", "CLAUDECODE"])
def test_ai_markdown_hint_shown_in_agent_environment(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner, cli: click.RichCommand, env_var: str
) -> None:
    monkeypatch.delenv("RICH_CLICK_AGENT_MODE")
    monkeypatch.setenv(env_var, "1")
    _reset_agent_cache()

    result = cli_runner.invoke(cli, "--help")

    assert result.exit_code == 0
    assert "Tip: Run '--help markdown'" in result.stdout


def test_ai_markdown_hint_shown_when_enabled(cli_runner: CliRunner) -> None:
    @click.command()
    @rich_config(help_config=RichHelpConfiguration(show_ai_markdown_hint=True))
    @click.option("--name", help="Your name.")
    def cli(name: str) -> None:
        """A demo command."""

    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                \n\
 Usage: cli [OPTIONS]                                                           \n\
                                                                                \n\
 A demo command.                                                                \n\
                                                                                \n\
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --name  TEXT                 Your name.                                      │
│ --help  [markdown|json|...]  Show this message and exit.                     │
╰──────────────────────────────────────────────────────────────────────────────╯
                                                                                \n\
 Tip: Run '--help markdown' to get AI-friendly CLI help with progressive        \n\
 disclosure.                                                                    \n\
"""
    )


def test_ai_markdown_hint_explicit_false_overrides_agent_environment(
    monkeypatch: pytest.MonkeyPatch, cli_runner: CliRunner
) -> None:
    monkeypatch.delenv("RICH_CLICK_AGENT_MODE")
    monkeypatch.setenv("CLAUDECODE", "1")
    _reset_agent_cache()

    @click.command()
    @rich_config(help_config=RichHelpConfiguration(show_ai_markdown_hint=False))
    def cli() -> None:
        """A demo command."""

    result = cli_runner.invoke(cli, "--help")

    assert result.exit_code == 0
    assert "AI-friendly" not in result.stdout


def test_ai_markdown_hint_not_shown_for_machine_formats(cli_runner: CliRunner) -> None:
    @click.command()
    @rich_config(help_config=RichHelpConfiguration(show_ai_markdown_hint=True))
    @click.option("--name", help="Your name.")
    def cli(name: str) -> None:
        """A demo command."""

    for fmt in ("json", "json-full", "markdown", "carapace"):
        result = cli_runner.invoke(cli, ["--help", fmt])
        assert result.exit_code == 0
        assert "AI-friendly" not in result.stdout, fmt


def test_ai_markdown_hint_custom_text_and_help_option_substitution(cli_runner: CliRunner) -> None:
    @click.command(context_settings={"help_option_names": ["-h", "--help"]})
    @rich_config(
        help_config=RichHelpConfiguration(
            show_ai_markdown_hint=True,
            ai_markdown_hint_text="LLM agents: run '{help_option} json-full' for the complete command tree.",
        )
    )
    @click.option("--name", help="Your name.")
    def cli(name: str) -> None:
        """A demo command."""

    result = cli_runner.invoke(cli, "-h")
    assert result.exit_code == 0
    # `{help_option}` resolves to the long flag, even though `-h` was used and comes first.
    assert "run '--help json-full'" in result.stdout
    assert result.stdout == snapshot(
        """\
                                                                                \n\
 Usage: cli [OPTIONS]                                                           \n\
                                                                                \n\
 A demo command.                                                                \n\
                                                                                \n\
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --name      TEXT                 Your name.                                  │
│ --help  -h  [markdown|json|...]  Show this message and exit.                 │
╰──────────────────────────────────────────────────────────────────────────────╯
                                                                                \n\
 LLM agents: run '--help json-full' for the complete command tree.              \n\
"""
    )
