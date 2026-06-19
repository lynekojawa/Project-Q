import sys
import json
import ollama
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from ingestion.pdf_processor import extract_text_from_pdf
from engine.models import AutomatedConceptSummary

DB_PATH = PROJECT_ROOT / "db" / "codex_ledger.db"
PDF_TARGET = PROJECT_ROOT / "data" / "raw" / "Algorithms-JeffE.pdf"

def get_concept_title(concept_id: str) -> str:
    """Looks up concept title from DB by concept_id."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT concept_title FROM concept_nodes WHERE concept_id = ?",
                (concept_id,)
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Concept ID '{concept_id}' not found in ledger.")
            return row["concept_title"]
    except sqlite3.Error as e:
        raise RuntimeError(f"DB lookup failed: {e}")

def locate_concept_page_bounds(pdf_path: Path, target_title: str, next_title_hint: str = None) -> tuple:
    """
    Scans PDF page by page to find where target_title starts
    and where next_title_hint begins (as the end boundary).
    """
    start_page = None
    end_page = None
    clean_target = target_title.strip().lower()

    with open(pdf_path, "rb") as f:
        import pypdf
        reader = pypdf.PdfReader(f)
        total_pages = len(reader.pages)

        for page_idx in range(total_pages):
            page_text = reader.pages[page_idx].extract_text()
            if not page_text:
                continue
            clean_page = page_text.lower()

            if start_page is None and clean_target in clean_page:
                if "contents" not in clean_page[:100]:
                    start_page = page_idx
                    print(f"Found '{target_title}' on page {page_idx}")

            elif start_page is not None and next_title_hint:
                if next_title_hint.strip().lower() in clean_page:
                    end_page = page_idx
                    print(f"Found boundary at page {page_idx}")
                    break

        if start_page is None:
            raise ValueError(f"Could not locate '{target_title}' in PDF.")
        if end_page is None:
            end_page = min(start_page + 5, total_pages)

    return start_page, end_page

def compile_concept_summary(concept_id: str, next_concept_id: str = None) -> AutomatedConceptSummary:
    """
    Looks up concept by ID, finds its pages dynamically, generates summary.
    """
    concept_title = get_concept_title(concept_id)
    next_title_hint = get_concept_title(next_concept_id) if next_concept_id else None

    start_page, end_page = locate_concept_page_bounds(
        PDF_TARGET, concept_title, next_title_hint
    )

    raw_text = extract_text_from_pdf(PDF_TARGET, start_page=start_page, end_page=end_page)

    system_instruction = (
        "You are an elite academic computer science distillation engine. "
        f"Analyze the provided text and summarize the section titled: '{concept_title}'.\n"
        "Extract core definitions, mathematical equations, Big-O complexities, and invariants. "
        "Return 'N/A' for fields not present. Do not fabricate data."
    )

    user_prompt = (
        f"Concept: {concept_title}\n"
        f"Source Text:\n{raw_text}\n\n"
        "Compile a strict JSON object matching the Pydantic contract."
    )

    print(f"Submitting to LLM: [{concept_id}] -> '{concept_title}'")

    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        format=AutomatedConceptSummary.model_json_schema(),
        options={"temperature": 0.1}
    )

    return AutomatedConceptSummary.model_validate_json(response.message.content.strip())


if __name__ == "__main__":
    try:
        summary = compile_concept_summary(
            concept_id="recursion_1_3_1_3_tower_of_hanoi",
            next_concept_id="recursion_1_4_1_4_mergesort"
        )
        print("\nSummary:")
        print(json.dumps(summary.model_dump(), indent=2))
    except Exception as e:
        print(f"Pipeline failed: {e}")