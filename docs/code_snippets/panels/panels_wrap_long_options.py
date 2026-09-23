# /// script
# dependencies = ["rich-click>=1.9"]
# ///
import rich_click as click

@click.command()
@click.option("--reject-output-outside-source/--no-reject-output-outside-source", default=True,
              help="Refuse to write output outside the source tree")
@click.option("--format", "-f", type=click.Choice(["svg", "png"]), help="Output format")
@click.option("--out", "-o", type=click.Path(), help="Where to write the rendered diagram")
@click.option("--verbose-progress", is_flag=True, help="Report each file as it is written")
@click.option("--report-but-do-not-write-it", is_flag=True, help="Say what would be written")
@click.rich_config({"wrap_long_options": 24})
def render(**kwargs):
    """A wide entry runs on under the empty columns, or drops its help below"""
    pass

if __name__ == "__main__":
    render()
