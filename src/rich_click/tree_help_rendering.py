from __future__ import annotations

import os
import sys
import textwrap
from typing import Dict, List

import click
from rich.console import Console
from rich.text import Text
from rich.tree import Tree


def tree_format_help(ctx: "RichContext", formatter: "RichHelpFormatter", is_group: bool) -> None:
    """Format the help in tree style. Adapted from treeclick."""
    term_width = formatter.width
    term_console = formatter.console

    # Get path
    path = []
    current_ctx = ctx
    while current_ctx:
        path.append(current_ctx.command.name)
        current_ctx = current_ctx.parent
    path = path[::-1]
    path_len = len(path)
    is_top_level = path_len == 1

    # Get root
    root_ctx = ctx
    while root_ctx.parent:
        root_ctx = root_ctx.parent
    root_command = root_ctx.command

    # Collect effective lengths from root
    indent_size = 4
    command_effectives: List[int] = []
    option_effectives: List[int] = []

    # Manual collect for root command and options
    root_left = f"[bold green]{path[0]}[/]"
    root_left_len = term_console.measure(Text.from_markup(root_left)).maximum
    command_effectives.append(root_left_len + 0 * indent_size)
    for param in root_command.params:
        if isinstance(param, click.Option) and param.name != "help":
            opts = ", ".join(param.opts)
            left = f"[bold yellow]{opts}[/bold yellow]"
            left_len = term_console.measure(Text.from_markup(left)).maximum
            option_effectives.append(left_len + 0 * indent_size)

    collect_effective_lengths(
        root_command.commands if isinstance(root_command, click.MultiCommand) else {},
        1,
        command_effectives,
        option_effectives,
        term_console,
        indent_size,
    )
    max_command_effective = max(command_effectives) if command_effectives else 0
    max_option_effective = max(option_effectives) if option_effectives else 0
    global_column = max(max_command_effective, max_option_effective - 4) + 1

    # Usage
    if is_group:
        usage_parts = "[OPTIONS] COMMAND [ARGS]..."
    else:
        args_part = " ".join(
            f"[[orange1]{p.name.upper()}[/orange1]]" for p in ctx.command.params if isinstance(p, click.Argument)
        )
        usage_parts = "[OPTIONS]" + (f" {args_part}" if args_part else "")
    term_console.print(f"\n[bold]Usage:[/bold] {ctx.command_path} {Text.from_markup(usage_parts)}\n")

    # Description
    help_text_str = ctx.command.help or ""
    desc_label = Text.from_markup("[bold]Description:[/bold] ")
    term_console.print(desc_label, end="")
    if help_text_str:
        desc_start = term_console.measure(desc_label).maximum
        available_width = term_width - desc_start
        if available_width < 10:
            available_width = term_width // 2
        lines = textwrap.wrap(help_text_str, width=available_width)
        term_console.print(Text(lines[0], style="bold"))
        for line in lines[1:]:
            term_console.print(Text(" " * desc_start + line, style="bold"))
    else:
        term_console.print()

    # Current options
    current_option_effectives = []
    has_options = False
    for param in ctx.command.params:
        if isinstance(param, click.Option) and param.name != "help":
            has_options = True
            opts = ", ".join(param.opts)
            left = f"[bold yellow]{opts}[/bold yellow]"
            left_len = term_console.measure(Text.from_markup(left)).maximum
            current_option_effectives.append(left_len)
    if has_options:
        term_console.print("[bold]Options:[/bold]")
        for param in ctx.command.params:
            if isinstance(param, click.Option) and param.name != "help":
                opts = ", ".join(param.opts)
                left_text = Text.from_markup(f"[bold yellow]{opts}[/bold yellow]")
                left_len = term_console.measure(left_text).maximum
                pad = global_column - left_len
                pad_text = Text(" " * pad)
                star = "[red]*[/red]" if param.required else ""
                star_space = star + " "
                star_space_len = term_console.measure(Text(star_space)).maximum
                help_text_str = param.help or ""
                help_start_relative = left_len + pad + star_space_len
                help_start_absolute = help_start_relative  # level 0
                available_width = term_console.width - help_start_absolute
                if available_width < 10:
                    available_width = term_console.width // 2
                lines = textwrap.wrap(help_text_str, width=available_width)
                option_label = left_text + pad_text + Text(star_space)
                if lines:
                    option_label.append(lines[0], style="italic yellow")
                    for line in lines[1:]:
                        option_label.append("\n")
                        indent_text = Text(" " * help_start_relative)
                        option_label.append_text(indent_text)
                        option_label.append(line, style="italic yellow")
                term_console.print(option_label)
        term_console.print()

    # Commands
    term_console.print("[bold]Commands:[/bold]")

    # Root name
    root_name = path[0]
    if sys.argv and sys.argv[0]:
        root_name = os.path.basename(sys.argv[0])

    # Build the tree
    level = 0
    color = "bold green"
    left = f"[{color}]{root_name}[/]"
    left_text = Text.from_markup(left)
    left_len = term_console.measure(left_text).maximum
    pad = global_column - level * indent_size - left_len
    pad_text = Text(" " * pad)
    help_text_str = root_command.help or ""
    help_start_relative = left_len + pad
    help_start_absolute = level * indent_size + help_start_relative
    available_width = term_console.width - help_start_absolute
    if available_width < 10:
        available_width = term_console.width // 2
    lines = textwrap.wrap(help_text_str, width=available_width)
    label = Text()
    if is_top_level:
        label.append_text(left_text)
        label.append_text(pad_text)
        if lines:
            label.append(lines[0], style="bold")
            for line in lines[1:]:
                label.append("\n")
                indent_text = Text(" " * help_start_relative)
                label.append_text(indent_text)
                label.append(line, style="bold")
    else:
        dim_left = left_text.copy()
        dim_left.stylize("dim")
        label.append_text(dim_left)
        label.append_text(pad_text)
        if lines:
            dim_help = Text(lines[0])
            dim_help.stylize("dim")
            label.append_text(dim_help)
            for line in lines[1:]:
                label.append("\n")
                indent_text = Text(" " * help_start_relative)
                indent_text.stylize("dim")
                label.append_text(indent_text)
                dim_line = Text(line)
                dim_line.stylize("dim")
                label.append_text(dim_line)

    tree = Tree(label, guide_style="dim")

    # Add options for root if not is_top_level
    if not is_top_level:
        for param in root_command.params:
            if isinstance(param, click.Option) and param.name != "help":
                add_option_branch(
                    tree,
                    param,
                    level,
                    global_column,
                    indent_size,
                    term_console,
                    dim=True,
                )

    # Add to tree
    add_to_tree(
        tree,
        root_command.commands if isinstance(root_command, click.MultiCommand) else {},
        level + 1,
        path,
        1,
        global_column,
        indent_size,
        term_console,
        is_top_level,
        path_len,
    )

    term_console.print(tree)
    term_console.print()


