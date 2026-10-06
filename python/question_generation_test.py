import json
import urllib.request

from pydantic import BaseModel

class DiagnosticQuestion(BaseModel):
    question: str


def generate_question(selected_information):
    prompt = f"""
Return JSON only.

You are a Virtual Automotive Customer Service Assistant.

The application has already decided what information
needs to be collected from the customer.

Your job is ONLY to turn the selected information into
ONE simple customer-friendly question.

Do not decide what information is needed.

Do not diagnose the vehicle.

Do not suggest a repair.

Do not assume the cause of the problem.

Ask exactly ONE question.

Selected information to collect:

{selected_information}

For "starting_behaviour", ask whether the engine:
- turns over normally
- turns over slowly
- does not turn over at all

Use simple language that a normal vehicle owner
can understand.

Return exactly this JSON structure:

{{
    "question": "your single question"
}}
"""

    payload = {
        "model": "qwen3:1.7b",
        "prompt": prompt,
        "stream": False,
        "think": False,
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    response = urllib.request.urlopen(request, timeout=60)
    result = json.loads(response.read().decode())

    return DiagnosticQuestion.model_validate_json(
    result["response"]
)


if __name__ == "__main__":
    selected_information = "starting_behaviour"

    question = generate_question(selected_information)

    print("Generated question:")
    print(question.question)