from typing import TYPE_CHECKING

import pytest

from rich_click import group, command, rich_config, RichHelpConfiguration, RichContext
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_8X
import rich_click.rich_click as rc
from dataclasses import asdict
import json

if CLICK_IS_BEFORE_VERSION_8X:
    pytest.skip(reason="rich_config not supported for click < 8.", allow_module_level=True)


def test_basic_config_for_group() -> None:
    @group(invoke_without_command=True)
    @rich_config(help_config=RichHelpConfiguration(style_option="parent-value"))
    def cli() -> None:
        pass

    @cli.command()
    @rich_config(help_config=RichHelpConfiguration(style_argument="child-value"))
    def subcommand1() -> None:
        pass

    @cli.command()
    @rich_config(help_config=dict(style_argument="child-value"))
    def subcommand2() -> None:
        pass

    @cli.command()
    @rich_config(help_config=dict(style_option="overwriting-parent-value"))
    def subcommand3() -> None:
        pass

    with cli.make_context("pytest-example", []) as ctx:
        if TYPE_CHECKING:
            # TODO: I don't understand this Mypy error.
            #  I wrap this one in if TYPE_CHECKING to signify that Mypy needs this.
            #  Every make_context() call in this file fails the type check though.
            assert isinstance(ctx, RichContext)
        assert ctx.help_config.style_option == "parent-value"

        with subcommand1.make_context("pytest-example", [], parent=ctx) as sub_ctx:
            assert isinstance(sub_ctx, RichContext)
            assert sub_ctx.help_config.style_option == RichHelpConfiguration().style_option
            assert sub_ctx.help_config.style_argument == "child-value"

        with subcommand2.make_context("pytest-example", [], parent=ctx) as sub_ctx:
            assert isinstance(sub_ctx, RichContext)
            assert sub_ctx.help_config.style_option == "parent-value"
            assert sub_ctx.help_config.style_argument == "child-value"

        with subcommand3.make_context("pytest-example", [], parent=ctx) as sub_ctx:
            assert isinstance(sub_ctx, RichContext)
            assert sub_ctx.help_config.style_option == "overwriting-parent-value"


def test_global_config_equal_config_defaults() -> None:
    config1 = RichHelpConfiguration()
    config2 = RichHelpConfiguration.load_from_globals(rc)
    for k in {*config1.__dict__.keys(), *config2.__dict__.keys()}:
        if k == "highlighter":
            continue
        v1 = config1.__dict__[k]
        v2 = config2.__dict__[k]
        assert v1 == v2, k


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
        config2.style_commands_table_column_width_ratio = tuple(config2.style_commands_table_column_width_ratio)  # type: ignore[arg-type,assignment]

        assert config == config2
