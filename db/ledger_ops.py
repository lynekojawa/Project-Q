import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).parent / "codex_ledger.db"

def fetch_daily_review_queue():
    """
    Queries nodes that have decayed or reached scheduled spacing timelines.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT concept_id, concept_title, parent_chapter, current_interval, ease_factor, repetitions
                FROM concept_nodes
                WHERE current_interval = 0 
                    OR datetime(last_reviewed_at, '+' || current_interval || ' days') <= datetime('now')
            """)
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"DB QUery Error:{e}")
        return []


def log_assessment_result(concept_id: str, new_interval: int, new_ef: float, new_rep: int, score: float):
    """Updates tracking state matrices for a target node upon exercise termination."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE concept_nodes
                SET current_interval =?,
                    ease_factor = ?,
                    repetitions = ?,
                    mastery_score = ?,
                    last_reviewed_at = CURRENT_TIMESTAMP
                WHERE concept_id = ?
            """, (new_interval, new_ef, new_rep, score, concept_id))
    except sqlite3.Error as e:
        print(f"[DB ERROR] Assessment update failed for {concept_id}: {e}")

def log_cognitive_fault(concept_id: str, logic_gap_str: str):
    """Saves targeted logical failure tracking records for execution analysis loops."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cognitive_error_logs (concept_id, logical_reasoning_gap)
                VALUES (?, ?)
            """, (concept_id, logic_gap_str))
    except sqlite3.Error as e:
        print(f"[DB ERROR] Fault log failed for {concept_id}: {e}")

def get_recent_failure_count(concept_id: str) -> int:
    """ Returns the number of failures for a specific nodes."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM cognitive_error_logs
                WHERE concept_id = ?
                AND error_timestamp >= datetime('now', '-7 days') 
            """, (concept_id,))
            return cursor.fetchone()[0]
    except sqlite3.Error:
        return 0

def record_assessment(concept_id: str, result: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO assessment_history (concept_id, result) VALUES (?, ?)", (concept_id, result))

def check_consecutive_failure(concept_id: str) -> bool:
    """Check if recent three are all 'Failed'"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT result FROM assessment_history
                WHERE concept_id = ?
                ORDER BY timestamp DESC LIMIT 3
            """, (concept_id,))
            results = cursor.fetchall()
            failure_list = [int(r[0]) for r in results]

            is_consecutive = (len(failure_list) == 3 and all(val == 0 for val in failure_list))
            print(f"DEBUG: Consecutive logic result for {concept_id}: {is_consecutive}")
            return is_consecutive

    except sqlite3.Error as e:
        print(f"DB Error: {e}")
        return False

def reset_failure_history(concept_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM assessment_history WHERE concept_id = ?", (concept_id,))

def apply_mentoring_recovery(concept_id: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE concept_nodes SET ease_factor = ease_factor + .2 WHERE concept_id = ?", (concept_id,))
