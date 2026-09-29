from diagnostic_schema import CustomerDiagnosticSummary


customer_summary = CustomerDiagnosticSummary(
    summary=(
        "We have collected information about your starting problem. "
        "You reported that the engine turns over slowly and that "
        "the problem happens after approximately 30 minutes of driving. "
        "We have not physically inspected the vehicle, so the cause "
        "cannot be confirmed at this stage."
    ),
    inspection_required=True,
    next_step=(
        "The vehicle should be inspected by a qualified technician "
        "so the cause can be investigated."
    ),
)


print("Customer diagnostic summary created successfully")

print()

print(
    customer_summary.model_dump_json(
        indent=2
    )
)