from typing import Literal
from pydantic import BaseModel, StrictBool


class CustomerReport(BaseModel):
    evidence_type: str
    observation: str
    context: str
    severity_or_intensity: Literal["mild", "moderate", "severe"]
    duration:
    confirmed_by_technician: StrictBool

report = CustomerReport(
    evidence_type="customer_reported",
    observation="My car makes a grinding noise when I brake hard",
    context="Braking hard",
    severity_or_intensity="severe",
    duration="occasional",
    confirmed_by_technician=False,
)

print(report)