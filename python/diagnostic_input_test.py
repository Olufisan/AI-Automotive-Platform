customer_facts = {
    "vehicle": {
        "make": "Volkswagen",
        "model": "Golf",
        "year": 2018,
    },
    "complaint": (
        "The vehicle is difficult to start after driving "
        "for about 30 minutes."
    ),
    "symptoms": [],
    "warning_lights": [],
    "starting_behaviour": "turns over slowly",
    "frequency": "once or twice a week",
}


diagnostic_input = {
    "vehicle": customer_facts["vehicle"],
    "complaint": customer_facts["complaint"],
    "symptoms": customer_facts["symptoms"],
    "warning_lights": customer_facts["warning_lights"],
    "starting_behaviour": customer_facts["starting_behaviour"],
    "frequency": customer_facts["frequency"],
}


print("Diagnostic input:")

for key, value in diagnostic_input.items():
    print(f"{key}: {value}")