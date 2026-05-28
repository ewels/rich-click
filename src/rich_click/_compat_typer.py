from __future__ import annotations

import warnings

import typer


try:
    with warnings.catch_warnings():
        warnings.simplefilter(category=DeprecationWarning, action="ignore")
        typer_version: str = typer.__version__
except Exception:
    TYPER_IS_BEFORE_VERSION_026 = True
else:
    typer_version, _, _ = typer_version.partition("+")
    _major = int(typer_version.split(".")[0])
    _minor = int(typer_version.split(".")[1])
    _patch = int(typer_version.split(".")[2])

    TYPER_IS_BEFORE_VERSION_026 = (_major, _minor, _patch) < (0, 26, 0)
