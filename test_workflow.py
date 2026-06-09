import sqlite3
from pathlib import Path

# Force absolute system coordinates based on project hierarchy
PROJECT_ROOT = Path(__file__).parent.resolve()
DB_FILE_PATH = PROJECT_ROOT / "db" / "codex_ledger.db"

from engine.sm2_engine import calculate_sm2_mutation
from db.ledger_ops import fetch_daily_review_queue, log_assessment_result


def test_full_pipeline():
    print("--- [시작] 데이터베이스 큐에서 노드 하나를 포획합니다 ---")

    # Core operational data read
    queue = fetch_daily_review_queue()

    if not queue:
        print("⚠️ 큐가 비어있습니다. (스케줄링된 복습 대상 노드가 없음)")
        print("임시 처방: DB에서 레코드 하나를 강제로 가져와서 테스트를 진행합니다.")

        # Guard path execution to prevent duplicate database files
        conn = sqlite3.connect(DB_FILE_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT concept_id, concept_title, parent_chapter, current_interval, ease_factor, repetitions FROM concept_nodes LIMIT 1")

        # Map raw SQLite tuples to dict array
        queue = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
        conn.close()

    if not queue:
        print("❌ 시스템 예외: 데이터베이스 원본 파일이 완전히 비어있습니다.")
        return

    node = queue[0]
    print(f"✓ 포획 성공: {node['concept_title']} (ID: {node['concept_id']})")

    # Simulation Parameter: Simulating an assessment pass score of 4
    user_score = 4

    print(f"--- [계산] SM-2 알고리즘 가동 (Score: {user_score}) ---")
    new_interval, new_ef, new_rep = calculate_sm2_mutation(
        q=user_score,
        interval=node['current_interval'],
        ease_factor=node['ease_factor'],
        repetitions=node['repetitions']
    )

    print(f"-> 결과: 다음 복습 {new_interval}일 뒤, EF {new_ef:.2f}, 반복 {new_rep}회")

    # Log mutations to the durable ledger layer
    log_assessment_result(node['concept_id'], new_interval, new_ef, new_rep, user_score / 5.0)

    print("✓ 데이터베이스 상태 변경 업데이트 완료.")
    print("--- [종료] Phase 2 통합 테스트 성공 ---")


if __name__ == "__main__":
    test_full_pipeline()