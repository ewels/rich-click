import rich_click as click
from rich import print

click.rich_click.USE_MARKDOWN = True

test_strings = [
    "# This is a test.",
    "**This is bold.**",
    "*This is italic.*",
]

print("[bold][underline]Use rich_click.echo just like click.echo")
for test_str in test_strings:
    click.echo(test_str)

print("\n[bold][underline]rich_click.echo takes same args as click.echo: nl=False")
for test_str in test_strings:
    click.echo(test_str, nl=False)

print(
    "\n\n[bold][underline]rich_click.echo passes any args besides file, nl, err, color to rich.console.Console.print"
)
print("[bold]end='\\n\\n'")
for test_str in test_strings:
    click.echo(test_str, end="\n\n")
