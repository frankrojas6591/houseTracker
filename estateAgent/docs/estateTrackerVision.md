# estateAgent Vision

*My Personal Assistant Ecosystem — One Trusted Advisor/Advocate backed by Expert Agents*

**Version:** 0.2 (Design Draft)
**Author:** Frank Rojas
**Date:** June 2026
**Parent:** [lifeTracker Vision](../../docs/lifeTrackerVision.md)
**UANS namespace:** `estate.*`

---

## 1. Why an Estate Tracker?

An estate is everything a person owns and owes — and everything that will pass from them when they die. For most people, the estate is never actually managed. Documents are signed and filed away. Beneficiary designations are set at account opening and never reviewed. Net worth is a number the accountant produces once a year. The plan exists on paper but is never stress-tested against reality.

The **estateAgent** makes the estate visible and active. It aggregates every asset from every tracker, models the retirement runway, tracks document currency, and surfaces the decisions that must be made before they become emergencies.

> Estate planning is not a one-time event. It is a continuous process of matching your assets, your intentions, and your documents — and verifying they are all pointing at the same outcome.

The stakes at 70 are specific: the 2026 estate tax exemption is $15M/person. The step-up in basis at death can eliminate decades of capital gains. The §121 exclusion shelters $250K of gain on a primary residence sale. These are real leverage points — but only for those who track them.

---

## 2. Legal Framework — The Seven Pillars

A complete personal estate requires seven legal instruments. The estateAgent tracks the status, date, and currency of each.

| Instrument | Purpose | Review Trigger |
|---|---|---|
| **Revocable Living Trust (RLT)** | Holds real estate and investments; avoids probate; assets step up at death | Any major asset change; every 5 years |
| **Pour-Over Will** | Catches assets not in trust at death; ensures nothing falls through | With any trust amendment |
| **Durable Power of Attorney** | Financial decisions if incapacitated; critical while alive, superseded by trust at death | Every 3-5 years or when agent changes |
| **Advance Healthcare Directive / POLST** | Medical decisions and end-of-life care preferences | Any major health change; annually after 70 |
| **Transfer on Death Deed (TODD)** | Transfers real property directly to heir — no probate, §121 exclusion intact | When primary beneficiary changes |
| **Beneficiary Designations** | Retirement accounts and life insurance — supersede the will and trust | At account opening and after any family event |
| **Letter of Instruction** | Non-legal; locates all assets, accounts, contacts, passwords; the document that actually helps heirs | Updated annually |

---

## 3. Asset Categories

### 3.1 Asset Registry

| Category | Examples | Source Agent |
|---|---|---|
| **Primary residence** | Home FMV, mortgage balance, equity, TODD status | houseAgent |
| **Traditional IRA / 401k** | Balance, institution, beneficiary, RMD status | moneyAgent |
| **Roth IRA** | Balance, institution, beneficiary (no RMD lifetime) | moneyAgent |
| **Taxable brokerage** | Balance, cost basis by lot (critical for step-up planning) | moneyAgent |
| **LLC business equity** | Estimated equity, K-1 distributions YTD, depreciation recapture exposure | llcRentalTracker |
| **Life insurance CSV** | Cash surrender value, death benefit, beneficiary | moneyAgent |
| **Personal property** | Vehicles, jewelry, collectibles — valued items only | Manual entry |
| **Digital assets** | Crypto, domain names, subscriptions — and how to access them | Manual entry |

### 3.2 Liabilities

| Category | Examples |
|---|---|
| Mortgage / HELOC | Source from houseAgent |
| Credit lines | Source from moneyAgent |
| Tax obligations | Estimated capital gains exposure on appreciated assets |

---

## 4. Tax Mechanics — The Three Levers

### 4.1 Step-Up in Basis

At death, all estate assets receive a new cost basis equal to their fair market value on the date of death. A home purchased for $200K worth $900K at death passes to heirs with a $900K basis — the $700K gain is permanently eliminated.

**Tracking requirement:** Every appreciating asset needs a recorded cost basis. Without it, heirs cannot calculate the step-up.

### 4.2 §121 Exclusion

$250K of gain on the sale of a primary residence is excluded from tax (single filer). This exclusion:
- Applies through a properly structured revocable trust (§121(d)(9))
- Applies through a TODD with specific trust beneficiary conditions
- Requires 24 months of primary residence use in the 60 months prior to sale

