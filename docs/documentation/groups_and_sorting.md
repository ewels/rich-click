# Groups & Sorting

**rich-click** gives functionality to list options and subcommands in groups, printed as separate panels.
It accepts a list of options / commands which means you can also choose a custom sorting order.

- For options / flags, set `click.rich_click.OPTION_GROUPS`
- For subcommands / Click groups, set `click.rich_click.COMMAND_GROUPS`

<div class="termy termy-static" static="true" style="width: 100%">

```console
$ python examples/03_groups_sorting.py --help

 <span style="color: #808000; text-decoration-color: #808000">Usage:</span> <span style="font-weight: bold">03_groups_sorting.py</span> [<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">OPTIONS</span>] <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">COMMAND</span> [<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">ARGS</span>]...
                                                                        
 My amazing tool does all the things.                                   
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">This is a minimal example based on documentation from the &#x27;click&#x27; </span>     
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">package.</span>                                                               
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">You can try using </span><span style="color: #7fbfbf; text-decoration-color: #7fbfbf; font-weight: bold">--help</span><span style="color: #7f7f7f; text-decoration-color: #7f7f7f"> at the top level and also for specific </span>       
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">subcommands.</span>                                                           
                                                                        
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Options ────────────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #800000; text-decoration-color: #800000">*</span>  <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--type</span>                     <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">TEXT</span>  Type of file to sync             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                     <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">[default: files]    </span>             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                     <span style="color: #bf7f7f; text-decoration-color: #bf7f7f">[required]          </span>             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>    <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--debug</span>/<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--no-debug</span>  <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">-d</span>/<span style="color: #008000; text-decoration-color: #008000; font-weight: bold">-n</span>  <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">    </span>  Show the debug log messages      <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                     <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">[default: no-debug]        </span>      <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>    <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--version</span>                  <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">    </span>  Show the version and exit.       <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>    <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--help</span>              <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">-h</span>     <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">    </span>  Show this message and exit.      <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Main usage ─────────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">sync       </span> Synchronise all your files between two places.           <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">download   </span> Pretend to download some files from somewhere.           <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Configuration ──────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">config     </span> Set up the configuration.                                <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">auth       </span> Authenticate the app.                                    <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
```

</div>

When grouping subcommands into more than one group (in above example: 'Main usage' and 'Configuration') you may find that the automatically calculated widths of different groups do not line up, due to varying option name lengths.

You can avoid this by enforcing the alignment of the help text across groups by setting `click.rich_click.STYLE_COMMANDS_TABLE_COLUMN_WIDTH_RATIO = (1, 2)`. This results in a fixed ratio of 1:2 for the width of command name and help text column.

!!! info
    See [`examples/03_groups_sorting.py`](https://github.com/ewels/rich-click/blob/main/examples/03_groups_sorting.py) for a full example.

### Options

To group option flags into two sections with custom names, see the following example:

```python
click.rich_click.OPTION_GROUPS = {
    "mytool": [
        {
            "name": "Simple options",
            "options": ["--name", "--description", "--version", "--help"],
        },
        {
            "name": "Advanced options",
            "options": ["--force", "--yes", "--delete"],
        },
    ]
}
```

If you omit `name` it will use `Commands` (can be configured with `OPTIONS_PANEL_TITLE`).

### Commands

Here we create two groups of commands for the base command of `mytool`.
Any subcommands not listed will automatically be printed in a panel at the end labelled "Commands" as usual.

```python
click.rich_click.COMMAND_GROUPS = {
    "mytool": [
        {
            "name": "Commands for uploading",
            "commands": ["sync", "upload"],
        },
        {
            "name": "Download data",
            "commands": ["get", "fetch", "download"],
        },
    ]
}
```

If you omit `name` it will use `Commands` (can be configured with `COMMANDS_PANEL_TITLE`).

### Multiple commands

If you use multiple nested subcommands, you can specify their commands using the top-level dictionary keys:

```python
click.rich_click.COMMAND_GROUPS = {
    "mytool": [{"commands": ["sync", "auth"]}],
    "mytool sync": [
        {
            "name": "Commands for uploading",
            "commands": ["sync", "upload"],
        },
        {
            "name": "Download data",
            "commands": ["get", "fetch", "download"],
        },
    ],
    "mytool auth":[{"commands": ["login", "logout"]}],
}
```

### Table styling

Typically you would style the option / command tables using the global config options.
However, if you wish you may style tables on a per-group basis using the `table_styles` key:

```python
click.rich_click.COMMAND_GROUPS = {
    "mytool": [
        {
            "commands": ["sync", "auth"],
            "table_styles": {
                "show_lines": True,
                "row_styles": ["magenta", "yellow", "cyan", "green"],
                "border_style": "red",
                "box": "DOUBLE",
            },
        },
    ],
}
```

The available keys are: `show_lines`, `leading`, `box`, `border_style`, `row_styles`, `pad_edge`, `padding`.
