"""
Diagnosis of Click usage errors: work out *which rule was broken*, not just that one was.

Click's stock usage errors report the symptom -- ``No such option: --repo`` -- and stop there. A human
reads that, remembers where the flag lives and moves on. An LLM agent driving the CLI often cannot: an
error that does not state the rule gives it nothing to correct against, so it retries variations of the
same broken invocation until it runs out of turns. An error that *does* state the rule ("``--repo`` is
an option of the parent group") is usually fixed on the very next attempt.

So this module computes a :class:`Diagnosis` once -- the violated rule, near matches over the command's
real names, valid choices, and a corrected invocation where one can be built confidently -- and leaves
the presenting to two renderers: a terse addition to the rich error panel for humans (in
``rich_help_rendering``), and the fuller plain-text block below for agents. Both describe the same
diagnosis; only the verbosity and the styling differ.

Everything here is strictly additive. Exit codes are untouched, the original Click message is still the
first thing emitted, and a usage error this module cannot say anything useful about produces no
diagnosis at all (see :func:`diagnose` returning ``None``) rather than padding the output with guesses.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from difflib import get_close_matches
from typing import Any

import click

from rich_click.utils import truthy


#: Click's "no such command" message, from which the offending name is recovered. Click raises this
#: through the generic ``ctx.fail()``, so there is no exception type to key off. The pattern is
#: deliberately loose, but a translated (non-English) message simply will not match -- which yields no
#: diagnosis, exactly like any other error we cannot speak to.
_NO_SUCH_COMMAND = re.compile(r"""[Nn]o such command ['"`](?P<name>[^'"`]+)['"`]""")

#: The offending value in Click's ``Choice`` failure message ("'x' is not one of 'a', 'b'.").
_NOT_ONE_OF = re.compile(r"""^['"`]?(?P<value>.+?)['"`]? is not one of""")

#: How many near matches to offer. Enough to cover a genuine typo; few enough that the list still reads
#: as a suggestion rather than a dump of the command's surface.
_MAX_SUGGESTIONS = 3


@dataclass
class Diagnosis:
    """
    What can be said about a usage error beyond the fact that it happened.

    Every field is optional: a diagnosis carries whichever parts could be derived with confidence, and
    the renderers skip the rest. A diagnosis with nothing in it is falsy, and is never rendered.
    """

    rule: str | None = None
    """The violated rule, stated as a rule -- the part an agent can actually correct against."""

    suggestions: list[str] = field(default_factory=list)
    """Near matches over the command's real names, or over the valid values of a choice."""

    correction: str | None = None
    """A corrected invocation, copyable as-is. Only set when it can be constructed confidently."""

    help_command: str | None = None
    """The ``--help`` invocation that documents the rule, when it is not the one already suggested."""

    def __bool__(self) -> bool:
        """Report whether anything useful was derived."""
        return bool(self.rule or self.suggestions or self.correction)


def diagnosis_enabled(config: Any) -> bool:
    """
    Report whether error diagnosis is switched on.

    The ``RICH_CLICK_ERROR_DIAGNOSIS`` environment variable outranks the ``error_diagnosis`` config
    option in both directions, so the behaviour can be toggled per-run -- for A/B benchmarking, or to
    get Click's bare messages back without touching the CLI's own source.
    """
    override = truthy(os.getenv("RICH_CLICK_ERROR_DIAGNOSIS"))
    if override is not None:
        return override
    return bool(getattr(config, "error_diagnosis", True))


def _params(ctx: click.Context) -> list[click.Parameter]:
    """Return a command's parameters, or nothing if it cannot report them off-cycle."""
    try:
        return list(ctx.command.get_params(ctx))
    except Exception:  # pragma: no cover - defensive: a custom command may need real parse state
        return []


def _option_names(ctx: click.Context, *, exclude_help: bool = False) -> list[str]:
    """
    Return every option name (including negation flags) the command actually accepts.

    ``exclude_help`` drops the help flag when offering near matches: ``--help`` is close enough to a lot
    of typos to keep surfacing as a suggestion, and it is never the option the caller was reaching for.
    """
    skip = set(ctx.help_option_names) if exclude_help else set()
    names: list[str] = []
    for param in _params(ctx):
        if isinstance(param, click.Option):
            names.extend(
                name for name in [*param.opts, *param.secondary_opts] if name.startswith("-") and name not in skip
            )
    return names


def _find_option(ctx: click.Context, name: str) -> click.Option | None:
    """Return the option a name belongs to on this command, if any."""
    for param in _params(ctx):
        if isinstance(param, click.Option) and name in [*param.opts, *param.secondary_opts]:
            return param
    return None


def _command_names(ctx: click.Context) -> list[str]:
    """Return the subcommand names (and aliases) the command accepts."""
    list_commands = getattr(ctx.command, "list_commands", None)
    if list_commands is None:
        return []
    try:
        names = list(list_commands(ctx))
    except Exception:  # pragma: no cover - defensive: a lazily-loaded group may need real args
        return []
    names.extend(getattr(ctx.command, "_alias_mapping", {}))
    return names


def _choices(param: click.Parameter | None) -> list[str]:
    """Return the valid values of a ``Choice``-typed parameter, or nothing."""
    choices = getattr(getattr(param, "type", None), "choices", None)
    return [str(choice) for choice in choices] if choices else []


def _param_label(error: click.BadParameter, ctx: click.Context) -> str | None:
    """Name the parameter a bad-value error is about, quoted the way the rest of the diagnosis quotes."""
    label: Any = None
    if error.param_hint is not None:
        label = error.param_hint if isinstance(error.param_hint, str) else " / ".join(error.param_hint)
    elif error.param is not None:
        label = error.param.get_error_hint(ctx) or error.param.name
    if not label:
        return None
    return f"'{str(label).strip(chr(39))}'"


def _value_metavar(param: click.Option, ctx: click.Context) -> str:
    """Return the placeholder to show after an option in a corrected invocation."""
    from rich_click.help_json import _param_metavar

    metavar = _param_metavar(param, ctx)
    return f" {metavar}" if metavar else ""


def _diagnose_unknown_option(error: click.NoSuchOption, ctx: click.Context) -> Diagnosis | None:
    """
    Diagnose an option the command does not accept.

    The parent-group case is checked first and deliberately: Click parses a group's options strictly
    *before* the subcommand name, so a flag written after the subcommand fails with a bare "no such
    option" even though the flag exists and is spelled correctly. Nothing in that message hints that the
    fix is to move the flag, which makes it one of the most reliable ways to get an agent stuck.
    """
    name = error.option_name

    parent = ctx.parent
    while parent is not None:
        owner = _find_option(parent, name)
        if owner is not None:
            tail = ctx.command_path[len(parent.command_path) :].strip()
            correction = " ".join(
                piece for piece in [parent.command_path, f"{name}{_value_metavar(owner, parent)}", tail, "..."] if piece
            )
            return Diagnosis(
                rule=(
                    f"'{name}' is an option of the parent group '{parent.command_path}', not of "
                    f"'{ctx.command_path}'. A group's options must be given before its subcommand."
                ),
                correction=correction,
                help_command=f"{parent.command_path} --help",
            )
        parent = parent.parent

    # No corrected invocation here: knowing the intended flag says nothing about the value it wants or
    # the arguments around it, and a half-built command line is worse than none.
    suggestions = get_close_matches(name, _option_names(ctx, exclude_help=True), n=_MAX_SUGGESTIONS)
    if not suggestions:
        return None
    return Diagnosis(rule=f"'{name}' is not an option of '{ctx.command_path}'.", suggestions=suggestions)


def _diagnose_unknown_command(error: click.UsageError, ctx: click.Context) -> Diagnosis | None:
    """
    Diagnose a subcommand name the group does not know, offering near matches over the real ones.

    Click raises this through the generic ``ctx.fail()``, so there is no exception type to key off and
    the name has to be recovered from the message. The group check comes first to keep that regex away
    from the errors it has no business reading: a leaf command cannot have an unknown subcommand, so
    every ``ctx.fail()`` a leaf's own callback raises is left alone.
    """
    if getattr(ctx.command, "list_commands", None) is None:
        return None
    match = _NO_SUCH_COMMAND.search(error.format_message())
    if match is None:
        return None
    name = match.group("name")
    suggestions = get_close_matches(name, _command_names(ctx), n=_MAX_SUGGESTIONS)
    if not suggestions:
        # "'x' is not a command of 'cli'" only restates "No such command 'x'", and the help pointer is
        # already on screen. Nothing to add, so nothing is added.
        return None
    # The single best match *is* the correction, so it is offered as one rather than repeated as both a
    # suggestion and a corrected invocation.
    return Diagnosis(
        rule=f"'{name}' is not a command of '{ctx.command_path}'.",
        suggestions=suggestions[1:],
        correction=f"{ctx.command_path} {suggestions[0]}",
    )


def _diagnose_missing_parameter(error: click.MissingParameter, ctx: click.Context) -> Diagnosis | None:
    """State a missing required parameter as the rule it is, and list its values if it takes a fixed set."""
    label = _param_label(error, ctx)
    if label is None:
        return None
    choices = _choices(error.param)
    rule = f"{label} is required." if not choices else f"{label} is required, and must be one of: {', '.join(choices)}."
    return Diagnosis(rule=rule)


def _diagnose_bad_value(error: click.BadParameter, ctx: click.Context) -> Diagnosis | None:
    """Diagnose a value a parameter rejected, spelling out the valid set when there is one."""
    choices = _choices(error.param)
    if not choices:
        return None
    label = _param_label(error, ctx) or "the value"
    diagnosis = Diagnosis(rule=f"{label} must be one of: {', '.join(choices)}.")
    match = _NOT_ONE_OF.match(error.message)
    if match is not None:
        near = get_close_matches(match.group("value"), choices, n=1)
        if near:
            diagnosis.suggestions = near
    return diagnosis


def diagnose(error: click.UsageError) -> Diagnosis | None:
    """
    Work out what rule a usage error broke, or return ``None`` when nothing can be said.

    ``None`` is the common and correct outcome for an error that already states its own rule -- a
    ``ctx.fail("exactly one seeding option is required")`` from a callback needs no help from us -- so
    diagnosis stays silent rather than restating what the message already says.
    """
    ctx = getattr(error, "ctx", None)
    if ctx is None:
        return None

    diagnosis: Diagnosis | None
    if isinstance(error, click.NoSuchOption):
        diagnosis = _diagnose_unknown_option(error, ctx)
    elif isinstance(error, click.MissingParameter):
        # Checked before BadParameter, which it subclasses.
        diagnosis = _diagnose_missing_parameter(error, ctx)
    elif isinstance(error, click.BadParameter):
        diagnosis = _diagnose_bad_value(error, ctx)
    else:
        diagnosis = _diagnose_unknown_command(error, ctx)
    return diagnosis or None


def format_diagnosis_for_agent(error: click.UsageError, diagnosis: Diagnosis | None, argv: list[str] | None) -> str:
    """
    Render an error for an AI agent: plain text, no ANSI, one fact per line.

    Deliberately fuller than the human rendering. A human has the terminal scrollback and knows what
    they just typed; an agent gets only this block, so it restates the attempted invocation, the rule,
    the alternatives and the corrected command as separate ``Key: value`` lines that survive being
    grepped, split or pasted. Click's own message stays the first line, unchanged, so anything matching
    on it keeps working.
    """
    lines = [f"Error: {error.format_message()}", ""]
    if argv:
        lines.append(f"Attempted: {' '.join(argv)}")
    if diagnosis is not None:
        if diagnosis.rule:
            lines.append(f"Rule: {diagnosis.rule}")
        if diagnosis.correction:
            lines.append(f"Try: {diagnosis.correction}")
        if diagnosis.suggestions:
            lines.append(f"Did you mean: {', '.join(diagnosis.suggestions)}")

    ctx = getattr(error, "ctx", None)
    if ctx is not None:
        lines.append(f"Usage: {' '.join([ctx.command_path, *ctx.command.collect_usage_pieces(ctx)])}")
        help_command = (diagnosis.help_command if diagnosis is not None else None) or f"{ctx.command_path} --help"
        lines.append(f"Help: {help_command}")
    return "\n".join(lines)
