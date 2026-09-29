from fastapi import FastAPI
from pydantic import BaseModel, StrictStr

from database import save_evidence

from evidence_extraction_test import extract_evidence


app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Automotive Platform",
    }


class CustomerMessage(BaseModel):
    customer_message: StrictStr


@app.post("/extract-evidence")
def extract_customer_evidence(request: CustomerMessage):
    evidence = extract_evidence(request.customer_message)

    if evidence is None:
        return {
            "success": False,
            "message": "Evidence extraction failed safely.",
        }

    record_id = save_evidence(
        request.customer_message,
        evidence,
    )

    return {
        "success": True,
        "record_id": record_id,
        "evidence": evidence.model_dump(),
    }