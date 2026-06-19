import re
from pathlib import Path


def sanitize_pdf_glyphs(text: str) -> str:
    """Cleans up oldstyle LaTeX font glyphs using string replacement."""
    glyph_map = {
        "/zero.oldstyle": "0",
        "/one.oldstyle": "1",
        "/one.Alt.oldstyle": "1",
        "/two.oldstyle": "2",
        "/three.oldstyle": "3",
        "/four.oldstyle": "4",
        "/five.oldstyle": "5",
        "/six.oldstyle": "6",
        "/seven.oldstyle": "7",
        "/eight.oldstyle": "8",
        "/nine.oldstyle": "9",
    }
    cleaned = text
    for literal, substitution in glyph_map.items():
        cleaned = cleaned.replace(literal, substitution)
    return cleaned


def sanitize_markdown_artifacts(text: str) -> str:
    """Cleans up page artifacts and structural whitespace."""
    page_artifact_pattern = r"(?m)^Page \d+ of \d+\s*$"
    text = re.sub(page_artifact_pattern, "", text)
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)
    return text.strip()


def sanitize_all(text: str) -> str:
    """The Master Sanitizer: Chains all cleaning processes for strings."""
    text = sanitize_pdf_glyphs(text)
    text = sanitize_markdown_artifacts(text)
    return text


def sanitize_markdown(file_path: Path) -> str:
    """Legacy interface: Reads a file and runs the master sanitizer."""
    with open(file_path, "r", encoding="utf-8") as f:
        raw_content = f.read()

    return sanitize_all(raw_content)