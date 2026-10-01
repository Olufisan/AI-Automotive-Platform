import logging
import time
import uuid

from fastapi import FastAPI
from pydantic import BaseModel, StrictStr

from database import check_database_connection, save_evidence
from evidence_extraction_test import extract_evidence


app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.get("/health")
def health_check():
    try:
        check_database_connection()
    except Exception:
        logger.exception("Database health check failed")
        return {
            "status": "unhealthy",
            "service": "AI Automotive Platform",
            "database": "unavailable",
        }

    return {
        "status": "healthy",
        "service": "AI Automotive Platform",
        "database": "available",
    }


class CustomerMessage(BaseModel):
    customer_message: StrictStr


class EvidenceResponse(BaseModel):
    success: bool
    record_id: int | None = None
    evidence: dict | None = None
    message: str | None = None


@app.post("/extract-evidence", response_model=EvidenceResponse)
def extract_customer_evidence(request: CustomerMessage):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info("Request %s: Starting evidence extraction", request_id)

    evidence = extract_evidence(request.customer_message)

    if evidence is None:
        logger.warning(
    "Request %s: Evidence extraction failed safely",
    request_id,
)
        return {
            "success": False,
            "message": "Evidence extraction failed safely.",
        }

    logger.info(
    "Request %s: Evidence extraction succeeded",
    request_id,
)

    try:
        record_id = save_evidence(
            request.customer_message,
            evidence,
        )
    except Exception:
        logger.exception(
    "Request %s: Failed to save evidence to database",
    request_id,
)
        return {
            "success": False,
            "message": "Evidence could not be saved.",
        }

    logger.info(
    "Request %s: Evidence saved with record ID %s",
    request_id,
    record_id,
)

    elapsed_time = time.perf_counter() - start_time

    logger.info(
        "Request %s: Completed in %.2f seconds",
        request_id,
        elapsed_time,
    )
    
    return {
        "success": True,
        "record_id": record_id,
        "evidence": evidence.model_dump(),
    }