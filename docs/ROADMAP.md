# AI Automotive Platform — Development Roadmap

## Phase 1 — Foundation

- [x] Create project workspace
- [x] Create project folders
- [x] Create architecture document
- [x] Create README
- [ ] Create development roadmap
- [ ] Verify local development environment

---

## Phase 2 — Local AI

- [ ] Install/verify Ollama
- [ ] Verify Ollama service
- [ ] Download a suitable local AI model
- [ ] Test local model from PowerShell
- [ ] Connect Python to Ollama
- [ ] Connect n8n to Ollama
- [ ] Test structured AI responses

---

## Phase 3 — Database

- [ ] Design PostgreSQL database
- [ ] Create customer table
- [ ] Create vehicle table
- [ ] Create diagnostic case table
- [ ] Create booking table
- [ ] Create inspection table
- [ ] Create diagnosis table
- [ ] Create repair table
- [ ] Create quote table
- [ ] Create customer approval table
- [ ] Create invoice table
- [ ] Create payment table
- [ ] Create service history table
- [ ] Create communication history table

---

## Phase 4 — Knowledge System

- [ ] Install/verify Qdrant
- [ ] Create automotive knowledge collection
- [ ] Create document ingestion process
- [ ] Create document chunking process
- [ ] Create embeddings
- [ ] Store embeddings in Qdrant
- [ ] Build semantic search
- [ ] Connect semantic search to the AI mechanic

---

## Phase 5 — AI Automotive Assistant

- [ ] Create customer conversation workflow
- [ ] Identify customer
- [ ] Identify vehicle
- [ ] Collect symptoms
- [ ] Ask targeted questions
- [ ] Identify relevant vehicle systems
- [ ] Identify possible causes
- [ ] Identify missing information
- [ ] Recommend workshop checks
- [ ] Generate structured pre-inspection diagnostic summary
- [ ] Add diagnostic confidence levels
- [ ] Prevent unsupported confirmed diagnoses
- [ ] Prevent repair quotes during customer chat

---

## Phase 6 — Customer and Vehicle Management

- [ ] Customer registration
- [ ] Customer lookup
- [ ] Vehicle registration
- [ ] Vehicle lookup
- [ ] Vehicle history
- [ ] Previous service history
- [ ] Previous diagnostic history
- [ ] MOT information
- [ ] Customer communication history

---

## Phase 7 — Workshop Booking

- [ ] Workshop availability
- [ ] Service booking
- [ ] Diagnostic booking
- [ ] Repair booking
- [ ] Booking confirmation
- [ ] Customer notifications
- [ ] Calendar integration

---

## Phase 8 — Physical Inspection and Diagnosis

- [ ] Retrieve pre-inspection case
- [ ] Present AI diagnostic summary
- [ ] Record physical inspection
- [ ] Record diagnostic trouble codes
- [ ] Record test results
- [ ] Record measurements
- [ ] Record technician observations
- [ ] AI evidence analysis
- [ ] Establish supported diagnosis
- [ ] Determine repair requirements

---

## Phase 9 — Quotes and Customer Approval

- [ ] Parts lookup
- [ ] Parts pricing
- [ ] Labour calculation
- [ ] Labour rates
- [ ] VAT/tax calculation
- [ ] Generate structured quote
- [ ] Send quote to customer
- [ ] Customer approval
- [ ] Record approval
- [ ] Create work order

The AI must not invent financial values.

---

## Phase 10 — Repair and Quality Control

- [ ] Record repair work
- [ ] Record parts fitted
- [ ] Record technician notes
- [ ] Post-repair inspection
- [ ] Test drive where appropriate
- [ ] Final diagnostic checks
- [ ] Compare results with original complaint
- [ ] Determine whether issue is resolved

If unresolved:

```text
Re-diagnose
    ↓
Additional repair
    ↓
Quality check