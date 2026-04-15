"""Text-to-speech engine integration using edge-tts."""

from __future__ import annotations

import asyncio
from pathlib import Path

from gawe_video.config import TTSConfig
from gawe_video.utils import ensure_parent_dir


async def synthesize_to_file(text: str, output_path: str | Path, config: TTSConfig | None = None) -> Path:
    """Synthesize speech into an audio file using edge-tts."""
    cfg = config or TTSConfig()
    out_path = ensure_parent_dir(output_path)

    try:
        import edge_tts
    except Exception as exc:  # pragma: no cover - runtime dependency
        raise RuntimeError("edge-tts is required for narration") from exc

    communicator = edge_tts.Communicate(text=text, voice=cfg.voice, rate=f"{(cfg.speed - 1.0) * 100:+.0f}%")
    await communicator.save(str(out_path))
    return out_path


def synthesize_to_file_sync(text: str, output_path: str | Path, config: TTSConfig | None = None) -> Path:
    """Synchronous wrapper for async TTS synthesis."""
    return asyncio.run(synthesize_to_file(text, output_path, config))
