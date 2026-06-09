import sqlite3
import json
import re
from pathlib import Path

DB_PATH = Path(__file__).parent / "codex_ledger.db"
JSON_PATH = Path(__file__).parent.parent / "data" / "concept_map.json"

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS concept_nodes (
        concept_id TEXT PRIMARY KEY,
        concept_title TEXT NOT NULL,
        parent_chapter TEXT NOT NULL,
        mastery_score REAL DEFAULT 0.0,
        current_interval INTEGER DEFAULT 0,
        ease_factor REAL DEFAULT 2.5,
        repetitions INTEGER DEFAULT 0,
        last_reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE IF NOT EXISTS dependency_edges (
        parent_concept_id TEXT,
        child_concept_id TEXT,
        PRIMARY KEY (parent_concept_id, child_concept_id),
        FOREIGN KEY(parent_concept_id) REFERENCES concept_nodes(concept_id),
        FOREIGN KEY(child_concept_id) REFERENCES concept_nodes(concept_id)
    );
    
    CREATE TABLE IF NOT EXISTS cognitive_error_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        concept_id TEXT,
        error_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        logical_reasoning_gap TEXT,
        FOREIGN KEY(concept_id) REFERENCES concept_nodes(concept_id)
    );
    """)
    conn.commit()
    conn.close()

def seed_database():
    if not JSON_PATH.exists(): return
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    node_count = 0
    for chapter_title, sections in data.items():
        chapter_slug = re.sub(r'\W+', '_', chapter_title)

        for section_title, nodes in sections.items():
            match = re.match(r'^([\d\.]+)', section_title)
            num_part = match.group(1).replace('.', '_') if match else "no_num"
            section_slug = re.sub(r'\W+', '_', section_title)
            concept_id = f"{chapter_slug}_{num_part}_{section_slug}"

            cursor.execute("""
                INSERT OR IGNORE INTO concept_nodes (concept_id, concept_title, parent_chapter)
                VALUES (?, ?, ?)
            """, (concept_id, section_title, chapter_title))
            node_count += 1

    conn.commit()
    conn.close()
    print(f"Seed phase complete. {node_count} node written.")

if __name__ == "__main__":
    initialize_database()
    seed_database()









