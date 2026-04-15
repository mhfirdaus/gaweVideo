"""Streamlit web UI for gaweVideo."""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path

import streamlit as st

from gawe_video.code_highlight import normalize_theme
from gawe_video.composer import compose_video
from gawe_video.config import AppConfig
from gawe_video.parser import Scene, parse_markdown
from gawe_video.renderer import render_scenes
from gawe_video.templates import TEMPLATES
from gawe_video.web_utils import (
    cleanup_temp_files,
    get_custom_css,
    init_session_state,
    make_temp_audio_path,
    make_temp_output_path,
    save_uploaded_file,
)

THEME_COLOR_PREVIEWS = {
    "monokai": ["#272822", "#a6e22e", "#f92672", "#66d9ef"],
    "dracula": ["#282a36", "#bd93f9", "#50fa7b", "#ff79c6"],
    "github-dark": ["#0d1117", "#58a6ff", "#7ee787", "#f778ba"],
    "one-dark": ["#282c34", "#61afef", "#98c379", "#c678dd"],
}

VOICE_OPTIONS = (
    "id-ID-ArdiNeural",
    "id-ID-GadisNeural",
    "en-US-GuyNeural",
    "en-US-JennyNeural",
)


def _scene_badge(scene: Scene) -> str:
    mapping = {
        "TitleScene": "Title",
        "ContentScene": "Content",
        "CodeScene": "Code",
        "ListScene": "List",
        "ImageScene": "Image",
    }
    return mapping.get(scene.scene_type, scene.scene_type.replace("Scene", ""))


def _build_config(theme: str, voice: str, speed: float, tts_enabled: bool, resolution: str, fps: int) -> AppConfig:
    config = AppConfig()
    config.theme.name = normalize_theme(theme)
    config.tts.voice = voice
    config.tts.speed = speed
    config.tts.enabled = tts_enabled
    config.video.resolution = resolution
    config.video.fps = fps
    return config


def _render_sidebar() -> dict[str, object]:
    st.sidebar.header("⚙️ Settings Panel")

    selected_theme = st.sidebar.selectbox(
        "🎨 Theme Selector",
        options=["monokai", "dracula", "github-dark", "one-dark"],
        format_func=lambda t: t.replace("-", " ").title(),
        help="Choose code highlight theme for generated tutorial scenes.",
    )
    swatches = "".join(
        f"<span class='theme-swatch' style='background:{color}'></span>" for color in THEME_COLOR_PREVIEWS[selected_theme]
    )
    st.sidebar.markdown(f"<div class='theme-preview'>{swatches}</div>", unsafe_allow_html=True)

    st.sidebar.subheader("🗣️ Voice Settings")
    voice = st.sidebar.selectbox("Voice", options=VOICE_OPTIONS, help="Narrator voice for TTS audio.")
    speed = st.sidebar.slider("Speed", 0.5, 2.0, 1.0, 0.1, help="Narration speed multiplier.")
    tts_enabled = st.sidebar.toggle("Enable TTS", value=True, help="Turn narration generation on or off.")

    st.sidebar.subheader("📐 Video Settings")
    resolution = st.sidebar.selectbox("Resolution", options=["1080p", "720p"], help="Choose output video resolution.")
    fps = st.sidebar.selectbox("FPS", options=[24, 30, 60], index=1, help="Frames per second for output video.")

    st.sidebar.subheader("🎵 Background Music")
    bgm_file = st.sidebar.file_uploader("Upload BGM (.mp3/.wav)", type=["mp3", "wav"], help="Optional background music.")

    st.sidebar.markdown(
        "<div class='sidebar-footer'>ℹ️ <b>About</b><br/>gaweVideo transforms Markdown into tutorial-style videos."
        "<br/>Preview/parsing works without FFmpeg; full production workflows may require FFmpeg.</div>",
        unsafe_allow_html=True,
    )
    return {
        "theme": selected_theme,
        "voice": voice,
        "speed": speed,
        "tts_enabled": tts_enabled,
        "resolution": resolution,
        "fps": fps,
        "bgm_file": bgm_file,
    }


def _update_markdown_from_template(template_content: str) -> None:
    st.session_state["markdown_editor"] = template_content
    st.session_state["current_markdown"] = template_content


