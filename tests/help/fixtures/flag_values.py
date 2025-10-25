import rich_click as click


@click.command()
@click.option("--a", "abc", flag_value="a_val", help="A flag.")
@click.option("--b", "abc", flag_value="b_cal", default=True, help="B flag.")
@click.option("--c", "abc", flag_value="c_val", help="C flag.")
def cli(abc: str) -> None:
    """Select one of three flags"""
    print(abc)


if __name__ == "__main__":
    cli()
