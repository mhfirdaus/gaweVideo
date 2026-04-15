"""Markdown parser that transforms markdown documents into scenes."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from gawe_video.utils import estimate_duration

try:
    from markdown_it import MarkdownIt
except Exception:  # pragma: no cover - optional import fallback
    MarkdownIt = None


@dataclass(slots=True)
class Scene:
    """Represents a scene extracted from markdown."""

    scene_type: str
    content: str
    duration: float
    metadata: dict[str, Any] = field(default_factory=dict)


def _parse_with_markdown_it(content: str) -> list[Scene]:
    md = MarkdownIt()
    tokens = md.parse(content)
    scenes: list[Scene] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.type == "heading_open":
            level = token.tag
            text_token = tokens[i + 1] if i + 1 < len(tokens) else None
            if text_token and text_token.type == "inline":
                text = text_token.content.strip()
                scenes.append(
                    Scene(
                        scene_type="TitleScene",
                        content=text,
                        duration=estimate_duration(text),
                        metadata={"level": level},
                    )
                )
            i += 3
            continue
        if token.type == "paragraph_open":
            text_token = tokens[i + 1] if i + 1 < len(tokens) else None
            if text_token and text_token.type == "inline":
                text = text_token.content.strip()
                if text.startswith("!") and "](" in text:
                    scenes.append(
                        Scene(
                            scene_type="ImageScene",
                            content=text,
                            duration=estimate_duration(text),
                            metadata={},
                        )
                    )
                else:
                    scenes.append(
                        Scene(
                            scene_type="ContentScene",
                            content=text,
                            duration=estimate_duration(text),
                            metadata={},
                        )
                    )
            i += 3
            continue
        if token.type == "fence":
            scenes.append(
                Scene(
                    scene_type="CodeScene",
                    content=token.content.rstrip("\n"),
                    duration=estimate_duration(token.content),
                    metadata={"language": token.info.strip() or "text"},
                )
            )
        if token.type in {"bullet_list_open", "ordered_list_open"}:
            items: list[str] = []
            list_type = "ordered" if token.type.startswith("ordered") else "bullet"
            j = i + 1
            while j < len(tokens) and tokens[j].type not in {"bullet_list_close", "ordered_list_close"}:
                if tokens[j].type == "inline":
                    items.append(tokens[j].content.strip())
                j += 1
            if items:
                joined = "\n".join(items)
                scenes.append(
                    Scene(
                        scene_type="ListScene",
                        content=joined,
                        duration=estimate_duration(joined),
                        metadata={"list_type": list_type, "items": items},
                    )
                )
            i = j + 1
            continue
        i += 1
    return scenes


def _parse_fallback(content: str) -> list[Scene]:
    scenes: list[Scene] = []
    lines = content.splitlines()
    in_code = False
    code_lang = "text"
    code_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_code:
                in_code = True
                code_lang = stripped.removeprefix("```").strip() or "text"
                code_lines = []
            else:
                code_content = "\n".join(code_lines)
                scenes.append(Scene("CodeScene", code_content, estimate_duration(code_content), {"language": code_lang}))
                in_code = False
            continue
        if in_code:
            code_lines.append(line)
            continue
        if stripped.startswith("#"):
            text = stripped.lstrip("# ").strip()
            level = f"h{stripped.count('#')}"
            scenes.append(Scene("TitleScene", text, estimate_duration(text), {"level": level}))
        elif stripped.startswith(("- ", "* ")):
            item = stripped[2:].strip()
            scenes.append(Scene("ListScene", item, estimate_duration(item), {"list_type": "bullet", "items": [item]}))
        elif stripped.startswith("!["):
            scenes.append(Scene("ImageScene", stripped, estimate_duration(stripped), {}))
        elif stripped:
            scenes.append(Scene("ContentScene", stripped, estimate_duration(stripped), {}))
    return scenes


def parse_markdown(content: str) -> list[Scene]:
    """Parse markdown content into a list of Scene objects."""
    if MarkdownIt is not None:
        return _parse_with_markdown_it(content)
    return _parse_fallback(content)


def parse_markdown_file(path: str | Path) -> list[Scene]:
    """Parse markdown file path into scenes."""
    file_path = Path(path)
    content = file_path.read_text(encoding="utf-8")
    return parse_markdown(content)
