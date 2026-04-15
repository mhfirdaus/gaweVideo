"""Tests for configuration defaults and overrides."""

import unittest

from gawe_video.config import AppConfig, TTSConfig, VideoConfig


class ConfigTests(unittest.TestCase):
    def test_default_values(self) -> None:
        config = AppConfig()
        self.assertEqual(config.video.resolution, "1080p")
        self.assertEqual(config.video.frame_size, (1920, 1080))
        self.assertEqual(config.tts.voice, "id-ID-ArdiNeural")
        self.assertTrue(config.tts.enabled)
        self.assertEqual(config.theme.name, "monokai")

    def test_custom_overrides(self) -> None:
        video = VideoConfig(resolution="720p", fps=24)
        tts = TTSConfig(voice="en-US-GuyNeural", speed=1.2, enabled=False)
        config = AppConfig(video=video, tts=tts)
        self.assertEqual(config.video.frame_size, (1280, 720))
        self.assertEqual(config.video.fps, 24)
        self.assertEqual(config.tts.voice, "en-US-GuyNeural")
        self.assertFalse(config.tts.enabled)


if __name__ == "__main__":
    unittest.main()
