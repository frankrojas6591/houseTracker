# RecordAgent — Common Records Service

**Version:** 1.0
**Date:** June 2026
**Scope:** All lifeTracker discipline agents

---

## 1. Purpose

RecordAgent is the **shared records infrastructure** for the entire lifeTracker ecosystem. Every discipline agent (houseAgent, emotionalAgent, estateAgent, faithAgent, medicalAgent, moneyAgent) reads and writes through RecordAgent. No agent accesses the filesystem directly.

RecordAgent has four responsibilities:

1. **Create and own the records directory tree** — the `records/agents/` subtree for every agent namespace. Creates the full tree on first run; agents read/write only their own directory via the RecordAgent interface.
2. **Provide the sole read/write/git-push interface** — discipline expertise builds up in the correct agent over time rather than scattering across the codebase. File I/O, path management, and git commits are concentrated here.
3. **Maintain the documents index** — every document (PDF, photo, note) registered with its local path, type, date, external custodian, and owning agent.
4. **Apply cross-disciplne records best practices** — knows what records a well-run life management system should have, flags gaps, and advises on retention.

---

## 2. UANS Namespace

RecordAgent operates under the `life.core.records` UANS identifier.

```
life.core.records
```

| Segment | Value | Meaning |
|---|---|---|
| `life` | always `life` | top-level ecosystem namespace |
| `core` | always `core` | infrastructure category (not a discipline agent) |
| `records` | always `records` | this service |

All discipline agent data lives under the `records/agents/<namespace>/` subtree. The namespace is the first segment of each agent's UANS (e.g., `house`, `medical`, `money`).

---

## 3. Records Directory Structure

Each discipline agent family owns a top-level subdirectory under `records/agents/` identified by its UANS namespace. Within that namespace, the directory layout mirrors the agent's `<category>/<agent>` segments exactly.

```
lifeTracker-data/
├── records/
│   └── agents/
│       ├── house/                    ← houseAgent namespace
│       │   ├── core/
│       │   │   ├── records/          ← house.core.records
│       │   │   ├── profile/          ← house.core.profile
│       │   │   └── comm/             ← house.core.comm
│       │   ├── systems/
│       │   │   ├── hvac/             ← house.systems.hvac
│       │   │   ├── electrical/       ← house.systems.electrical
│       │   │   ├── plumbing/         ← house.systems.plumbing
│       │   │   ├── roofing/          ← house.systems.roofing
│       │   │   ├── security/         ← house.systems.security
│       │   │   └── appliances/       ← house.systems.appliances
│       │   ├── designs/
│       │   │   ├── architecture/     ← house.designs.architecture
│       │   │   ├── landscaping/      ← house.designs.landscaping
│       │   │   └── interior/         ← house.designs.interior
│       │   ├── finance/
│       │   │   ├── budget/           ← house.finance.budget
│       │   │   ├── tax/              ← house.finance.tax
│       │   │   └── investment/       ← house.finance.investment
│       │   └── life/
│       │       └── accessibility/    ← house.life.accessibility
│       │
│       ├── medical/                  ← medicalAgent namespace
│       │   ├── health/
│       │   │   ├── profile/          ← medical.health.profile
│       │   │   ├── conditions/       ← medical.health.conditions
│       │   │   └── medications/      ← medical.health.medications
│       │   ├── vitals/
│       │   │   ├── labs/             ← medical.vitals.labs
│       │   │   ├── bp/               ← medical.vitals.bp
│       │   │   └── cpap/             ← medical.vitals.cpap
│       │   └── care/
│       │       ├── appointments/     ← medical.care.appointments
│       │       └── directives/       ← medical.care.directives
│       │
│       ├── money/                    ← moneyAgent namespace
│       │   ├── accounts/
│       │   │   └── registry/         ← money.accounts.registry
│       │   ├── transactions/
│       │   │   └── log/              ← money.transactions.log
│       │   └── planning/
│       │       ├── rmd/              ← money.planning.rmd
│       │       └── runway/           ← money.planning.runway
│       │
│       ├── estate/                   ← estateAgent namespace
│       │   ├── assets/
│       │   │   └── registry/         ← estate.assets.registry
│       │   ├── legal/
│       │   │   └── documents/        ← estate.legal.documents
│       │   └── planning/
│       │       └── runway/           ← estate.planning.runway
│       │
│       ├── emotional/                ← emotionalAgent namespace
│       │   ├── core/
│       │   │   └── checkin/          ← emotional.core.checkin
│       │   ├── grief/
│       │   │   └── companion/        ← emotional.grief.companion
│       │   └── legacy/
│       │       └── review/           ← emotional.legacy.review
│       │
│       └── faith/                    ← faithAgent namespace
│           ├── core/
│           │   └── practice/         ← faith.core.practice
│           ├── examen/
│           │   └── reflection/       ← faith.examen.reflection
│           └── legacy/
│               └── ethical_will/     ← faith.legacy.ethical_will
│
└── documents/                        ← not committed to Git; filesystem only
    ├── house/
    │   ├── legal/
    │   ├── inspection/
    │   ├── insurance/
    │   ├── plumbing/
    │   ├── electrical/
    │   ├── hvac/
    │   ├── roofing/
    │   ├── structural/
    │   └── financial/
    ├── medical/
    │   ├── labs/
    │   ├── imaging/
    │   ├── insurance/
    │   └── directives/
    ├── money/
    │   ├── statements/
    │   └── tax/
    ├── estate/
    │   ├── legal/
    │   └── policies/
    └── faith/
        └── documents/
```

