# BrandKit Studio

Generate a consistent mini brand kit from a brand name, a tagline and
two colours — no design tool needed:

* `logo.png` — 1080×1080 logo lockup
* `post.png` — 1080×1080 social-media post creative
* `thumbnail.png` — 1280×720 thumbnail

The tool also checks colour contrast (WCAG-style luminance ratio) and
picks black or white text, whichever is actually readable on the
background. A palette whose text contrast falls below 4.5:1 prints a
warning instead of silently producing unreadable text.

## Install

```bash
pip install -e .
```

## Use

```bash
python -m brandkit \
  --name ORBITA \
  --tagline "Tech, made simple." \
  --primary "#0F172A" \
  --secondary "#F59E0B" \
  --out kit/
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Example

The `examples/orbita/` folder holds a sample kit for "ORBITA", a
fictional sample brand used only to demonstrate the output — it is not
a real client.

## Why this exists

Built by Shoaib Ahmed (Python developer + graphic designer) as a
portfolio project: the same "one palette, every format" idea behind his
daily LinkedIn design work, packaged as a reusable tool with tests.
