import rich_click as click


@click.command()
@click.option(
    "--output",
    type=click.Choice(["svg", "html", "png", "gif", "webp", "webm"]),
    help="Output format.",
)
@click.option("--center-ports/--no-center-ports", help="Centre inter-section ports.")
@click.option("--mode", type=click.Choice(["light", "dark", "auto"]), help="Palette to render with.")
@click.option("--compact-offsets/--no-compact-offsets", help="Size each station for its lines.")
@click.option(
    "--reject-output-outside-source/--no-reject-output-outside-source",
    help="Reject an output path outside the source repository.",
)
@click.option_panel("Output", options=["output", "reject_output_outside_source"])
@click.option_panel("Layout", options=["center_ports", "mode", "compact_offsets"])
@click.rich_config({"align_columns_across_panels": True, "wrap_long_options": 32})
def cli() -> None:
    """CLI help text"""
