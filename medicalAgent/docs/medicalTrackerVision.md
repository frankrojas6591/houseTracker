# medicalAgent Vision

*My Personal Assistant Ecosystem — One Trusted Advisor/Advocate backed by Expert Agents*

**Version:** 0.3 (Design Draft — supersedes initial design doc)
**Author:** Frank Rojas
**Date:** June 2026
**Parent:** [lifeTracker Vision](../../docs/lifeTrackerVision.md)
**UANS namespace:** `medical.*`

---

## 1. Why a Medical Tracker?

A person who has lived to their 70s has accumulated decades of medical history distributed across dozens of doctors, labs, portals, and paper files. That history lives in the heads of physicians who have retired, in MyChart portals that don't talk to each other, in a "health folder" that contains a hopgepodge of test results and discharge summaries, and in the owner's own memory — the least reliable archive of all.

The **medicalAgent** is the institutional memory of one person's health. It knows every condition, every medication, every lab result trend, every specialist, every test, and every care preference. It is not a doctor. It is the one entity that has read everything and remembers all of it — so that when you walk into an appointment, you are not starting from scratch.

> A personalized medical tracker is, in the deepest sense, one and the same with the individual. It is the individual — because it has incorporated all knowledge about every aspect of their health. As the individual changes, so does the tracker.

The specific mission for a person in their 70s: know this individual at a very deep level, and advocate for and counsel them through every medical event and condition until end of life.

---

## 2. Clinical Data Model — FHIR R4

The **HL7 FHIR R4** (4.0.1) standard is the canonical clinical data model. It is what Epic MyChart exposes via API, what Apple Health uses internally, and what the 21st Century Cures Act mandates for patient data portability. The medicalAgent does not run a FHIR server — it stores a local JSON subset modeled on FHIR field names so that future import/export from any Epic/MyChart source is trivial.

### Core FHIR Resources Tracked

| FHIR Resource | Purpose |
|---|---|
| `Patient` | Demographics, identifiers, emergency contacts |
| `Condition` | Active and resolved diagnoses (ICD-10 coded) |
| `Observation` | Labs, vitals, wearable data, CPAP metrics |
| `MedicationStatement` | Current and historical medications |
| `AllergyIntolerance` | Drug, food, and environment allergies |
| `Immunization` | Vaccines with dates and manufacturers |
| `DiagnosticReport` | Radiology, pathology, specialty reports |
| `Appointment` | Visit history and upcoming schedule |
| `Consent` | Advance directives, POLST, DNR preferences |
| `Device` | CPAP machine, CGM, hearing aids |
| `CarePlan` | Goals, care team, and "Matters Most" preferences |

---

## 3. Frank Rojas — Current Health Profile

*This section is initialized from existing records and updated as conditions change.*

| Field | Current Value |
|---|---|
| **Age** | 68 (b. 1957) |
| **Height / Weight** | 6'0" / 299 lbs |
| **Primary Care** | Austin Regional Clinic (ARC) — Epic/MyChart |
| **Insurance** | IBM Post-Retirement UHC Advantage Medicare |
| **Active Conditions** | Venous insufficiency (bilateral, confirmed 2025); hearing loss (bilateral, 2022/2025); sleep apnea (CPAP); thyroid condition; urology (2026); hypertension (BP tracking active) |
| **Existing Data Assets** | `frankrojas_labHistory.json`, `BloodPressure.xlsx`, `Providers.json`, CPAP data, urology/thyroid notebooks |

### Priority Lab Panel

| Test | Target / Flag Threshold | Why Critical |
|---|---|---|
| **HbA1c** | ≤7.0% (non-frail senior) | Pre-diabetes/T2D given weight; drives diet, medication, and kidney care decisions |
| **eGFR** | Flag if <60 mL/min/1.73m² | Kidney function — determines safe medication dosing |
| **UACR** | Flag if >30 mg/g | Cardiovascular mortality marker; early kidney damage indicator |
| **Lipid panel** | LDL, HDL, TG, AIP ratio | Atherosclerosis risk, statin efficacy |
| **TSH / Free T4** | Per endocrinology targets | Active thyroid tracking |
| **PSA** | Per urology guideline | Active urology tracking |
| **Blood pressure** | Systolic <130 (AHA target) | Already tracked in `BloodPressure.xlsx` — highest priority ingest |
| **CBC / CMP / Vit D / B12** | Age-appropriate reference ranges | Comprehensive senior baseline panel |

