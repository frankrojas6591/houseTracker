# HouseRecords Agent — Data Design

**Version:** 0.3
**Date:** June 2026
**Parent:** [Design Index](../houseMgrAgent.md)

---

## 1. Agent Responsibilities

The HouseRecords agent is the **institutional memory of the property**. It has three jobs:

1. **Store and track all existing records** — every document, invoice, photo, and event, indexed so any other agent can retrieve context about the house without scanning the filesystem.
2. **Track where official records live** — deed, title, surveys, permits, homestead exemption, and insurance policies each have an authoritative external location; the agent knows both the local file path and the official custodian.
3. **Apply property management best practices** — the agent is the on-call expert in five disciplines: construction, real estate, legal, finance, and database services. It knows what records a well-run property should have, flags gaps, and advises on retention.
4. **Keeper of Per Agent Data** — HouseRecords creates and owns the `records/agents/` directory tree. Every discipline agent stores its knowledge and action items under its own subdirectory; HouseRecords provides the single read/write/git-push interface all agents use. No agent reads or writes its own files directly — it calls HouseRecords. This concentrates file I/O, path management, and git commits in one place, ensuring discipline expertise builds up in the correct agent over time rather than scattering across the codebase.

Every other agent (HVAC, Plumbing, Financing, etc.) reads and writes through HouseRecords. No agent accesses the filesystem directly.

---

## 2. Multi-Discipline Expert Perspective

The schema is designed from the combined perspective of five disciplines a professional property manager must master:

| Discipline | What it demands of records |
|---|---|
| **Construction** | Every system documented with make/model/serial/install date; inspection reports preserved; before-and-after photos for each repair; pipe diagrams and floor plans as first-class records |
| **Real Estate** | Cost basis maintained from day one (purchase price + every capital improvement); deed, title insurance, and survey all current and filed; market comparables tracked over time |
| **Legal** | Permits pulled for every permitted work item; easements and encroachments documented; neighbor disputes logged with dates and communications; homestead exemption status current |
| **Finance** | Insurance policy history with claim log; property tax assessments vs. actual payments; capital improvements separated from maintenance for IRS purposes; warranty expiration calendar |
| **Database** | Normalized entities (property, systems, events, contractors, documents) with stable IDs; no duplication; every document in the index with path + external custodian; consistent `YYYYMMDD-` filename prefix |

---

## 3. Official Records Custodian Map

Best-practice property management requires knowing not just where the local file is, but who holds the authoritative original.

| Record | Local File | External Custodian |
|---|---|---|
| Deed | `documents/legal/Deed.pdf` | Hays County Clerk (recorded) |
| Title Insurance | `documents/legal/20230201-TitleInsurance.pdf` | Title company; insured policy is permanent |
| Survey (current) | `documents/legal/Survey-2014.pdf` | Original surveyor + county records |
| Homestead Exemption | `documents/legal/20230501-HomesteadExemption.pdf` | Hays CAD parcel R33204 — verify annually at `esearch.hayscad.com` |
| Property Tax | `documents/legal/20240329-PropTaxPayment.pdf` | Hays CAD — `esearch.hayscad.com/Property/View/R33204` |
| HUD Settlement | `documents/legal/20230117-HUD_Settlement_Statement.pdf` | Lender archive; IRS requires 7 years |
| Home Inspection | `documents/inspection/Inspection_Report_177_Kingsway.pdf` | Owner — no external registry |
| Insurance Policy | `documents/insurance/20230110-HomeIns.pdf` | Carrier |
| Sellers Disclosure | `documents/legal/20221106-SellersDisclosureNotice.pdf` | Owner — retain permanently |

---

## 4. Records Directory Structure

Each discipline agent owns a subdirectory under `records/agents/`. HouseRecords creates the tree; agents read/write only their own directory via the HouseRecords interface.

