"""
Error diagnosis: a usage error should teach the rule it broke, not just report the symptom.

One diagnosis layer, two renderers -- a terse addition to the rich error panel for humans, and a fuller
plain-text block when an AI agent is detected. Both are strictly additive: exit codes are unchanged, and
Click's own message is still the first thing emitted.
"""

from collections.abc import Callable

import pytest
from click.testing import CliRunner, Result

import rich_click as click
from rich_click import RichHelpConfiguration, rich_config
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_821
from rich_click.error_diagnosis import diagnose


#: The `agent_env` fixture from conftest; see there for what it does.
ConfigureEnv = Callable[..., None]

pytestmark = pytest.mark.skipif(
    CLICK_IS_BEFORE_VERSION_821,
    reason="CliRunner's stderr capture doesn't work before Click 8.2.1.",
)


@pytest.fixture
def cli() -> click.RichGroup:
    @click.group()
    @click.option("--repo", help="Which repository to act on.")
    def tool(repo: str) -> None:
        """A tool."""

    @tool.command()
    @click.option("--report", help="Where to write the report.")
    @click.option("--mode", type=click.Choice(["fast", "safe"]), help="How to run.")
    @click.argument("name")
    def build(report: str, mode: str, name: str) -> None:
        """Build a thing."""

    @tool.command()
    def check() -> None:
        """Check a thing."""

    return tool


def errors(result: Result) -> str:
    """The error output, whichever stream this Click version puts it on."""
    return result.stderr or result.output


def flat(result: Result) -> str:
    """The error output as one line, so assertions do not depend on where the error panel wraps."""
    return " ".join(errors(result).replace("\u2502", " ").split())


# --------------------------------------------------------------------------------------------------
# The diagnosis layer: what can be derived from each kind of usage error.
# --------------------------------------------------------------------------------------------------


def test_option_of_the_parent_group_is_named_as_such(cli_runner: CliRunner, cli: click.RichGroup) -> None:
    # The doom-loop case. Click parses a group's options before the subcommand name, so a correctly
    # spelled `--repo` written after the subcommand fails with a bare "no such option" -- nothing in
    # which says the fix is to move it.
    result = cli_runner.invoke(cli, ["build", "--repo", "x", "thing"])
    output = flat(result)

    assert result.exit_code == 2
    assert "'--repo' is an option of the parent group 'tool', not of 'tool build'." in output
    assert "A group's options must be given before its subcommand." in output
    assert "tool --repo TEXT build ..." in output
    assert "tool --help" in output


def test_unknown_option_offers_near_matches(cli_runner: CliRunner, cli: click.RichGroup) -> None:
    output = flat(cli_runner.invoke(cli, ["build", "--repot", "x", "thing"]))

    assert "'--repot' is not an option of 'tool build'." in output
    assert "--report" in output


def test_unknown_option_ignores_the_help_flag_when_suggesting(cli_runner: CliRunner, cli: click.RichGroup) -> None:
    # `--help` is close enough to a great many typos to keep surfacing, and is never what was meant.
    output = flat(cli_runner.invoke(cli, ["build", "--hepl", "thing"]))

    assert "Did you mean: --help" not in output


def test_unknown_command_offers_the_corrected_invocation(cli_runner: CliRunner, cli: click.RichGroup) -> None:
    output = flat(cli_runner.invoke(cli, ["biuld"]))

    assert "'biuld' is not a command of 'tool'." in output
    assert "tool build" in output


def test_bad_choice_value_states_the_valid_set(cli_runner: CliRunner, cli: click.RichGroup) -> None:
    output = flat(cli_runner.invoke(cli, ["build", "--mode", "quick", "thing"]))

    assert "'--mode' must be one of: fast, safe." in output


def test_missing_parameter_states_the_requirement(cli_runner: CliRunner, cli: click.RichGroup) -> None:
    output = flat(cli_runner.invoke(cli, ["build"]))

    assert "'NAME' is required." in output


def test_nothing_to_diagnose_is_a_no_op(cli_runner: CliRunner) -> None:
    # An error a callback raised already states its own rule; restating it would be noise. And an
    # unknown option with no near match has no rule to offer beyond the message itself.
    @click.command()
    @click.option("--seed", type=int)
    @click.option("--from-file")
    def cli(seed: int, from_file: str) -> None:
        """Hi."""
        raise click.UsageError("exactly one seeding option is required")

    output = flat(cli_runner.invoke(cli, []))
    assert "exactly one seeding option is required" in output
    assert "Rule:" not in output

    assert "Rule:" not in flat(cli_runner.invoke(cli, ["--zzzzzzzz"]))


def test_diagnose_returns_none_without_a_context() -> None:
    # A ClickException raised outside any command (no ctx) cannot be diagnosed, and must not raise.
    assert diagnose(click.UsageError("something went wrong")) is None