---

## 4. Geriatric Framework — The 5M's

The **5M's of Geriatric Medicine** (Tinetti, Huang & Molnar, 2017; Age-Friendly Health Systems) provide the organizing clinical lens. Every major agent decision references the 5M's:

| M | Domain | Key Data | Agent Behavior |
|---|---|---|---|
| **Mind** | Cognition + mental health | MMSE/MoCA scores, PHQ-9 depression screen, cognitive event notes | Alert on change patterns; link to emotionalAgent |
| **Mobility** | Fall risk, physical function | Gait assessment, fall history, venous insufficiency status, PT notes, exercise log | Mobility decline → houseAgent accessibility alert |
| **Medications** | Polypharmacy safety | Full medication list; Beers Criteria review; drug interaction flags | Run Beers check at each medication change; alert on age-inappropriate drugs |
| **Multi-complexity** | Comorbidity burden | Conditions list with ICD-10, active/inactive, treating specialist | Show comorbidity interaction map; flag when conditions affect each other |
| **Matters Most** | Patient goals and values | Advance directive, POLST, care preferences, personal goal statements | Surface at appointment prep; feed advance spiritual care directive from faithAgent |

---

## 5. Agent Catalog

### 5.1 PersonProfile Agent (`medical.core.profile`)
The master person record — demographics, providers, insurance, emergency contacts, blood type, allergies. The "Patient" resource in FHIR terms. All other agents reference this as the person anchor.

### 5.2 ConditionsLog Agent (`medical.health.conditions`)
Tracks all diagnoses — active and resolved — with ICD-10 code, onset date, specialist, and status. Displays the comorbidity map and flags when conditions interact (e.g., kidney function limits metformin use for pre-diabetes).

### 5.3 MedicationsManager Agent (`medical.health.medications`)
Complete medication list: name, generic, dose, frequency, route, prescriber, start/stop dates, indication. Runs **Beers Criteria** checks for age-inappropriate medications on each change. Tracks polypharmacy threshold (>5 medications is a flag).

### 5.4 LabsTracker Agent (`medical.labs.results`)
Ingests lab results from MyChart FHIR API or manual CSV/JSON import. Stores each test result with LOINC code, value, unit, reference range, flag (normal/low/high/critical), and ordering provider. Shows trends over time for tracked panels.

### 5.5 VitalsMonitor Agent (`medical.vitals.monitor`)
Tracks blood pressure, weight, glucose, SpO2, heart rate. Sources: manual entry, ARC MyChart, Apple Health export, wearables. `BloodPressure.xlsx` is the first ingest. Surfaces trends and anomaly flags (e.g., sustained hypertension above target).

### 5.6 CPAPMonitor Agent (`medical.devices.cpap`)
Pulls CPAP session data from ResMed myAir API (`resmed_myair_sensors`) or from SD card via OSCAR export. Tracks AHI, usage minutes, mask leak, and pressure settings. AHI > 5 on consecutive nights triggers an alert.

### 5.7 AppointmentLog Agent (`medical.appointments.log`)
Tracks past and upcoming appointments: provider, specialty, date, type, reason, notes, and follow-up actions. Generates appointment prep summaries (recent labs, medication changes, open questions) via the LLM layer.

### 5.8 DirectivesKeeper Agent (`medical.directives.advance`)
Tracks advance healthcare directive, POLST, DNR preferences, healthcare proxy designation, and organ donor status. Links to faithAgent's advance spiritual care directive. Surfaces to estateAgent for estate plan currency.

### 5.9 FiveMsAssessment Agent (`medical.geriatrics.fivems`)
Maintains the structured 5M's assessment as a sub-document updated at major health events or annually. The primary signal source for cross-agent integration (mobility → houseAgent, mind → emotionalAgent, Matters Most → faithAgent + estateAgent).

---

## 6. Records Structure — UANS

