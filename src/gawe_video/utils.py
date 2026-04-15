"""Utility helpers for gawe_video."""

from __future__ import annotations

from pathlib import Path


def estimate_duration(text: str, words_per_minute: int = 150, min_seconds: float = 2.5) -> float:
    """Estimate speech duration for text in seconds."""
    words = len(text.split())
    estimated = (words / max(words_per_minute, 1)) * 60
    return round(max(estimated, min_seconds), 2)


def ensure_parent_dir(path: str | Path) -> Path:
    """Ensure parent directory exists and return Path object."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path
