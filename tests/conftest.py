# flake8: noqa D*
import importlib
import json
import os
import re
from dataclasses import asdict
from importlib import reload
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, cast, Dict, Optional, Type, Union

import click
import pytest
from click.testing import CliRunner, Result
from typing_extensions import Protocol

import rich_click.rich_click as rc
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_8X
from rich_click.rich_command import RichCommand, RichGroup
from rich_click.rich_help_configuration import OptionHighlighter, RichHelpConfiguration


@pytest.fixture
def root_dir() -> Path:
    return Path(__file__).parent


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def tmpdir(root_dir: Path) -> Path:
    return root_dir / "tmp"


@pytest.fixture
def expectations_dir(root_dir: Path) -> Path:
    return root_dir / "expectations"


@pytest.fixture
def click_major_version() -> int:
    return int(click.__version__.split(".")[0])


class AssertStr(Protocol):
    def __call__(self, actual: str, expectation: Union[str, Path]) -> None:
        """Assert strings by normalizining line endings

        Args:
            actual: actual result
            expectation: expected result `str` or `Path` to load result
        """
        ...


@pytest.fixture
def assert_str(request: pytest.FixtureRequest, tmpdir: Path) -> Callable[[str, Union[str, Path]], None]:
    def assertion(actual: str, expectation: Union[str, Path]) -> None:
        if isinstance(expectation, Path):
            if expectation.exists():
                expected = expectation.read_text()
            else:
                expected = ""
        else:
            expected = expectation
        normalized_expected = "\n".join([line.strip() for line in expected.strip().splitlines() if line.strip()])
        normalized_actual = "\n".join([line.strip() for line in actual.strip().splitlines() if line.strip()])

        try:
            assert normalized_expected == normalized_actual
        except Exception:
            tmpdir.mkdir(parents=True, exist_ok=True)
            tmppath = tmpdir / f"{request.node.name}.out"
            tmppath.write_text(actual.strip())
            raise

    return assertion


class AssertDicts(Protocol):
    def __call__(self, actual: Dict[str, Any], expectation: Union[Path, Dict[str, Any]]) -> None:
        """Assert two dictionaries by normalizing as json

        Args:
            actual: actual result
            expectation: expected result `Dict` or `Path` to load result
        """
        ...


@pytest.fixture
def assert_dicts(request: pytest.FixtureRequest, tmpdir: Path) -> AssertDicts:
    def load_obj(s: str) -> Any:
        return json.loads(s)

    def dump_obj(obj: Any) -> str:
        return json.dumps(obj, indent=4)

    def roundtrip(obj: Any) -> Any:
        return load_obj(dump_obj(obj))

    def assertion(actual: Dict[str, Any], expectation: Union[Path, Dict[str, Any]]) -> None:
        if isinstance(expectation, Path):
            if expectation.exists():
                expected = load_obj(expectation.read_text())
            else:
                expected = {}
        else:
            expected = expectation

        # need to perform a roundtrip to convert to
        # supported json data types (i.e. tuple -> list, datetime -> str, etc...)
        actual = roundtrip(actual)

        try:
            assert actual == expected
        except Exception:
            tmpdir.mkdir(parents=True, exist_ok=True)
            tmppath = tmpdir / f"{request.node.name}.config.json"
            with tmppath.open("w") as stream:
                stream.write(dump_obj(actual))
            raise

    return assertion


@pytest.fixture(autouse=True)
def initialize_rich_click() -> None:
    """Initialize `rich_click` module."""
    # to isolate module-level configuration we
    # must reload the rich_click module between
    # each test
    reload(rc)
    # default config settings from https://github.com/Textualize/rich/blob/master/tests/render.py
    rc.WIDTH = 100
    rc.COLOR_SYSTEM = None
    rc.FORCE_TERMINAL = True


class CommandModuleType(ModuleType):
    cli: RichCommand


class LoadCommandModule(Protocol):
    def __call__(self, namespace: str) -> CommandModuleType:
        """Dynamically loads a rich cli fixture.

        Args:
            namespace: Namespace of the rich cli module under test.
                Example: fixtures.arguments
        """
        ...


re_link_ids = re.compile(r"id=[\d.\-]*?;.*?\x1b")


def replace_link_ids(render: str) -> str:
    """Link IDs have a random ID and system path which is a problem for
    reproducible tests.

    From: https://github.com/Textualize/rich/blob/master/tests/render.py
    """
    return re_link_ids.sub("id=0;foo\x1b", render)


