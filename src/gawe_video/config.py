"""Configuration models for gawe_video."""

from __future__ import annotations

from dataclasses import dataclass, field


SUPPORTED_THEMES = ("monokai", "dracula", "github-dark", "one-dark")
SUPPORTED_RESOLUTIONS = {
    "1080p": (1920, 1080),
    "720p": (1280, 720),
}


@dataclass(slots=True)
class VideoConfig:
    """Video rendering settings."""

    resolution: str = "1080p"
    fps: int = 30
    bitrate: str = "8M"

    @property
    def frame_size(self) -> tuple[int, int]:
        """Return width and height from configured resolution."""
        return SUPPORTED_RESOLUTIONS.get(self.resolution, SUPPORTED_RESOLUTIONS["1080p"])


@dataclass(slots=True)
class TTSConfig:
    """Text-to-speech settings."""

    voice: str = "id-ID-ArdiNeural"
    speed: float = 1.0
    enabled: bool = True


@dataclass(slots=True)
class ThemeConfig:
    """Theme settings for code rendering."""

    name: str = "monokai"
    background_color: str = "#0f172a"
    text_color: str = "#e2e8f0"
    font_name: str = "DejaVuSans.ttf"


@dataclass(slots=True)
class AppConfig:
    """Main configuration object for the application."""

    video: VideoConfig = field(default_factory=VideoConfig)
    tts: TTSConfig = field(default_factory=TTSConfig)
    theme: ThemeConfig = field(default_factory=ThemeConfig)
