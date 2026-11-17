"""
Detect whether the terminal has a dark or light background.

Detection runs in this order, stopping at the first answer:

1. The ``RICH_CLICK_BACKGROUND`` env var (``dark`` or ``light``), so users can always override detection.
2. The ``COLORFGBG`` env var (``fg;bg``), which some terminals set (rxvt, Konsole, iTerm2).
3. Asking the terminal for its background color with an OSC 11 query.

The OSC 11 query is only sent when stdin and stdout are both an interactive terminal on POSIX,
and the process is in the foreground. Otherwise, the result is ``None`` (unknown).
"""

from __future__ import annotations

import os
import re
import sys
from functools import lru_cache
from typing import Literal


Background = Literal["dark", "light"]

# Max seconds to wait for the terminal to reply.
QUERY_TIMEOUT = 0.1

# ANSI colors 0-6 and 8 are dark; 7 and 9-15 are light.
_DARK_ANSI_COLORS = {0, 1, 2, 3, 4, 5, 6, 8}

_RE_DA1_REPLY = re.compile(rb"\x1b\[\?[\d;]*c")
_RE_OSC11_REPLY = re.compile(rb"\x1b\]11;rgba?:([0-9a-f]{1,4})/([0-9a-f]{1,4})/([0-9a-f]{1,4})", re.IGNORECASE)


def _from_env_override() -> Background | None:
    value = os.environ.get("RICH_CLICK_BACKGROUND", "").strip().lower()
    if value in ("dark", "light"):
        return value  # type: ignore[return-value]
    return None


def _from_colorfgbg() -> Background | None:
    value = os.environ.get("COLORFGBG")
    if not value:
        return None
    bg = value.split(";")[-1]
    if not bg.isdigit():
        return None
    return "dark" if int(bg) in _DARK_ANSI_COLORS else "light"


def parse_osc11_reply(reply: bytes) -> Background | None:
    """Parse a terminal's OSC 11 reply, e.g. ``ESC ] 11 ; rgb:ffff/ffff/ffff BEL``."""
    m = _RE_OSC11_REPLY.search(reply)
    if not m:
        return None
    r, g, b = (int(x, 16) / (16 ** len(x) - 1) for x in m.groups())
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return "dark" if luminance < 0.5 else "light"


def _query_terminal(timeout: float = QUERY_TIMEOUT) -> bytes:
    if os.name != "posix" or os.environ.get("TERM") == "dumb":
        return b""
    try:
        if not (sys.stdin.isatty() and sys.stdout.isatty()):
            return b""
        fd_in = sys.stdin.fileno()
        fd_out = sys.stdout.fileno()
        # Changing terminal modes from a background process would stop it with SIGTTOU.
        if os.tcgetpgrp(fd_in) != os.getpgrp():
            return b""
    except (AttributeError, OSError, ValueError):
        return b""

    import select
    import termios
    import time
    import tty

    try:
        old_attrs = termios.tcgetattr(fd_in)
    except termios.error:
        return b""

    buf = b""
    try:
        tty.setcbreak(fd_in, termios.TCSANOW)
        sys.stdout.flush()
        # Send the OSC 11 query followed by a DA1 query. Almost every terminal answers DA1,
        # so its reply tells us to stop waiting even if OSC 11 is unsupported.
        os.write(fd_out, b"\x1b]11;?\x1b\\\x1b[c")
        deadline = time.monotonic() + timeout
        while not _RE_DA1_REPLY.search(buf):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            ready, _, _ = select.select([fd_in], [], [], remaining)
            if not ready:
                break
            chunk = os.read(fd_in, 1024)
            if not chunk:
                break
            buf += chunk
    except (OSError, termios.error):
        pass
    finally:
        try:
            termios.tcsetattr(fd_in, termios.TCSADRAIN, old_attrs)
        except termios.error:
            pass
    return buf


@lru_cache(maxsize=1)
def detect_background() -> Background | None:
    """
    Detect whether the terminal has a dark or light background.

    Returns
    -------
        ``"dark"``, ``"light"``, or ``None`` if the background could not be detected.

    """
    return _from_env_override() or _from_colorfgbg() or parse_osc11_reply(_query_terminal())
