from typing import TYPE_CHECKING

import pytest

from rich_click import group, rich_config, RichHelpConfiguration, RichContext
from rich_click._compat_click import CLICK_IS_BEFORE_VERSION_8X

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
