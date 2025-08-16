import rich_click as click

# This is not the best example since you could also
# set panel_styles={"title_align": "center"} without subclassing.

class CustomOptionPanel(click.RichOptionPanel):

    def render(self, command, ctx, formatter):
        panel = super().render(command, ctx, formatter)
        panel.title_align = "center"
        return panel

@click.command()
@click.argument("src")
@click.argument("dest")
@click.option("--env")
@click.option("--log-level")
@click.option_panel("Arguments", cls=CustomOptionPanel)
@click.option_panel("Options", cls=CustomOptionPanel)
@click.rich_config()
def move_item(src, dest, env, log_level):
    """Move an item from a src location to a dest location"""
    pass

if __name__ == "__main__":
    move_item()
