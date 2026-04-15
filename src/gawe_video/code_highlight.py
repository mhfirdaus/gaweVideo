"""Code syntax highlighting utilities."""

from __future__ import annotations

from dataclasses import dataclass

THEME_MAP = {
    "monokai": "monokai",
    "dracula": "dracula",
    "github-dark": "github-dark",
    "one-dark": "one-dark",
}

LANGUAGE_ALIASES = {
    "py": "python",
    "python3": "python",
    "js": "javascript",
    "ts": "typescript",
    "sh": "bash",
    "shell": "bash",
    "yml": "yaml",
}


@dataclass(slots=True)
class HighlightConfig:
    """Configuration for code highlighting visuals."""

    theme: str = "monokai"
    line_numbers: bool = True
    language_badge: bool = True


def normalize_theme(theme: str) -> str:
    """Normalize and validate theme name."""
    lowered = theme.strip().lower()
    if lowered not in THEME_MAP:
        raise ValueError(f"Unsupported theme: {theme}")
    return THEME_MAP[lowered]


def detect_language(language_hint: str | None) -> str:
    """Detect normalized language name from user hint."""
    if not language_hint:
        return "text"
    key = language_hint.strip().lower()
    return LANGUAGE_ALIASES.get(key, key)


def render_code_image(code: str, language: str = "text", theme: str = "monokai") -> bytes:
    """Render highlighted code into PNG bytes."""
    try:
        from io import BytesIO

        from PIL import Image
        from pygments import highlight
        from pygments.formatters import ImageFormatter
        from pygments.lexers import TextLexer, get_lexer_by_name
    except Exception as exc:  # pragma: no cover - external dependency runtime
        raise RuntimeError("Code rendering requires Pillow and Pygments") from exc

    safe_theme = normalize_theme(theme)
    try:
        lexer = get_lexer_by_name(detect_language(language))
    except Exception:
        lexer = TextLexer()

    formatter = ImageFormatter(style=safe_theme, line_numbers=True, font_name="DejaVu Sans Mono", image_pad=20)
    raw_png = highlight(code, lexer, formatter)

    image = Image.open(BytesIO(raw_png)).convert("RGBA")
    out = BytesIO()
    image.save(out, format="PNG")
    return out.getvalue()
