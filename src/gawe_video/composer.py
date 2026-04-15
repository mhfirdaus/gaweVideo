"""Compose rendered scenes and audio into final video."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from gawe_video.renderer import RenderedScene
from gawe_video.utils import ensure_parent_dir


@dataclass(slots=True)
class CompositionResult:
    """Represents the composition output metadata."""

    output_path: Path
    scene_count: int
    has_tts: bool
    has_bgm: bool


def compose_video(
    rendered_scenes: list[RenderedScene],
    output_path: str | Path,
    narration_path: str | Path | None = None,
    bgm_path: str | Path | None = None,
) -> CompositionResult:
    """Compose final output file.

    Current implementation writes a placeholder MP4 file so flow can be tested.
    """
    out = ensure_parent_dir(output_path)
    out.write_bytes(b"gawe-video-placeholder")
    return CompositionResult(
        output_path=out,
        scene_count=len(rendered_scenes),
        has_tts=narration_path is not None,
        has_bgm=bgm_path is not None,
    )
