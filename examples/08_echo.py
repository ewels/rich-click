import rich_click as click
from rich import print

test_strings = [
    "This is a test.",
    "[bold]This is bold.[/bold]",
    "[italic]This is italic.[/italic]",
    "[bold][italic]This is bold and italic.[/italic][/bold]",
    "[red]This is red[/red]",
    "[green]This is green.[/green]",
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
