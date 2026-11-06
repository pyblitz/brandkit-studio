"""BrandKit Studio — generate a consistent mini brand kit from a name + palette.

Pure-Python (Pillow only) tool that turns a brand name, tagline and two
hex colours into three ready-to-post images:

* ``logo.png``      — 1080x1080 logo lockup
* ``post.png``      — 1080x1080 social-media post creative
* ``thumbnail.png`` — 1280x720 YouTube-style thumbnail

It also checks colour contrast (WCAG-style luminance ratio) so the text
colour it picks is actually readable on the chosen background.
"""

from .colours import contrast_ratio, parse_hex, pick_text_colour
from .generate import generate_kit

__all__ = ["contrast_ratio", "parse_hex", "pick_text_colour", "generate_kit"]
__version__ = "0.1.0"
