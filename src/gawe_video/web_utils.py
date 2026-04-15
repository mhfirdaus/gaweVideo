"""Utility helpers for Streamlit web UI."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import streamlit as st


def get_custom_css() -> str:
    """Return custom CSS for a dark, modern UI."""
    return """
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #1b2a41 0%, #0a0f1f 45%, #080c18 100%);
        color: #e6f0ff;
    }
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 0.1rem;
    }
    .subtitle {
        color: #93c5fd;
        margin-bottom: 1.2rem;
    }
    .card {
        border: 1px solid rgba(56, 189, 248, 0.25);
        background: linear-gradient(150deg, rgba(15,23,42,0.92), rgba(30,41,59,0.82));
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 12px;
        box-shadow: 0 8px 24px rgba(2, 6, 23, 0.4);
        transition: all 0.25s ease;
    }
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(14, 116, 144, 0.28);
    }
    .badge {
        display: inline-block;
        border-radius: 999px;
        padding: 4px 10px;
        font-size: 0.78rem;
        color: #cffafe;
        background: rgba(14, 165, 233, 0.25);
        border: 1px solid rgba(34, 211, 238, 0.4);
        margin-bottom: 8px;
    }
    .theme-preview {
        display: flex;
        gap: 8px;
        margin-top: 6px;
        margin-bottom: 10px;
    }
    .theme-swatch {
        width: 18px;
        height: 18px;
        border-radius: 5px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    div.stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.5);
        background: linear-gradient(120deg, #06b6d4 0%, #2563eb 100%);
        color: white;
        font-weight: 700;
        padding: 0.65rem 1rem;
    }
    .sidebar-footer {
        margin-top: 2rem;
        color: #94a3b8;
        font-size: 0.85rem;
        border-top: 1px solid rgba(148,163,184,0.3);
        padding-top: 0.8rem;
    }
    </style>
    """


def init_session_state() -> None:
    """Initialize default session keys."""
    defaults: dict[str, Any] = {
        "markdown_editor": "",
        "current_markdown": "",
        "generated_video": None,
        "generated_video_filename": "gaweVideo-output.mp4",
        "generation_message": "",
        "history": [],
        "temp_files": [],
        "scene_order": [],
        "skipped_scenes": set(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def register_temp_file(path: Path) -> None:
    """Track temporary file path for optional cleanup."""
    files: list[str] = st.session_state.get("temp_files", [])
    files.append(str(path))
    st.session_state["temp_files"] = files


def save_uploaded_file(uploaded_file: Any) -> Path:
    """Persist uploaded file into a temporary path."""
    suffix = Path(uploaded_file.name).suffix or ".tmp"
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp.write(uploaded_file.getbuffer())
    temp.flush()
    temp.close()
    path = Path(temp.name)
    register_temp_file(path)
    return path


def make_temp_output_path() -> Path:
    """Create temporary output path for generated video file."""
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp.close()
    path = Path(temp.name)
    register_temp_file(path)
    return path


def make_temp_audio_path() -> Path:
    """Create temporary narration path placeholder."""
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    temp.close()
    path = Path(temp.name)
    register_temp_file(path)
    return path


def cleanup_temp_files() -> None:
    """Delete tracked temporary files if they still exist."""
    for raw_path in st.session_state.get("temp_files", []):
        path = Path(raw_path)
        path.unlink(missing_ok=True)
    st.session_state["temp_files"] = []