@pytest.fixture
def load_command() -> LoadCommandModule:
    def load(namespace: str) -> CommandModuleType:
        module = importlib.import_module(namespace)
        reload(module)
        return cast(CommandModuleType, module)

    return load


class InvokeCli(Protocol):
    def __call__(self, cmd: click.Command, *args: Any, **kwargs: Any) -> Result:
        """Invoke click command.

        Small convenience fixture to allow invoking a click Command
        without standalone mode.

        Args:
            cmd: Click Command
        """
        ...


@pytest.fixture
def invoke() -> InvokeCli:
    runner = CliRunner()

    def invoke(cmd: click.Command, *args: Any, **kwargs: Any) -> Result:
        result = runner.invoke(cmd, *args, **kwargs)
        return result

    return invoke


class AssertRichFormat(Protocol):
    def __call__(
        self,
        cmd: Union[str, RichCommand, RichGroup],
        args: str,
        error: Optional[Type[Exception]],
        rich_config: Optional[Callable[[Any], Union[RichGroup, RichCommand]]],
    ) -> None:
        """Invokes the cli command and applies assertions against the results

        This command resolves the cli application from the fixtures directory dynamically
        to isolate module configuration state between tests. It will also assert that
        the configuration (input), stdout (output) are as expected.

        If an assertion fails. It will dump the output into a tmp directory under the test
        folder with the name of the the test. The idea is that you can then validate the
        output visually, and once satisfied, copy it into the expectations folder.

        NOTE: This could be made better by dumping Rich's render tree as a dictionary.
        Currently it only asserts the output from the string rendered by Rich Console.
        This means it may miss cases where assertion of styles is desired.

        Args:
            cmd: The name of the module under test, or a `RichCommand` or `RichGroup` object.
                If given a module name. This module must have a module-level
                `cli` attribute that resolves to a Rich Command or Group
            args: The arguments to invoke the command with
            error: Optional exception to assert
            rich_config: Optional rich_config function to be applied to the command
        """
        ...


@pytest.fixture
def assert_rich_format(
    request: pytest.FixtureRequest,
    expectations_dir: Path,
    invoke: InvokeCli,
    load_command: LoadCommandModule,
    assert_dicts: AssertDicts,
    assert_str: AssertStr,
    click_major_version: int,
) -> AssertRichFormat:
    def config_to_dict(config: RichHelpConfiguration) -> Dict[Any, Any]:
        config_dict = asdict(config)
        config_dict["highlighter"] = cast(OptionHighlighter, config.highlighter).highlights
        return config_dict

    def assertion(
        cmd: Union[str, RichCommand],
        args: str,
        error: Optional[Type[Exception]],
        rich_config: Optional[Callable[[Any], RichCommand]],
    ) -> None:
        if isinstance(cmd, str):
            command = load_command(f"fixtures.{cmd}").cli
        else:
            command = cmd

        if rich_config:
            command = rich_config(command)
            help_config: Optional[RichHelpConfiguration] = command.context_settings.get("rich_help_config")
            if help_config:
                help_config.color_system = rc.COLOR_SYSTEM
                help_config.width = rc.WIDTH
                help_config.max_width = rc.MAX_WIDTH
                help_config.force_terminal = rc.FORCE_TERMINAL

        if error:
            result_nonstandalone = invoke(command, args, standalone_mode=False)
            assert isinstance(result_nonstandalone.exception, error)
            assert result_nonstandalone.exit_code != 0

        result = invoke(command, args)
        actual = replace_link_ids(result.stdout)

        expectation_output_path = expectations_dir / f"{request.node.name}-click{click_major_version}.out"
        expectation_config_path = expectations_dir / f"{request.node.name}-click{click_major_version}.config.json"
        if os.getenv("UPDATE_EXPECTATIONS"):
            with open(expectation_output_path, "w") as stream:
                stream.write(actual)
        assert_str(actual, expectation_output_path)
        if os.getenv("UPDATE_EXPECTATIONS"):
            with open(expectation_config_path, "w") as stream:
                if command.help_config is not None:
                    stream.write(json.dumps(config_to_dict(command.help_config), indent=2) + "\n")
        if command.help_config is not None:
            assert_dicts(config_to_dict(command.help_config), expectation_config_path)
        else:
            pass
            # TODO: uncomment below out
            # assert not os.path.exists(expectation_config_path)

    return assertion
