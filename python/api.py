import logging

from fastapi import FastAPI
from pydantic import BaseModel, StrictStr

from database import save_evidence

from evidence_extraction_test import extract_evidence


app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
    logger.info("Starting evidence extraction")
    evidence = extract_evidence(request.customer_message)

    if evidence is None:
        logger.warning("Evidence extraction failed safely")
        return {
            "success": False,
            "message": "Evidence extraction failed safely.",
        }
    logger.info("Evidence extraction succeeded")

    record_id = save_evidence(
        request.customer_message,
        evidence,
    )

    logger.info("Evidence saved with record ID %s", record_id)

    return {
        "success": True,
        "record_id": record_id,
        "evidence": evidence.model_dump(),
    }