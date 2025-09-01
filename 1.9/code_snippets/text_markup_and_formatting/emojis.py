# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.command()
@click.option("--foo", "-f", help="Boo! :ghost: Oops, I mean... foo! :sweat_smile:")
@click.option("--bar", "-b", help="Bar - :bar_chart:")
@click.rich_config({"text_emojis": True})
def cli():
    """Demo of :heart_eyes_cat: emojis!

    Note that this text is not rich markup: [b]See?[/b] :joy:

    Emojis can be controlled independent of markup. :point_up: :nerd_face:
    """

if __name__ == "__main__":
    cli()
