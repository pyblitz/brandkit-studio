"""Colour helpers: hex parsing, WCAG-style luminance and contrast."""

from __future__ import annotations

import re

_HEX_RE = re.compile(r"^#?([0-9a-fA-F]{6})$")


def parse_hex(value: str) -> tuple[int, int, int]:
    """Parse ``#RRGGBB`` (``#`` optional) into an ``(r, g, b)`` tuple.

    Raises ValueError on anything else, so a typoed palette fails fast
    instead of silently producing a black image.
    """
    match = _HEX_RE.match(value.strip())
    if not match:
        raise ValueError(f"expected a #RRGGBB colour, got {value!r}")
    hexpart = match.group(1)
    return tuple(int(hexpart[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _linearise(channel: int) -> float:
    c = channel / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(rgb: tuple[int, int, int]) -> float:
    """Relative luminance of an sRGB colour (0.0 black … 1.0 white)."""
    r, g, b = (_linearise(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    """WCAG contrast ratio between two colours (1.0 … 21.0)."""
    la, lb = luminance(a), luminance(b)
    light, dark = max(la, lb), min(la, lb)
    return (light + 0.05) / (dark + 0.05)


def pick_text_colour(background: tuple[int, int, int]) -> tuple[int, int, int]:
    """Return black or white, whichever contrasts better with ``background``."""
    black, white = (0, 0, 0), (255, 255, 255)
    return white if contrast_ratio(background, white) >= contrast_ratio(background, black) else black
