from __future__ import annotations

import os
import sys
from typing import Iterator

import pytest

import rich_click._agent_detection as agent_detection
from rich_click._agent_detection import (
    _AGENT_ENV_VARS,
    _SUPPRESSION_ENV_VARS,
    _reset_agent_cache,
    detect_agent,
    is_agent_mode,
)


@pytest.fixture(autouse=True)
def clean_agent_environment(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    env_vars = {
        "RICH_CLICK_AGENT_MODE",
        "AI_AGENT",
        "AGENT",
        "CLAUDE_CODE_IS_COWORK",
        "CURSOR_EXTENSION_HOST_ROLE",
        "TERM_PROGRAM",
        "PATH",
        *_AGENT_ENV_VARS,
    }
    for env_var in env_vars:
        monkeypatch.delenv(env_var, raising=False)

    # The suite runs under pytest, whose variables suppress detection -- and `PYTEST_CURRENT_TEST` is
    # re-set at the start of every test phase, so deleting it here would not hold for the test body.
    # Ignore the suppression markers by default instead; `real_suppression` opts back in to them.
    monkeypatch.setattr(agent_detection, "_SUPPRESSION_ENV_VARS", ())
    monkeypatch.setattr(os.path, "exists", lambda path: False)
    _reset_agent_cache()
    yield
    _reset_agent_cache()


@pytest.fixture
def real_suppression(clean_agent_environment: None, monkeypatch: pytest.MonkeyPatch) -> None:
    """Restore the real suppression markers, which `clean_agent_environment` ignores by default."""
    monkeypatch.setattr(agent_detection, "_SUPPRESSION_ENV_VARS", _SUPPRESSION_ENV_VARS)
    _reset_agent_cache()


@pytest.mark.parametrize("env_var", _AGENT_ENV_VARS)
def test_agent_environment_markers(env_var: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(env_var, "")

    assert detect_agent() == "agent"
    assert is_agent_mode() is True


def test_cowork_markers_detect_agent_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLAUDE_CODE_IS_COWORK", "1")
    monkeypatch.setenv("CLAUDECODE", "1")

    assert is_agent_mode() is True


def test_cursor_agent_exec_role(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CURSOR_EXTENSION_HOST_ROLE", "agent-exec")

    assert is_agent_mode() is True


def test_kiro_non_tty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TERM_PROGRAM", "kiro-terminal")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)

    assert is_agent_mode() is True


def test_kiro_tty_is_not_agent_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TERM_PROGRAM", "kiro-terminal")
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)

    assert is_agent_mode() is False


def test_pi_path(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PATH", os.pathsep.join(("/usr/bin", "/tmp/.pi/agent/bin")))

    assert is_agent_mode() is True


def test_devin_path_is_checked_last(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(os.path, "exists", lambda path: path == "/opt/.devin")

    assert is_agent_mode() is True


def test_truthy_override_forces_agent_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RICH_CLICK_AGENT_MODE", "true")

    assert detect_agent() == "agent"
    assert is_agent_mode() is True


def test_falsy_override_forces_agent_mode_off(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RICH_CLICK_AGENT_MODE", "false")
    monkeypatch.setenv("CLAUDECODE", "1")

    assert detect_agent() is None
    assert is_agent_mode() is False


@pytest.mark.parametrize("env_var", _SUPPRESSION_ENV_VARS)
def test_suppression_variables_disable_detection(
    env_var: str, real_suppression: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(env_var, "1")
    monkeypatch.setenv("CLAUDECODE", "1")
    _reset_agent_cache()

    assert detect_agent() is None
    assert is_agent_mode() is False


@pytest.mark.parametrize("env_var", _SUPPRESSION_ENV_VARS)
def test_override_outranks_suppression_variables(
    env_var: str, real_suppression: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(env_var, "1")
    monkeypatch.setenv("RICH_CLICK_AGENT_MODE", "true")
    _reset_agent_cache()

    assert detect_agent() == "agent"
    assert is_agent_mode() is True


def test_pytest_variables_suppress_with_their_real_values(
    real_suppression: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    # pytest's values are a test ID and a version -- neither truthy nor falsy, but still suppressing.
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "tests/test_agent_detection.py::test_thing (call)")
    monkeypatch.setenv("PYTEST_VERSION", "8.3.4")
    monkeypatch.setenv("CLAUDECODE", "1")
    _reset_agent_cache()

    assert is_agent_mode() is False


def test_explicitly_falsy_suppression_variable_does_not_suppress(
    real_suppression: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Dropped from the test body, not a fixture: pytest re-sets `PYTEST_CURRENT_TEST` for each phase.
    for env_var in _SUPPRESSION_ENV_VARS:
        monkeypatch.delenv(env_var, raising=False)
    monkeypatch.setenv("RICH_CODEX", "0")
    monkeypatch.setenv("CLAUDECODE", "1")
    _reset_agent_cache()

    assert is_agent_mode() is True


def test_unparseable_override_falls_through(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RICH_CLICK_AGENT_MODE", "auto")
    monkeypatch.setenv("GEMINI_CLI", "")

    assert is_agent_mode() is True


@pytest.mark.parametrize("env_var", ["AI_AGENT", "AGENT"])
def test_named_agent_environment_variables(env_var: str, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(env_var, "My Custom Agent")

    assert detect_agent() == "my-custom-agent"


def test_ai_agent_precedes_agent(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_AGENT", "first-agent")
    monkeypatch.setenv("AGENT", "second-agent")

    assert detect_agent() == "first-agent"


def test_falsy_agent_value_stops_detection(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGENT", "false")
    monkeypatch.setenv("CLAUDECODE", "1")

    assert detect_agent() is None


def test_detection_is_cached_until_reset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CLAUDECODE", "1")
    assert detect_agent() == "agent"

    monkeypatch.delenv("CLAUDECODE")
    assert detect_agent() == "agent"

    _reset_agent_cache()
    assert detect_agent() is None


def test_empty_environment_returns_none() -> None:
    assert detect_agent() is None
    assert is_agent_mode() is False
