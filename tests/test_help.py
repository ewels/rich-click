from importlib import metadata  # type: ignore
from typing import Optional, Type

import click
import pytest
from click import UsageError
from conftest import AssertRichFormat, AssertStr, InvokeCli
from packaging import version
from rich.console import Console

from rich_click import command, rich_config, RichContext, RichHelpConfiguration
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_8X
from rich_click.rich_command import RichCommand

rich_version = version.parse(metadata.version("rich"))


@pytest.mark.parametrize(
    "cmd, args, error, rich_config",
    [
        pytest.param("arguments", "--help", None, None, id="test arguments"),
        pytest.param("custom_errors", "1", UsageError, None, id="test custom errors help"),
        pytest.param("declarative", "--help", None, None, id="test declarative"),
        pytest.param("envvar", "greet --help", None, None, id="test envvar"),
        pytest.param("groups_sorting", "--help", None, None, id="test group sorting"),
        pytest.param("table_alignment", "--help", None, None, id="test command column alignment"),
        pytest.param(
            "markdown",
            "--help",
            None,
            None,
            id="test markdown",
            marks=pytest.mark.skipif(
                rich_version < version.parse("13.0.0"), reason="Markdown h1 borders are different."
            ),
        ),
        pytest.param("metavars_default", "--help", None, None, id="test metavars default"),
        pytest.param("metavars", "--help", None, None, id="test metavars"),
        pytest.param("rich_markup", "--help", None, None, id="test rich markup"),
        pytest.param("simple", "--help", None, None, id="test simple"),
        pytest.param("table_styles", "--help", None, None, id="test table styles"),
        pytest.param(
            "arguments",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration(show_arguments=True)),
            id="test arguments with rich_config",
        ),
        pytest.param(
            "custom_errors",
            "1",
            UsageError,
            rich_config(
                help_config=RichHelpConfiguration(
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
            rich_config(help_config=RichHelpConfiguration()),
            id="test declarative with rich_config",
        ),
        pytest.param(
            "envvar",
            "greet --help",
            None,
            rich_config(help_config=RichHelpConfiguration()),
            id="test environment variables with rich_config",
        ),
        pytest.param(
            "groups_sorting",
            "--help",
            None,
            rich_config(
                help_config=RichHelpConfiguration(
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
            rich_config(help_config=RichHelpConfiguration(use_markdown=True)),
            id="test markdown with rich_config",
            marks=pytest.mark.skipif(
                rich_version < version.parse("13.0.0"), reason="Markdown h1 borders are different."
            ),
        ),
        pytest.param(
            "metavars_default",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration()),
            id="test metavars default with rich_config",
        ),
        pytest.param(
            "metavars",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration(show_metavars_column=False, append_metavars_help=True)),
            id="test metavars with rich_config",
        ),
        pytest.param(
            "rich_markup",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration(use_rich_markup=True)),
            id="test rich markup with rich_config",
        ),
        pytest.param(
            "simple",
            "--help",
            None,
            rich_config(help_config=RichHelpConfiguration()),
            id="test simple with rich_config",
        ),
        pytest.param(
            "table_styles",
            "--help",
            None,
            rich_config(
                help_config=RichHelpConfiguration(
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
@pytest.mark.filterwarnings("ignore:^.*click prior to.*$:RuntimeWarning")
def test_rich_click(
    cmd: str, args: str, error: Optional[Type[Exception]], rich_config, assert_rich_format: AssertRichFormat
):
    assert_rich_format(cmd, args, error, rich_config)


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_8X, reason="rich_config not supported prior to click v8")
def test_rich_config_decorator_order(invoke: InvokeCli, assert_str: AssertStr):
    @command()
    @rich_config(Console(), RichHelpConfiguration(max_width=80, use_markdown=True))
    def cli():
        """Some help

        # Header
        """
        pass

    assert hasattr(cli, "__rich_context_settings__") is False
    assert cli.console is not None
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
                                                                                                    
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
    """,
    )


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_8X, reason="rich_config not supported prior to click v8")
def test_rich_config_context_settings(invoke: InvokeCli):
    @click.command(
        cls=RichCommand, context_settings={"rich_console": Console(), "rich_help_config": RichHelpConfiguration()}
    )
    @click.pass_context
    def cli(ctx: RichContext):
        assert isinstance(ctx, RichContext)
        assert ctx.console is not None
        assert ctx.help_config is not None

    result = invoke(cli)
    assert result.exit_code == 0
    assert result.exception is None


@pytest.mark.skipif(not CLICK_IS_BEFORE_VERSION_8X, reason="This is to test a warning when using for click v7.")
def test_rich_config_warns_before_click_v8(invoke: InvokeCli):
    with pytest.warns(RuntimeWarning, match="does not work with versions of click prior to version 8[.]0[.]0"):

        @rich_config(help_config=RichHelpConfiguration())
        @click.command("test-cmd")
        def cli():
            # Command should still work, regardless.
            click.echo("hello, world!")

    result = invoke(cli)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.stdout == "hello, world!\n"
