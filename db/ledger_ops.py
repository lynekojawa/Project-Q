import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "codex_ledger.db"

def fetch_daily_review_queue():
    """
    Queries nodes that have decayed or reached scheduled spacing timelines.
    Returns elements where (last_view + interval) is less than or equal to now.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
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
    finally:
        conn.close()

def log_assessment_result(concept_id: str, new_interval: int, new_ef: float, new_rep: int, score: float):
    """Updates tracking state matrices for a target node upon exercise termination."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE concept_nodes
        SET current_interval =?,
            ease_factor = ?,
            repetitions = ?,
            mastery_score = ?,
            last_reviewed_at = CURRENT_TIMESTAMP
        Where concept_id = ?
    """, (new_interval, new_ef, new_rep, score, concept_id))

    conn.commit()
    conn.close()
def log_cognitive_fault(concept_id: str, logic_gap_str: str):
    """Saves targeted logical failure tracking records for execution analysis loops."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO cognitive_error_logs (concept_id, logical_reasoning_gap)
        VALUES (?, ?)
        """, (concept_id, logic_gap_str))

    conn.commit()
    conn.close()