```
houseTracker-data/kingsway_dr/
├── records/
│   └── agents/
│       ├── house_records/        ← property-wide index (HouseRecords agent)
│       │   ├── legal_records.json
│       │   ├── insurance.json
│       │   ├── utilities.json
│       │   ├── contractors.json
│       │   ├── documents_index.json
│       │   └── action_items.json
│       ├── house_profile/        ← House Profile agent
│       │   ├── house_profile.json
│       │   └── action_items.json
│       ├── communication/        ← Communication agent
│       │   ├── check_in_log.json
│       │   └── action_items.json
│       ├── architecture/         ← Architecture agent
│       │   ├── floor_plan.json
│       │   ├── structural_notes.json
│       │   └── action_items.json
│       ├── security_safety/      ← Security & Safety agent
│       │   ├── systems.json
│       │   └── action_items.json
│       ├── accessibility/        ← Accessibility agent
│       │   ├── assessment.json
│       │   └── action_items.json
│       ├── hvac/                 ← HVAC agent
│       │   ├── systems.json
│       │   ├── maintenance_log.json
│       │   └── action_items.json
│       ├── electrical/           ← Electrical agent
│       │   ├── panel.json
│       │   ├── circuits.json
│       │   ├── maintenance_log.json
│       │   └── action_items.json
│       ├── plumbing/             ← Plumbing agent
│       │   ├── systems.json
│       │   ├── sewer_diagram.json
│       │   ├── maintenance_log.json
│       │   └── action_items.json
│       ├── roofing/              ← Roofing agent
│       │   ├── systems.json
│       │   ├── maintenance_log.json
│       │   └── action_items.json
│       ├── financing/            ← Financing agent
│       │   ├── capital_improvements.json
│       │   ├── budget.json
│       │   └── action_items.json
│       ├── tax/                  ← Tax agent
│       │   ├── basis_log.json
│       │   └── action_items.json
│       ├── investment/           ← Investment agent
│       │   ├── valuation.json
│       │   └── action_items.json
│       ├── appliances/           ← Appliances agent
│       │   ├── registry.json
│       │   ├── maintenance_log.json
│       │   └── action_items.json
│       ├── landscaping/          ← Landscaping agent
│       │   ├── site_map.json
│       │   ├── maintenance_log.json
│       │   └── action_items.json
│       └── decoration/           ← Decoration agent
│           ├── rooms.json
│           └── action_items.json
└── documents/                    ← not committed to Git; filesystem only
    ├── legal/
    ├── inspection/
    ├── insurance/
    ├── plumbing/
    │   └── photos/
    ├── electrical/
    ├── hvac/
    ├── roofing/
    ├── structural/
    │   └── 20250215-LivingKitchenFloors/
    ├── outdoor/
    ├── financial/
    └── neighbor/
```

### 4.1 Agent Records Ownership

Every JSON file belongs to exactly one agent. The owning agent is the sole writer; other agents may read via HouseRecords query interface but never write outside their own directory.

| Agent | Records Dir | Owned JSON Files |
|---|---|---|
| HouseRecords | `agents/house_records/` | legal_records · insurance · utilities · contractors · documents_index · action_items |
| House Profile | `agents/house_profile/` | house_profile · action_items |
| Communication | `agents/communication/` | check_in_log · action_items |
| Architecture | `agents/architecture/` | floor_plan · structural_notes · action_items |
| Security & Safety | `agents/security_safety/` | systems · action_items |
| Accessibility | `agents/accessibility/` | assessment · action_items |
| HVAC | `agents/hvac/` | systems · maintenance_log · action_items |
| Electrical | `agents/electrical/` | panel · circuits · maintenance_log · action_items |
| Plumbing | `agents/plumbing/` | systems · sewer_diagram · maintenance_log · action_items |
| Roofing | `agents/roofing/` | systems · maintenance_log · action_items |
| Financing | `agents/financing/` | capital_improvements · budget · action_items |
| Tax | `agents/tax/` | basis_log · action_items |
| Investment | `agents/investment/` | valuation · action_items |
| Appliances | `agents/appliances/` | registry · maintenance_log · action_items |
| Landscaping | `agents/landscaping/` | site_map · maintenance_log · action_items |
| Decoration | `agents/decoration/` | rooms · action_items |

---

## 5. Best Practices Flagged for KingswayDr

