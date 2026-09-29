from typing import Literal

from pydantic import BaseModel, StrictBool


class AutomotiveEvidence(BaseModel):
    evidence_type: Literal["customer_reported"]
    observation: str
    context: str
    severity_or_intensity: Literal[
        "mild",
        "moderate",
        "severe",
        "not specified",
    ]
    duration: str
    confirmed_by_technician: StrictBool