### 3.1 Directory Ownership Rules

| Rule | Detail |
|---|---|
| **One agent per directory** | Every JSON file belongs to exactly one agent — the sole writer |
| **Read via interface** | Other agents may read any record via the RecordAgent query interface but never write outside their own directory |
| **Path derives from UANS** | `records/agents/<namespace>/<category>/<agent>/` — no exceptions, no aliases |
| **RecordAgent creates the tree** | On first run, RecordAgent provisions every `action_items.json` file and the full directory skeleton |
| **Documents are filesystem only** | Physical files (PDFs, photos) go under `documents/` — not committed to Git. Metadata and event entries go into the owning agent's JSON — committed to Git |

---

## 4. Universal Agent Naming Schema — Records Layer

RecordAgent is the physical implementation of the UANS. The four-segment name maps to a path automatically:

```
<namespace>.<category>.<agent>.<record>
       ↓          ↓        ↓        ↓
records/agents/<namespace>/<category>/<agent>/<record>.json
```

**Examples across all disciplines:**

| UANS Identifier | Meaning | File Path |
|---|---|---|
| `house.systems.hvac.maintenance_log` | HVAC maintenance history | `records/agents/house/systems/hvac/maintenance_log.json` |
| `house.core.records.legal_records` | House legal records index | `records/agents/house/core/records/legal_records.json` |
| `medical.health.conditions.current` | Active conditions list | `records/agents/medical/health/conditions/current.json` |
| `medical.vitals.labs.history` | Lab results history | `records/agents/medical/vitals/labs/history.json` |
| `money.planning.rmd.schedule` | RMD calendar | `records/agents/money/planning/rmd/schedule.json` |
| `estate.assets.registry.current` | Asset registry | `records/agents/estate/assets/registry/current.json` |
| `emotional.core.checkin.log` | Daily emotional check-in log | `records/agents/emotional/core/checkin/log.json` |
| `faith.examen.reflection.log` | Ignatian Examen reflection log | `records/agents/faith/examen/reflection/log.json` |

---

## 5. RecordAgent Interface

All discipline agents call RecordAgent methods — never the filesystem directly.

```python
# Read a record
record = record_agent.read("medical.health.conditions.current")

# Write a record (auto-commits and pushes to git)
record_agent.write("house.systems.hvac.maintenance_log", updated_log)

# Append an event to a log
record_agent.append_event("emotional.core.checkin.log", new_entry)

# Register a document (metadata only — file already copied to documents/)
record_agent.register_document({
    "doc_id":      "deed-001",
    "namespace":   "house",
    "file":        "documents/house/legal/Deed.pdf",
    "type":        "deed",
    "date":        "2023-01-19",
    "custodian":   "Hays County Clerk",
    "owner_agent": "house.core.records"
})

# Query the documents index
docs = record_agent.find_documents(namespace="medical", type="lab_report")

# Get action items across all agents or one namespace
items = record_agent.get_action_items(namespace="house")
```

Every `write()` and `append_event()` call results in a git commit + push if `auto_push=true` in the RecordAgent config. This implements git-as-master records: the git history IS the audit trail.

---

## 6. Documents Index

Every physical file under `documents/` is registered in `documents_index.json` at the namespace root.