```
medical.*
└── records/agents/
    ├── core/
    │   └── profile/                ← medical.core.profile
    │       ├── person_profile.json
    │       ├── providers.json
    │       ├── allergies.json
    │       └── action_items.json
    ├── health/
    │   ├── conditions/             ← medical.health.conditions
    │   │   ├── conditions.json
    │   │   └── action_items.json
    │   └── medications/            ← medical.health.medications
    │       ├── medications.json
    │       └── action_items.json
    ├── labs/
    │   └── results/                ← medical.labs.results
    │       ├── lab_history.json    (seeded from frankrojas_labHistory.json)
    │       ├── immunizations.json
    │       └── action_items.json
    ├── vitals/
    │   └── monitor/                ← medical.vitals.monitor
    │       ├── vitals_log.json     (seeded from BloodPressure.xlsx)
    │       └── action_items.json
    ├── devices/
    │   └── cpap/                   ← medical.devices.cpap
    │       ├── sessions.json
    │       └── action_items.json
    ├── appointments/
    │   └── log/                    ← medical.appointments.log
    │       ├── appointments.json
    │       └── action_items.json
    ├── directives/
    │   └── advance/                ← medical.directives.advance
    │       ├── directives.json
    │       └── action_items.json
    └── geriatrics/
        └── fivems/                 ← medical.geriatrics.fivems
            ├── assessment.json
            └── action_items.json
```

### Key JSON Schema: `medical.health.medications`

```json
{
  "medications": [
    {
      "med_id":        "uuid",
      "name":          "Metformin",
      "generic_name":  "Metformin HCl",
      "dose":          "500mg",
      "frequency":     "twice daily",
      "route":         "oral",
      "prescriber":    "Dr. Smith, ARC Endocrinology",
      "start_date":    "2024-03-15",
      "end_date":      null,
      "indication":    "Pre-diabetes",
      "beers_flag":    false,
      "notes":         "Hold if eGFR < 30"
    }
  ],
  "polypharmacy_flag": false,
  "med_count":         4,
  "last_beers_review": "2026-06-01"
}
```

### Key JSON Schema: `medical.geriatrics.fivems`

```json
{
  "assessment_date": "2026-06-27",
  "mind": {
    "phq9_score": 3,
    "phq9_date":  "2026-03-01",
    "cognitive_events": [],
    "cognitive_anxiety_flag": false
  },
  "mobility": {
    "fall_risk_level": "moderate",
    "last_fall_date":  null,
    "assistive_device": null,
    "venous_insufficiency_active": true,
    "pt_active": false,
    "exercise_frequency_per_week": 2
  },
  "medications": {
    "med_count": 4,
    "polypharmacy_flag": false,
    "beers_issues": []
  },
  "multi_complexity": {
    "active_condition_count": 5,
    "specialist_count": 4,
    "conditions": ["venous_insufficiency","hearing_loss","sleep_apnea","thyroid","hypertension"]
  },
  "matters_most": {
    "goals": ["maintain independence at home", "stay active", "manage weight"],
    "care_preferences": "Prefer to age in place; discuss all options before any procedure",
    "directives_complete": false
  }
}
```

---

## 7. FHIR API Access — Epic MyChart (ARC)

### 7.1 fhirclient Python Library

```bash
pip install fhirclient  # v4.4.0, released Feb 2026; FHIR R4 + SMART on FHIR OAuth
```

**SMART on FHIR patient standalone launch flow:**
1. Redirect to ARC MyChart authorization URL (Epic FHIR endpoint)
2. Patient authenticates with 2FA (required — cannot be fully automated headless)
3. Token exchange → access token + refresh token
4. Pull all relevant resources in one session

**Resources accessible via ARC/Epic FHIR:**
`Patient`, `Condition`, `Observation` (labs + vitals), `MedicationRequest`, `AllergyIntolerance`, `Immunization`, `Appointment`, `DiagnosticReport`, `DocumentReference`

### 7.2 Priority Ingest Sequence

1. **`frankrojas_labHistory.json`** → `medical.labs.results` — richest existing asset; seed the lab history
2. **`BloodPressure.xlsx`** → `medical.vitals.monitor` — BP time series; highest clinical value
3. **`Providers.json`** → `medical.core.profile.providers` — existing structured data
4. **Epic FHIR API pull** — Observation (labs), MedicationRequest, Condition, Appointment
5. **CPAP data** — ResMed myAir API or OSCAR SD card export

---

## 8. CPAP Integration

ResMed AirSense data can be pulled via:

