"""Scene renderer for generating visual scene data."""

from __future__ import annotations

from dataclasses import dataclass

from gawe_video.config import VideoConfig
from gawe_video.parser import Scene


@dataclass(slots=True)
class RenderedScene:
    """Lightweight rendered scene representation."""

    scene: Scene
    width: int
    height: int
    background: str = "gradient-dark"


def render_scene(scene: Scene, config: VideoConfig | None = None) -> RenderedScene:
    """Render one scene into an intermediate representation."""
    cfg = config or VideoConfig()
    width, height = cfg.frame_size
    return RenderedScene(scene=scene, width=width, height=height)


def render_scenes(scenes: list[Scene], config: VideoConfig | None = None, preview: bool = False) -> list[RenderedScene]:
    """Render multiple scenes. If preview is enabled, render first scene only."""
    target = scenes[:1] if preview else scenes
    return [render_scene(scene, config) for scene in target]
