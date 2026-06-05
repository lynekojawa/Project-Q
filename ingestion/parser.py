import re
from typing import Dict, Any


def parse_toc_to_json(sanitized_text: str) -> Dict[str, Any]:
    hierarchy: Dict[str, Any] = {}
    current_chapter = None
    current_section = None

    span_pattern = re.compile(r'<span.*?>.*?</span>')

    for line in sanitized_text.splitlines():
        line = line.strip()
        if not line:
            continue

        clean_line = span_pattern.sub('', line).strip()

        if not clean_line:
            continue

        if len(clean_line) > 60 or any(char in clean_line for char in "♥*():\\"):
            continue

        if line.startswith("# "):
            current_chapter = re.sub(r'^[#\- ]+', '', clean_line).strip()
            hierarchy[current_chapter] = {}
            current_section = None

        elif line.startswith("## ") and current_chapter:
            current_section = re.sub(r'^[#\- ]+', '', clean_line).strip()
            hierarchy[current_chapter][current_section] = [
                {
                    "title": "Overview",
                    "content": []
                }
            ]


        elif (clean_line.startswith("### ") or clean_line.startswith("#### ")) and current_section is not None:
            curr_sub = re.sub(r'^[#\- ]+', '', clean_line).strip()
            hierarchy[current_chapter][current_section].append({
                "title": curr_sub,
                "content": []
            })

        elif line.startswith("- ") and current_chapter and current_section:
            content_text = re.sub(r'^[#\- ]+', '', clean_line).strip()
            hierarchy[current_chapter][current_section][-1]["content"].append(content_text)

    return hierarchy