| Option | Tool | Notes |
|---|---|---|
| **myAir API** (undocumented) | [resmed_myair_sensors](https://github.com/prestomation/resmed_myair_sensors) | Python; pulls AHI, usage min, mask on/off, mask leak; real-time |
| **SD card + OSCAR** | [OSCAR](https://www.sleepfiles.com/OSCAR/) | Desktop CPAP analysis app; reads SD card; export to CSV/JSON for ingest |
| **cpap-monitor** | [eimi-codes/cpap-monitor](https://github.com/eimi-codes/cpap-monitor) | Python app; tracks device maintenance; syncs from myAir; JSON/YAML export |

**Key metrics tracked per session:**
- AHI (events/hour) — target: <5
- Total usage minutes — target: ≥4 hours
- Mask leak rate (L/min)
- Pressure settings (EPAP/IPAP or APAP range)
- Obstructive / central / hypopnea event counts

---

## 9. AI / LLM Layer

### 9.1 Health Literacy Layer (NOT Diagnosis)

The LLM's role is **health literacy and navigation** — not clinical diagnosis:
- Explain lab results in plain language
- Generate appointment prep summaries (recent changes, open questions for the doctor)
- Surface relevant context when answering health questions
- Translate medical notes into understandable summaries

### 9.2 OpenMed — Local Clinical AI

[OpenMed](https://openmed.life) is an open-source Python + Swift runtime for local clinical AI across 13 biomedical domains. Privacy-preserving (on-device). Use for medication interaction checks and lab trend interpretation without sending data to external APIs.

### 9.3 RAG Architecture

```
frankrojas_labHistory.json  →  ChromaDB local vector index
BloodPressure.xlsx          →  (time-series; separate index)
conditions.json             →
medications.json            →

Query: "How has my blood pressure trended this year?"
→ Retrieve relevant vitals records from ChromaDB
→ Inject into Claude API context
→ Return plain-language trend summary
```

---

## 10. Cross-Agent Integration

| Agent | What medicalAgent Sends | What It Receives |
|---|---|---|
| **emotionalAgent** | Diagnosis events, medication changes, procedure/surgery dates, hospitalization — all elevate depression/anxiety risk | PHQ-9 score, mood trend (mental health → physical health link) |
| **houseAgent** | Mobility decline flag, fall event, new diagnosis affecting physical function (venous insufficiency, balance issues) | Accessibility modifications completed |
| **estateAgent** | Longevity P50/P90 estimate, long-term care cost projection, advance directive status | None |
| **moneyAgent** | HSA-eligible expense events, insurance premium amounts, out-of-pocket tracking | HSA balance, insurance coverage details |
| **faithAgent** | None directly | Advance spiritual care directive (priest at death, last rites preference) |
| **PersonalAssistant** | Monthly health summary (conditions, medications, upcoming appointments, 5M's alert) | Cross-agent event stream (for context in health queries) |

---

## 11. Design Principles

1. **This is the individual's own record, not the doctor's.** The medicalAgent holds what the individual knows, believes, and has experienced — including things not in any EHR. It supplements the clinical record; it does not replace it.

2. **FHIR R4 field names as the schema.** Using FHIR field names for local JSON records means zero translation work when importing from or exporting to any Epic/MyChart-compatible system.

3. **The 5M's are the clinical lens, not a checkbox.** The 5M's assessment is a living document, not a one-time intake form. It updates at every major health event and drives the cross-agent integration signals.

4. **Labs are a time series, not a snapshot.** One HbA1c reading is a data point. Five readings over three years is a trend. medicalAgent stores every result and surfaces the trend, not just the latest.

5. **CPAP data is a vital sign.** AHI and usage are as important as blood pressure for a person with sleep apnea. They belong in the vitals layer with daily tracking.

6. **Advance directives are first-class records.** The DirectivesKeeper agent exists because these documents are most commonly missing when they are most urgently needed.

---

## 12. Implementation Plan

| Phase | Milestone |
|---|---|
| 0 | Records scaffold — UANS directory tree, stub JSON files |
| 1 | Seed from existing data: `frankrojas_labHistory.json` → `labs/results`; `BloodPressure.xlsx` → `vitals/monitor`; `Providers.json` → `core/profile/providers` |
| 2 | ConditionsLog + MedicationsManager — back-fill from memory and MyChart PDF summaries |
| 3 | Epic FHIR API pull — authenticate once; pull Observation, MedicationRequest, Condition, Appointment |
| 4 | CPAPMonitor — wire resmed_myair_sensors or OSCAR export; AHI trending visible |
| 5 | 5M's Assessment — initial structured assessment; Beers Criteria check on medication list |
| 6 | DirectivesKeeper — advance healthcare directive drafted; POLST preferences documented |
| 7 | LLM layer — RAG over health history; appointment prep summaries; lab trend explanations |
| 8 | Cross-agent integration — mobility alerts to houseAgent; health events to emotionalAgent; longevity model to estateAgent |
