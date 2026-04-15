"""Command line interface for gawe_video."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from gawe_video.code_highlight import normalize_theme
from gawe_video.composer import compose_video
from gawe_video.config import AppConfig
from gawe_video.parser import parse_markdown_file
from gawe_video.renderer import render_scenes

app = typer.Typer(help="Generate tutorial videos from markdown files")
console = Console()


@app.callback()
def main() -> None:
    """gawe-video command group."""


@app.command("generate")
def generate(
    input_md: Path = typer.Argument(..., exists=True, help="Input markdown file"),
    output: Path = typer.Option(Path("output.mp4"), "--output", "-o", help="Output video file path"),
    voice: str = typer.Option("id-ID-ArdiNeural", "--voice", "-v", help="TTS voice"),
    theme: str = typer.Option("monokai", "--theme", "-t", help="Code theme"),
    resolution: str = typer.Option("1080p", "--resolution", help="Video resolution"),
    bgm: Path | None = typer.Option(None, "--bgm", help="Background music path"),
    speed: float = typer.Option(1.0, "--speed", help="Narration speed multiplier"),
    no_tts: bool = typer.Option(False, "--no-tts", help="Disable TTS narration"),
    preview: bool = typer.Option(False, "--preview", help="Render first scene only"),
) -> None:
    """Generate video from markdown input."""
    try:
        normalize_theme(theme)
    except ValueError as exc:
        raise typer.BadParameter(str(exc)) from exc

    config = AppConfig()
    config.video.resolution = resolution
    config.tts.voice = voice
    config.tts.speed = speed
    config.tts.enabled = not no_tts
    config.theme.name = theme

    console.print(Panel.fit("[bold cyan]gaweVideo[/bold cyan]\nMarkdown to YouTube-ready tutorial video"))

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
        task = progress.add_task("Parsing markdown...", total=None)
        scenes = parse_markdown_file(input_md)

        progress.update(task, description="Rendering scenes...")
        rendered = render_scenes(scenes, config.video, preview=preview)

        progress.update(task, description="Composing video...")
        result = compose_video(rendered, output, narration_path=None if no_tts else "narration.wav", bgm_path=bgm)

        progress.update(task, description="Done")

    console.print(
        Panel.fit(
            f"[green]Video generated[/green]\n"
            f"Scenes: {result.scene_count}\n"
            f"Output: {result.output_path}\n"
            f"TTS: {'off' if no_tts else 'on'}"
        )
    )


if __name__ == "__main__":  # pragma: no cover
    app()