**Tracking requirement:** Acquisition date, cost basis, any capital improvements (from houseAgent), and months of primary residence use.

### 4.3 Estate Tax Threshold (2026+)

The One Big Beautiful Bill Act raised the estate tax exemption to $15M/person permanently (up from $13.99M in 2025). For most individuals, estate tax is not a current concern. Track cumulative gifts + projected estate value against this threshold annually.

---

## 5. Retirement Runway Modeling

The central question of the estate's financial health: **will the money last?**

### 5.1 Owl Retirement Planner

[Owl](https://github.com/mdlacasse/Owl) (`pip install owlplanner`) is the best open-source Python tool for this problem. It uses:
- **Mixed-integer linear programming** (scipy) for optimal withdrawal sequencing — not just simulation
- **SSA/VBT/RP-2014/IAM-2012 mortality tables** for realistic longevity modeling
- **Tax-aware modeling**: RMDs, Roth conversions, bracket management, IRMAA thresholds, Social Security taxability
- **Monte Carlo + historical backtesting** for portfolio survival probabilities

### 5.2 Key Model Inputs (70s Single Person)

| Input | Value to Track |
|---|---|
| Portfolio balance | IRA + Roth + taxable, monthly snapshot |
| Annual spend baseline | From moneyAgent actual spending |
| Healthcare cost inflation | 5–7%/yr for senior care; apply over longevity range |
| Longevity range | P50 = 85, P90 = 92 (SSA 2026 tables) |
| Long-term care trigger | Age estimate + cost range ($5K–$10K/month) |
| Social Security income | Monthly amount, taxability % |
| LLC distributions | Annual K-1 income from llcRentalTracker |

### 5.3 Withdrawal Sequencing

The standard order (taxable → traditional IRA → Roth) should be reviewed against:
- Roth conversions in low-income years (reduces future RMD burden and creates tax-free inherited assets)
- IRMAA bracket management (Medicare premium surcharges triggered by MAGI two years prior)
- 0% LTCG bracket (applies up to ~$47K AGI single, 2026)

---

## 6. Agent Catalog

### 6.1 AssetRegistry Agent (`estate.assets.registry`)
Maintains the complete asset and liability ledger. Pulls snapshots from all source trackers on schedule. Calculates net worth on demand.

### 6.2 DocumentVault Agent (`estate.documents.vault`)
Tracks all legal instruments: type, date signed, attorney, physical location, digital file path, and next review date. Alerts when documents are due for review or when a life event suggests a review.

### 6.3 BeneficiaryManager Agent (`estate.legal.beneficiaries`)
Tracks beneficiary designations per account. Alerts when a family event (death, divorce, birth) suggests a review. Verifies that trust beneficiaries are correctly designated as primary or contingent.

### 6.4 RunwayModel Agent (`estate.finance.runway`)
Runs the retirement runway model using Owl. Updated quarterly. Outputs: P50/P90 portfolio survival age, recommended annual spending ceiling, Roth conversion opportunity analysis, RMD calendar.

### 6.5 TaxPlanner Agent (`estate.finance.tax`)
Tracks the tax mechanics: step-up basis eligibility for all assets, §121 exclusion status for primary residence, capital gains exposure on taxable accounts, cumulative gifts against $15M threshold.

### 6.6 NetWorthHistory Agent (`estate.finance.networth`)
Append-only time series of net worth. Monthly snapshot aggregated from all source trackers. Surfaces trend and anomaly detection.

---

## 7. Records Structure — UANS

```
estate.*
└── records/agents/
    ├── assets/
    │   └── registry/              ← estate.assets.registry
    │       ├── asset_registry.json
    │       ├── liability_log.json
    │       └── action_items.json
    ├── documents/
    │   └── vault/                 ← estate.documents.vault
    │       ├── document_vault.json
    │       └── action_items.json
    ├── legal/
    │   └── beneficiaries/         ← estate.legal.beneficiaries
    │       ├── beneficiary_table.json
    │       └── action_items.json
    └── finance/
        ├── runway/                ← estate.finance.runway
        │   ├── runway_model.json
        │   ├── rmd_schedule.json
        │   └── action_items.json
        ├── tax/                   ← estate.finance.tax
        │   ├── basis_registry.json
        │   ├── sect121_log.json
        │   ├── gifts_log.json
        │   └── action_items.json
        └── networth/              ← estate.finance.networth
            ├── history.json
            └── action_items.json
```

### Key JSON Schema: `estate.assets.registry`

```json
{
  "assets": [
    {
      "asset_id":         "home_kingsway",
      "type":             "real_estate",
      "name":             "177 Kingsway Dr",
      "source_tracker":   "houseAgent",
      "fmv":              850000,
      "cost_basis":       335000,
      "acquisition_date": "2022-12-31",
      "titling":          "revocable_trust",
      "beneficiary_id":   "ben_001",
      "step_up_eligible": true,
      "sect121_eligible": true,
      "residence_months_last5yrs": 36,
      "last_updated":     "2026-06-01"
    }
  ],
  "liabilities": [
    {
      "liability_id": "heloc_001",
      "type":         "heloc",
      "creditor":     "Chase",
      "balance":      0,
      "secured_by":   "home_kingsway"
    }
  ]
}
```

---

## 8. Cross-Agent Integration

| Agent | What estateAgent Receives | What It Sends |
|---|---|---|
| **houseAgent** | FMV, mortgage balance, equity, TODD status, capital improvements log | None (reader only) |
| **moneyAgent** | All account balances, cost basis, RMD status, income sources | None (reader only) |
| **llcRentalTracker** | LLC equity, K-1 distributions YTD, depreciation recapture exposure | None (reader only) |
| **medicalAgent** | Longevity P50/P90, long-term care cost projection, advance directive status | Long-term care funding need (to runway model) |
| **faithAgent** | Ethical will draft, charitable bequest intentions | None (reader only) |
| **PersonalAssistant** | Net worth trend, document review alerts, runway health | Annual estate summary; document expiry alerts |

estateAgent is **read-only from all source agents** — it aggregates but never writes into sibling agents.

---

## 9. Open-Source Reference Projects

| Project | Relevance |
|---|---|
| [mdlacasse/Owl](https://github.com/mdlacasse/Owl) | Python retirement planner; RMD + Roth conversion + Monte Carlo + tax-aware |
| [slavhate/legacy-vault](https://github.com/slavhate/legacy-vault) | Self-hosted estate document vault; dead man's switch; JSON schema reference |
| [Ghostfolio](https://ghostfol.io) | Privacy-first open-source wealth management; Angular/NestJS; net worth dashboard reference |
| [Wealthfolio](https://wealthfolio.app) | Offline cross-platform asset tracker; net worth + portfolio analysis |
| [beancount.io](https://beancount.io) | Double-entry plaintext accounting; used by estate executors for estate settlement accounting |

---

## 10. Design Principles

1. **The estate is a system, not a document.** A signed trust is not an estate plan — it is one component. The estateAgent holds the full system view: assets, documents, beneficiaries, and the runway model all together.

2. **estateAgent reads; trackers write.** Every number in the estate view is sourced from the tracker that owns it. estateAgent never maintains its own copy of the home value or the IRA balance — it pulls the authoritative source.

3. **Step-up basis is the most undertracked high-value number in most estates.** Track it for every appreciated asset. It should be visible at all times.

4. **Beneficiary designations supersede everything.** A will means nothing for a retirement account if the beneficiary form says otherwise. The BeneficiaryManager agent exists specifically because this is the most common and most costly estate mistake.

5. **The runway model is a living document.** Run it quarterly, not annually. A market drop, an unexpected medical expense, or a policy change can shift the P90 survival age significantly. Surface changes immediately.

---

## 11. Implementation Plan

| Phase | Milestone |
|---|---|
| 0 | Records scaffold — UANS directory tree, stub JSON files |
| 1 | AssetRegistry — manual entry for all current assets with cost basis |
| 2 | DocumentVault — log all existing legal instruments with review dates |
| 3 | NetWorthHistory — aggregate from houseAgent + moneyAgent snapshots |
| 4 | RunwayModel — embed Owl for RMD calendar and P50/P90 survival modeling |
| 5 | TaxPlanner — step-up basis registry, §121 tracking, Roth conversion analysis |
| 6 | PersonalAssistant integration — annual estate summary; document review alerts surfaced to monthly check-in |
