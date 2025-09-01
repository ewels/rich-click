# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.command("newline-control")
@click.rich_config({"text_paragraph_linebreaks": "\n\n"})
def cli():
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
