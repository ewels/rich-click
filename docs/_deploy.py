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
from importlib.metadata import version
from typing import Optional, Sequence, Tuple

import packaging.version


def print_section(v: str) -> None:
    print("=" * 79)
    print(v)
    print("=" * 79)


def print_subsection(v: str) -> None:
    print("-" * 79)
    print(v)
    print("-" * 79)


def cmd(args: Sequence[str]) -> subprocess.CompletedProcess[str]:
    print_section(f"Command: {' '.join(args)}")
    res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, text=True)
    if res.returncode:
        if res.stdout:
            print_subsection("Stdout:")
            print(res.stdout)
        if res.stderr:
            print_subsection("Stderr:")
            print(res.stderr)
        res.check_returncode()
    return res


def get_series(identifier: str) -> Optional[Tuple[int, int]]:
    """(major, minor) of the version an alias/version points at, or None if it does not exist."""
    try:
        res = cmd(["mike", "list", identifier, "-j"])
    except subprocess.SubprocessError:
        return None
    if not res.stdout.strip():
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
    elif latest is None or head >= latest:
        aliases.append("latest")

    if not v.is_prerelease and prerelease == head:
        cmd(["mike", "delete", "--push", "prerelease"])

    cmd(["mike", "deploy", "--push", "--update-aliases", f"{v.major}.{v.minor}", *aliases])

    if latest is not None or "latest" in aliases:
        cmd(["mike", "set-default", "--push", "latest"])


if __name__ == "__main__":
    deploy()
