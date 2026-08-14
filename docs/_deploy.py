# fmt: off
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "packaging"
# ]
# ///
"""Build and deploy the Astro docs site to GitHub Pages.

Replaces the previous mike-based deploy while keeping the same gh-pages layout:
each X.Y version lives in its own directory, with `latest` (and `prerelease`)
as additional deployed copies, tracked in a mike-format versions.json. Old
mkdocs-built versions are left untouched.

The site is built once per deployed directory because the Astro `base` path is
baked into every URL at build time (see ASTRO_BASE in docs/astro.config.mjs).
"""
import json
import os
import shutil
import subprocess
import tempfile
from importlib.metadata import version
from pathlib import Path

import packaging.version

DOCS_DIR = Path(__file__).parent.resolve()
# Must stay in sync with the default `base` in astro.config.mjs
# (BASE_PREFIX/DEFAULT_ALIAS compose the ASTRO_BASE passed to each build).
BASE_PREFIX = "/rich-click"
DEFAULT_ALIAS = "latest"
PRERELEASE_ALIAS = "prerelease"


def announce(message: str) -> None:
    # Flushed because the subprocesses below write straight to our stdout,
    # and CI logs are block-buffered.
    print("=" * 79, flush=True)
    print(message, flush=True)
    print("=" * 79, flush=True)


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    announce(f"Command: {' '.join(cmd)}")
    return subprocess.run(cmd, check=True, **kwargs)


def get_series(versions: list[dict], identifier: str) -> tuple[int, int] | None:
    """(major, minor) of the version an alias or version id points at, or None if absent."""
    for entry in versions:
        if entry["version"] == identifier or identifier in entry["aliases"]:
            major, minor, *_ = entry["version"].split(".")
            return int(major), int(minor)
    return None


def remove(path: Path) -> None:
    """Delete a deployed directory, whether it is a real directory or a mike-era symlink."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def build(base: str, dest: Path, docs_versions: str) -> None:
    env = os.environ | {"ASTRO_BASE": base, "DOCS_VERSIONS": docs_versions}
    run(["npm", "run", "build"], cwd=DOCS_DIR, env=env)
    remove(dest)
    # Move rather than copy: the next build regenerates dist/ from scratch.
    shutil.move(DOCS_DIR / "dist", dest)


def deploy() -> None:
    v = packaging.version.parse(version(os.environ["PACKAGE_NAME"]))
    version_id = f"{v.major}.{v.minor}"

    run(["git", "fetch", "origin", "gh-pages:gh-pages"])
    with tempfile.TemporaryDirectory() as tmp:
        worktree = Path(tmp) / "gh-pages"
        run(["git", "worktree", "add", str(worktree), "gh-pages"])
        try:
            versions_file = worktree / "versions.json"
            versions = json.loads(versions_file.read_text()) if versions_file.exists() else []

            head = (v.major, v.minor)
            latest = get_series(versions, DEFAULT_ALIAS)
            prerelease = get_series(versions, PRERELEASE_ALIAS)

            # Aliases this deploy takes ownership of, carrying over any the
            # series already has, plus aliases to retire from gh-pages entirely.
            aliases = set()
            for entry in versions:
                if entry["version"] == version_id:
                    aliases.update(entry["aliases"])
            retired: set[str] = set()

            if v.is_prerelease:
                if latest is None or head > latest:
                    aliases.add(PRERELEASE_ALIAS)
                else:
                    # Docs are published per `major.minor`, so a prerelease of an already
                    # released series has nowhere of its own to go and overwrites it.
                    announce(
                        f"WARNING: {v} is a prerelease of {version_id}, which is already released."
                        f" Deploying it will overwrite the published {version_id} docs."
                    )
            else:
                if latest is None or head >= latest:
                    aliases.add(DEFAULT_ALIAS)
                # A release supersedes the prerelease alias once it is at least as new as
                # the series that alias points at — otherwise an rc series that never ships
                # a final release strands the alias forever.
                if prerelease is not None and head >= prerelease:
                    aliases.discard(PRERELEASE_ALIAS)
                    retired.add(PRERELEASE_ALIAS)

            # Update the version list first: the header's version dropdown is
            # rendered at build time from DOCS_VERSIONS (see Header.astro).
            versions = [e for e in versions if e["version"] != version_id]
            for entry in versions:
                entry["aliases"] = [a for a in entry["aliases"] if a not in aliases | retired]
            versions.append({"version": version_id, "title": version_id, "aliases": sorted(aliases)})
            versions.sort(key=lambda e: packaging.version.parse(e["version"]), reverse=True)
            docs_versions = json.dumps(versions)

            run(["npm", "ci"], cwd=DOCS_DIR)
            for directory in [version_id, *sorted(aliases)]:
                build(f"{BASE_PREFIX}/{directory}", worktree / directory, docs_versions)

            # Retire superseded aliases only once the builds have succeeded, so a failed
            # build never leaves gh-pages with the directory already gone.
            for alias in sorted(retired):
                announce(f"Retiring superseded alias: {alias}")
                remove(worktree / alias)

            versions_file.write_text(json.dumps(versions, indent=2) + "\n")

            index = worktree / "index.html"
            # Only point the site root at `latest` once such a build exists.
            if not index.exists() and (latest is not None or DEFAULT_ALIAS in aliases):
                index.write_text(
                    '<!DOCTYPE html><html><head><meta charset="utf-8">'
                    f'<meta http-equiv="refresh" content="0; url={DEFAULT_ALIAS}/">'
                    f'</head><body>Redirecting to <a href="{DEFAULT_ALIAS}/">{DEFAULT_ALIAS}/</a>...</body></html>\n'
                )

            run(["git", "add", "--all"], cwd=worktree)
            status = subprocess.run(
                ["git", "status", "--porcelain"], cwd=worktree, stdout=subprocess.PIPE, check=True
            )
            if not status.stdout.strip():
                print("No changes to deploy.")
                return
            run(["git", "commit", "-m", f"Deploy docs for {v} ({', '.join(sorted(aliases)) or version_id})"], cwd=worktree)
            run(["git", "push", "origin", "gh-pages"], cwd=worktree)
        finally:
            # Best-effort cleanup: never mask an exception from the deploy itself.
            subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], check=False)


if __name__ == "__main__":
    deploy()
