import rich_click as click

click.rich_click.OPTION_GROUPS = {
    "03_groups_sorting.py": [
        {
            "name": "Inputs and Outputs",
            "options": ["--input", "--output"],
        },
        {
            "name": "Advanced options",
            "options": ["--debug", "--version", "--help"],
        },
    ],
    "03_groups_sorting.py sync": [
        {
            "name": "Basic usage",
            "options": ["--type", "--all", "--help"],
        },
        {
            "name": "Advanced usage",
            "options": ["--overwrite"],
        },
    ],
}
click.rich_click.COMMAND_GROUPS = {
    "03_groups_sorting.py": [
        {
            "name": "Main usage",
            "commands": ["download", "sync"],
        },
        {
            "name": "Configuration",
            "commands": ["config", "auth"],
        },
    ]
}


@click.group()
@click.option("--input", "-i", help="Input path")
@click.option("--output", "-o", help="Output path")
@click.option(
    "--debug/--no-debug",
    "-d/-n",
    default=False,
    show_default=True,
    help="Show the debug log messages",
)
@click.version_option("1.23", prog_name="multiqc")
def cli(input, output, debug):
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific group subcommands.
    """
    print(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.option(
    "--type",
    required=True,
    default="files",
    show_default=True,
    help="Type of file to sync",
)
@click.option("--all", is_flag=True, help="Sync all the things?")
@click.option("--overwrite", is_flag=True, help="Overwrite local files")
def sync(type, all, overwrite):
    """Synchronise all your files between two places"""
    print("Syncing")


@cli.command()
@click.option("--all", is_flag=True, help="Get everything")
def download(all):
    """Pretend to download some files from somewhere"""
    print("Downloading")


@cli.command()
def auth():
    """Authenticate the app"""
    print("Downloading")


@cli.command()
def config():
    """Set up the configuration"""
    print("Downloading")


if __name__ == "__main__":
    cli()
