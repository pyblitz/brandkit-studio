"""Tests for BrandKit Studio — run with ``python -m unittest discover -s tests -v``."""

import os
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from brandkit import contrast_ratio, generate_kit, parse_hex, pick_text_colour


class TestColours(unittest.TestCase):
    def test_parse_hex(self):
        self.assertEqual(parse_hex("#0F172A"), (15, 23, 42))
        self.assertEqual(parse_hex("F59E0B"), (245, 158, 11))

    def test_parse_hex_rejects_bad_input(self):
        for bad in ("red", "#12345", "#GGGGGG", ""):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_hex(bad)

    def test_contrast_black_white_is_21(self):
        self.assertAlmostEqual(contrast_ratio((0, 0, 0), (255, 255, 255)), 21.0, places=1)

    def test_pick_text_colour(self):
        self.assertEqual(pick_text_colour((15, 23, 42)), (255, 255, 255))
        self.assertEqual(pick_text_colour((245, 158, 11)), (0, 0, 0))


class TestGenerate(unittest.TestCase):
    def test_kit_dimensions_and_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = generate_kit("ORBITA", "Tech, made simple.", "#0F172A", "#F59E0B", tmp)
            self.assertEqual(set(paths), {"logo", "post", "thumbnail"})
            expected = {"logo": (1080, 1080), "post": (1080, 1080), "thumbnail": (1280, 720)}
            for kind, size in expected.items():
                with Image.open(paths[kind]) as img:
                    self.assertEqual(img.size, size, kind)

    def test_empty_name_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                generate_kit("  ", "tag", "#000000", "#FFFFFF", tmp)


if __name__ == "__main__":
    unittest.main()
