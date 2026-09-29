import json
import urllib.request


selected_information = "warning_lights"


prompt = f"""
Return JSON only.

You are a Virtual Automotive Customer Service Assistant.

The application has already decided what information
needs to be collected.

Your job is ONLY to turn the selected information into
ONE simple customer-friendly question.

Do not decide what information is needed.

Do not diagnose the vehicle.

Do not suggest a repair.

Ask exactly ONE question.

Selected information:

{selected_information}

If the selected information is "warning_lights",
ask whether any warning lights are currently displayed
on the dashboard.

Return exactly:

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


response = urllib.request.urlopen(
    request,
    timeout=60,
)


result = json.loads(
    response.read().decode()
)


parsed = json.loads(
    result["response"]
)


print("Selected information:")
print(selected_information)

print("\nAI question:")
print(parsed["question"])