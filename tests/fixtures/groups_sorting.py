from click import password_option

import rich_click as click

click.rich_click.OPTION_GROUPS = {
    "cli": [
        {
            "name": "Basic usage",
            "options": ["--type", "--output"],
        },
        {
            "name": "Advanced options",
            "options": ["--version", "--debug"],
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
    ],
    "* auth": [
        {
            "name": "Required",
            "options": ["--user", "--password"],
        },
        {
            "name": "Misc.",
            "options": ["--email", "--role"],
        },
        {
            # This should deduplicate the "--help" panels elsewhere.
            # It should also be guaranteed to occur at the bottom.
            "name": "Auth help",
            "options": ["--help"],
        },
    ],
    "*": [
        {
            "name": "Help",
            "options": ["--help"],
        },
    ],
    "* *": [
        {
            "name": "Subcommand help",
            "options": ["--help"],
        },
    ],
}
click.rich_click.COMMAND_GROUPS = {
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
}


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("--type", default="files", show_default=True, required=True, help="Type of file to sync")
@click.option("--debug/--no-debug", "-d/-n", default=False, show_default=True, help="Show the debug log messages")
@click.version_option("1.23", prog_name="mytool")
def cli(type: str, debug: bool) -> None:
    """
    My amazing tool does all the things.

    This is a minimal example based on documentation
    from the 'click' package.

    You can try using --help at the top level and also for
    specific subcommands.
    """
    print(f"Debug mode is {'on' if debug else 'off'}")


@cli.command()
@click.option("--input", "-i", "input_", required=True, help="Input path")
@click.option("--output", "-o", help="Output path")
@click.option("--all", "all_", is_flag=True, help="Sync all the things?")
@click.option("--overwrite", is_flag=True, help="Overwrite local files")
def sync(input_: str, output: str, all_: bool, overwrite: bool) -> None:
    """Synchronise all your files between two places."""
    print("Syncing")


@cli.command()
@click.option("--all", is_flag=True, help="Get everything")
def download(all: bool) -> None:
    """Pretend to download some files from somewhere."""
    print("Downloading")


@cli.command()
@click.password_option("--user", "-u", help="User", required=True)
@click.password_option("--password", "-p", help="Password", required=True)
@click.password_option("--email", "-e", help="Email")
@click.password_option("--role", "-r", help="Role", default="admin")
def auth(user: str, password: str, email: str) -> None:
    """Authenticate the app."""
    print("Authenticating")


@cli.command()
def config() -> None:
    """Set up the configuration."""
    print("Downloading")


if __name__ == "__main__":
    cli()
