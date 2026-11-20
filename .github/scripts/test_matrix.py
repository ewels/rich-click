"""Run the test suite against every supported click / rich / typer combination.

Each combination runs in its own throwaway uv environment, several at once, so one CI
runner can work through the whole matrix for a Python version. Run it from the repo
root after `uv sync`:

    python .github/scripts/test_matrix.py
"""

from __future__ import annotations

import argparse
import itertools
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


CLICK = ["8.0.*", "8.1.*", "8.2.*", "8.3.*", "8.4.*", "8.5.*"]
RICH = ["12.*", "13.*", "14.*", "15.*"]
TYPER = ["0.17.*", "0.25.*"]

Combo = tuple[str, str, str]


def combos() -> list[Combo]:
    """List the click, rich and typer versions to test together.

    Returns:
        One (click, rich, typer) version spec tuple per combination.
    """
    result = []
    for click, rich, typer in itertools.product(CLICK, RICH, TYPER):
        # Typer 0.25 is only tested against click>=8.3 and rich>=13.
        if typer == "0.25.*" and (rich == "12.*" or click in ("8.0.*", "8.1.*", "8.2.*")):
            continue
        result.append((click, rich, typer))
    return result


def run_combo(combo: Combo) -> tuple[Combo, int, str, float]:
    """Run the test suite with one combination installed.

    Args:
        combo: The click, rich and typer version specs to install.

    Returns:
        The combination, pytest's exit code, its combined output and the run time.
    """
    click, rich, typer = combo
    cmd = [
        "uv",
        "run",
        "--no-sync",
        "--prerelease=allow",
        f"--with=click=={click}",
        f"--with=rich=={rich}",
        f"--with=typer=={typer}",
        "pytest",
        # Override the verbose, coverage-enabled addopts from pyproject.toml.
        "-o",
        "addopts=",
        "-q",
        "--showlocals",
        # Parallel runs share the working directory, so skip the shared cache.
        "-p",
        "no:cacheprovider",
    ]
    start = time.monotonic()
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return combo, proc.returncode, proc.stdout, time.monotonic() - start


def main() -> int:
    """Run all combinations and report the ones that failed.

    Returns:
        0 if every combination passed, otherwise 1.
    """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-j", "--jobs", type=int, default=os.cpu_count() or 1, help="combinations to run at once")
    args = parser.parse_args()

    in_actions = os.environ.get("GITHUB_ACTIONS") == "true"
    todo = combos()
    failed: list[Combo] = []
    print(f"Running {len(todo)} click / rich / typer combinations, {args.jobs} at a time", flush=True)

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for future in as_completed(pool.submit(run_combo, c) for c in todo):
            combo, returncode, output, duration = future.result()
            label = "click {} / rich {} / typer {}".format(*combo)
            if returncode == 0:
                summary = output.strip().splitlines()[-1] if output.strip() else ""
                if in_actions:
                    print(f"::group::PASS {label} ({duration:.1f}s) {summary}")
                    print(output)
                    print("::endgroup::", flush=True)
                else:
                    print(f"PASS {label} ({duration:.1f}s) {summary}", flush=True)
            else:
                failed.append(combo)
                print(f"\n{'=' * 30} FAIL {label} ({duration:.1f}s) {'=' * 30}")
                print(output, flush=True)
                if in_actions:
                    print(f"::error title=Tests failed::{label}", flush=True)

    if failed:
        print(f"\n{len(failed)} of {len(todo)} combinations failed:")
        for combo in sorted(failed):
            print("  click {} / rich {} / typer {}".format(*combo))
        return 1
    print(f"\nAll {len(todo)} combinations passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
