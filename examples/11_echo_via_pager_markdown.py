import rich_click as click
from rich.__main__ import make_test_card

click.rich_click.USE_MARKDOWN = True

# regular text
sample_text = """
# Lorem Ipsum

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sollicitudin tempor id eu nisl nunc mi ipsum. Consequat mauris nunc congue nisi vitae suscipit tellus mauris a. Dapibus ultrices in iaculis nunc sed augue lacus viverra vitae. Rutrum quisque non tellus orci ac auctor augue. Praesent tristique magna sit amet purus. Orci phasellus egestas tellus rutrum. Nibh praesent tristique magna sit amet purus gravida. Aliquam eleifend mi in nulla posuere sollicitudin aliquam ultrices sagittis. Tellus molestie nunc non blandit massa enim nec. Quam id leo in vitae turpis massa sed elementum tempus.

Pulvinar neque laoreet suspendisse interdum consectetur libero id faucibus. Tellus id interdum velit laoreet id donec ultrices tincidunt arcu. Eros in cursus turpis massa tincidunt. Lorem dolor sed viverra ipsum nunc. Et tortor at risus viverra adipiscing at in tellus integer. Nulla malesuada pellentesque elit eget gravida cum sociis natoque. Tincidunt nunc pulvinar sapien et ligula. Amet venenatis urna cursus eget nunc. Et egestas quis ipsum suspendisse ultrices gravida. Tellus mauris a diam maecenas. Tellus elementum sagittis vitae et leo. Facilisis sed odio morbi quis commodo odio aenean sed adipiscing. Blandit massa enim nec dui nunc mattis enim ut tellus. Aenean sed adipiscing diam donec adipiscing. Sapien faucibus et molestie ac feugiat sed lectus. Aenean et tortor at risus viverra adipiscing. Odio euismod lacinia at quis. Proin libero nunc consequat interdum varius sit amet. Viverra tellus in hac habitasse platea dictumst vestibulum.

Luctus accumsan tortor posuere ac ut consequat semper viverra nam. Gravida arcu ac tortor dignissim. Arcu cursus euismod quis viverra nibh cras pulvinar mattis nunc. Consequat ac felis donec et odio. Eros donec ac odio tempor orci dapibus ultrices in. Etiam tempor orci eu lobortis elementum nibh tellus. Penatibus et magnis dis parturient montes nascetur ridiculus mus. Quam viverra orci sagittis eu volutpat odio facilisis. Duis at tellus at urna condimentum mattis pellentesque id nibh. Lobortis feugiat vivamus at augue eget arcu dictum varius. Nibh tellus molestie nunc non blandit massa enim nec. Dapibus ultrices in iaculis nunc sed augue lacus viverra. Faucibus et molestie ac feugiat sed lectus. Etiam erat velit scelerisque in dictum non consectetur a. Scelerisque fermentum dui faucibus in ornare quam viverra orci. Sed sed risus pretium quam vulputate dignissim suspendisse. Feugiat in fermentum posuere urna. Montes nascetur ridiculus mus mauris vitae ultricies leo integer malesuada. Nunc id cursus metus aliquam eleifend. Nisl condimentum id venenatis a condimentum.

Augue mauris augue neque gravida in fermentum. Augue mauris augue neque gravida. Felis eget nunc lobortis mattis aliquam faucibus purus in. Nisl condimentum id venenatis a condimentum. Imperdiet dui accumsan sit amet. Quis enim lobortis scelerisque fermentum dui. Turpis massa tincidunt dui ut ornare lectus sit amet. Viverra justo nec ultrices dui sapien eget. Vitae semper quis lectus nulla at volutpat diam. Est ante in nibh mauris cursus.

Egestas dui id ornare arcu. Risus in hendrerit gravida rutrum. Sed lectus vestibulum mattis ullamcorper. Mauris a diam maecenas sed enim ut sem viverra aliquet. Et netus et malesuada fames ac turpis egestas maecenas. Odio eu feugiat pretium nibh ipsum consequat. Aliquet lectus proin nibh nisl condimentum id venenatis a condimentum. Sed cras ornare arcu dui. Turpis tincidunt id aliquet risus feugiat. Vel pretium lectus quam id leo in. Cras sed felis eget velit aliquet sagittis id consectetur purus. Vulputate enim nulla aliquet porttitor. Non curabitur gravida arcu ac tortor dignissim convallis. Rutrum quisque non tellus orci ac auctor. Mauris nunc congue nisi vitae suscipit tellus mauris a. Fringilla urna porttitor rhoncus dolor purus non enim praesent. Est pellentesque elit ullamcorper dignissim cras tincidunt lobortis. Mattis aliquam faucibus purus in. Euismod elementum nisi quis eleifend quam.
    """.replace(
    "Lorem", "**Lorem**"
).replace(
    "ipsum", "*ipsum*"
)

input("Press Enter to see pager with sample text")
click.echo_via_pager(sample_text)
