import re
from pathlib import Path
def sanitize_markdown(file_path: Path) -> str:
    with open(file_path, "r", encoding = "utf-8") as f:
        raw_content = f.read()

    page_artifact_pattern = r"(?m)^Page \d+ of \d+\s*$"
    clean_content = re.sub(page_artifact_pattern, "", raw_content)

    clean_content = re.sub(r"[ \t]+$", "", clean_content, flags=re.MULTILINE)

    return clean_content.strip()