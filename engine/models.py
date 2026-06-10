from pydantic import BaseModel, Field
from typing import List

class MultipleChoiceQuestion(BaseModel):
    question_text: str = Field(description = "The structural text or algorithmic scenario set up")
    choices: List[str] = Field(description = "Exactly 4 potential answer vectors")
    correct_choice_index: int = Field(description = "0-indexed value(0-3) indicating the ground-truth")
    mathematical_proof: str = Field(description = "Detailed Big-O complexity or discrete mathematical justification")

class CodeTracingQuestion(BaseModel):
    pseudocode_block: str = Field(description = "Syntactically valid algorithm array mutation string.")
    question_prompt: str = Field(description = "Asking for index states or tracking values after loop execution")
    expected_answer: str = Field(description = "Exact alphanumeric literal target.")

class ConceptQuizPackage(BaseModel):
    concept_id: str
    mcq_items: List[MultipleChoiceQuestion] = Field(..., max_items=3)
    tracing_items:List[CodeTracingQuestion] = Field(..., max_items=2)