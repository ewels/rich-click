from typing import Optional, Type

import pytest
from click import UsageError
from conftest import AssertRichFormat, AssertStr, InvokeCli
from rich.console import Console

from rich_click import command, rich_config
from rich_click.rich_help_configuration import RichHelpConfiguration


@pytest.mark.parametrize(
    "cmd, args, error, rich_config",
    [
        pytest.param("arguments", "--help", None, None, id="test arguments"),
        pytest.param("custom_errors", "1", UsageError, None, id="test custom errors help"),
        pytest.param("declarative", "--help", None, None, id="test declarative"),
        pytest.param("envvar", "greet --help", None, None, id="test envvar"),
        pytest.param("groups_sorting", "--help", None, None, id="test group sorting"),
        pytest.param("markdown", "--help", None, None, id="test markdown"),
        pytest.param("metavars_default", "--help", None, None, id="test metavars default"),
        pytest.param("metavars", "--help", None, None, id="test metavars"),
        pytest.param("rich_markup", "--help", None, None, id="test rich markup"),
        pytest.param("simple", "--help", None, None, id="test simple"),
        pytest.param("table_styles", "--help", None, None, id="test table styles"),
        pytest.param(
            "arguments",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration(max_width=80, show_arguments=True)),
            id="test arguments with rich_config",
        ),
        pytest.param(
            "custom_errors",
            "1",
            UsageError,
            rich_config(
                help_config=RichHelpConfiguration(
                    max_width=80,
                    style_errors_suggestion="magenta italic",
                    errors_suggestion="Try running the '--help' flag for more information.",
                    errors_epilogue="To find out more, visit [link=https://mytool.com]https://mytool.com[/link]",
                )
            ),
            id="test custom errors with rich_config",
        ),
        pytest.param(
            "declarative",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration(max_width=80)),
            id="test declarative with rich_config",
        ),
        pytest.param(
            "envvar",
            "greet --help",
            None,
            rich_config(help_config=RichHelpConfiguration(max_width=80)),
            id="test environment variables with rich_config",
        ),
        pytest.param(
            "groups_sorting",
            "--help",
            None,
            rich_config(
                help_config=RichHelpConfiguration(
                    max_width=80,
                    option_groups={
                        "cli": [
                            {
                                "name": "Basic usage",
                                "options": ["--type", "--output"],
                            },
                            {
                                "name": "Advanced options",
                                "options": ["--help", "--version", "--debug"],
                                # You can also set table styles at group-level instead of using globals if you want
                                "table_styles": {
                                    "row_styles": ["bold", "yellow", "cyan"],
                                },
                            },
                        ],
                        "cli sync": [
                            {
                                "name": "Inputs and outputs",
                                "options": ["--input", "--output"],
                            },
                            {
                                "name": "Advanced usage",
                                "options": ["--overwrite", "--all", "--help"],
                            },
                        ],
                    },
                    command_groups={
                        "cli": [
                            {
                                "name": "Main usage",
                                "commands": ["sync", "download"],
                            },
                            {
                                "name": "Configuration",
                                "commands": ["config", "auth"],
                            },
                        ]
                    },
                )
            ),
            id="test groups sorting with rich_config",
        ),
        pytest.param(
            "markdown",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration(max_width=80, use_markdown=True)),
            id="test markdown with rich_config",
        ),
        pytest.param(
            "metavars_default",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration(max_width=80)),
            id="test metavars default with rich_config",
        ),
        pytest.param(
            "metavars",
            "--help",
            None,
            rich_config(
                help_config=RichHelpConfiguration(max_width=80, show_metavars_column=False, append_metavars_help=True)
            ),
            id="test metavars with rich_config",
        ),
        pytest.param(
            "rich_markup",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration(max_width=80, use_rich_markup=True)),
            id="test rich markup with rich_config",
        ),
        pytest.param(
            "simple",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration(max_width=80)),
            id="test simple with rich_config",
        ),
        pytest.param(
            "table_styles",
            "--help",
            None,
            rich_config(
                help_config=RichHelpConfiguration(
                    max_width=80,
                    style_options_table_leading=1,
                    style_options_table_box="SIMPLE",
                    style_options_table_row_styles=["bold", ""],
                    style_commands_table_show_lines=True,
                    style_commands_table_pad_edge=True,
                    style_commands_table_box="DOUBLE",
                    style_commands_table_border_style="red",
                    style_commands_table_row_styles=["magenta", "yellow", "cyan", "green"],
                )
            ),
            id="test table styles with rich_config",
        ),
    ],
)
def test_rich_click(
    cmd: str, args: str, error: Optional[Type[Exception]], rich_config, assert_rich_format: AssertRichFormat
):
    assert_rich_format(cmd, args, error, rich_config)


def test_rich_config_decorator_order(invoke: InvokeCli, assert_str: AssertStr):
    @command()
    @rich_config(Console(), RichHelpConfiguration(max_width=80, use_markdown=True))
    def cli():
        """Some help

        # Header
        """
        pass

    assert hasattr(cli, "__rich_context_settings__") is False
    assert cli.__doc__ is not None
    assert_str(
        cli.__doc__,
        """
    Some help

    # Header
    """,
    )

    result = invoke(cli, "--help")

    assert_str(
        result.stdout,
        """
Usage: cli [OPTIONS]                                                           
                                                                                
 Some help                                                                      
 # Header                                                                       
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                      │
╰──────────────────────────────────────────────────────────────────────────────╯
    """,
    )
