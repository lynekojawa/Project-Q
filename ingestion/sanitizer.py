import re
from pathlib import Path
def sanitize_markdown(file_path: Path) -> str:
    with open(file_path, "r", encoding = "utf-8") as f:
        raw_content = f.read()

    page_artifact_pattern = r"(?m)^Page \d+ of \d+\s*$"
    clean_content = re.sub(page_artifact_pattern, "", raw_content)

    clean_content = re.sub(r"[ \t]+$", "", clean_content, flags=re.MULTILINE)

    return clean_content.strip()
def sanitize_pdf_glyphs(text: str)-> str:
    """
    Cleans up oldstyle LaTeX font glyph injections specific to academic PDFs
    While maintaining paragraph spacing structure intact
    """
    glyph_map = {
        r"/zero\.oldstyle": "0",
        r"/one\.oldstyle": "1",
        r"/one\.Alt\.oldstyle": "1",
        r"/two\.oldstyle": "2",
        r"/three\.oldstyle": "3",
        r"/four\.oldstyle": "4",
        r"/five\.oldstyle": "5",
        r"/six\.oldstyle": "6",
        r"/seven\.oldstyle": "7",
        r"/eight\.oldstyle": "8",
        r"/nine\.oldstyle": "9",
    }
    cleaned= text
    for pattern, substitution in glyph_map.items():
        cleaned = re.sub(pattern, substitution, cleaned)
    return cleaned
