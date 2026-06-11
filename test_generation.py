import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import json
import ollama
from pydantic import ValidationError
from engine.models import ConceptQuizPackage
from db.ledger_ops import fetch_daily_review_queue

def run_inference_validation_test():
    print("===Phase 3: OLLAMA Structured Generation Test====")

    queue = fetch_daily_review_queue()
    target_concept = queue[0]['concept_title'] if queue else "0.1 What is an algorithm?"

    print(f"Target Concept Selected: '{target_concept}'")
    print("Invoking local LLM context generation layer (this may take a moment)...")

    system_prompt = (
        "You are a level-2 system architect and theoretical mathematician."
        "Generate a rigorous, highly technical academic quiz package matching the requested concept."
        "Do not include conversational filler or markdown notes outside the JSON structure."
    )

    user_prompt = f"Generate an advanced quiz package for the topic: '{target_concept}' matching the technical depth of Jeff Erickson's 'Algorithms'."

    try:
        response = ollama.chat(
            model = "llama3.1:latest",
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            format = ConceptQuizPackage.model_json_schema(),
            options={"temperature": 0.0}
        )

        raw_output = response.message.content
        print("\n Raw Token Stream Captured from Ollama")

        validated_package = ConceptQuizPackage.model_validate_json(raw_output)
        print("Success: Data contract verified type-safe. Pydantic verification passed")
        #remove truncation when turning into UI
        print("\n---Compiled Data Payload Preview----")
        print(json.dumps(validated_package.model_dump(), indent = 2, ensure_ascii = False)[:1000] + "\n...")

    except Exception as e:

        print(f"❌ Test Failed: {str(e)}")
if __name__ == "__main__":
    run_inference_validation_test()