```json
{
  "documents": [
    {
      "doc_id":      "deed-001",
      "namespace":   "house",
      "file":        "documents/house/legal/Deed.pdf",
      "type":        "deed",
      "date":        "2023-01-19",
      "custodian":   "Hays County Clerk (authoritative — local is a copy)",
      "owner_agent": "house.core.records"
    },
    {
      "doc_id":      "lab-bmp-20260115",
      "namespace":   "medical",
      "file":        "documents/medical/labs/20260115-BMP.pdf",
      "type":        "lab_report",
      "date":        "2026-01-15",
      "custodian":   "ARC (Epic patient portal)",
      "owner_agent": "medical.vitals.labs"
    }
  ]
}
```

**Filename convention (enforced on ingest):** `YYYYMMDD-<ShortDescription>.<ext>`

---

## 7. Action Items Schema

Every agent directory contains an `action_items.json` file. RecordAgent provides a unified view across all agents.

```json
{
  "action_items": [
    {
      "item_id":     "house-hvac-001",
      "agent":       "house.systems.hvac",
      "priority":    "high",
      "created":     "2026-06-01",
      "due":         "2026-09-01",
      "title":       "Schedule pre-season A/C service",
      "description": "Unit is 12 years old — coil cleaning and refrigerant check before summer peak",
      "status":      "open"
    },
    {
      "item_id":     "medical-meds-001",
      "agent":       "medical.health.medications",
      "priority":    "medium",
      "created":     "2026-06-15",
      "due":         "2026-07-01",
      "title":       "Refill thyroid prescription",
      "status":      "open"
    }
  ]
}
```

---

## 8. Git-as-Master Records

The `lifeTracker-data/` repository is a **private Git repo** (`frankrojas6591/lifeTracker-data`). Every write through RecordAgent results in a commit. Physical documents (`documents/`) are excluded via `.gitignore` — only JSON records are committed.

```
# lifeTracker-data/.gitignore
documents/
```

**Config:**

```json
{
  "record_agent": {
    "data_repo":   "~/GDrive/dev/pyTrackers/lifeTracker-data",
    "auto_push":   true,
    "remote":      "git@github.com-fxr:frankrojas6591/lifeTracker-data.git",
    "commit_msg_prefix": "[RecordAgent]"
  }
}
```

The git history IS the audit trail. Every change to every agent's records is timestamped, attributed, and recoverable.

---

## 9. Implementation Plan

| Phase | Title | Depends On |
|---|---|---|
| [#1](https://github.com/frankrojas6591/lifeTracker/issues/1) | RecordAgent: Phase 0 — Bootstrap Directory Tree | — |
| [#2](https://github.com/frankrojas6591/lifeTracker/issues/2) | RecordAgent: Phase 1 — Read/Write/Git Interface | #1 |
| [#3](https://github.com/frankrojas6591/lifeTracker/issues/3) | RecordAgent: Phase 2 — Documents Index + Action Items API | #1, #2 |
| [#4](https://github.com/frankrojas6591/lifeTracker/issues/4) | RecordAgent: Phase 3 — Cross-Agent Query Interface | #2, #3 |

Phase 0 builds the full directory tree for all six agent namespaces and creates empty `action_items.json` stubs. Discipline agents can be built in any order after Phase 0.

---

## Appendix A — Per-Discipline Expert Perspective

The records schema for each discipline is designed from the combined perspective of the domain's professional standards:

| Discipline | What it demands of records |
|---|---|
| **houseAgent** | Systems documented with make/model/serial/install date; permits and legal records; cost basis maintained from day one; official custodian tracked for every legal document |
| **medicalAgent** | FHIR R4 resource types (Patient, Condition, Observation, MedicationStatement); lab history with reference ranges; provider directory; advance directives |
| **moneyAgent** | Double-entry Beancount structure; RMD schedule with Uniform Lifetime Table divisors; account registry with beneficiary designations; tax-lot tracking for step-up basis |
| **estateAgent** | 7 legal pillars (RLT, Pour-Over Will, DPOA, POLST, TODD, Beneficiary Designations, Letter of Instruction); FMV and cost basis for every asset; step-up eligibility flags |
| **emotionalAgent** | Daily entries with mood score, PERMA subscores, cognitive patterns, crisis flag; grief task progression; no PII in record bodies (de-identified keys only) |
| **faithAgent** | Liturgical context on every entry (season, feast, lectionary cycle); consolation/desolation score; sacramental history milestones; ethical will versioned over time |

---

## Appendix B — houseAgent Records Reference

The original house-specific records design (JSON schemas, custodian map, migration map from GDrive, and discipline agent ownership table) is maintained in:

```
houseAgent/docs/design/houseRecords/houseRecordsData.md
```

That document remains authoritative for house-specific schemas. RecordAgent is the infrastructure layer; houseAgent defines what goes in it.
