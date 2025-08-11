import click

@click.command()
@click.argument("name")
@click.option("--times", "-t",
              default=1,
              type=click.INT,
              show_default=True,
              help="Number of times to print the greeting.")
@click.option("--say-goodbye",
              is_flag=True,
              default=False,
              help="After saying hello, say goodbye.")
def hello(name, times, say_goodbye):
    """Prints 'hello, [name]!' into the terminal N times."""
    for t in range(times):
        print(f"Hello, {name}!")
    if say_goodbye:
        print("Goodbye!")

if __name__ == "__main__":
    hello()
