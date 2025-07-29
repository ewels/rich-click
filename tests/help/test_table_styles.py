import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.fixtures.table_styles")
    return cmd


def test_table_styles_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot(
        """\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 My amazing tool does all the things.                                                               \n\
 This is a minimal example based on documentation from the 'click' package.                         \n\
 You can try using --help at the top level and also for specific group subcommands.                 \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                  │
│  --type                       TEXT   Type of file to sync. Lorem ipsum dolor sit amet,           │
│                                      consectetur adipiscing elit. Sed sed mauris euismod,        │
│                                      semper leo quis, sodales augue. Donec posuere nulla quis    │
│                                      egestas ornare. Nam efficitur ex quis diam tempus, nec      │
│                                      euismod diam consectetur. Etiam vitae nisi at odio          │
│                                      hendrerit dictum in at dui. Aliquam nulla lacus,            │
│                                      pellentesque id ultricies sit amet, mollis nec tellus.      │
│                                      Aenean arcu justo, pellentesque viverra justo eget, tempus  │
│                                      tincidunt lectus. Maecenas porttitor risus vitae libero     │
│                                      dapibus ullamcorper. Cras faucibus euismod erat in porta.   │
│                                      Phasellus cursus gravida ante vel aliquet. In accumsan      │
│                                      enim nec ullamcorper gravida. Donec malesuada dui ac metus  │
│                                      tristique cursus. Sed gravida condimentum fermentum. Ut     │
│                                      sit amet nulla commodo, iaculis tellus vitae, accumsan      │
│                                      enim. Curabitur mollis semper velit a suscipit.             │
│                                                                                                  │
│  --debug/--no-debug   -d/-n          Show the debug log messages. Suspendisse dictum hendrerit   │
│                                      turpis eu rutrum. Vivamus magna ex, elementum sit amet      │
│                                      sapien laoreet, tempor consequat eros. Morbi semper         │
│                                      feugiat nisi eget sodales. Pellentesque et turpis erat.     │
│                                      Donec ac aliquam risus. Nam leo tellus, rutrum et           │
│                                      scelerisque vitae, ultrices sed metus. Ut sollicitudin      │
│                                      convallis turpis, sit amet sollicitudin felis semper        │
│                                      feugiat. In sapien dui, aliquam eget dui quis, auctor       │
│                                      maximus nibh. Suspendisse maximus sem arcu. Pellentesque    │
│                                      sit amet semper est. Cras pulvinar ut tellus a semper. In   │
│                                      facilisis tellus odio, non porta nisl accumsan nec.         │
│                                      Pellentesque sollicitudin quam ac felis congue, ac congue   │
│                                      enim tempor.                                                │
│                                                                                                  │
│  --version                           Show the version and exit.                                  │
│                                                                                                  │
│  --help                              Show this message and exit.                                 │
│                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ ╔══════════╦═══════════════════════════════════════════════════════════════════════════════════╗ │
│ ║ auth     ║ Authenticate the app. Duis lacus nibh, feugiat a nibh a, commodo dictum libero.   ║ │
│ ║          ║ Ut ac nulla tincidunt, bibendum nisi vitae, sodales ex. Vestibulum efficitur,     ║ │
│ ║          ║ lectus quis venenatis porta, dolor elit varius mauris, consequat interdum lectus  ║ │
│ ║          ║ est quis mi. Vestibulum imperdiet sed dolor eget semper. Cras ut mauris ac libero ║ │
│ ║          ║ hendrerit congue. Vivamus pretium nunc turpis, eget imperdiet sapien tempor       ║ │
│ ║          ║ auctor. Phasellus risus nisi, laoreet in posuere sit amet, sodales non diam.      ║ │
│ ║          ║ Aliquam non malesuada urna, a faucibus risus.                                     ║ │
│ ╠══════════╬═══════════════════════════════════════════════════════════════════════════════════╣ │
│ ║ config   ║ Set up the configuration. Sed accumsan ornare odio dictum aliquam. Pellentesque   ║ │
│ ║          ║ habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.  ║ │
│ ║          ║ Curabitur in pellentesque mauris. Nulla mollis dui finibus, dictum neque id,      ║ │
│ ║          ║ suscipit nisl. Nunc mauris ex, laoreet nec tincidunt ut, pellentesque ut tortor.  ║ │
│ ║          ║ Mauris fermentum diam at porttitor tempor. Aliquam euismod nisi massa, nec        ║ │
│ ║          ║ placerat ante euismod quis.                                                       ║ │
│ ╠══════════╬═══════════════════════════════════════════════════════════════════════════════════╣ │
│ ║ download ║ Pretend to download some files from somewhere. Integer bibendum libero nunc, sed  ║ │
│ ║          ║ aliquet ex tincidunt vel. Duis vitae sem vel odio luctus suscipit nec vitae enim. ║ │
│ ║          ║ Curabitur vel lectus nec quam maximus dapibus. Phasellus eros velit, maximus non  ║ │
│ ║          ║ hendrerit nec, tempor fringilla urna. Vivamus vel nibh quis sapien consectetur    ║ │
│ ║          ║ fermentum. Curabitur at ultrices quam, vel molestie justo. Nunc lobortis orci vel ║ │
│ ║          ║ nibh sagittis pretium. Morbi rhoncus sapien luctus, ultrices urna vel, convallis  ║ │
│ ║          ║ tortor.                                                                           ║ │
│ ╠══════════╬═══════════════════════════════════════════════════════════════════════════════════╣ │
│ ║ sync     ║ Synchronise all your files between two places. Curabitur congue eget lorem in     ║ │
│ ║          ║ lacinia. Praesent tempus nunc nec nulla dignissim, et lacinia ipsum accumsan.     ║ │
│ ║          ║ Duis sodales, sapien at fermentum condimentum, diam metus porttitor lacus, nec    ║ │
│ ║          ║ gravida mi diam eget ligula. Pellentesque elementum at justo a luctus. Mauris a   ║ │
│ ║          ║ interdum odio. Maecenas in consectetur velit. Ut tristique congue felis at        ║ │
│ ║          ║ tempus. Donec pulvinar tortor ut odio posuere imperdiet. Fusce lacinia iaculis    ║ │
│ ║          ║ diam in scelerisque. Pellentesque in lorem est. Nulla efficitur luctus lacus,     ║ │
│ ║          ║ auctor auctor dui hendrerit a. Ut nec iaculis dolor. Morbi metus lectus, aliquet  ║ │
│ ║          ║ et sapien nec, congue euismod lorem. Pellentesque tristique tempus augue at       ║ │
│ ║          ║ convallis.                                                                        ║ │
│ ╚══════════╩═══════════════════════════════════════════════════════════════════════════════════╝ │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
"""
    )
    assert result.stderr == snapshot("")
