from pathlib import Path
import sys

ROOT_DIR = Path(__file__).parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from engine.sm2_engine import calculate_sm2_mutation
from db.ledger_ops import log_assessment_result, log_cognitive_fault

def process_node_review(concept_id: str, current_interval: int, current_ef: float, current_rep: int,
                        user_score: int, reasoning_gap:str = None) -> dict:
    """Orchestrates the transactional execution loop between tracking evaluation scores,
    running the SM-2 mutation calculator, and logging errors back to the database."""
    new_interval, new_ef, new_rep = calculate_sm2_mutation(
        q = user_score,
        interval = current_interval,
        ease_factor = current_ef,
        repetitions = current_rep
    )

    normalized_mastery_score = round(user_score / 5.0, 2)

    log_assessment_result(
        concept_id= concept_id,
        new_interval = new_interval,
        new_ef = new_ef,
        new_rep = new_rep,
        score = normalized_mastery_score
    )

    if user_score < 3 and reasoning_gap:
        log_cognitive_fault(concept_id = concept_id, logic_gap_str = reasoning_gap)

    return{
        "concept_id": concept_id,
        "new_review_interval": new_interval,
        "mutated_ease_factor": new_ef,
        "repetitions_completed": new_rep,
        "status": "Passed" if user_score >= 3 else "Failed/Collapsed"
    }