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


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    print(f"Running {' '.join(cmd)}")
    return subprocess.run(cmd, check=True, **kwargs)


def get_latest(versions: list[dict]) -> tuple[int, int] | None:
    for entry in versions:
        if DEFAULT_ALIAS in entry["aliases"]:
            major, minor, *_ = entry["version"].split(".")
            return int(major), int(minor)
    return None


def build(base: str, dest: Path) -> None:
    env = os.environ | {"ASTRO_BASE": base}
    run(["npm", "run", "build"], cwd=DOCS_DIR, env=env)
    if dest.is_symlink() or dest.is_file():
        dest.unlink()
    elif dest.is_dir():
        shutil.rmtree(dest)
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

            aliases = set()
            for entry in versions:
                if entry["version"] == version_id:
                    aliases.update(entry["aliases"])
            if v.is_prerelease:
                aliases.add("prerelease")
            else:
                latest = get_latest(versions)
                if latest is None or (v.major, v.minor) >= latest:
                    aliases.add(DEFAULT_ALIAS)

            run(["npm", "ci"], cwd=DOCS_DIR)
            for directory in [version_id, *sorted(aliases)]:
                build(f"{BASE_PREFIX}/{directory}", worktree / directory)

            versions = [e for e in versions if e["version"] != version_id]
            for entry in versions:
                entry["aliases"] = [a for a in entry["aliases"] if a not in aliases]
            versions.append({"version": version_id, "title": version_id, "aliases": sorted(aliases)})
            versions.sort(key=lambda e: packaging.version.parse(e["version"]), reverse=True)
            versions_file.write_text(json.dumps(versions, indent=2) + "\n")

            index = worktree / "index.html"
            if not index.exists():
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
            run(["git", "worktree", "remove", "--force", str(worktree)])


if __name__ == "__main__":
    deploy()
