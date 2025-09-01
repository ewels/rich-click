# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.group("app", epilog="For more assistance, visit https://example.com/")
@click.option("--environment", "-e",
              type=click.Choice(["dev", "staging", "prod"]),
              help="Environment to run in",
              required=True,
              envvar="APP_ENV",
              show_envvar=True)
@click.option("--env-file",
              type=click.Path(),
              help=".env file")
@click.option("--retries", "-r",
              type=click.IntRange(min=0, max=10),
              help="Num retries for failed tasks")
@click.option("--vcpu", "-c",
              type=click.IntRange(min=1, max=32),
              default=4,
              show_default=True,
              help="Num vCPUs")
@click.option("--memory", "-m",
              type=click.IntRange(min=1, max=32),
              default=4,
              show_default=True,
              hidden=True,
              help="Memory (this is hidden)")
@click.option("--log-level", "-l",
              type=click.Choice(["debug", "info", "warning", "error"]),
              default="info",
              show_default=True,
              help="Log level",
              envvar="APP_LOG_LEVEL",
              show_envvar=True)
@click.option("--colors/--no-colors", "-C/-n",
              default=True,
              show_default=True,
              help="Whether to show colors in logs")
@click.option("--log-format",
              type=click.Choice(["json", "text"]),
              show_choices=False,
              deprecated=True,
              help="Log format")
@click.option("--quiet/--no-quiet", "-q",
              deprecated="use --log-level instead",
              help="Print text")
@click.help_option("--help", "-h")
@click.version_option("1.2.3", "--version", "-v")
@click.option_panel("Runtime options",
                    options=["environment", "env_file", "retries", "vcpu"],
                    help="Options specifying the runtime")
@click.option_panel("Logging options",
                    options=["log_level", "colors", "log_format", "quiet"],
                    help="Logging config options")
@click.option_panel("Misc. options", options=["--version", "--help"])
@click.command_panel("Commands", help="All subcommands")
def cli(*args, **kwargs):
    """
    CLI for app

    This is a production-ready application.
    """

@cli.command("db")
def db():
    """Database commands for app"""

@cli.command("deploy")
def deploy():
    """Deploy app"""

@cli.command("admin")
def admin():
    """Administrative commands"""

@cli.command("self", deprecated="Use admin commands")
def self():
    """Manage app"""

@cli.command("user", hidden=True)
def user():
    """User commands (This is hidden)"""

if __name__ == "__main__":
    cli()
