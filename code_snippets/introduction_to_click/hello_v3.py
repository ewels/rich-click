import click

@click.group("greetings")
def greetings_cli():
    """CLI for greetings."""

@greetings_cli.command("english")
@click.argument("name")
def english(name):
    """Greet in English"""
    print(f"Hello, {name}!")

@greetings_cli.command("french")
@click.argument("name")
def french(name):
    """Greet in French"""
    print(f"Bonjour, {name}!")

if __name__ == "__main__":
    greetings_cli()
