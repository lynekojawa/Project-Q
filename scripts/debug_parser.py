import json
import os
from pathlib import Path
from ingestion.sanitizer import sanitize_markdown
from ingestion.parser import parse_toc_to_json
import re

def run_initialization_pipeline():
    input_dir = Path("../data/raw/Algorithms-JeffE")
    output_path = Path("../data/concept_map.json")

    if not input_dir.exists():
        print(f"❌ Critical Error: Directory {input_dir} not found.")
        return

    target_files = list(input_dir.glob("*.md"))

    if not target_files:
        print(f"Tracking Error: No markdown source files discovered inside {input_dir.resolve()}")
        print("Action Required: Please ensure your Erickson textbook .md file is placed there.")
        return

    source_file = target_files[0]
    print(f"Executing phase 1 pipeline target: {source_file.name}")

    try:
        print("-> Running sanitization step...")
        sanitized_text = sanitize_markdown(source_file)

        print("-> Compiling structural hierarchy ...")
        master_hierarchy = parse_toc_to_json(sanitized_text)


        print(f"-> Writing unified tracking mp to {output_path}")
        with open(output_path, "w", encoding="utf-8") as json_file:
            json.dump(master_hierarchy, json_file, indent=4, ensure_ascii=False)

        print("\n Phase 1 Ingestion fully operational!")
        print(f"Node compiled. Total root chapters discovered: {len(master_hierarchy.keys())}")

    except Exception as error:
        print(f"\n Pipeline Exception Caught during exraction run: {str(error)}")

    def full_structure_scan(sanitized_text: str):
        lines = sanitized_text.splitlines()

        print("=== HEADING LEVELS ===")
        heading_counts = {}
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#"):
                level = len(stripped) - len(stripped.lstrip("#"))
                heading_counts[level] = heading_counts.get(level, 0) + 1
        for level, count in sorted(heading_counts.items()):
            print(f"  {'#' * level}: {count} occurrences")

        print("\n=== SAMPLE # HEADINGS (first 20) ===")
        count = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("# ") and count < 20:
                clean = re.sub(r'<span[^>]*>.*?</span>', '', stripped)
                clean = re.sub(r'\*\*(.*?)\*\*', r'\1', clean)
                clean = re.sub(r'^[#\s]+', '', clean).strip()
                print(f"  Line {i:4d}: {repr(clean[:60])}")
                count += 1

        print("\n=== SAMPLE ## HEADINGS (first 20) ===")
        count = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("## ") and count < 20:
                clean = re.sub(r'<span[^>]*>.*?</span>', '', stripped)
                clean = re.sub(r'\*\*(.*?)\*\*', r'\1', clean)
                clean = re.sub(r'^[#\s]+', '', clean).strip()
                print(f"  Line {i:4d}: {repr(clean[:60])}")
                count += 1

        print("\n=== TABLE ROW SAMPLES (first 10) ===")
        count = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("|") and count < 10:
                print(f"  Line {i:4d}: {repr(stripped[:80])}")
                count += 1

    full_structure_scan(sanitized_text)



if __name__ == "__main__":
    os.makedirs("../raw_inputs", exist_ok=True)
    run_initialization_pipeline()


