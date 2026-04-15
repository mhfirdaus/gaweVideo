"""Tests for markdown parser scene extraction."""

import unittest

from gawe_video.parser import parse_markdown


class ParserTests(unittest.TestCase):
    def test_parse_mixed_markdown_elements(self) -> None:
        markdown = """# Title\n\nParagraph text.\n\n- Item one\n- Item two\n\n```python\nprint('hi')\n```\n\n![Alt](img.png)\n"""
        scenes = parse_markdown(markdown)
        scene_types = [scene.scene_type for scene in scenes]
        self.assertIn("TitleScene", scene_types)
        self.assertIn("ContentScene", scene_types)
        self.assertIn("ListScene", scene_types)
        self.assertIn("CodeScene", scene_types)

    def test_code_language_metadata(self) -> None:
        markdown = """```javascript\nconsole.log('x')\n```"""
        scenes = parse_markdown(markdown)
        code_scene = next(scene for scene in scenes if scene.scene_type == "CodeScene")
        self.assertEqual(code_scene.metadata.get("language"), "javascript")
        self.assertGreater(code_scene.duration, 0)


if __name__ == "__main__":
    unittest.main()
