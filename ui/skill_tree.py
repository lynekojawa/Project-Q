import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from db.ledger_ops import fetch_daily_review_queue
from engine.evaluation import process_node_review
from engine.socratic_mentor import generate_socratic_hint
import streamlit as st
import sqlite3

DB_PATH = PROJECT_ROOT / "db" / "codex_ledger.db"


def get_macro_metrics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM concept_nodes")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM concept_nodes WHERE mastery_score >= 0.80")
    mastered = cursor.fetchone()[0]
    conn.close()
    return total, mastered, len(fetch_daily_review_queue())


def get_chapters_and_nodes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM concept_nodes ORDER BY parent_chapter, concept_id")
    rows = cursor.fetchall()
    conn.close()

    data_tree = {}
    for row in rows:
        chap = row["parent_chapter"]
        if chap not in data_tree:
            data_tree[chap] = []
        data_tree[chap].append(dict(row))
    return data_tree


def render_ui_dashboard():
    st.set_page_config(page_title="Project Q // Codex Skill Tree", layout="wide")
    st.title("🏛️ Project Q: Codex Skill Tree Terminal")
    st.caption("Strategic Mathematical Core & Spaced Repetition Engine")
    st.markdown("---")

    # Initialize hint containers in session state to prevent white-screen crashes
    if "active_hint" not in st.session_state:
        st.session_state.active_hint = {}

    total, mastered, due_count = get_macro_metrics()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Nodes", value=total)
    col2.metric("Mastered (q>=4)", value=mastered)
    col3.metric("Pending Queue", value=due_count)
    st.markdown("---")

    data_tree = get_chapters_and_nodes()
    chapter_list = list(data_tree.keys())
    tabs = st.tabs(chapter_list)

    for idx, chapter_name in enumerate(chapter_list):
        with tabs[idx]:
            st.header(f"Chapter: {chapter_name}")
            for node in data_tree[chapter_name]:
                node_id = node['concept_id']
                expander_title = f"{node['concept_title']} [Int: {node['current_interval']}d | Reps: {node['repetitions']}]"

                with st.expander(expander_title):
                    score_input = st.slider("Accuracy (0-5):", 0, 5, 5, key=f"s_{node_id}")
                    reasoning = st.text_input("Logic Gap:", key=f"g_{node_id}")

                    # Render cached Socratic hints if they exist for this specific node
                    if node_id in st.session_state.active_hint:
                        hint_data = st.session_state.active_hint[node_id]
                        if hint_data["type"] == "audit":
                            st.error(f"🚨 FORCED SOCRATIC AUDIT: {hint_data['text']}")
                        else:
                            st.warning(f"💡 Socratic Hint: {hint_data['text']}")

                    if st.button("Commit Run", key=f"btn_{node_id}"):
                        with st.spinner("Synchronizing engine state..."):
                            res = process_node_review(
                                concept_id=node_id,
                                current_interval=node['current_interval'],
                                current_ef=node['ease_factor'],
                                current_rep=node['repetitions'],
                                user_score=score_input,
                                reasoning_gap=reasoning if reasoning else None
                            )

                            # Handle Socratic failure states cleanly by caching them in session memory
                            if res.get("force_hint"):
                                fault_trace = reasoning if reasoning else "Algorithmic execution failure."
                                hint_text = generate_socratic_hint(node['concept_title'], fault_trace, node_id)
                                st.session_state.active_hint[node_id] = {"type": "audit", "text": hint_text}
                                st.rerun()

                            elif res.get("show_hint_button") or res.get("status") == "Failed":
                                fault_trace = reasoning if reasoning else "General conceptual gap."
                                hint_text = generate_socratic_hint(node['concept_title'], fault_trace, node_id)
                                st.session_state.active_hint[node_id] = {"type": "hint", "text": hint_text}
                                st.rerun()

                            elif score_input >= 4:
                                # Clear active hints on success
                                if node_id in st.session_state.active_hint:
                                    del st.session_state.active_hint[node_id]
                                st.success(f"🎉 Core Matrix Updated. Status: {res.get('status')}")
                                st.rerun()


if __name__ == "__main__":
    render_ui_dashboard()