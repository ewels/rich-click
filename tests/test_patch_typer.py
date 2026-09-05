"""Tests for rich_click.patch.patch_typer()'s Typer version compatibility handling."""

from __future__ import annotations

import warnings

import pytest
import typer.core
from pytest import MonkeyPatch

import rich_click._compat_typer as compat_typer
import rich_click.patch as patch_module


def test_patch_typer_does_not_warn_when_typer_supports_patching(monkeypatch: MonkeyPatch) -> None:
    """When Typer's own internals are compatible with patching, no compatibility warning should fire."""
    monkeypatch.setattr(compat_typer, "TYPER_IS_BEFORE_VERSION_026", True)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        patch_module.patch_typer()

    assert not any("may not support rich-click patching" in str(w.message) for w in caught)


def test_patch_typer_warns_when_typer_is_incompatible(monkeypatch: MonkeyPatch) -> None:
    """When Typer's version is flagged as incompatible, patch_typer() should warn about it."""
    monkeypatch.setattr(compat_typer, "TYPER_IS_BEFORE_VERSION_026", False)

    with pytest.warns(RuntimeWarning, match="may not support rich-click patching"):
        patch_module.patch_typer()


def test_patch_typer_falls_back_gracefully_on_metaclass_conflict(monkeypatch: MonkeyPatch) -> None:
    """
    Simulate the failure mode seen with Typer>=0.26.

    Typer>=0.26 vendors its own internal fork of Click, so building the patched subclass
    raises a metaclass conflict. patch_typer() should catch it, warn, and leave Typer's
    classes untouched instead of crashing the caller's CLI.
    """

    class _UnrelatedMeta(type):
        pass

    class _DummyTyperCommand(metaclass=_UnrelatedMeta):
        pass

    monkeypatch.setattr(compat_typer, "TYPER_IS_BEFORE_VERSION_026", False)
    monkeypatch.setattr(typer.core, "TyperCommand", _DummyTyperCommand, raising=False)

    with pytest.warns(RuntimeWarning, match="Failed to patch Typer"):
        patch_module.patch_typer()

    # Typer's class (the dummy, standing in for the real vendored one) must be left untouched.
    assert typer.core.TyperCommand is _DummyTyperCommand  # type: ignore[comparison-overlap]
