from typing import Any, Callable, Optional, Type, Union

import click
import pytest
from click import UsageError
from packaging import version
from rich.console import Console

from tests.conftest import AssertRichFormat, AssertStr, InvokeCli

import rich_click.rich_click as rc
from rich_click import command, group, pass_context, rich_config, RichContext, RichHelpConfiguration
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_8X, CLICK_IS_VERSION_80
from rich_click.rich_command import RichCommand, RichGroup

try:
    from importlib import metadata  # type: ignore[import,unused-ignore]
except ImportError:
    # Python < 3.8
    import importlib_metadata as metadata  # type: ignore[no-redef,import-not-found]


rich_version = version.parse(metadata.version("rich"))
click_version = version.parse(metadata.version("click"))


@pytest.mark.parametrize(
    "cmd, args, error, rich_config",
    [
        pytest.param("arguments", "--help", None, None, id="test arguments"),
        pytest.param(
            "context_settings",
            "--help",
            None,
            None,
            id="test context_settings",
            marks=[
                pytest.mark.skipif(
                    click_version < version.parse("7.1.0"), reason="show_default is invalid kwarg for click.Context()."
                ),
                pytest.mark.skipif(CLICK_IS_VERSION_80, reason="Options render slightly differently."),
            ],
        ),
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
    cmd: str,
    args: str,
    error: Optional[Type[Exception]],
    rich_config: Optional[Callable[[Any], Union[RichGroup, RichCommand]]],
    assert_rich_format: AssertRichFormat,
) -> None:
    assert_rich_format(cmd, args, error, rich_config)


class ClickGroupWithRichCommandClass(click.Group):
    command_class = RichCommand
    group_class = RichGroup


if rich_version.major == 12:
    command_help_output = """
 Usage: cli [OPTIONS]                                       

 Some help                                                  
 ╔════════════════════════════════════════════════════════╗ 
 ║                         Header                         ║ 
 ╚════════════════════════════════════════════════════════╝ 

╭─ Options ────────────────────────────────────────────────╮
│ --help      Show this message and exit.                  │
╰──────────────────────────────────────────────────────────╯
"""
    group_help_output = """
 Usage: cli [OPTIONS] COMMAND [ARGS]...                     
                                                            
 Some help                                                  
 ╔════════════════════════════════════════════════════════╗ 
 ║                         Header                         ║ 
 ╚════════════════════════════════════════════════════════╝ 
                                                            
╭─ Options ────────────────────────────────────────────────╮
│ --help      Show this message and exit.                  │
╰──────────────────────────────────────────────────────────╯
"""
else:
    command_help_output = """
 Usage: cli [OPTIONS]                                       

 Some help                                                  
 ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ 
 ┃                         Header                         ┃ 
 ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ 

╭─ Options ────────────────────────────────────────────────╮
│ --help      Show this message and exit.                  │
╰──────────────────────────────────────────────────────────╯
"""
    group_help_output = """
 Usage: cli [OPTIONS] COMMAND [ARGS]...                     
                                                            
 Some help                                                  
 ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ 
 ┃                         Header                         ┃ 
 ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ 
                                                            
╭─ Options ────────────────────────────────────────────────╮
│ --help      Show this message and exit.                  │
╰──────────────────────────────────────────────────────────╯
"""


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_8X, reason="rich_config not supported prior to click v8")
@pytest.mark.parametrize(
    ("command_callable", "expected_command_type", "expected_help_output"),
    [
        pytest.param(
            lambda: command,
            RichCommand,
            command_help_output,
            marks=pytest.mark.skipif(
                click_version < version.parse("8.1.0"), reason="decorator must be called prior to click 8.1.0"
            ),
            id="command1",
        ),
        pytest.param(lambda: command(), RichCommand, command_help_output, id="command2"),
        pytest.param(lambda: command("cli"), RichCommand, command_help_output, id="command3"),
        pytest.param(
            lambda: group,
            RichGroup,
            group_help_output,
            id="group1",
            marks=pytest.mark.skipif(
                click_version < version.parse("8.1.0"), reason="decorator must be called prior to click 8.1.0"
            ),
        ),
        pytest.param(lambda: group(), RichGroup, group_help_output, id="group2"),
        pytest.param(lambda: group("cli"), RichGroup, group_help_output, id="group3"),
        pytest.param(lambda: click.command(cls=RichCommand), RichCommand, command_help_output, id="click_command1"),
        pytest.param(
            lambda: click.command("cli", cls=RichCommand), RichCommand, command_help_output, id="click_command2"
        ),
        pytest.param(lambda: click.group(cls=RichGroup), RichGroup, group_help_output, id="click_group1"),
        pytest.param(lambda: click.group("cli", cls=RichGroup), RichGroup, group_help_output, id="click_group2"),
        pytest.param(
            lambda: RichGroup(name="grp", callback=lambda: None).command,
            RichCommand,
            command_help_output,
            id="RichGroup1",
            marks=pytest.mark.skipif(
                click_version < version.parse("8.1.0"), reason="decorator must be called prior to click 8.1.0"
            ),
        ),
        pytest.param(
            lambda: RichGroup(name="grp", callback=lambda: None).command("cli"),
            RichCommand,
            command_help_output,
            id="RichGroup2",
        ),
        pytest.param(
            lambda: ClickGroupWithRichCommandClass(name="grp", callback=lambda: None).command,
            RichCommand,
            command_help_output,
            id="ClickGroup1",
            marks=pytest.mark.skipif(
                click_version < version.parse("8.1.0"), reason="decorator must be called prior to click 8.1.0"
            ),
        ),
        pytest.param(
            lambda: ClickGroupWithRichCommandClass(name="grp", callback=lambda: None).command("cli"),
            RichCommand,
            command_help_output,
            id="ClickGroup2",
        ),
        pytest.param(
            lambda: ClickGroupWithRichCommandClass(name="grp", callback=lambda: None).group,
            RichGroup,
            group_help_output,
            id="ClickGroup3",
            marks=pytest.mark.skipif(
                click_version < version.parse("8.1.0"), reason="decorator must be called prior to click 8.1.0"
            ),
        ),
        pytest.param(
            lambda: ClickGroupWithRichCommandClass(name="grp", callback=lambda: None).group("cli"),
            RichGroup,
            group_help_output,
            id="ClickGroup4",
        ),
    ],
)
def test_rich_config_decorator_order(
    invoke: InvokeCli,
    assert_str: AssertStr,
    command_callable: Callable[..., Any],
    expected_command_type: Type[RichCommand],
    expected_help_output: str,
) -> None:
    @command_callable()  # type: ignore[misc]
    @rich_config(Console(), RichHelpConfiguration(max_width=60, use_markdown=True, color_system=None))
    def cli() -> None:
        """Some help

        # Header
        """
        pass

    assert hasattr(cli, "__rich_context_settings__") is False
    assert type(cli) is expected_command_type
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
        actual=result.stdout,
        expectation=expected_help_output,
    )


