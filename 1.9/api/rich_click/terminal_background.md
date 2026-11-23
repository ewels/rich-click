---
project: "rich-click"
title: "rich_click.terminal_background"
description: "Detect whether the terminal has a dark or light background."
url: "https://ewels.github.io/rich-click/latest/api/rich_click/terminal_background/"
---

# rich_click.terminal_background

*module*

Detect whether the terminal has a dark or light background.

Detection runs in this order, stopping at the first answer:

1. The ``RICH_CLICK_BACKGROUND`` env var (``dark`` or ``light``), so users can always override detection.
2. The ``COLORFGBG`` env var (``fg;bg``), which some terminals set (rxvt, Konsole, iTerm2).
3. Asking the terminal for its background color with an OSC 11 query.

The OSC 11 query is only sent when stdin and stdout are both an interactive terminal on POSIX,
and the process is in the foreground. Otherwise, the result is ``None`` (unknown).

How the terminal query works:

- We write two escape sequences to the terminal. The terminal answers them by "typing" its
  replies into our stdin, so we switch stdin to cbreak mode and read them back.
- ``ESC ] 11 ; ? ESC \`` (OSC 11) asks for the background color. A terminal that supports it
  replies ``ESC ] 11 ; rgb:RRRR/GGGG/BBBB``, which we convert to dark or light by its luminance.
  Terminals that don't support it stay silent.
- ``ESC [ c`` (DA1, "Primary Device Attributes") asks what kind of terminal this is. Nearly every
  terminal replies, with something like ``ESC [ ? 62 ; 22 c``. We don't care about its contents.
- Terminals reply in the order they were asked, so once the DA1 reply (``_RE_DA1_REPLY``) has
  arrived, any OSC 11 reply has already arrived too. That lets us stop reading straight away,
  rather than waiting out the timeout on terminals that never answer OSC 11.
- If no DA1 reply arrives before the timeout, we give up and discard any unread input. A reply
  that arrives after that is left for the shell to read, and shows up as garbage at the prompt.

[View source](https://github.com/ewels/rich-click/blob/520af5d995a2fb4611f2af73df5e09e6a358d866/src/rich_click/terminal_background.py#L1-L1)

## rich_click.terminal_background.Background

*attribute* · *module attribute*

```python
Background = Literal['dark', 'light']
```

[View source](https://github.com/ewels/rich-click/blob/520af5d995a2fb4611f2af73df5e09e6a358d866/src/rich_click/terminal_background.py#L38-L38)

## rich_click.terminal_background.QUERY_TIMEOUT

*attribute* · *module attribute*

```python
QUERY_TIMEOUT = 0.1
```

[View source](https://github.com/ewels/rich-click/blob/520af5d995a2fb4611f2af73df5e09e6a358d866/src/rich_click/terminal_background.py#L40-L40)

## rich_click.terminal_background.QUERY_TIMEOUT_SSH

*attribute* · *module attribute*

```python
QUERY_TIMEOUT_SSH = 0.5
```

[View source](https://github.com/ewels/rich-click/blob/520af5d995a2fb4611f2af73df5e09e6a358d866/src/rich_click/terminal_background.py#L41-L41)

## rich_click.terminal_background.detect_background

*function*

```python
def detect_background() -> Background | None
```

Detect whether the terminal has a dark or light background.

**Returns**

- (`Background | None`) — ``"dark"``, ``"light"``, or ``None`` if the background could not be detected.

[View source](https://github.com/ewels/rich-click/blob/520af5d995a2fb4611f2af73df5e09e6a358d866/src/rich_click/terminal_background.py#L141-L148)

## rich_click.terminal_background.parse_osc11_reply

*function*

```python
def parse_osc11_reply(reply: bytes) -> Background | None
```

Parse a terminal's OSC 11 reply, e.g. ``ESC ] 11 ; rgb:ffff/ffff/ffff BEL``.

[View source](https://github.com/ewels/rich-click/blob/520af5d995a2fb4611f2af73df5e09e6a358d866/src/rich_click/terminal_background.py#L68-L75)
