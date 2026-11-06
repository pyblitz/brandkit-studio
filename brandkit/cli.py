"""Command line: ``python -m brandkit --name ORBITA --tagline "..." --primary #0F172A --secondary #F59E0B --out kit/``."""

from __future__ import annotations

import argparse
import json

from .generate import generate_kit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="brandkit", description="Generate a mini brand kit (logo, social post, thumbnail).")
    parser.add_argument("--name", required=True, help="Brand name")
    parser.add_argument("--tagline", default="", help="Tagline under the name")
    parser.add_argument("--primary", required=True, help="Primary colour, #RRGGBB")
    parser.add_argument("--secondary", required=True, help="Secondary colour, #RRGGBB")
    parser.add_argument("--out", default="kit", help="Output directory (default: kit)")
    args = parser.parse_args(argv)
    paths = generate_kit(args.name, args.tagline, args.primary, args.secondary, args.out)
    print(json.dumps(paths, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
