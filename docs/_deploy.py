# fmt: off
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "packaging"
# ]
# ///
import json
import os
import subprocess
from collections.abc import Sequence
from importlib.metadata import version

import packaging.version


def print_section(v: str) -> None:
    # Flushed because the subprocesses below write straight to our stdout,
    # and CI logs are block-buffered.
    print("=" * 79, flush=True)
    print(v, flush=True)
    print("=" * 79, flush=True)


def cmd(args: Sequence[str], *, capture: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    """Run a command, echoing it first.

    Output goes straight to the console unless `capture` is set, in which case it is
    returned for parsing (and only printed if the command fails). Pass `check=False`
    for commands that are expected to fail, e.g. probing for an alias that may not exist.
    """
    print_section(f"Command: {' '.join(args)}")
    pipe = subprocess.PIPE if capture else None
    res = subprocess.run(args, stdout=pipe, stderr=pipe, check=False, text=True)
    if res.returncode and capture:
        # Nothing was streamed, so surface whatever was captured.
        for name, out in [("Stdout", res.stdout), ("Stderr", res.stderr)]:
            if out and out.strip():
                print(f"{name}: {out.strip()}", flush=True)
    if check:
        res.check_returncode()
    return res


def get_series(identifier: str) -> tuple[int, int] | None:
    """(major, minor) of the version an alias/version points at, or None if it does not exist."""
    res = cmd(["mike", "list", identifier, "-j"], capture=True, check=False)
    if res.returncode or not res.stdout.strip():
        return None
    data = json.loads(res.stdout)
    major, minor, *_ = data["version"].split(".")
    return int(major), int(minor)


def deploy() -> None:
    cmd(["git", "fetch", "origin", "gh-pages:gh-pages"])
    v = packaging.version.parse(version(os.environ["PACKAGE_NAME"]))

    head = (v.major, v.minor)
    latest = get_series("latest")
    prerelease = get_series("prerelease")

    aliases = []
    if v.is_prerelease:
        if latest is None or head > latest:
            aliases.append("prerelease")
        else:
            # Docs are published per `major.minor`, so a prerelease of an already-released
            # series has nowhere of its own to go and overwrites the released docs.
            print_section(
                f"WARNING: {v} is a prerelease of {v.major}.{v.minor}, which is already released."
                f" Deploying it will overwrite the published {v.major}.{v.minor} docs."
            )

    elif latest is None or head >= latest:
        aliases.append("latest")

    cmd(["mike", "deploy", "--push", "--update-aliases", f"{v.major}.{v.minor}", *aliases])

    # `mike deploy --update-aliases` only touches the aliases it is given, so the `prerelease`
    # alias has to be removed explicitly once a release supersedes the series it points at.
    if not v.is_prerelease and prerelease is not None and head >= prerelease:
        cmd(["mike", "delete", "--push", "prerelease"])

    if latest is not None or "latest" in aliases:
        cmd(["mike", "set-default", "--push", "latest"])


if __name__ == "__main__":
    deploy()
