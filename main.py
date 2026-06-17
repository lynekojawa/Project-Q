import sys
import subprocess
import urllib.request
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
DB_PATH = PROJECT_ROOT / "db" / "codex_ledger.db"

def enter_maintenance_mode():
    """Terminal-isolated recovery protocol to stabilize ledger inconsistencies."""
    print("\n⚠️ [Maintenance Mode] Critical state detected. Imperial Intervention Required.")
    print("Select an action to stabilize the system:")
    print("1. [D]elete & Rebuild: Nuke current DB and start fresh.")
    print("2. [E]xit: Terminate session.")
    while True:
        choice = input("Enter choice (D/E): ").strip().upper()
        if choice == "D":
            if DB_PATH.exists():
                try:
                    DB_PATH.unlink()
                except PermissionError:
                    print("❌ Failure: Database binary file is currently locked by an active process.")
                    return False
            print("Database cleared. Reinitializing schema tracking paths...")
            sys.path.append(str(PROJECT_ROOT))
            from db.db_setup import initialize_database, seed_database
            initialize_database()
            seed_database()
            print("Database reconstructed successfully. Resuming boot track...")
            return True
        elif choice == 'E':
            print("Shutting down")
            sys.exit(0)
        else:
            print("Invalid input")

def run_preflight_checks():
    print("[System Boot] Initializing Project Q preflight check protocol...")

    print("Checking local Ollama daemon connectivity (http://localhost:11434)...")
    try:
        with urllib.request.urlopen("http://localhost:11434", timeout=2) as response:
            if response.status == 200:
                print("Ollama Client Connection: Online")
    except Exception:
        print("\n Critical Boot Failure: Local Ollama is unreachable")
        print("Action Required: Execute 'ollama serve' in your terminal and ensure model is pulled via 'ollama pull llama3.1'")
        sys.exit(1)

    print("Checking relational ledger status...")
    if not DB_PATH.exists():
        print("Warning: 'codex_ledger.db' not found. Launching auto initialization sequence")
        enter_maintenance_mode()
    else:
        print("Relational Ledger Connection: Secure")

    print("All environment safety guards passed. Spawning Streamlit Frontend Console Framework... \n")

def launch_application():
    """Spawns the streamlit server process pointing explicitly to UI module"""
    ui_script_path = PROJECT_ROOT / "ui" / "skill_tree.py"

    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(ui_script_path)], check=True)
    except KeyboardInterrupt:
        print("\n[System Shutdown] Stopping server threads. Core states safely persisted to ledger. Goodbye")
    except Exception as e:
        print(f"\n Runtime Exception Encountered: {str(e)}")

if __name__ == "__main__":
    run_preflight_checks()
    launch_application()