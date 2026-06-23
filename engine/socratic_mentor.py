import ollama
from pathlib import Path
from db.ledger_ops import get_recent_error_logs


PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DB_PATH = PROJECT_ROOT / "db" / "codex_ledger.db"


def generate_socratic_hint(concept_title: str, faulty_answer: str, concept_id: str) -> str:
    """
    Read the past fail logs, generate socratics style hints
    """
    logs = get_recent_error_logs(concept_id)

    historical_gaps = " | ".join([logs]) if logs else "No prior history."

    system_instruction = (
        "You are an elite academic computer science distillation engine. "
        "YOUR READING PROTOCOL:\n"
        "1. SCAN: Search the provided text for the exact header: '{concept_title}'.\n"
        "2. IGNORE: Discard all text appearing BEFORE this header, as it is context drift from previous chapters.\n"
        "3. ANALYZE: Summarize ONLY the content starting from that header until the end of the section.\n"
        "4. FORMAT: Extract core definitions, mathematical equations, Big-O complexities, and invariants.\n"
        "5. If information is missing, return 'N/A'. Do not fabricate."
    )

    user_prompt = (
        f"Concept: {concept_title}\n"
        f"Student Error: {faulty_answer}\n"
        f"Prior Mistakes: {historical_gaps}\n\n"
        f"Generate a sharp, guiding Socratic question."
    )

    try:
        response = ollama.chat(
            model="llama3.1",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": 0.4}
        )
        return response.message.content.strip()
    except Exception:
        return f"Mentor is currently busy. Focus on the core logic: {concept_title}"