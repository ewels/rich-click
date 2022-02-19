"""The command line interface."""

import sys
from importlib import import_module
try:
    from importlib.metadata import entry_points
except ImportError:
    from importlib_metadata import entry_points

import click
from rich_click import group, command


def main(args=None):
    args = args or sys.argv[1:]
    if not args:
        # without args we assume we want to run rich-click on itself
        # TODO: rewrite using argparse
        script_name = "rich-click"
    else:
        script_name = args[0]
    scripts = {script.name: script for script in entry_points().get("console_scripts")}
    if script_name in scripts:
        # a valid script was passed
        script = scripts[script_name]
        module_path = script.module
        function_name = script.attr
        prog = script_name
    elif ":" in script_name:
        # the path to a function was passed
        module_path, function_name = args[0].split(":")
        prog = module_path.split(".", 1)[0]
    else:
        print("usage: rich-click [SCRIPT | MODULE:FUNCTION] [-- SCRIPT_ARGS...]", file=sys.stderr)
        sys.exit(1)
    if len(args) > 1:
        if args[1] == "--":
            del args[1]
    sys.argv = [prog, *args[1:]]
    # patch click before importing the program function
    click.group = group
    click.command = command
    # import the program function
    module = import_module(module_path)
    function = getattr(module, function_name)
    # simply run it: it should be patched as well
    return function()