def _render_generate_tab(settings: dict[str, object]) -> None:
    st.subheader("Upload & Generate")
    uploaded_md = st.file_uploader("Upload Markdown (.md)", type=["md"], help="Drag & drop markdown file here.")
    if uploaded_md is not None:
        content = uploaded_md.getvalue().decode("utf-8", errors="replace")
        st.session_state["markdown_editor"] = content
        st.session_state["current_markdown"] = content

    markdown_input = st.text_area(
        "Or write/paste markdown",
        key="markdown_editor",
        height=260,
        placeholder=(
            "# Your Tutorial Title\n\n"
            "Explain concepts in markdown.\n\n"
            "```python\nprint('Hello gaweVideo')\n```\n\n"
            "- Point one\n- Point two"
        ),
        help="Paste markdown directly if you do not want to upload a file.",
    )
    st.session_state["current_markdown"] = markdown_input

    generate_clicked = st.button("✨ Generate Video", use_container_width=True, help="Generate tutorial video from markdown.")
    if generate_clicked:
        markdown = st.session_state.get("current_markdown", "").strip()
        if not markdown:
            st.toast("Please provide markdown input first.", icon="⚠️")
            st.error("Markdown input is empty. Upload a file or type markdown content.")
            return

        try:
            config = _build_config(
                theme=str(settings["theme"]),
                voice=str(settings["voice"]),
                speed=float(settings["speed"]),
                tts_enabled=bool(settings["tts_enabled"]),
                resolution=str(settings["resolution"]),
                fps=int(settings["fps"]),
            )
            scenes = parse_markdown(markdown)
            if not scenes:
                st.toast("No scenes detected from markdown.", icon="⚠️")
                st.warning("No scenes found. Please check markdown format.")
                return

            skipped = st.session_state.get("skipped_scenes", set())
            scene_order = st.session_state.get("scene_order", list(range(len(scenes))))
            if len(scene_order) != len(scenes):
                scene_order = list(range(len(scenes)))
                st.session_state["scene_order"] = scene_order
            selected = [scenes[index] for index in scene_order if index not in skipped]
            if not selected:
                st.toast("All scenes are skipped. Please enable at least one scene.", icon="⚠️")
                st.warning("Cannot generate video with zero active scenes.")
                return

            bgm_path: Path | None = None
            if settings["bgm_file"] is not None:
                bgm_path = save_uploaded_file(settings["bgm_file"])

            progress = st.progress(0)
            status = st.empty()
            with st.spinner("Generating your video..."):
                status.info("Parsing markdown...")
                time.sleep(0.2)
                progress.progress(25)

                status.info("Rendering scenes...")
                rendered = render_scenes(selected, config.video, preview=False)
                time.sleep(0.2)
                progress.progress(50)

                if config.tts.enabled:
                    status.info("Processing TTS...")
                else:
                    status.info("Skipping TTS...")
                time.sleep(0.2)
                progress.progress(75)

                status.info("Composing final video...")
                output_path = make_temp_output_path()
                narration_path = make_temp_audio_path() if config.tts.enabled else None
                result = compose_video(
                    rendered,
                    output_path,
                    narration_path=narration_path,
                    bgm_path=bgm_path,
                )
                progress.progress(100)
                status.success("Video generation complete.")

            video_bytes = result.output_path.read_bytes()
            st.session_state["generated_video"] = video_bytes
            st.session_state["generation_message"] = (
                f"Generated {result.scene_count} scenes • TTS: {'on' if result.has_tts else 'off'}"
            )
            history_item = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": f"gawevideo-{datetime.now().strftime('%H%M%S')}.mp4",
                "video_bytes": video_bytes,
                "markdown": markdown,
                "scene_count": result.scene_count,
            }
            st.session_state["history"] = [history_item, *st.session_state.get("history", [])][:20]
            st.toast("Video generated successfully!", icon="✅")
        except Exception as exc:
            st.toast("Generation failed. See details below.", icon="❌")
            st.error(f"Sorry, we couldn't generate the video: {exc}")

    if st.session_state.get("generated_video") is not None:
        st.success(st.session_state.get("generation_message", "Video ready."))
        st.video(st.session_state["generated_video"])
        st.download_button(
            "⬇️ Download Video",
            data=st.session_state["generated_video"],
            file_name="gawevideo-output.mp4",
            mime="video/mp4",
            use_container_width=True,
        )


