#Orion Suggested
#Both agreed with 114 nodes from manually audited concept_map json

import sys
from pathlib import Path


def run_workspace_audit():
    print("=== PROJECT-Q DATA TRACK VERIFICATION ===")

    # 1. Structural File Existence Checks
    root_dir = Path(__file__).parent.parent.resolve()
    db_dir = root_dir / "db"
    data_file = root_dir / "data" / "concept_map.json"

    print(f"Root Workspace Path: {root_dir}")
    print(f"Checking 'db/' workspace track layout...")

    db_setup_path = db_dir / "db_setup.py"
    ledger_ops_path = db_dir / "ledger_ops.py"

    assert db_setup_path.exists(), f"❌ Alignment Error: db_setup.py is missing from {db_dir}"
    assert ledger_ops_path.exists(), f"❌ Alignment Error: ledger_ops.py is missing from {db_dir}"
    assert data_file.exists(), f"❌ Configuration Error: concept_map.json is missing from {data_file.parent}"

    print("✓ All structural engine script targets discovered in valid directories.")

    # 2. Execution Run Verification
    print("\nExecuting database instantiation and seeding run...")
    try:
        # Append the root path to system pathways to ensure clean module discovery
        sys.path.append(str(root_dir))

        from db.db_setup import initialize_database, seed_database
        from db.ledger_ops import fetch_daily_review_queue

        # Run DB generation sequence
        initialize_database()
        seed_database()

        # Verify database file was generated inside the db/ directory natively
        generated_db = db_dir / "codex_ledger.db"
        assert generated_db.exists(), f"❌ Runtime Path Error: codex_ledger.db was not generated at {generated_db}"
        print(f"✓ Active database tracking file verified at: {generated_db.name}")

        # Run test read query through ledger_ops
        queue = fetch_daily_review_queue()
        print(f"✓ Ledger Operations Integration Verified. Initial Queue Size: {len(queue)} nodes.")
        print("\n🎉 STATUS: DATABASE INITIALIZATION PHASE COMPLETE AND VERIFIED.")

    except Exception as error:
        print(f"\n❌ Verification Pipeline Failure: {str(error)}")
        print("Review your directory locations or structural variable path scopes.")


if __name__ == "__main__":
    run_workspace_audit()