import importlib
import sys
from pathlib import Path
from typing import Any, Callable, Dict

import pytest

from rich_click.rich_command import RichCommand


if sys.version_info < (3, 11):
    from typing_extensions import NotRequired
else:
    from typing import NotRequired


if sys.version_info < (3, 9):
    pytest.skip(reason="typing._eval_type doesn't work how we need it to before 3.9", allow_module_level=True)


def eval_type(t: Any, globalns: Dict[str, Any], localns: Dict[str, Any]) -> Any:
    import typing

    if sys.version_info >= (3, 12):
        return typing._eval_type(t, globalns, localns, type_params=None)  # type: ignore[attr-defined]
    else:
        return typing._eval_type(t, globalns, localns)  # type: ignore[attr-defined]


def test_config_typed_dict_annotations(mock_script_writer: Callable[[str, str], Path]) -> None:
    IGNORED_KEYS = {"highlighter"}

    with open("src/rich_click/_internal_types.py") as f:
        mod_str = f.read()
        mod_str = mod_str.replace("\nif TYPE_CHECKING:", "\nif True:")
        # pyright gets mad at StyleType so we have to replace it with `str`.
        mod_str = mod_str.replace("from rich.style import StyleType", "StyleType = str")
        mock_script_writer(mod_str, "_internal_types_pytest.py")

    # When importing directly from the config module, this test causes side-effects that
    # are very difficult to fully squash.
    #
    # Importing from a copy of the module and editing it in place prevents requiring side-effects
    # which could negatively impact other tests.
    with open("src/rich_click/rich_help_configuration.py") as f:
        mod_str = f.read()
        mod_str = mod_str.replace("\nif TYPE_CHECKING:", "\nif True:")
        # pyright gets mad at StyleType so we have to replace it with `str`.
        mod_str = mod_str.replace("from rich.style import StyleType", "StyleType = str")
        mock_script_writer(mod_str, "_rich_configuration_pytest.py")

    config_mod = importlib.import_module("_rich_configuration_pytest")
    RichHelpConfiguration = config_mod.RichHelpConfiguration

    types_mod = importlib.import_module("_internal_types_pytest")
    RichHelpConfigurationDict = types_mod.RichHelpConfigurationDict

    for attr, field in RichHelpConfiguration.__dataclass_fields__.items():
        if attr in IGNORED_KEYS:
            continue
        expected_ann = field.type
        actual_ann = RichHelpConfigurationDict.__annotations__[attr]

        actual_typ = eval_type(actual_ann, types_mod.__dict__, {})
        expected_typ = eval_type(NotRequired[expected_ann], config_mod.__dict__, {})
        assert actual_typ == expected_typ, f"Failed attr={attr}"

    # Assert the reverse
    assert all(k in RichHelpConfiguration.__dataclass_fields__ for k in RichHelpConfigurationDict.__annotations__)


def test_all_rich_group_attrs_in_annotation(mock_script_writer: Callable[[str, str], Path]) -> None:
    # This is a weak test.
    # It does not assert that annotations, function signatures, etc. are correct.
    # It only asserts that nothing is obviously missing.

    with open("src/rich_click/rich_command.pyi") as f:
        mod_str = f.read()
        mock_script_writer(mod_str, "_rich_command_pyi.py")

    rich_command_pyi_mod = importlib.import_module("_rich_command_pyi")
    AnnotatedRichGroup = rich_command_pyi_mod.RichGroup

    for i in dir(RichCommand):
        assert i in dir(AnnotatedRichGroup)


def test_all_rich_command_attrs_in_annotation(mock_script_writer: Callable[[str, str], Path]) -> None:
    # This is a weak test.
    # It does not assert that annotations, function signatures, etc. are correct.
    # It only asserts that nothing is obviously missing.

    with open("src/rich_click/rich_command.pyi") as f:
        mod_str = f.read()
        mock_script_writer(mod_str, "_rich_command_pyi.py")

    rich_command_pyi_mod = importlib.import_module("_rich_command_pyi")
    AnnotatedRichCommand = rich_command_pyi_mod.RichCommand

    for i in dir(RichCommand):
        assert i in dir(AnnotatedRichCommand)
