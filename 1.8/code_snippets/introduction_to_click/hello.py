import click

@click.command()
def hello():
    """Prints 'hello, world!' into the terminal."""
    print("Hello, world!")

if __name__ == "__main__":
    hello()
