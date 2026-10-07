import json
import os
import urllib.error
import urllib.request

from pydantic import ValidationError

from automotive_evidence import AutomotiveEvidence


def extract_evidence(customer_message, max_attempts=2):

    message_lower = customer_message.lower()

    if "mild" in message_lower:
        severity = "mild"
    elif "moderate" in message_lower:
        severity = "moderate"
    elif "severe" in message_lower:
        severity = "severe"
    else:
        severity = "not specified"

    for attempt in range(1, max_attempts + 1):

        print(f"AI extraction attempt {attempt} of {max_attempts}")

        prompt = f"""
Return JSON only.

You are an automotive information extraction system.

Extract ONLY facts explicitly stated by the customer.

Do NOT:
- diagnose the vehicle
- guess possible causes
- recommend repairs
- recommend tests
- invent information

Return exactly these fields:

observation
context
duration
confirmed_by_technician

Field rules:

- observation: the main problem or symptom explicitly reported by the customer.

- context: relevant circumstances explicitly stated by the customer,
  such as when, where, or under what conditions the problem occurs.
  Do NOT put duration information in context.

- duration: copy the exact time or duration explicitly stated by the customer.
  This includes expressions such as "yesterday", "today", "three days ago",
  "last week", "for two weeks", "for three months", "occasionally",
  "sometimes", or "frequently".
  If the customer does not explicitly state a time or duration,
  return an empty string.
  Never infer or invent a duration.
  Only use a time or duration that appears explicitly in the customer message.

- confirmed_by_technician: true only when the customer explicitly says
  that a technician, mechanic, garage, or workshop inspected, checked,
  diagnosed, or confirmed the issue.

Rules:

- confirmed_by_technician must be true ONLY when the customer
  explicitly states that a technician, mechanic, garage, or workshop
  inspected, checked, diagnosed, or confirmed the issue.

- If the customer does not mention a technician, mechanic, garage,
  or workshop, confirmed_by_technician MUST be false.

- Never infer technician confirmation from the type or severity
  of the problem.

- A statement such as "the problem is severe" does NOT mean
  a technician confirmed it.

Customer message:
{customer_message}
"""

        payload = {
            "model": os.getenv("OLLAMA_MODEL", "qwen3:1.7b"),
            "prompt": prompt,
            "stream": False,
            "think": False,
        }

        request = urllib.request.Request(
            os.getenv(
             "OLLAMA_URL",
             "http://localhost:11434/api/generate",
            ),
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},

       )

        try:
            response = urllib.request.urlopen(
                 request,   
                 timeout=int(os.getenv("OLLAMA_TIMEOUT", "60")),
       )
            result = json.loads(response.read().decode())

        except TimeoutError:
            print("AI request timed out.")
            print("Retrying AI extraction...")
            continue

        except urllib.error.URLError as error:
            print("AI connection failed.")
            print(error)
            print("Retrying AI extraction...")
            continue

        raw_response = result.get("response")

        if not raw_response:
            print("AI response did not contain generated content.")
            print("Retrying AI extraction...")
            continue

        print("AI response received.")

        try:
            parsed_json = json.loads(raw_response)

            parsed_json["evidence_type"] = "customer_reported"
            parsed_json["severity_or_intensity"] = severity

            evidence = AutomotiveEvidence.model_validate(parsed_json)

            print("Parsed evidence before verification:")
            print(evidence.model_dump_json(indent=2))

            allowed_severity_words = {
                "mild",
                "moderate",
                "severe",
            }

            if evidence.severity_or_intensity in allowed_severity_words:
                if evidence.severity_or_intensity not in customer_message.lower():
                    raise ValueError(
                        "AI inferred severity that was not explicitly "
                        "stated by the customer."
                    )
            print("AI RETURNED DURATION:", evidence.duration)

            duration_words = {
            "second",
            "seconds",
            "minute",
            "minutes",
            "hour",
            "hours",
            "day",
            "days",
            "week",
            "weeks",
            "month",
            "months",
            "year",
            "years",
            "yesterday",
            "today",
            "tomorrow",
            "recently",
            "occasionally",
            "sometimes",
            "frequently",
            "always",
            "never",
        }

            if evidence.duration:
                duration_lower = evidence.duration.lower()

                if not any(
                    word in duration_lower
                    for word in duration_words
                ):
                    evidence.duration = ""
            if (
                evidence.duration
                and evidence.duration.lower() in evidence.context.lower()
            ):
                evidence.context = ""

            technician_words = {
                "technician",
                "mechanic",
                "garage",
                "workshop",
            }

            if (
                evidence.confirmed_by_technician
                and not any(
                    word in customer_message.lower()
                    for word in technician_words
                )
            ):
                raise ValueError(
                    "AI inferred technician confirmation that was not "
                    "explicitly stated by the customer."
                )

            print("Pydantic validation passed")
            print(evidence.model_dump_json(indent=2))

            return evidence

        except json.JSONDecodeError as error:
            print("AI returned invalid JSON")
            print(error)

        except ValidationError as error:
            print("Pydantic validation failed")
            print(error)

        except ValueError as error:
            print("Evidence verification failed")
            print(error)

        if attempt < max_attempts:
            print("Retrying AI extraction...")

    print("Maximum extraction attempts reached.")
    print("Evidence extraction failed safely.")

    return None


test_messages = [
    """
    The grinding noise is mild.
    """,
    """
    The vibration is moderate.
    """,
    """
    The braking problem is severe.
    """,
    """
    My car makes a grinding noise when I brake hard.
    """,
    """
    The brake pedal feels soft.
    """,
    """
    There is a loud noise coming from the engine.
    """,
    """
    The vehicle has a strange noise when starting.
    It has been happening for 15 minutes.
    """,
        """
    The steering wheel shakes badly when I drive above 60 mph.
    It started yesterday.
    """,
]


if __name__ == "__main__":
    for message in test_messages:
        print("\n" + "=" * 60)
        print("CUSTOMER MESSAGE")
        print(message.strip())
        print("=" * 60)

        evidence = extract_evidence(message)

        print("RESULT:")
        print(evidence)