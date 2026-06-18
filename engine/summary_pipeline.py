import sys
import json
import ollama
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from ingestion.pdf_processor import extract_text_from_pdf
from engine.models import AutomatedConceptSummary

def compile_concept_summary(pdf_path: Path, start_page: int, end_page: int, concept_title: str) -> AutomatedConceptSummary:
    """
    Extracts textbook pages, sanitizes glyphs, and orchestrates a local LLM run
    via a strict Pydantic JSON structure to yield an algorithmic summary.
    """
    raw_text = extract_text_from_pdf(pdf_path, start_page = start_page, end_page = end_page)
    print(f"DEBUG: Extracted text preview (first 500 chars): {raw_text[:500]}")
    system_instruction = (
        "You are an elite academic computer science distillation engine. "
        "Analyze the provided textbook text. If the text does not contain mathematical proofs or complexity bounds, "
        "you MUST return 'N/A' for those fields. Do not fabricate data. "
        "Output a strict JSON object matching the requested schema exactly. "
    )

    user_prompt = (
        f"Target Concept Title: {concept_title}\n"
        f"Source Document Extract Material:\n{raw_text}\n\n"
        f"Extract technical specifications matching the structural Pydantic blueprint contract."
    )

    print(f"🧠 [LLM Summary Engine] Submitting tokens to Llama for concept: {concept_title}...")

    response = ollama.chat(
        model="llama3.1",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_prompt}
        ],
        format=AutomatedConceptSummary.model_json_schema(),
        options={"temperature": 0.1}
    )

    json_payload = response.message.content.strip()
    validated_summary = AutomatedConceptSummary.model_validate_json(json_payload)

    return validated_summary

if __name__ == "__main__":
    PDF_TARGET = PROJECT_ROOT / "data" / "raw" / "Algorithms-JeffE.pdf"

    if PDF_TARGET.exists():
        try:
            # Let's test compiling a structured analysis of the introduction chapter
            summary = compile_concept_summary(
                pdf_path=PDF_TARGET,
                start_page=41,
                end_page=43,
                concept_title="1.3 Tower of Hanoi"
            )
            print("\n🎯 [Pipeline Pass] Validated Summary JSON Returned:")
            print(json.dumps(summary.model_dump(), indent=2))
        except Exception as e:
            print(f"\n❌ Pipeline Breakdown: {str(e)}")