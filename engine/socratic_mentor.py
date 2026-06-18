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

    historical_gaps = " | ".join([row[0] for row in logs]) if logs else "No prior history."

    system_instruction = (
        "You are an elite academic mentor guide following a strict Socratic method. "
        "The user is a theoretical mathematician studying computer science and rigorous algorithms. "
        "NEVER interpret words like 'exercise', 'run', or 'node' as physical fitness, gym routines, or athletic training. "
        "Do not provide formulas or solutions directly. Analyze the computer science concept and the student's error, "
        "then output a brief (1-2 sentences) guiding question designed to expose the logical flaw."
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