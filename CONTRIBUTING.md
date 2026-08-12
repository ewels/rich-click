# Contributing

Contributions and suggestions for new features are welcome, as are bug reports!
Please create a new [issue](https://github.com/ewels/rich-click/issues)
or better still, dive right in with a pull-request.

## Local setup

Requirements:

- `uv` https://docs.astral.sh/uv/getting-started/installation/

```shell
uv python pin 3.13
uv venv .venv
source .venv/bin/activate
uv sync --all-groups
prek install
```

## Prek

We use [prek](https://github.com/j178/prek) to manage our git hooks.
It is installed as part of `uv sync --all-groups`, and it is configured in
[`prek.toml`](https://github.com/ewels/rich-click/blob/main/prek.toml).

`prek install` sets up the git hook, so the checks run automatically whenever you commit.
To run every hook against the whole repo without committing, use:

```shell
prek run -a
```

> [!NOTE]
> We used to use [pre-commit](https://pre-commit.com/) with a `.pre-commit-config.yaml` file.
> If you set up your local checkout before that change, re-run `prek install` to replace the
> old hook — otherwise the stale `pre-commit` hook will no longer find a config it recognises.

`prek.toml` contains the following hooks:

- [actionlint](https://github.com/rhysd/actionlint): lints our GitHub Actions workflow files.
- [pyproject-fmt](https://pyproject-fmt.readthedocs.io/): formats and normalizes `pyproject.toml`.
- [Ruff](https://docs.astral.sh/ruff/): does linting checks (including import sorting) and automatically fixes what it can.
- [Ruff format](https://docs.astral.sh/ruff/formatter/): automatically formats your code to a standardized Python format.
- [mypy](http://mypy-lang.org/): static type checker which verifies you are not using objects incorrectly.
- [codespell](https://github.com/codespell-project/codespell): catches common spelling mistakes in the docs.

As mentioned, some of these tools automatically fix your code while other only highlight potential issues.
Sometimes it will be enough to try to commit a second time and it will pass, while other times it may require
manual changes to your code.

In rare cases it may be difficult or undesirable to change to code to pass the linting rules.
If this happens, it's ok to add a Ruff `# noqa` or mypy `# type: ignore` comment to skip that line.
For details of how to do this, please see the [Ruff docs](https://docs.astral.sh/ruff/linter/#error-suppression)
and [mypy docs](https://mypy.readthedocs.io/en/stable/common_issues.html#spurious-errors-and-locally-silencing-the-checker).

## Credits

This package was written by Phil Ewels ([@ewels](http://github.com/ewels/)),
based on initial code by Will McGugan ([@willmcgugan](https://github.com/willmcgugan)).

rich-click is co-maintained by Daniel Reeves ([@dwreeves](http://github.com/dwreeves/)).

Furthermore, these contributors helped make the package what it is today:

- [@BrutalSimplicity](https://github.com/BrutalSimplicity)
- [@harens](http://github.com/harens/)
- [@fridex](http://github.com/fridex/)
- [@pawamoy](http://github.com/pawamoy/)
- [@jorrick](http://github.com/harens/)

See the full list of contributors [here](https://github.com/ewels/rich-click/graphs/contributors).