def _render_scene_preview_tab() -> None:
    st.subheader("Preview Scenes")
    markdown = st.session_state.get("current_markdown", "").strip()
    if not markdown:
        st.info("Upload or write markdown in the first tab to preview scenes.")
        return

    scenes = parse_markdown(markdown)
    if not scenes:
        st.warning("No scenes were parsed from markdown.")
        return

    if len(st.session_state.get("scene_order", [])) != len(scenes):
        st.session_state["scene_order"] = list(range(len(scenes)))
        st.session_state["skipped_scenes"] = set()
    order: list[int] = st.session_state["scene_order"]
    skipped: set[int] = st.session_state["skipped_scenes"]

    for position, scene_idx in enumerate(order):
        scene = scenes[scene_idx]
        badge = _scene_badge(scene)
        preview_text = scene.content if len(scene.content) <= 220 else f"{scene.content[:220]}..."
        st.markdown(
            f"<div class='card'><span class='badge'>{badge}</span><br/>"
            f"<b>Scene #{position + 1}</b><br/><br/>{preview_text}<br/><br/>"
            f"<small>Estimated duration: {scene.duration:.1f}s</small></div>",
            unsafe_allow_html=True,
        )
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("⬆️ Up", key=f"up_{position}", disabled=position == 0):
                order[position - 1], order[position] = order[position], order[position - 1]
                st.session_state["scene_order"] = order
                st.rerun()
        with col2:
            if st.button("⬇️ Down", key=f"down_{position}", disabled=position == len(order) - 1):
                order[position + 1], order[position] = order[position], order[position + 1]
                st.session_state["scene_order"] = order
                st.rerun()
        with col3:
            should_skip = st.checkbox("Skip scene", value=scene_idx in skipped, key=f"skip_{scene_idx}")
            if should_skip:
                skipped.add(scene_idx)
            else:
                skipped.discard(scene_idx)
            st.session_state["skipped_scenes"] = skipped


def _render_templates_tab() -> None:
    st.subheader("Templates")
    for template in TEMPLATES:
        st.markdown(
            f"<div class='card'><b>{template['icon']} {template['name']}</b><br/>{template['description']}</div>",
            unsafe_allow_html=True,
        )
        if st.button(f"Use {template['name']}", key=f"use_tpl_{template['name']}"):
            _update_markdown_from_template(template["content"])
            st.toast(f"{template['name']} loaded into editor.", icon="📄")


def _render_history_tab() -> None:
    st.subheader("History")
    history = st.session_state.get("history", [])
    if not history:
        st.info("No generated videos in this session yet.")
        return
    for idx, item in enumerate(history):
        with st.expander(f"🎞️ {item['filename']} • {item['timestamp']}"):
            st.write(f"Scenes: {item['scene_count']}")
            st.download_button(
                "Download again",
                data=item["video_bytes"],
                file_name=item["filename"],
                mime="video/mp4",
                key=f"dl_history_{idx}",
            )
            if st.button("Re-use markdown", key=f"reuse_markdown_{idx}"):
                _update_markdown_from_template(item["markdown"])
                st.toast("Markdown loaded to editor for re-generation.", icon="♻️")


def run_app() -> None:
    """Run the Streamlit application."""
    st.set_page_config(
        page_title="🎬 gaweVideo - MD to Video Maker",
        page_icon="🎬",
        layout="wide",
    )
    st.markdown(get_custom_css(), unsafe_allow_html=True)
    init_session_state()

    settings = _render_sidebar()

    st.markdown("<div class='main-title'>🎬 gaweVideo</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Transform your Markdown into YouTube-ready tutorial videos</div>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Upload & Generate", "Preview Scenes", "Templates", "History"])
    with tab1:
        _render_generate_tab(settings)
    with tab2:
        _render_scene_preview_tab()
    with tab3:
        _render_templates_tab()
    with tab4:
        _render_history_tab()

    if st.button("🧹 Clear temporary files", help="Delete temporary files created in this browser session."):
        cleanup_temp_files()
        st.toast("Temporary files cleaned.", icon="🧹")


if __name__ == "__main__":
    run_app()