def test_a_failed_diagnosis_never_costs_the_error_message(
    cli_runner: CliRunner, cli: click.RichGroup, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A diagnosis is an enhancement, never a prerequisite. If working one out raises -- a custom command
    # whose introspection needs real parse state, an exotic ParamType -- the user must still get the
    # error they actually need to read, not a traceback in place of it.
    import rich_click.error_diagnosis as error_diagnosis

    def boom(*args: object, **kwargs: object) -> None:
        raise RuntimeError("diagnosis blew up")

    monkeypatch.setattr(error_diagnosis, "_diagnose_unknown_option", boom)

    result = cli_runner.invoke(cli, ["build", "--repo", "x", "thing"])
    assert result.exit_code == 2
    assert "No such option" in flat(result)
    assert "parent group" not in flat(result)


# --------------------------------------------------------------------------------------------------
# The two renderers, chosen by the same agent detection that drives agent help.
# --------------------------------------------------------------------------------------------------


def test_human_rendering_extends_the_error_panel(
    cli_runner: CliRunner, cli: click.RichGroup, agent_env: ConfigureEnv
) -> None:
    agent_env(marker=False)
    output = flat(cli_runner.invoke(cli, ["build", "--repo", "x", "thing"]))

    # Still the familiar panel, with the diagnosis inside it -- and terse: no restated argv.
    assert "─ Error ─" in output
    assert "is an option of the parent group" in output
    assert "Attempted:" not in output


def test_agent_rendering_is_a_plain_text_block(
    cli_runner: CliRunner, cli: click.RichGroup, agent_env: ConfigureEnv
) -> None:
    agent_env(marker=True)
    result = cli_runner.invoke(cli, ["build", "--repo", "x", "thing"])
    output = errors(result)

    # No panel, no ANSI, and one fact per line.
    assert "─ Error ─" not in output
    assert "\x1b[" not in output
    assert "Attempted:" not in output
    assert "Rule: '--repo' is an option of the parent group" in output
    # The placeholder is Click's own metavar for the option, so it matches what the help shows.
    assert "Try: tool --repo TEXT build ..." in output
    assert "Usage: tool build [OPTIONS] NAME" in output
    assert "Help: tool --help" in output

    # Strictly additive: Click's own message is still the first line, and the exit code is untouched.
    assert output.splitlines()[0].startswith("Error: No such option")
    assert result.exit_code == 2


def test_agent_rendering_does_not_echo_secrets(cli_runner: CliRunner, agent_env: ConfigureEnv) -> None:
    agent_env(marker=True)

    @click.command()
    @click.password_option("--password")
    def cli(password: str) -> None:
        """A command."""

    output = errors(cli_runner.invoke(cli, ["--password", "SUPERSECRET", "--bogus"]))
    assert "SUPERSECRET" not in output
    assert "No such option" in output


def test_agent_rendering_keeps_configured_error_epilogue(cli_runner: CliRunner, agent_env: ConfigureEnv) -> None:
    agent_env(marker=True)

    @click.command()
    @rich_config(help_config=RichHelpConfiguration(errors_epilogue="CONTACT SUPPORT"))
    def cli() -> None:
        """A command."""

    output = errors(cli_runner.invoke(cli, ["--bogus"]))
    assert "CONTACT SUPPORT" in output


def test_agent_rendering_still_reports_undiagnosable_errors(
    cli_runner: CliRunner, cli: click.RichGroup, agent_env: ConfigureEnv
) -> None:
    agent_env(marker=True)
    output = errors(cli_runner.invoke(cli, ["nope"]))

    assert output.splitlines()[0] == "Error: No such command 'nope'."
    assert "Usage: tool [OPTIONS] COMMAND [ARGS]..." in output


# --------------------------------------------------------------------------------------------------
# The off switch, so the behaviour can be A/B'd without touching the CLI's source.
# --------------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("env_var", "diagnosed"),
    [
        (None, False),  # the config option alone
        ("0", False),  # ...and the env var, which outranks it in both directions
        ("false", False),
        ("1", True),
    ],
)
def test_diagnosis_can_be_switched_off(
    cli_runner: CliRunner, monkeypatch: pytest.MonkeyPatch, env_var: str | None, diagnosed: bool
) -> None:
    if env_var is None:
        monkeypatch.delenv("RICH_CLICK_ERROR_DIAGNOSIS", raising=False)
    else:
        monkeypatch.setenv("RICH_CLICK_ERROR_DIAGNOSIS", env_var)

    @click.group()
    @rich_config(help_config=RichHelpConfiguration(error_diagnosis=False))
    @click.option("--repo", help="Which repository.")
    def tool(repo: str) -> None:
        """A tool."""

    @tool.command()
    @click.argument("name")
    def build(name: str) -> None:
        """Build a thing."""

    output = flat(cli_runner.invoke(tool, ["build", "--repo", "x", "thing"]))
    assert "No such option" in output  # Click's own message is never suppressed
    assert ("parent group" in output) is diagnosed


def test_turning_diagnosis_off_restores_the_rich_panel_for_agents(
    cli_runner: CliRunner, cli: click.RichGroup, monkeypatch: pytest.MonkeyPatch, agent_env: ConfigureEnv
) -> None:
    agent_env(marker=True)
    monkeypatch.setenv("RICH_CLICK_ERROR_DIAGNOSIS", "0")

    output = flat(cli_runner.invoke(cli, ["build", "--repo", "x", "thing"]))
    assert "─ Error ─" in output
    assert "Attempted:" not in output
