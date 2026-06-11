from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from engine.sm2_engine import calculate_sm2_mutation
from db.ledger_ops import log_assessment_result, log_cognitive_fault, get_recent_failure_count, record_assessment, check_consecutive_failure

PASS_Q_THRESHOLD = 4

def process_node_review(concept_id: str, concept_title: str, current_interval: int, current_ef: float,
                        current_rep: int, user_score: int, reasoning_gap:str = None) -> dict:
    """Orchestrates the transactional execution loop between tracking evaluation scores,
    running the SM-2 mutation calculator, and logging errors back to the database."""
    new_interval, new_ef, new_rep = calculate_sm2_mutation(
        q = user_score,
        interval = current_interval,
        ease_factor = current_ef,
        repetitions = current_rep
    )

    passed = user_score >= PASS_Q_THRESHOLD

    log_assessment_result(
        concept_id= concept_id,
        new_interval = new_interval,
        new_ef = new_ef,
        new_rep = new_rep,
        score = round(user_score / 5.0, 2)
    )

    if not passed and reasoning_gap:
        log_cognitive_fault(concept_id = concept_id, logic_gap_str = reasoning_gap)
    result_int = 1 if passed else 0
    record_assessment(concept_id, result_int)
    failure_count = get_recent_failure_count(concept_id)
    show_hint_button = (failure_count > 0)

    force_hint = check_consecutive_failure(concept_id)

    return {
        "concept_id": concept_id,
        "status": "Passed" if passed else "Failed",
        "show_hint_button": show_hint_button,
        "force_hint": force_hint
    }