def collect_effective_lengths(
    commands: Dict[str, click.Command],
    level: int,
    command_effectives: List[int],
    option_effectives: List[int],
    console: Console,
    indent_size: int,
) -> None:
    for cmd_name, cmd in sorted(commands.items()):
        color = "bold green" if isinstance(cmd, click.Group) else "cyan"
        args = [
            f"[[orange1]{param.name.upper()}[/orange1]]" for param in cmd.params if isinstance(param, click.Argument)
        ]
        arg_str = " ".join(args) if args else ""
        left = f"[{color}]{cmd_name}[/] {arg_str}"
        left_len = console.measure(Text.from_markup(left)).maximum
        command_effectives.append(left_len + level * indent_size)
        for param in cmd.params:
            if isinstance(param, click.Option) and param.name != "help":
                opts = ", ".join(param.opts)
                left = f"[bold yellow]{opts}[/bold yellow]"
                left_len = console.measure(Text.from_markup(left)).maximum
                option_effectives.append(left_len + (level + 1) * indent_size)
        if isinstance(cmd, click.Group) and cmd.commands:
            collect_effective_lengths(
                cmd.commands,
                level + 1,
                command_effectives,
                option_effectives,
                console,
                indent_size,
            )


def add_option_branch(
    parent_branch: Tree,
    param: click.Option,
    level: int,
    global_column: int,
    indent_size: int,
    console: Console,
    dim: bool = False,
) -> None:
    opts = ", ".join(param.opts)
    left = f"[bold yellow]{opts}[/bold yellow]"
    left_text = Text.from_markup(left)
    left_len = console.measure(left_text).maximum
    pad = global_column + 4 - (level + 1) * indent_size - left_len
    pad_text = Text(" " * pad)
    star = "[red]*[/red]" if param.required else ""
    star_space = star + " "
    star_space_text = Text(star_space)
    star_space_len = console.measure(star_space_text).maximum
    help_text_str = param.help or ""
    label_start = (level + 1) * indent_size
    help_start_relative = left_len + pad + star_space_len
    help_start_absolute = label_start + help_start_relative
    available_width = console.width - help_start_absolute
    if available_width < 10:
        available_width = console.width // 2
    lines = textwrap.wrap(help_text_str, width=available_width)
    option_label = Text()
    if dim:
        dim_left = left_text.copy()
        dim_left.stylize("dim")
        option_label.append_text(dim_left)
        dim_pad = pad_text.copy()
        dim_pad.stylize("dim")
        option_label.append_text(dim_pad)
        dim_star = star_space_text.copy()
        dim_star.stylize("dim")
        option_label.append_text(dim_star)
        if lines:
            dim_help = Text(lines[0], style="italic yellow")
            dim_help.stylize("dim")
            option_label.append_text(dim_help)
            for line in lines[1:]:
                option_label.append("\n")
                indent_text = Text(" " * help_start_relative)
                indent_text.stylize("dim")
                option_label.append_text(indent_text)
                dim_line = Text(line, style="italic yellow")
                dim_line.stylize("dim")
                option_label.append_text(dim_line)
    else:
        option_label.append_text(left_text)
        option_label.append_text(pad_text)
        option_label.append(star_space)
        if lines:
            option_label.append(lines[0], style="italic yellow")
            for line in lines[1:]:
                option_label.append("\n")
                indent_text = Text(" " * help_start_relative)
                option_label.append_text(indent_text)
                option_label.append(line, style="italic yellow")
    parent_branch.add(option_label)


