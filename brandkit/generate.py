"""Image generation: one palette in, three consistent images out."""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .colours import contrast_ratio, parse_hex, pick_text_colour

_FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
_FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _fit_font(draw: ImageDraw.ImageDraw, text: str, path: str, start: int, max_width: int) -> ImageFont.FreeTypeFont:
    """Shrink the font until ``text`` fits ``max_width`` (never below 24px)."""
    size = start
    while size > 24:
        font = _font(path, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 4
    return _font(path, 24)


def _gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    width, height = size
    base = Image.new("RGB", (1, height))
    for y in range(height):
        t = y / max(height - 1, 1)
        base.putpixel(
            (0, y),
            tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)),
        )
    return base.resize((width, height))


def _text(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font, fill, anchor: str = "mm") -> None:
    draw.text(xy, text, font=font, fill=fill, anchor=anchor)


def _accent_circle(image: Image.Image, colour, diameter: int, xy: tuple[int, int]) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    x, y = xy
    draw.ellipse([x, y, x + diameter, y + diameter], fill=colour + (70,))
    image.paste(Image.alpha_composite(image.convert("RGBA"), overlay).convert("RGB"), (0, 0))


def generate_kit(
    name: str,
    tagline: str,
    primary: str,
    secondary: str,
    outdir: str | os.PathLike,
) -> dict[str, str]:
    """Build the three kit images; return ``{kind: path}``.

    Raises ValueError for a bad palette. A contrast warning is printed
    (not raised) when the chosen text colour still falls below 4.5:1,
    so a weak palette is visible instead of silently unreadable.
    """
    if not name.strip():
        raise ValueError("brand name must not be empty")
    primary_rgb = parse_hex(primary)
    secondary_rgb = parse_hex(secondary)
    text = pick_text_colour(primary_rgb)
    ratio = contrast_ratio(primary_rgb, text)
    if ratio < 4.5:
        print(f"warning: text/background contrast is only {ratio:.1f}:1 (< 4.5:1)")

    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}

    # 1. Logo lockup — 1080x1080, monogram + name + tagline.
    img = _gradient((1080, 1080), primary_rgb, secondary_rgb)
    _accent_circle(img, secondary_rgb, 520, (700, -120))
    draw = ImageDraw.Draw(img)
    monogram = name.strip()[0].upper()
    _text(draw, (540, 380), monogram, _font(_FONT_BOLD, 260), text)
    name_font = _fit_font(draw, name.upper(), _FONT_BOLD, 120, 880)
    _text(draw, (540, 640), name.upper(), name_font, text)
    draw.rectangle([390, 720, 690, 730], fill=text)
    tag_font = _fit_font(draw, tagline, _FONT_REGULAR, 48, 880)
    _text(draw, (540, 780), tagline, tag_font, text)
    paths["logo"] = str(out / "logo.png")
    img.save(paths["logo"])

    # 2. Social post — 1080x1080, name as hero text, accent band at foot.
    img = _gradient((1080, 1080), secondary_rgb, primary_rgb)
    draw = ImageDraw.Draw(img)
    hero_font = _fit_font(draw, name.upper(), _FONT_BOLD, 150, 900)
    _text(draw, (540, 420), name.upper(), hero_font, pick_text_colour(secondary_rgb))
    tag_font = _fit_font(draw, tagline, _FONT_REGULAR, 52, 900)
    _text(draw, (540, 580), tagline, tag_font, pick_text_colour(secondary_rgb))
    draw.rectangle([0, 980, 1080, 1080], fill=secondary_rgb)
    _text(draw, (540, 1030), name.upper(), _font(_FONT_BOLD, 44), text)
    paths["post"] = str(out / "post.png")
    img.save(paths["post"])

    # 3. Thumbnail — 1280x720, bold name left, monogram disc right.
    img = _gradient((1280, 720), primary_rgb, secondary_rgb)
    draw = ImageDraw.Draw(img)
    draw.ellipse([880, 140, 1180, 440], fill=text)
    _text(draw, (1030, 290), monogram, _font(_FONT_BOLD, 180), primary_rgb)
    thumb_font = _fit_font(draw, name.upper(), _FONT_BOLD, 130, 800)
    _text(draw, (60, 300), name.upper(), thumb_font, text, anchor="lm")
    tag_font = _fit_font(draw, tagline, _FONT_REGULAR, 46, 800)
    _text(draw, (60, 430), tagline, tag_font, text, anchor="lm")
    paths["thumbnail"] = str(out / "thumbnail.png")
    img.save(paths["thumbnail"])

    return paths