def test_rich_config_max_width(invoke: InvokeCli, assert_str: AssertStr) -> None:
    rc.WIDTH = 100
    rc.MAX_WIDTH = 64

    @command()
    def cli() -> None:
        """Some help text"""
        pass

    result = invoke(cli, "--help")

    assert_str(
        result.stdout,
        """
Usage: cli [OPTIONS]                                            
                                                                
 Some help text                                                 
                                                                
╭─ Options ────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                      │
╰──────────────────────────────────────────────────────────────╯
        """,
    )


@pytest.mark.skipif(CLICK_IS_BEFORE_VERSION_8X, reason="rich_config not supported prior to click v8")
def test_rich_config_context_settings(invoke: InvokeCli) -> None:
    @click.command(
        cls=RichCommand, context_settings={"rich_console": Console(), "rich_help_config": RichHelpConfiguration()}
    )
    @pass_context
    def cli(ctx: RichContext) -> None:
        assert isinstance(ctx, RichContext)
        assert ctx.console is not None
        assert ctx.help_config is not None

    result = invoke(cli)
    assert result.exit_code == 0
    assert result.exception is None


@pytest.mark.skipif(not CLICK_IS_BEFORE_VERSION_8X, reason="This is to test a warning when using for click v7.")
def test_rich_config_warns_before_click_v8(invoke: InvokeCli) -> None:
    with pytest.warns(RuntimeWarning, match="does not work with versions of click prior to version 8[.]0[.]0"):

        @rich_config(help_config=RichHelpConfiguration())
        @click.command("test-cmd")
        def cli() -> None:
            # Command should still work, regardless.
            click.echo("hello, world!")

    result = invoke(cli)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.stdout == "hello, world!\n"
