# /// script
# dependencies = ["click<9"]
# ///
import click

@click.command("newline-control")
def cli(*args, **kwargs):
    """Newline control

    Double newlines are always preserved.
    But single newlines are usually not.

    There are however a few situations where we preserve single newlines.

    Indented lines with 4+ spaces are preserved:
        ```python
        from foo import bar

        bar.action()
        ```

    Unordered lists are preserved:

    - like
    - this

    or:

    * like
    * this

    Last but not least, we preserve:

    > block
    > quotes

    """

if __name__ == "__main__":
    cli()