From the current GDrive analysis, the HouseRecords agent should raise these action items on first audit:

| Gap | Discipline | Action |
|---|---|---|
| No permits on file for electrical work (2024) or floor repair (2025) | Legal/Construction | Confirm whether permits were pulled; obtain copies from Hays County if so |
| Capital improvements log missing | Finance/Legal | Create `capital_improvements.json`; back-fill floor repair (2025) and any other qualifying work |
| Roof metal decking (2016) — pre-purchase, no install details | Construction | Extract make/model/warranty from invoice; add to systems_registry |
| Sewer layout is "spaghetti" (owner description) | Construction | Populate `sewer_diagram.json` from the matplotlib notebook; add cleanout locations |
| Homestead exemption — verify it remains active each year | Finance/Legal | Check Hays CAD R33204 annually; add to check-in calendar |
| No current survey (2014 survey is 12 years old) | Real Estate/Legal | Consider updated survey, especially given neighbor dispute history |
| Prior water loss claim (2021-07-28, $13K) on insurance history | Finance | 5-year lookback period expires 2026-07-28; affects insurance premiums |
| Hot tub surface damage (chemical roughness noted) | Construction | Document current state; schedule refinishing assessment |
| Pier-to-slab conversion — researched 2023, not decided | Construction | Record as open project in Architecture agent; link research notebooks |

---

## 6. Implementation Plan

