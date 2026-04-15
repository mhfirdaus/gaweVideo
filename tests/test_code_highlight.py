"""Tests for code highlighting helpers."""

import unittest

from gawe_video.code_highlight import detect_language, normalize_theme


class CodeHighlightTests(unittest.TestCase):
    def test_theme_loading(self) -> None:
        self.assertEqual(normalize_theme("monokai"), "monokai")
        self.assertEqual(normalize_theme("Dracula"), "dracula")

    def test_theme_loading_invalid(self) -> None:
        with self.assertRaises(ValueError):
            normalize_theme("unknown")

    def test_language_detection(self) -> None:
        self.assertEqual(detect_language("py"), "python")
        self.assertEqual(detect_language("js"), "javascript")
        self.assertEqual(detect_language("go"), "go")
        self.assertEqual(detect_language(None), "text")


if __name__ == "__main__":
    unittest.main()
