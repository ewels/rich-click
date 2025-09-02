# /// script
# dependencies = ["click<9"]
# ///
import click

@click.command("newline-control")
def cli():
    """Newline
    control

    Double newlines are always preserved.
    But single newlines are usually not.

    There are however a few situations where we preserve single newlines.

    Indented lines with 4+ spaces are preserved:
        ```python
        from foo import bar
        \n\
        bar.action()
        ```

    Unordered lists are preserved:

    - like
    - this

    also:

    * newlines within unordered lists
      are collapsed
      down.
    * pretty neat!

    Last but not least, we preserve:

    > block
    > quotes
    """

if __name__ == "__main__":
    cli()
