import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, StrictStr
from diagnostic_schema import DiagnosticAnswer
from automotive_evidence import AutomotiveEvidence

from database import check_database_connection, save_evidence
from diagnostic_orchestrator import process_customer_answer
from evidence_extraction import extract_evidence


app = FastAPI(
    title="AI Automotive Platform API",
    description=(
        "AI-powered automotive diagnostic and evidence "
        "extraction API."
    ),
    version="1.0.0",
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    request_id = str(uuid.uuid4())

    logger.warning(
        "Request %s: Request validation failed: %s",
        request_id,
        exc.errors(),
    )

    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "request_id": request_id,
        },
    )


@app.get(
    "/health",
    summary="Check API and database health",
    description=(
        "Checks whether the AI Automotive Platform API is running "
        "and whether a connection to the PostgreSQL database is available."
    ),
)
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
        "version": "1.0.0",
    }


class CustomerMessage(BaseModel):
    customer_message: StrictStr = Field(max_length=2000)


class DiagnosticRequest(BaseModel):
    customer_facts: dict
    customer_answer: StrictStr = Field(max_length=2000)
    information_type: StrictStr

class DiagnosticResult(BaseModel):
    answer: DiagnosticAnswer
    updated_facts: dict
    next_information: str | None = None
    next_question: str | None = None


class DiagnosticResponse(BaseModel):
    success: bool
    result: DiagnosticResult | None = None
    error_code: str | None = None
    message: str | None = None
    request_id: str
    processing_time_seconds: float | None = None

class EvidenceResponse(BaseModel):
    success: bool
    request_id: str
    record_id: int | None = None
    evidence: AutomotiveEvidence | None = None
    error_code: str | None = None
    message: str | None = None
    processing_time_seconds: float | None = None


@app.post(
    "/process-diagnostic",
    response_model=DiagnosticResponse,
    summary="Process a diagnostic answer",
    description=(
        "Extracts a customer's answer, updates the diagnostic facts, "
        "identifies missing information, and generates the next "
        "diagnostic question."
    ),
)

def process_diagnostic(request: DiagnosticRequest):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info(
        "Request %s: Starting diagnostic processing",
        request_id,
    )

    result = process_customer_answer(
        request.customer_facts,
        request.customer_answer,
        request.information_type,
    )

    elapsed_time = time.perf_counter() - start_time

    if result is None:
        logger.warning(
            "Request %s: Diagnostic processing failed safely",
            request_id,
        )

        return {
            "success": False,
            "request_id": request_id,
            "error_code": "DIAGNOSTIC_PROCESSING_FAILED",
            "message": "Diagnostic processing failed safely.",
            "processing_time_seconds": round(
                elapsed_time,
                2,
            ),
        }

    logger.info(
        "Request %s: Diagnostic processing succeeded",
        request_id,
    )

    return {
        "success": True,
        "request_id": request_id,
        "result": result,
        "processing_time_seconds": round(
            elapsed_time,
            2,
        ),
    }


@app.post(
    "/extract-evidence",
    response_model=EvidenceResponse,
    summary="Extract customer evidence",
    description=(
        "Extracts structured evidence from a customer's message "
        "using explicit customer-reported information and validates "
        "the result before returning it."
    ),
)
def extract_customer_evidence(request: CustomerMessage):
    request_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info(
        "Request %s: Starting evidence extraction",
        request_id,
    )

    try:
        evidence = extract_evidence(
            request.customer_message,
        )

    except Exception:
        logger.exception(
            "Request %s: Unexpected AI extraction failure",
            request_id,
        )
        logger.warning(
            "Request %s: Evidence extraction failed safely",
            request_id,
        )

        return {
            "success": False,
            "request_id": request_id,
            "error_code": "AI_EXTRACTION_EXCEPTION",
            "message": "AI extraction failed unexpectedly.",
            "processing_time_seconds": round(
                time.perf_counter() - start_time,
                2,
            ),
        }

    if evidence is None:
        return {
            "success": False,
            "request_id": request_id,
            "error_code": "AI_EXTRACTION_FAILED",
            "message": "Evidence extraction failed safely.",
            "processing_time_seconds": round(
                time.perf_counter() - start_time,
                2,
            ),
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
            "request_id": request_id,
            "error_code": "DATABASE_SAVE_FAILED",
            "message": "Evidence could not be saved.",
            "processing_time_seconds": round(
                time.perf_counter() - start_time,
                2,
            ),
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
        "request_id": request_id,
        "record_id": record_id,
        "evidence": evidence.model_dump(),
        "processing_time_seconds": round(
            elapsed_time,
            2,
        ),
    }