| Issue | Title | Depends On |
|---|---|---|
| [#1](https://github.com/frankrojas6591/houseTracker/issues/1) | houseRecords: Phase 0 — Bootstrap Records | — |
| [#2](https://github.com/frankrojas6591/houseTracker/issues/2) | houseRecords: Phase 1 — Migrate KingswayDr Files | #1 |
| [#3](https://github.com/frankrojas6591/houseTracker/issues/3) | houseRecords: Phase 2 — Agent Query Interface | #1, #2 |

---

## Appendix A — JSON Schemas by Agent Owner

Schemas are grouped by the agent that owns them. Each agent is the sole writer of its files; other agents read via the HouseRecords interface. As each discipline agent gets its own design doc, its schemas migrate there; this appendix serves as the canonical reference until then.

---

### A.1 HouseRecords Agent — `agents/house_records/`

#### `legal_records.json`

```json
{
  "deed": {
    "file":          "documents/legal/Deed.pdf",
    "recorded_with": "Hays County Clerk",
    "record_date":   "2023-01-19",
    "grantee":       "Frank Rojas"
  },
  "title_insurance": {
    "file":           "documents/legal/20230201-TitleInsurance.pdf",
    "commitment_file":"documents/legal/20230105-CommitmentForTitleInsurance_T-7.pdf"
  },
  "surveys": [
    { "date": "1979-01-01", "type": "Plat",   "file": "documents/legal/Survey-1979Plat.tiff" },
    { "date": "1985-01-01", "type": "Survey", "file": "documents/legal/Survey-1985.pdf" },
    { "date": "2014-01-01", "type": "Survey", "file": "documents/legal/Survey-2014.pdf",
      "notes": "Most recent — use for boundary disputes" }
  ],
  "homestead_exemption": {
    "status":     "active",
    "county":     "Hays",
    "parcel_id":  "R33204",
    "filed_date": "2023-05-01",
    "file":       "documents/legal/20230501-HomesteadExemptionForm.pdf"
  },
  "permits": [],
  "easements": [],
  "neighbor_disputes": [
    { "neighbor": "D", "log_file": "documents/neighbor/HistoryOfEventsWithNeighborD.gdoc", "status": "documented" }
  ],
  "sellers_disclosure": {
    "file":  "documents/legal/20221106-SellersDisclosureNotice.pdf",
    "notes": "Retain permanently"
  }
}
```

#### `insurance.json`

```json
{
  "current": {
    "file":  "documents/insurance/20230110-HomeIns.pdf",
    "notes": "April 2025 quotes compared in HomeInsurance notebook"
  },
  "claims": [
    { "date": "2021-07-28", "type": "water loss", "paid": 13000,
      "notes": "Prior owner claim. 5-year lookback expires 2026-07-28." }
  ],
  "history": [
    { "carrier": "Choice Home Warranty", "type": "home warranty",
      "start": "2022-01-10", "end": "2025-04-02", "cancelled": true,
      "file": "documents/insurance/20250402-Cancel-ChoiceHomeWarranty.pdf" }
  ]
}
```

#### `utilities.json`

```json
{
  "utilities": [
    { "utility_id": "electricity", "provider": "PEC", "account": "3000789437", "phone": "888-554-4732" },
    { "utility_id": "water", "provider": "Wimberley Water Supply Corp", "phone": "512-847-2323",
      "pay_url": "https://payclix.com/wimberleywater",
      "notes": "Pressure regulator installed — line pressure exceeds 100 PSI." },
    { "utility_id": "cable", "provider": "Spectrum" },
    { "utility_id": "waste", "provider": "Texas Waste" }
  ]
}
```

#### `contractors.json`

```json
{
  "contractors": [
    { "contractor_id": "casa_lago_inspection", "name": "Casa Lago Home Inspections & Mold Consultants",
      "contact": "Casey Herbert", "license": "TREC #24484", "phone": "830-200-9098",
      "email": "crherber1@gmail.com", "specialty": "home inspection, mold", "last_used": "2022-11-13" },
    { "contractor_id": "wimberley_plumbing", "name": "Wimberley Plumbing",
      "specialty": "plumbing", "last_used": "2022-12-06" },
    { "contractor_id": "atex_spa", "name": "A-Tex (Spa Service)",
      "contact": "Joseph Polvado", "phone": "512-508-9702", "specialty": "hot tub / spa service" },
    { "contractor_id": "new_braunfels_pool", "name": "New Braunfels Pool & Spa",
      "contact": "Emalie or Kat", "phone": "830-660-6270", "specialty": "spa chemicals / water chemistry" }
  ]
}
```

---

### A.2 House Profile Agent — `agents/house_profile/`

#### `house_profile.json`

```json
{
  "house_id":     "kingsway_dr",
  "house_name":   "177 Kingsway Dr",
  "address":      "177 Kingsway Dr, Wimberley, TX 78676",
  "county":       "Hays",
  "parcel_id":    "R33204",
  "year_built":   1982,
  "style":        "Ranch — single family",
  "sqft_living":  1232,
  "lot_acres":    0.5,
  "foundation":   "pier-and-beam",
  "sewer":        "septic",
  "water_source": "Wimberley Water Supply Corp",
  "acquisition":  { "date": "2022-12-31", "price": 335000, "method": "cash",
                    "hud_file": "documents/legal/20230117-HUD_Settlement_Statement.pdf" },
  "prior_sale":   { "date": "2014-01-01", "price": 114000 }
}
```

---

### A.3 Plumbing Agent — `agents/plumbing/`

#### `systems.json`

```json
{
  "systems": [
    { "system_id": "septic", "name": "Septic Tank", "capacity_gal": 1000,
      "last_pumped": "2026-06-21", "recommended_interval_yrs": 3,
      "notes": "Complex drain layout — see sewer_diagram.json.",
      "files": ["documents/plumbing/photos/"] },
    { "system_id": "water_softener", "name": "Water Softener / Filtration",
      "files": ["documents/plumbing/Water_Softener_Filtration.gdoc"] }
  ]
}
```

#### `sewer_diagram.json`

```json
{
  "diagram_version": "2026-06",
  "source_file":     "documents/plumbing/kingswaySewer2D.ipynb",
  "description":     "Top-view drain line layout. Pier-and-beam — pipes accessible from crawl space.",
  "nodes": [
    { "id": "o1", "label": "Kitchen Sink drain",       "connects_to": "y1" },
    { "id": "o2", "label": "Guest Bath Sink drain",    "connects_to": "y1" },
    { "id": "t1", "label": "Master Bath Tub drain",    "connects_to": "main" },
    { "id": "t2", "label": "Guest Bath Tub drain",     "connects_to": "y2" },
    { "id": "T1", "label": "Master Bath Toilet drain", "connects_to": "main" },
    { "id": "T2", "label": "Guest Bath Toilet drain",  "connects_to": "y2" },
    { "id": "y1", "label": "T-connector (kitchen+sink)","connects_to": "main" },
    { "id": "y2", "label": "T-connector (guest bath)", "connects_to": "main" },
    { "id": "main","label": "Main drain → Septic",     "connects_to": "septic" }
  ],
  "known_issues": "K.Sink and G.Tub share drain through y1. Clog at y1 backs up both. Snake from cleanout, not from fixture."
}
```

#### `maintenance_log.json`

```json
{
  "events": [
    { "event_id": "plumb-001", "date": "2022-12-06", "type": "repair",
      "description": "Post-inspection plumbing repairs — major pipe opening found",
      "contractor_id": "wimberley_plumbing",
      "invoice_file": "documents/plumbing/20221210-PlumbingInvoice_7284.pdf" },
    { "event_id": "plumb-002", "date": "2024-10-21", "type": "maintenance",
      "description": "Septic maintenance",
      "files": ["documents/plumbing/20241021-SepticMaintenance.gdoc"] },
    { "event_id": "plumb-003", "date": "2026-06-21", "type": "repair",
      "description": "K.Sink and G.Tub backup. Tank pumped. G.Tub and M.Tub lines snaked.",
      "files": ["documents/plumbing/20260522-PlumbingService_Kingsway.gdoc",
                "documents/plumbing/photos/20260523-KSinkCleanout.png"] }
  ]
}
```

---

### A.4 Financing Agent — `agents/financing/`

#### `capital_improvements.json`

```json
{
  "purchase_basis": 335000,
  "improvements": [
    { "date": "2025-02-15",
      "description": "Living room and kitchen floor replacement (structural beam rot)",
      "cost": null, "is_capital": true, "permit_required": false,
      "notes": "Qualifies as capital improvement, not maintenance repair" }
  ],
  "notes": "Total basis = purchase_basis + sum(improvements.cost). Required at sale."
}
```

---

### A.5 Appliances Agent — `agents/appliances/`

#### `registry.json`

```json
{
  "appliances": [
    { "appliance_id": "hot_tub", "name": "Marquis Spa",
      "make": "Marquis", "model": "VEGA SIL SL CHA", "serial": "0101667",
      "install_date": "2017-09-27", "filter_part": "20342",
      "dealer": "Southern Leisure Spas and Patio", "dealer_phone": "512-240-7727",
      "service_contact": "Joseph Polvado 512-508-9702 (A-Tex)",
      "notes": "Surface roughness from excess shock+bromine. Texas Refinish (210) 903-6990." }
  ]
}
```

---

### A.6 Architecture Agent — `agents/architecture/`

#### `structural_notes.json`

```json
{
  "foundation_type": "pier-and-beam",
  "known_issues": [
    { "date": "2025-02-15", "area": "living room / kitchen",
      "description": "Beam rot discovered during floor replacement",
      "status": "repaired",
      "files": ["documents/structural/20250215-LivingKitchenFloors/"] }
  ],
  "open_projects": [
    { "project": "pier-to-slab conversion", "status": "researched — not approved",
      "files": ["documents/structural/20231113-ConvertToSlab.ipynb"] }
  ]
}
```

---

*Remaining agent schemas (HVAC, Electrical, Roofing, Security, Accessibility, Tax, Investment, Landscaping, Decoration, Communication) follow the same pattern — `systems.json` or domain equivalent + `maintenance_log.json` where applicable + `action_items.json`. Each is defined in its agent's design doc when that agent is built.*

---

## Appendix B — Documents Index Strategy

Every file under `documents/` is registered in `documents_index.json` with its local path, type, date, external custodian, and owning agent.

```json
{
  "documents": [
    {
      "doc_id":      "deed-001",
      "file":        "documents/legal/Deed.pdf",
      "type":        "deed",
      "date":        "2023-01-19",
      "custodian":   "Hays County Clerk (authoritative — local is a copy)",
      "owner_agent": "house_records"
    },
    {
      "doc_id":      "survey-2014",
      "file":        "documents/legal/Survey-2014.pdf",
      "type":        "survey",
      "date":        "2014-01-01",
      "custodian":   "Hays County records + original surveyor",
      "owner_agent": "house_records"
    }
  ]
}
```

**Filename convention (enforced by agent on ingest):** `YYYYMMDD-<ShortDescription>.<ext>`

---

## Appendix C — Migration Map from GDrive

Source: `~/GDrive/Family/Assets/KingswayDr`

Each GDrive item has **two destinations**: the physical file is copied to `documents/` (not committed to Git); the metadata or event entry is written into the owning agent's JSON under `records/agents/` (committed to Git).

| GDrive Source | `→ documents/` | `→ records/agents/` |
|---|---|---|
| `Home Docs/Deed.pdf` | `legal/` | `house_records/legal_records.json` |
| `Home Docs/20221106-SellersDisclosureNotice.pdf` | `legal/` | `house_records/legal_records.json` |
| `Home Docs/Survey-*.pdf / .tiff` | `legal/` | `house_records/legal_records.json` |
| `Home Docs/20230117-HUD Settlement Statement-Final.pdf` | `legal/` | `house_records/legal_records.json` |
| `Home Docs/20230201-TitleInsurance.pdf` | `legal/` | `house_records/legal_records.json` |
| `Home Docs/20221231-Contract-Closing-335k_Cash/` | `legal/` | `house_records/legal_records.json` |
| `20230501-HomesteadExemptionForm.pdf` | `legal/` | `house_records/legal_records.json` |
| `20240329-PropTaxPayment.pdf` | `legal/` | `house_records/legal_records.json` |
| `History of Events with Neighbor D.gdoc` | `neighbor/` | `house_records/legal_records.json` |
| `20221113-Inspection/` (full report) | `inspection/` | `house_records/documents_index.json` |
| `Reciepts/20221112-HomeInspection.pdf` | `inspection/` | `house_records/documents_index.json` |
| `HomeInsurance/` (policy docs) | `insurance/` | `house_records/insurance.json` |
| `Reciepts/20250402-Cancel-Choice Home Warranty.pdf` | `insurance/` | `house_records/insurance.json` |
| `Morg-checklist/` (income, tax, ID docs) | `financial/` | `house_records/documents_index.json` (archive) |
| `Home Docs/20230105-10KLoan-Amplify.pdf` | `financial/` | `house_records/documents_index.json` |
| `HouseMaintainanceReciepts/Plumbing/` (invoices, notes) | `plumbing/` | `plumbing/maintenance_log.json` |
| `HouseMaintainanceReciepts/Plumbing/kingswaySewer2D.ipynb` | `plumbing/` | `plumbing/sewer_diagram.json` *(data extraction — not just file copy)* |
| `HouseMaintainanceReciepts/Plumbing/photos/` | `plumbing/photos/` | `plumbing/maintenance_log.json` (file refs) |
| `HouseMaintainanceReciepts/Water Softner-Filtration.gdoc` | `plumbing/` | `plumbing/systems.json` |
| `HouseMaintainanceReciepts/20241130-ElectricalWork.gdoc` | `electrical/` | `electrical/maintenance_log.json` |
| `HouseMaintainanceReciepts/20160516-AC_Service_*.pdf` | `hvac/` | `hvac/systems.json` |
| `HouseMaintainanceReciepts/20161212-Roof_Metal-decking.pdf` | `roofing/` | `roofing/systems.json` |
| `HouseMaintainanceReciepts/20250215-LivingKitchenFloors/` (photos, notes) | `structural/` | `architecture/structural_notes.json` + `financing/capital_improvements.json` |
| `HomeImprovements/` (window contract, cancelled) | `structural/` | `architecture/structural_notes.json` |
| `PierMorter2Slab/` (research notebooks) | `structural/` | `architecture/structural_notes.json` (open project) |
| `Home Docs/2016-2017 Celebrity Owners Manual.pdf` | `outdoor/` | `appliances/registry.json` |
| `Notebooks/HotTubInfo.ipynb` | `outdoor/` | `appliances/registry.json` |
