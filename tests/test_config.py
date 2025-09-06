import io
import json
import sys
from dataclasses import asdict
from importlib import reload
from typing import TYPE_CHECKING

import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot
from rich.console import Console

import rich_click.rich_click as rc
from rich_click import RichContext, RichHelpConfiguration, command, group, rich_config


if sys.version_info < (3, 11):
    pass
else:
    pass


def test_basic_config_for_group() -> None:
    @group(invoke_without_command=True)
    @rich_config(help_config=RichHelpConfiguration(style_option="#111111"))
    def cli() -> None:
        pass

    @cli.command()
    @rich_config(help_config=RichHelpConfiguration(style_argument="#222222"))
    def subcommand1() -> None:
        pass

    @cli.command()
    @rich_config(help_config=dict(style_argument="#333333"))
    def subcommand2() -> None:
        pass

    @cli.command()
    @rich_config(help_config=dict(style_option="#444444"))
    def subcommand3() -> None:
        pass

    with cli.make_context("pytest-example", []) as ctx:
        if TYPE_CHECKING:
            # TODO: I don't understand this Mypy error.
            #  I wrap this one in if TYPE_CHECKING to signify that Mypy needs this.
            #  Every make_context() call in this file fails the type check though.
            assert isinstance(ctx, RichContext)
        assert ctx.help_config.style_option == "#111111"

        with subcommand1.make_context("pytest-example", [], parent=ctx) as sub_ctx:
            assert isinstance(sub_ctx, RichContext)
            assert sub_ctx.help_config.style_option == RichHelpConfiguration().style_option
            assert sub_ctx.help_config.style_argument == "#222222"

        with subcommand2.make_context("pytest-example", [], parent=ctx) as sub_ctx:
            assert isinstance(sub_ctx, RichContext)
            assert sub_ctx.help_config.style_option == "#111111"
            assert sub_ctx.help_config.style_argument == "#333333"

        with subcommand3.make_context("pytest-example", [], parent=ctx) as sub_ctx:
            assert isinstance(sub_ctx, RichContext)
            assert sub_ctx.help_config.style_option == "#444444"


def test_global_config_equal_config_defaults() -> None:
    reload(rc)
    config1 = RichHelpConfiguration()
    config2 = RichHelpConfiguration.load_from_globals(rc)
    for k in {*config1.__dict__.keys(), *config2.__dict__.keys()}:
        if k == "highlighter":
            continue
        v1 = config1.__dict__[k]
        v2 = config2.__dict__[k]
        assert v1 == v2, f"{k}: {v1} != {v2}"


def test_config_from_globals_behavior() -> None:
    original_style_option_value = rc.STYLE_OPTION
    rc.STYLE_OPTION = "new-value"

    @command()
    def cli1() -> None:
        pass

    with cli1.make_context("pytest-example", []) as ctx:
        if TYPE_CHECKING:
            assert isinstance(ctx, RichContext)
        assert ctx.help_config.style_option == "new-value"

    @command()
    @rich_config(help_config=RichHelpConfiguration())
    def cli2() -> None:
        pass

    with cli2.make_context("pytest-example", []) as ctx:
        if TYPE_CHECKING:
            assert isinstance(ctx, RichContext)
        assert ctx.help_config.style_option == original_style_option_value

    @command()
    @rich_config(help_config=RichHelpConfiguration.load_from_globals())
    def cli3() -> None:
        pass

    with cli3.make_context("pytest-example", []) as ctx:
        if TYPE_CHECKING:
            assert isinstance(ctx, RichContext)
        assert ctx.help_config.style_option == "new-value"

    @command()
    @rich_config(help_config={})
    def cli4() -> None:
        pass

    with cli4.make_context("pytest-example", []) as ctx:
        if TYPE_CHECKING:
            assert isinstance(ctx, RichContext)
        assert ctx.help_config.style_option == "new-value"


def test_config_is_serializable_and_invertible() -> None:
    config = RichHelpConfiguration()
    config.apply_theme(force_default=True)

    try:
        serialized_data = json.dumps(asdict(config))
    except TypeError as e:
        pytest.fail(f"RichHelpConfiguration is not serializable: Error raised: {e.__class__.__name__}{e.args}")
    else:
        deserialized_data = json.loads(serialized_data)
        config2 = RichHelpConfiguration(**deserialized_data)

        # Correct types.
        config2.style_options_table_padding = tuple(config2.style_options_table_padding)  # type: ignore[arg-type,assignment]
        config2.style_commands_table_padding = tuple(config2.style_commands_table_padding)  # type: ignore[arg-type,assignment]
        config2.style_options_panel_padding = tuple(config2.style_options_panel_padding)  # type: ignore[arg-type,assignment]
        config2.style_commands_panel_padding = tuple(config2.style_commands_panel_padding)  # type: ignore[arg-type,assignment]
        config2.style_commands_table_column_width_ratio = tuple(config2.style_commands_table_column_width_ratio)  # type: ignore[arg-type,assignment]
        config2.padding_header_text = tuple(config2.padding_header_text)  # type: ignore[arg-type,assignment]
        config2.padding_helptext = tuple(config2.padding_helptext)  # type: ignore[arg-type,assignment]
        config2.padding_errors_panel = tuple(config2.padding_errors_panel)  # type: ignore[arg-type,assignment]
        config2.padding_errors_suggestion = tuple(config2.padding_errors_suggestion)  # type: ignore[arg-type,assignment]
        config2.padding_errors_epilogue = tuple(config2.padding_errors_epilogue)  # type: ignore[arg-type,assignment]

        assert config == config2


def test_multiple_rich_config_passes_is_ok() -> None:
    # It's not advisable that users do any of this,
    # but it shouldn't break anything to do so either.
    c = Console()

    @command()
    @rich_config(help_config={"style_option": "a"})
    @rich_config(help_config={"style_option": "b"})  # should be overwritten
    @rich_config(console=c)
    def cli() -> None:
        pass

    assert cli.context_settings.get("rich_help_config") == {"style_option": "a"}
    assert cli.context_settings.get("rich_console") is c

    @rich_config(help_config={"style_option": "c"})
    @rich_config(help_config={"style_option": "d"})  # should be overwritten
    @rich_config(console=c)
    @command()
    def cli2() -> None:
        pass

    assert cli2.context_settings.get("rich_help_config") == {"style_option": "c"}
    assert cli2.context_settings.get("rich_console") is c


def test_custom_console(cli_runner: CliRunner) -> None:
    # It's not advisable that users do any of this,
    # but it shouldn't break anything to do so either.
    f = io.StringIO()
    c = Console(file=f, width=rc.WIDTH)

    @command()
    @rich_config(console=c)
    def cli() -> None:
        """My CLI help text"""

    cli_runner.invoke(cli, "--help")

    assert f.getvalue() == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 My CLI help text                                                                                   \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help  Show this message and exit.                                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
