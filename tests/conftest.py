import os
from pathlib import Path
from typing import Any, Callable

import pytest
from click.testing import CliRunner, Result
from typing_extensions import Protocol


@pytest.fixture
def root_dir():
    return Path(__file__).parent


@pytest.fixture
def fixtures_dir():
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def tmpdir(root_dir: Path):
    tmpdir = root_dir / "tmp"
    tmpdir.mkdir(parents=True, exist_ok=True)
    return tmpdir


@pytest.fixture
def assert_str(request: pytest.FixtureRequest, tmpdir: Path):
    def assertion(actual: str, expected: str):
        normalized_expected = [line.strip() for line in expected.strip().splitlines() if line.strip()]
        normalized_actual = [line.strip() for line in actual.strip().splitlines() if line.strip()]

        try:
            assert normalized_expected == normalized_actual
        except Exception:
            tmppath = tmpdir / f"{request.node.name}.out"
            tmppath.write_text(actual.strip())
            raise

    return assertion


class InvokeCli(Protocol):
    def __call__(self, cmd: Callable[..., Any], *args: str) -> Result:
        ...


@pytest.fixture
def invoke():
    runner = CliRunner()

    def invoke(cmd, *args, **kwargs):
        result = runner.invoke(cmd, *args, **kwargs, standalone_mode=False)
        if result.exception:
            raise result.exception
        return result

    return invoke
