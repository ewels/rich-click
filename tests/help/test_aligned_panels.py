import pytest
from click.testing import CliRunner
from inline_snapshot import snapshot

import rich_click
from tests.conftest import load_command_from_module


@pytest.fixture
def cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.help.fixtures.aligned_panels")
    return cmd


@pytest.fixture
def wrap_cli() -> rich_click.RichCommand:
    cmd = load_command_from_module("tests.help.fixtures.aligned_panels_wrap")
    return cmd


def test_aligned_panels_help(cli_runner: CliRunner, cli: rich_click.RichCommand) -> None:
    result = cli_runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS] COMMAND [ARGS]...                                                             \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --config   -c  PATH  Config file. [required]                                                  │
│    --help               Show this message and exit.                                              │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Core ───────────────────────────────────────────────────────────────────────────────────────────╮
│ run                     Run the thing.                                                           │
│ a-much-longer-name      Do something else.                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Extras ─────────────────────────────────────────────────────────────────────────────────────────╮
│ tidy                    Tidy up.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Logging ────────────────────────────────────────────────────────────────────────────────────────╮
│    --verbose            Be loud.                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")


def test_aligned_panels_wide_entries(cli_runner: CliRunner, wrap_cli: rich_click.RichCommand) -> None:
    """Entries too wide for their own column spill into the empty ones, or fall to the next line."""
    result = cli_runner.invoke(wrap_cli, "--help")
    assert result.exit_code == 0
    assert result.stdout == snapshot("""\
                                                                                                    \n\
 Usage: cli [OPTIONS]                                                                               \n\
                                                                                                    \n\
 CLI help text                                                                                      \n\
                                                                                                    \n\
╭─ Output ─────────────────────────────────────────────────────────────────────────────────────────╮
│ --output                          [svg|html|png|gif|webp|webm]  Output format.                   │
│ --reject-output-outside-source/--no-reject-output-outside-source                                 │
│                                                                 Reject an output path outside    │
│                                                                 the source repository.           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Layout ─────────────────────────────────────────────────────────────────────────────────────────╮
│ --center-ports/--no-center-ports                                Centre inter-section ports.      │
│ --mode                            [light|dark|auto]             Palette to render with.          │
│ --compact-offsets/--no-compact-offsets                          Size each station for its lines. │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help                                                          Show this message and exit.      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
""")
