import re
from typing import Dict, Any

ERICKSON_CHAPTERS = [
    "Introduction",
    "Recursion",
    "Backtracking",
    "Dynamic Programming",
    "Greedy Algorithms",
    "Basic Graph Algorithms",
    "Depth-First Search",
    "Minimum Spanning Trees",
    "Shortest Paths",
    "All-Pairs Shortest Paths",
    "Maximum Flows & Minimum Cuts",
    "Applications of Flows and Cuts",
    "NP-Hardness",
    "Polynomial Space",
    "Exponential Time"
]


def parse_toc_to_json(sanitized_text: str) -> Dict[str, Any]:
    lines = sanitized_text.splitlines()

    span_pattern = re.compile(r'<span[^>]*>.*?</span>')
    bold_pattern = re.compile(r'\*\*(.*?)\*\*')
    italic_pattern = re.compile(r'\*(.*?)\*')
    section_pattern = re.compile(r'^(\d+\.\d+)\s+(.+)')


    skip_exact = {
        "Algorithms", "Preface", "About This Book", "Prerequisites",
        "Additional References", "About the Exercises", "Steal This Book!",
        "Acknowledgments", "Caveat Lector!", "Table of Contents",
        "Index", "Index of People", "Index of Pseudocode",
        "Image Credits", "Colophon"
    }

    skip_contains = ["♥", "BottlesOfBeer", "BEAMILLIONAIRE", "NO!! STOP!!",
                     "ALGOR I THM", "PRIMVS"]

    def clean(raw: str) -> str:
        text = span_pattern.sub('', raw)
        text = bold_pattern.sub(r'\1', text)
        text = italic_pattern.sub(r'\1', text)
        text = re.sub(r'^[#\s]+', '', text)
        return text.strip()

    chapter_positions = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("# "):
            continue
        text = clean(stripped)
        if text in ERICKSON_CHAPTERS:
            chapter_positions.append((i, text))

        text = clean(stripped)

        if not text:
            continue
        if text in skip_exact:
            continue
        if any(s in text for s in skip_contains):
            continue
        if len(text) > 40:
            continue
        if section_pattern.match(text):
            continue
        # Must start with capital letter
        if not text[0].isupper():
            continue
        # Must be mostly alphabetic (no special chars)
        if any(c in text for c in "♥*():\\$@|0123456789"):
            continue

        chapter_positions.append((i, text))

    hierarchy: Dict[str, Any] = {}

    for idx, (start_line, chapter_title) in enumerate(chapter_positions):
        end_line = chapter_positions[idx + 1][0] \
            if idx + 1 < len(chapter_positions) else len(lines)

        hierarchy[chapter_title] = {}
        current_section = None

        for line in lines[start_line:end_line]:
            stripped = line.strip()
            if not stripped.startswith("#"):
                continue

            text = clean(stripped)
            if not text:
                continue
            if any(s in text for s in skip_contains):
                continue

            # Section: # X.Y Title
            if stripped.startswith("# "):
                match = section_pattern.match(text)
                if match and len(text) < 60:
                    current_section = text
                    hierarchy[chapter_title][current_section] = [
                        {"title": "Overview", "content": []}
                    ]
                continue

            # Subsection: ### or ####
            if stripped.startswith("###") or stripped.startswith("####"):
                if current_section is not None and len(text) < 60:
                    if not any(s in text for s in skip_exact):
                        hierarchy[chapter_title][current_section].append(
                            {"title": text, "content": []}
                        )
                continue

    return hierarchy