"""Detect AI coding-agent environments."""

from __future__ import annotations

import os
import re
import sys
from functools import lru_cache
from typing import Optional, Tuple

from rich_click.utils import truthy


_AGENT_ENV_VARS: Tuple[str, ...] = (
    # Claude Code and Cowork
    "CLAUDECODE",
    "CLAUDE_CODE",
    # Cursor CLI and editor
    "CURSOR_AGENT",
    "CURSOR_TRACE_ID",
    # OpenAI Codex CLI
    "CODEX_SANDBOX",
    "CODEX_THREAD_ID",
    "CODEX_CI",
    "CODEX_SANDBOX_NETWORK_DISABLED",
    # Google Gemini CLI and Antigravity
    "GEMINI_CLI",
    "ANTIGRAVITY_AGENT",
    "ANTIGRAVITY_CLI_ALIAS",
    # GitHub Copilot
    "COPILOT_MODEL",
    "COPILOT_ALLOW_ALL",
    "COPILOT_GITHUB_TOKEN",
    # Cline
    "CLINE_ACTIVE",
    # OpenCode
    "OPENCODE",
    "OPENCODE_CLIENT",
    # Goose
    "GOOSE_PROVIDER",
    # Augment CLI
    "AUGMENT_AGENT",
    # JetBrains Junie
    "JUNIE_DATA",
    "JUNIE_SHIM_PATH",
    # Kimi
    "KIMI_PLUGIN_ROOT",
    # Grok
    "GROK_PLUGIN_ROOT",
    "GROK_PLUGIN_DATA",
    # OpenClaw
    "OPENCLAW_SHELL",
    # Replit
    "REPL_ID",
    # Trae
    "TRAE_AI_SHELL_ID",
)
"""Agent markers mirrored from Vercel's ``detect-agent`` ``agents.json``.

The generic ``AGENT`` variable follows the proposal in
``agentsmd/agents.md#136``. Keep this list synchronized with those sources.
"""


_SUPPRESSION_ENV_VARS: Tuple[str, ...] = (
    # pytest: per-test (all modern versions) and process-wide (pytest >= 8.2)
    "PYTEST_CURRENT_TEST",
    "PYTEST_VERSION",
    # rich-codex, which generates the help screenshots in our docs
    "RICH_CODEX",
)
"""Markers of tooling that captures ``--help`` output for humans to read later.

A test suite or a screenshot generator run from an agent shell inherits that shell's agent markers, but
its output is committed and compared, so it must stay human-readable. These variables suppress detection
so downstream snapshot tests and generated docs need no action from their maintainers. Anything set to an
explicitly falsy value (e.g. ``RICH_CODEX=0``) is ignored, since pytest's own variables carry values
(a test ID, a version) that are neither truthy nor falsy.
"""


def _normalize_agent_name(name: str) -> Optional[str]:
    normalized = re.sub(r"[^a-z0-9]+", "-", name.strip().lower()).strip("-")
    return normalized or None


@lru_cache(maxsize=1)
def detect_agent() -> Optional[str]:
    """Return a lowercase-hyphenated agent identifier when in agent mode."""
    override = truthy(os.getenv("RICH_CLICK_AGENT_MODE"))
    if override is True:
        return "agent"
    if override is False:
        return None

    # Only the explicit override outranks the suppression markers: everything else is a guess about the
    # environment, whereas these say the output is being captured for human consumption.
    for env_var in _SUPPRESSION_ENV_VARS:
        if env_var in os.environ and truthy(os.environ[env_var]) is not False:
            return None

    for env_var in ("AI_AGENT", "AGENT"):
        if env_var not in os.environ:
            continue
        value = os.environ[env_var]
        if not value or truthy(value) is False:
            return None
        return _normalize_agent_name(value)

    if any(env_var in os.environ for env_var in _AGENT_ENV_VARS):
        return "agent"
    if os.getenv("CURSOR_EXTENSION_HOST_ROLE") == "agent-exec":
        return "agent"
    if "kiro" in os.getenv("TERM_PROGRAM", "").lower() and not sys.stdout.isatty():
        return "agent"
    if re.search(r"(?:^|[\\/])\.pi[\\/]agent(?:[\\/]|$)", os.getenv("PATH", "")):
        return "agent"
    if os.path.exists("/opt/.devin"):
        return "agent"
    return None


def is_agent_mode() -> bool:
    """Return whether an AI coding agent was detected."""
    return detect_agent() is not None


def _reset_agent_cache() -> None:
    """Clear cached detection state."""
    detect_agent.cache_clear()
