from typing import Any, Optional, Sequence

import click


class RichParameter(click.Parameter):
    r"""
    A parameter to a command comes in two versions: they are either
    :class:`Option`\s or :class:`Argument`\s.  Other subclasses are currently
    not supported by design as some of the internals for parsing are
    intentionally not finalized.
    """

    def __init__(self, *args: Any, panel: Optional[str] = None, **kwargs: Any):
        """Create RichParameter instance."""
        super().__init__(*args, **kwargs)
        self.panel = panel


class RichArgument(click.Argument, RichParameter):
    """
    Arguments are positional parameters to a command.  They generally
    provide fewer features than options but can have infinite ``nargs``
    and are required by default.

    All parameters are passed onwards to the constructor of :class:`Parameter`.
    """

    param_type_name = "argument"

    def __init__(
        self,
        param_decls: Sequence[str],
        required: Optional[bool] = None,
        help: Optional[str] = None,
        panel: Optional[str] = None,
        **attrs: Any,
    ) -> None:
        """Create RichArgument instance."""
        super().__init__(param_decls, required=required, **attrs)
        self.help = help
        self.panel = panel


class RichOption(click.Option, RichParameter):
    """
    Options are usually optional values on the command line and
    have some extra features that arguments don't have.

    All other parameters are passed onwards to the parameter constructor.
    """

    pass


if hasattr(click, "HelpOption"):
    # click.HelpOption existed for a brief moment in time in 8.1.x.
    # This is a way to make sure it works for all click versions.

    class RichHelpOption(click.HelpOption, RichOption):
        """
        Pre-configured ``--help`` option which immediately prints the help page
        and exits the program.
        """

else:

    RichHelpOption = None  # type: ignore[misc,assignment]
