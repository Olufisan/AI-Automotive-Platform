from automotive_evidence import AutomotiveEvidence
from database import save_evidence


def test_save_evidence():
    evidence = AutomotiveEvidence(
        evidence_type="customer_reported",
        observation="The grinding noise is mild.",
        context="",
        severity_or_intensity="mild",
        duration="",
        confirmed_by_technician=False,
    )

    record_id = save_evidence(
        "The grinding noise is mild.",
        evidence,
    )

    assert isinstance(record_id, int)
    assert record_id > 0