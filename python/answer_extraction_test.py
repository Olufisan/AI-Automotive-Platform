import json
import urllib.error
import urllib.request

from pydantic import ValidationError

from diagnostic_schema import (
    DiagnosticAnswer,
    StartingBehaviourAnswer,
)

def extract_answer(customer_answer, information_type):
    prompt = f"""
Return JSON only.

You are an information extraction assistant.

Extract ONLY information explicitly stated
in the customer's answer.

Do not diagnose the vehicle.

Do not suggest a repair.

Do not add information that the customer did not provide.

The information being collected is:

{information_type}

The customer's answer is:

{customer_answer}

Return exactly this JSON structure:

{{
    "information_type": "{information_type}",
    "answer": "..."
}}

If the customer's answer does not clearly provide
the requested information, return:

"unknown"
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

    try:
        response = urllib.request.urlopen(
            request,
            timeout=60,
        )

    except TimeoutError as error:
        print("\nAI request failed")
        print(error)
        return None

    except urllib.error.URLError as error:
        print("\nAI request failed")
        print(error)
        return None

    result = json.loads(
        response.read().decode()

    
    )

    

    try:
        parsed_json = json.loads(
            result["response"]
        )

        return DiagnosticAnswer.model_validate(
            parsed_json
        )

    except json.JSONDecodeError as error:
        print("\nAI returned invalid JSON")
        print(error)
        return None

    except ValidationError as error:
        print("\nPydantic validation failed")
        print(error)
        return None

def extract_starting_behaviour(customer_answer):
    prompt = f"""
Return JSON only.

You are an information extraction assistant.

Extract the customer's answer into the specified field.

Do not diagnose the vehicle.

Do not suggest a repair.

Do not add information that the customer did not provide.

The information being collected is:

starting_behaviour

The customer's answer is:

{customer_answer}

Return exactly this JSON structure:

{{
    "starting_behaviour": "..."
}}

Use one of these values when supported by the customer's answer:

- turns over normally
- turns over slowly
- does not turn over at all

If the answer does not clearly provide the information,
return:

"unknown"
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

    try:
        response = urllib.request.urlopen(
            request,
            timeout=60,
        )

    except urllib.error.URLError as error:
        print("\nAI request failed")
        print(error)
        return None

    result = json.loads(
        response.read().decode()
    )

    print("Raw AI response:")
    print(result["response"])

    try:
        parsed_json = json.loads(
            result["response"]
        )

        answer = StartingBehaviourAnswer.model_validate(
            parsed_json
        )

        print("\nPydantic validation passed")
        print(answer.model_dump_json(indent=2))

        return answer

    except json.JSONDecodeError as error:
        print("\nAI returned invalid JSON")
        print(error)
        return None

    except ValidationError as error:
        print("\nPydantic validation failed")
        print(error)
        return None

if __name__ == "__main__":
    customer_answer = "It turns over slowly."

    answer = extract_starting_behaviour(
        customer_answer
    )