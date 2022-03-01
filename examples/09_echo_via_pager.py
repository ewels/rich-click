import rich_click as click
from rich.__main__ import make_test_card

# default settings
input("Press Enter to see default pager settings")
click.echo_via_pager(make_test_card())

# pass color param like click.echo_via_pager
input("Press Enter to see pager with color=False")
click.echo_via_pager(make_test_card(), color=False)

# any other args are passed to rich.console.Console.print
input("Press Enter to see pager with width=40")
click.echo_via_pager(make_test_card(), width=40)
