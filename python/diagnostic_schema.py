from pydantic import BaseModel, Field
from typing import Literal


class EvidenceItem(BaseModel):
    source: Literal[
        "customer_reported",
        "technician_observed",
        "diagnostic_test",
        "ai_inference",
    ]
    information: str

class TechnicianEvidence(BaseModel):
    observation: str
    technician_name: str | None = None


class DiagnosticTestEvidence(BaseModel):
    test_name: str
    result: str
    measurement: str | None = None


class StartingBehaviourAnswer(BaseModel):
    starting_behaviour: Literal[
        "turns over normally",
        "turns over slowly",
        "does not turn over at all",
        "unknown",
    ]


class Vehicle(BaseModel):
    make: str
    model: str
    year: int = Field(ge=1900, le=2100)


class DiagnosticRecord(BaseModel):
    vehicle: Vehicle
    complaint: str
    evidence: list[EvidenceItem] = []
    symptoms: list[str] = []
    warning_lights: list[str] = []
    conditions: list[str] = []
    possible_systems: list[str] = []
    possible_causes: list[str] = []
    missing_information: list[str] = []
    recommended_checks: list[str] = []
    confidence: Literal[
        "Confirmed",
        "Highly likely",
        "Possible",
        "Unknown / requires inspection",
    ] = "Unknown / requires inspection"


class ReasoningLink(BaseModel):
    evidence_source: Literal[
        "customer_reported",
        "technician_observed",
        "diagnostic_test",
        "ai_inference",
    ]
    evidence_information: str
    reasoning: str

class DiagnosticAnalysis(BaseModel):
    reasoning_links: list[ReasoningLink] = []
    key_observations: list[str] = []
    possible_systems: list[str] = []
    possible_causes: list[str] = []
    reasons_to_consider: list[str] = []
    missing_information: list[str] = []
    recommended_checks: list[str] = []
    confidence: Literal[
        "Confirmed",
        "Highly likely",
        "Possible",
        "Unknown / requires inspection",
    ] = "Unknown / requires inspection"


class WorkshopDiagnosticReport(BaseModel):
    vehicle: Vehicle
    customer_complaint: str
    evidence: list[EvidenceItem] = []
    technician_evidence: list[TechnicianEvidence] = []
    diagnostic_tests: list[DiagnosticTestEvidence] = []
    reasoning_links: list[ReasoningLink] = []
    key_observations: list[str] = []
    possible_systems: list[str] = []
    possible_causes: list[str] = []
    reasons_to_consider: list[str] = []
    missing_information: list[str] = []
    recommended_checks: list[str] = []
    confidence: Literal[
        "Confirmed",
        "Highly likely",
        "Possible",
        "Unknown / requires inspection",
    ] = "Unknown / requires inspection"
    physical_inspection_required: bool = True


class CustomerDiagnosticSummary(BaseModel):
    summary: str
    inspection_required: bool = True
    next_step: str