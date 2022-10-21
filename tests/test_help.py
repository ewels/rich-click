from pathlib import Path
from typing import List, Union

import pytest
from conftest import InvokeCli
from fixtures.arguments import cli as arguments_cli
from fixtures.custom_errors import cli as custom_errors_cli
from fixtures.declarative import cli as declarative_cli
from fixtures.envvar import cli as envvar_cli
from fixtures.groups_sorting import cli as groups_sorting_cli
from fixtures.markdown import cli as markdown_cli
from fixtures.metavars import cli as metavars_cli
from fixtures.metavars_default import cli as metavars_default_cli
from fixtures.rich_markup import cli as rich_markup_cli
from fixtures.simple import cli as simple_cli
from fixtures.table_styles import cli as table_styles_cli

import rich_click.rich_click as rc
from rich_click.rich_command import RichCommand
from rich_click.rich_group import RichGroup

rc.MAX_WIDTH = 80


@pytest.mark.parametrize(
    "cli, command, fixture",
    [
        pytest.param(arguments_cli, "--help", "test_arguments.out", id="test arguments"),
        pytest.param(custom_errors_cli, "--help", "test_custom_errors.out", id="test custom errors help"),
        pytest.param(declarative_cli, "--help", "test_declarative.out", id="test declarative"),
        pytest.param(envvar_cli, "--help", "test_envvar.out", id="test envvar"),
        pytest.param(groups_sorting_cli, "--help", "test_groups_sorting.out", id="test group sorting"),
        pytest.param(markdown_cli, "--help", "test_markdown.out", id="test markdown"),
        pytest.param(metavars_default_cli, "--help", "test_metavars_default.out", id="test metavars default"),
        pytest.param(metavars_cli, "--help", "test_metavars.out", id="test metavars"),
        pytest.param(rich_markup_cli, "--help", "test_rich_markup.out", id="test rich markup"),
        pytest.param(simple_cli, "--help", "test_simple.out", id="test simple"),
        pytest.param(table_styles_cli, "--help", "test_table_styles.out", id="test table styles"),
    ],
)
def test_rich_click(
    cli: Union[RichCommand, RichGroup],
    command: str,
    fixture: str,
    fixtures_dir: Path,
    invoke: InvokeCli,
    assert_str,
):
    result = invoke(cli, command)
    actual = result.stdout
    expected = (fixtures_dir / fixture).read_text()
    assert_str(actual, expected)
