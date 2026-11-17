import inspect
from importlib.util import find_spec

import pytest

import rich_click


pytestmark = pytest.mark.skipif(find_spec("asyncclick") is not None, reason="requires no asyncclick installation")


def test_module_introspection_without_asyncclick() -> None:
    async_names = {
        "RichAsyncCommand",
        "RichAsyncCommandCollection",
        "RichAsyncContext",
        "RichAsyncGroup",
    }

    assert async_names.isdisjoint(dir(rich_click))
    for name in async_names:
        assert not hasattr(rich_click, name)
    inspect.getmembers(rich_click)
