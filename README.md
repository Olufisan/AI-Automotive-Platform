# AI Automotive Platform

A local-first AI-powered automotive customer service and workshop automation platform.

## Purpose

This project is designed to automate repetitive customer-service, workshop administration, diagnostic support, communication, and record-keeping tasks.

The system combines:

- Local AI
- Workflow automation
- PostgreSQL
- Vector search
- CRM
- Automotive diagnostic knowledge
- Workshop processes
- Payment simulation
- Customer communication

The goal is to reduce repetitive manual administration while keeping human involvement where physical inspection, safety, customer approval, or professional judgement is required.

---

## Initial Vehicle Focus

The initial automotive knowledge and diagnostic support will focus on:

- Toyota
- Volkswagen Golf
- Honda
- Audi
- Mercedes-Benz

The system can later be expanded to additional manufacturers and models.

---

## AI Mechanic

The platform includes a virtual AI diagnostic assistant:

**Virtual Senior Automotive Diagnostic Mechanic — 15+ Years Simulated Experience**

The AI assists with:

- Understanding customer symptoms
- Asking targeted questions
- Identifying relevant vehicle systems
- Finding possible causes
- Searching technical knowledge
- Reviewing previous diagnostic information
- Preparing workshop diagnostic suggestions
- Summarising evidence
- Supporting technician decision-making

The AI must clearly distinguish between:

- Confirmed
- Highly likely
- Possible
- Unknown / requires inspection

The AI must not claim that a physical fault has been confirmed without appropriate workshop evidence.

---

## Customer Journey

The main customer journey is:

```text
Customer
   ↓
AI Customer Chat
   ↓
Customer Record
   ├── PostgreSQL
   └── CRM
   ↓
Vehicle Record
   ↓
AI Pre-Inspection Diagnostic
   ↓
Booking
   ↓
Vehicle Arrives
   ↓
Physical Inspection
   ↓
Confirmed Diagnosis
   ↓
Repair Requirements
   ↓
Quote
   ↓
Customer Approval
   ↓
Repair
   ↓
Post-Repair Quality Check
   ↓
Final Diagnostic / Test
   ↓
Resolved?
   ├── No → Re-Diagnose → Repair
   └── Yes
        ↓
Job Completed
        ↓
Invoice
        ↓
Payment
        ↓
Service History
        ↓
Customer Handover
        ↓
Thank-You Email
        ↓
Follow-Up