def add_to_tree(
    branch: Tree,
    commands: Dict[str, click.Command],
    level: int,
    path: List[str],
    path_index: int,
    global_column: int,
    indent_size: int,
    console: Console,
    is_top_level: bool,
    path_len: int,
) -> None:
    if level > 5:
        branch.add("[red]Recursion limit reached (max 5 levels)[/red]")
        return
    if is_top_level or path_index == path_len:
        for cmd_name, cmd in sorted(commands.items()):
            color = "bold green" if isinstance(cmd, click.Group) else "cyan"
            args = [
                f"[[orange1]{param.name.upper()}[/orange1]]"
                for param in cmd.params
                if isinstance(param, click.Argument)
            ]
            arg_str = " ".join(args) if args else ""
            left = f"[{color}]{cmd_name}[/] {arg_str}"
            left_text = Text.from_markup(left)
            left_len = console.measure(left_text).maximum
            pad = global_column - level * indent_size - left_len
            pad_text = Text(" " * pad)
            help_text_str = cmd.help or ""
            help_start_relative = left_len + pad
            help_start_absolute = level * indent_size + help_start_relative
            available_width = console.width - help_start_absolute
            if available_width < 10:
                available_width = console.width // 2
            lines = textwrap.wrap(help_text_str, width=available_width)
            label = Text()
            label.append_text(left_text)
            label.append_text(pad_text)
            if lines:
                label.append(lines[0])
                for line in lines[1:]:
                    label.append("\n")
                    indent_text = Text(" " * help_start_relative)
                    label.append_text(indent_text)
                    label.append(line)
            cmd_branch = branch.add(label)
            for param in cmd.params:
                if isinstance(param, click.Option) and param.name != "help":
                    add_option_branch(cmd_branch, param, level, global_column, indent_size, console)
            if isinstance(cmd, click.Group) and cmd.commands:
                add_to_tree(
                    cmd_branch,
                    cmd.commands,
                    level + 1,
                    path,
                    path_index,
                    global_column,
                    indent_size,
                    console,
                    is_top_level,
                    path_len,
                )
    else:
        next_cmd_name = path[path_index]
        cmd = commands.get(next_cmd_name)
        if cmd:
            color = "bold green" if isinstance(cmd, click.Group) else "cyan"
            args = [
                f"[[orange1]{param.name.upper()}[/orange1]]"
                for param in cmd.params
                if isinstance(param, click.Argument)
            ]
            arg_str = " ".join(args) if args else ""
            left = f"[{color}]{next_cmd_name}[/] {arg_str}"
            left_text = Text.from_markup(left)
            left_len = console.measure(left_text).maximum
            pad = global_column - level * indent_size - left_len
            pad_text = Text(" " * pad)
            is_current = path_index + 1 == path_len
            help_text_str = cmd.help or ""
            help_start_relative = left_len + pad
            help_start_absolute = level * indent_size + help_start_relative
            available_width = console.width - help_start_absolute
            if available_width < 10:
                available_width = console.width // 2
            lines = textwrap.wrap(help_text_str, width=available_width)
            label = Text()
            if is_current:
                label.append_text(left_text)
                label.append_text(pad_text)
                if lines:
                    label.append(lines[0], style="bold")
                    for line in lines[1:]:
                        label.append("\n")
                        indent_text = Text(" " * help_start_relative)
                        label.append_text(indent_text)
                        label.append(line, style="bold")
            else:
                dim_left = left_text.copy()
                dim_left.stylize("dim")
                label.append_text(dim_left)
                label.append_text(pad_text)
                if lines:
                    dim_help = Text(lines[0])
                    dim_help.stylize("dim")
                    label.append_text(dim_help)
                    for line in lines[1:]:
                        label.append("\n")
                        indent_text = Text(" " * help_start_relative)
                        indent_text.stylize("dim")
                        label.append_text(indent_text)
                        dim_line = Text(line)
                        dim_line.stylize("dim")
                        label.append_text(dim_line)
            cmd_branch = branch.add(label)
            for param in cmd.params:
                if isinstance(param, click.Option) and param.name != "help":
                    add_option_branch(
                        cmd_branch,
                        param,
                        level,
                        global_column,
                        indent_size,
                        console,
                        dim=not is_current,
                    )
            if isinstance(cmd, click.Group) and cmd.commands:
                add_to_tree(
                    cmd_branch,
                    cmd.commands,
                    level + 1,
                    path,
                    path_index + 1,
                    global_column,
                    indent_size,
                    console,
                    is_top_level,
                    path_len,
                )
