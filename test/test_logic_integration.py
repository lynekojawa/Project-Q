
from engine.evaluation import process_node_review
from db.ledger_ops import reset_failure_history

# Test-ID
TEST_ID = "introduction_0_1_0_1_what_is_an_algorithm"
TEST_TITLE = "0.1 What is an algorithm"


def run_logic_test():
    print(f"=== [START] Testing Hybrid Scaffolding Logic ===")

    # 0. Reset: clear previous test data
    reset_failure_history(TEST_ID)
    print("✓ History reset.")

    # 1. Simulate 3 consecutive failures
    for i in range(1, 4):
        result = process_node_review(
            concept_id=TEST_ID,
            concept_title=TEST_TITLE,
            current_interval=1,
            current_ef=2.5,
            current_rep=0,
            user_score=1,
            reasoning_gap="Test fail"
        )
        print(f"Trial {i}: Status={result['status']}, HintBtn={result['show_hint_button']}, ForceHint={result['force_hint']}")


    if result['force_hint'] is True:
        print("\n🎉 SUCCESS: System triggered 'Forced Hint' after 3 consecutive failures.")
    else:
        print("\n❌ FAILURE: Logic failed. Check check_consecutive_failure logic.")


if __name__ == "__main__":
    run_logic_test()