"""Run the test suite against every supported click / rich / typer combination.

Each combination runs in its own throwaway uv environment, one per CPU core, so one
CI runner can work through the whole matrix for a Python version. Run it from the
repo root after `uv sync`: `python .github/scripts/test_matrix.py`
"""

from __future__ import annotations

import itertools
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


CLICK = ["8.0", "8.1", "8.2", "8.3", "8.4", "8.5"]
RICH = ["12", "13", "14", "15"]
TYPER = ["0.17", "0.25"]

PASS = "\033[30;42m PASS \033[0m"
FAIL = "\033[97;41m FAIL \033[0m"
# ANSI colours for the counts in pytest's summary line: green, red, dim and yellow.
# Plurals ("3 warnings") match the singular keys once the trailing s is stripped.
COLOURS = {"passed": "32", "failed": "31", "error": "31", "skipped": "2", "warning": "33"}

Combo = tuple[str, str, str]


def combos() -> list[Combo]:
    """List the click, rich and typer versions to test together.

    Returns:
        One (click, rich, typer) version tuple per combination.
    """
    result = []
    for click, rich, typer in itertools.product(CLICK, RICH, TYPER):
        # Typer 0.25 is only tested against click>=8.3 and rich>=13.
        if typer == "0.25" and (rich == "12" or click in ("8.0", "8.1", "8.2")):
            continue
        result.append((click, rich, typer))
    return result


def run_combo(combo: Combo) -> tuple[Combo, int, str]:
    """Run the test suite with one combination installed.

    Args:
        combo: The click, rich and typer versions to install.

    Returns:
        The combination, pytest's exit code and its output.
    """
    click, rich, typer = combo
    cmd = ["uv", "run", "--no-sync", "--prerelease=allow"]
    cmd += [f"--with=click=={click}.*", f"--with=rich=={rich}.*", f"--with=typer=={typer}.*"]
    # `-o addopts=` drops the verbose, coverage-enabled options in pyproject.toml.
    # Parallel runs share the working directory, so skip pytest's cache too.
    cmd += ["pytest", "-q", "-o", "addopts=", "--showlocals", "-p", "no:cacheprovider"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return combo, proc.returncode, proc.stdout


def summary(output: str) -> str:
    """Colour the counts from pytest's last line, e.g. "207 passed, 21 skipped, 1 warning in 5.3s".

    Args:
        output: pytest's output.

    Returns:
        The counts with ANSI colours, or an empty string if pytest didn't get that far.
    """
    lines = [line for line in output.splitlines() if re.search(r"\d+ (passed|failed|errors?)\b", line)]
    if not lines:
        return ""
    counts = re.sub(r" in [\d.]+s.*", "", lines[-1].strip("= "))
    return re.sub(r"\d+ (\w+)", lambda m: f"\033[{COLOURS.get(m[1].rstrip('s'), '0')}m{m[0]}\033[0m", counts) + "."


def main() -> int:
    """Run all combinations and report the ones that failed.

    Returns:
        0 if every combination passed, otherwise 1.
    """
    todo = combos()
    failed = []
    print(f"Testing {len(todo)} click / rich / typer combinations", flush=True)
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as pool:
        for future in as_completed(pool.submit(run_combo, combo) for combo in todo):
            combo, returncode, output = future.result()
            label = "click {} / rich {} / typer {}".format(*combo)
            if returncode == 0:
                print(f"::group::{PASS} {summary(output)} {label}\n{output.rstrip()}\n::endgroup::", flush=True)
            else:
                failed.append(label)
                print(f"{FAIL} {summary(output)} {label}\n{output.rstrip()}")
                print(f"::error title=Tests failed::{label}", flush=True)

    if failed:
        print(f"\n{len(failed)} of {len(todo)} combinations failed:", *sorted(failed), sep="\n  ")
        return 1
    print(f"\nAll {len(todo)} combinations passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
