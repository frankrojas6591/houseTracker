# moneyAgent Vision

*My Personal Assistant Ecosystem — One Trusted Advisor/Advocate backed by Expert Agents*

**Version:** 0.2 (Design Draft)
**Author:** Frank Rojas
**Date:** June 2026
**Parent:** [lifeTracker Vision](../../docs/lifeTrackerVision.md)
**UANS namespace:** `money.*`

---

## 1. Why a Money Tracker?

Personal finance for a retired individual in their 70s is not about accumulation — it is about **sequencing, preservation, and distribution**. The decisions that matter most are:

- In what order do I draw from taxable, IRA, and Roth accounts to minimize lifetime taxes?
- Am I taking the right RMD amount and timing?
- Can I afford the HVAC replacement without disrupting my retirement income?
- Is my Medicare coverage and premium cost optimized?
- Will the money last?

Most personal finance tools are built for accumulators. They optimize savings rates, track spending categories, and show net worth trending up. For a 70-year-old, the optimization is inverted: the goal is sustainable withdrawal while preserving optionality, managing tax brackets, and protecting against late-life care costs.

The **moneyAgent** is purpose-built for this life stage. It tracks all personal accounts (not business — that is llcRentalTracker), models the retirement runway, manages the RMD calendar, and feeds the estateAgent with the authoritative account view.

---

## 2. Senior Finance Framework

The key financial management domains for a 70s-retired profile, in priority order:

### 2.1 Required Minimum Distributions (RMDs)

- **Mandatory at age 73** (SECURE 2.0 Act). Applies to: traditional IRA, 401k, 403b, SEP-IRA.
- **Roth IRA**: no lifetime RMD — a key estate planning lever.
- **Penalty for shortfall**: 25% excise tax (reduced to 10% if corrected within 2 years).
- **RMD cascade**: RMD amount increases annual MAGI → affects Social Security taxability (up to 85%), IRMAA Medicare surcharges, and LTCG bracket.
- **Action**: moneyAgent calculates each year's RMD per account, tracks distributions, and alerts if underdistributed.

### 2.2 IRMAA / Medicare Premium Management

Medicare Part B and D surcharges (IRMAA) are triggered by MAGI from **two years prior**. The 2026 surcharges kick in at $106K (single). A large IRA withdrawal or Roth conversion in 2024 shows up as a 2026 IRMAA bill.

moneyAgent tracks projected MAGI annually and surfaces IRMAA risk before the year that causes it.

### 2.3 Withdrawal Sequencing

The optimal withdrawal order reduces lifetime tax burden:

1. **Taxable accounts** (capital gains rates; step-up basis reduces estate tax)
2. **Traditional IRA / 401k** (ordinary income; must take RMDs in any case)
3. **Roth IRA** (tax-free; preserve for last — or for heirs)

**Key lever**: Roth conversions in years when income is low (before RMDs, after Social Security deferral, during market downturns) permanently reduce future RMD burden and create tax-free inheritance.

### 2.4 Bucket Strategy

Three-bucket approach buffers against sequence-of-returns risk:

| Bucket | Time Horizon | Allocation | Purpose |
|---|---|---|---|
| **Cash** | 0–2 years | HYSA / T-Bills | Living expenses; never invested; immune to market |
| **Conservative** | 3–7 years | Bonds / dividend stocks | Replenishes cash; low volatility |
| **Growth** | 8+ years | Equities | Long-term growth; rides out downturns |

Replenishment rule: refill Cash from Conservative annually if Conservative has gained; refill Conservative from Growth in strong years.

### 2.5 Social Security

Track monthly gross amount, taxability percentage (0%, 50%, or 85% based on combined income), and COLA adjustments. Social Security income is a factor in IRMAA and bracket calculations.

### 2.6 Long-Term Care / Medicare Supplement

Track premiums, coverage details, and deductible/copay structure for:
- Medicare Part A, B, D
- Medicare Supplement (Medigap) policy
- Long-term care insurance (if any) — premium, benefit period, elimination period, daily benefit

---

## 3. Accounting Core — Beancount

**[Beancount](https://beancount.io)** is the open-source Python double-entry accounting system used as the moneyAgent's ledger core. It is:
- pip-installable (`pip install beancount`)
- Fully scriptable via Python API (`beancount.loader`)
- Paired with **Fava** for a web-based ledger view
- Used by personal finance practitioners for estate settlement, tax prep, and portfolio analysis

Beancount provides the auditable double-entry foundation. The moneyAgent agent layer sits on top, reading/writing Beancount journal entries as the source of truth and maintaining JSON summaries for the agent interface and cross-agent consumption.

---

## 4. Account Aggregation

### 4.1 OFX/QFX File Import (Primary)

Banks and brokerages (Chase, Schwab, Vanguard, Fidelity) offer OFX/QFX download from their web portals. Parse with `ofxparse` (Python library). Zero API cost, no authentication complexity, works with any institution.

```bash
pip install ofxparse
```

**Recommended cadence**: monthly download and import for all accounts.

### 4.2 Plaid (Optional — Live Balances)

[Plaid Python SDK](https://github.com/plaid/plaid-python) for live balance queries. First 200 calls/month free; ~$0.10–0.60/call thereafter. Use selectively — for real-time liquidity checks when houseAgent needs a budget approval or estateAgent needs a snapshot.

### 4.3 Retirement Account Aggregation

Schwab, Vanguard, and Fidelity each offer CSV/OFX download of holdings, transactions, and cost basis. For retirement accounts:
- Download holdings monthly → `balance_history.json`
- Download transactions quarterly → Beancount journal entry
- Track cost basis per lot for taxable accounts (critical for step-up basis planning)

---

## 5. Retirement Runway Modeling

### 5.1 Owl Retirement Planner

[Owl](https://github.com/mdlacasse/Owl) (`pip install owlplanner`) is the strongest open-source Python tool for this problem:

- **Linear programming optimizer** (SciPy) — finds the withdrawal sequence that minimizes lifetime taxes, not just a simulation
- **RMD-aware**: calculates required distributions per IRS Uniform Lifetime Table
- **Roth conversion analysis**: identifies optimal conversion amounts and timing
- **IRMAA bracket management**: models Medicare surcharges based on projected income
- **Monte Carlo + historical backtesting**: 10,000 scenarios using historical return distributions
- **Mortality tables**: SSA/VBT/RP-2014 — not a fixed end date
- **All 50 state taxes**: models state income tax alongside federal

**Key outputs**: P50/P90 portfolio survival age; annual spending ceiling; recommended Roth conversion amount; RMD calendar for all accounts.

### 5.2 In-House Monte Carlo (NumPy)

For quick scenario runs — "what if I spend $10K more/year?" — a simple NumPy-based Monte Carlo (10,000 scenarios, historical return distribution) provides a portfolio survival probability in seconds. Complement to Owl's optimizer.

---

## 6. Agent Catalog

### 6.1 AccountRegistry Agent (`money.accounts.registry`)
Master list of all personal financial accounts with type, institution, tax status, and beneficiary. Source of truth for estateAgent's asset view.

### 6.2 TransactionLog Agent (`money.accounts.transactions`)
Ingests OFX/QFX files and categorizes transactions by expense type. Feeds monthly spending report to PersonalAssistant. Tracks income events (Social Security, distributions from llcRentalTracker).

### 6.3 BalanceHistory Agent (`money.accounts.balances`)
Monthly snapshots of all account balances and net worth (assets minus liabilities). Feeds estateAgent's net worth history.

### 6.4 RMDCalendar Agent (`money.rmd.calendar`)
Calculates each year's RMD per traditional IRA/401k account. Tracks distributions. Alerts in Q4 if remaining RMD is underdistributed. Models multi-year RMD trajectory.

### 6.5 RunwayModel Agent (`money.finance.runway`)
Runs Owl's linear programming optimizer and Monte Carlo quarterly. Outputs spending ceiling, Roth conversion recommendation, IRMAA risk assessment. Feeds estateAgent.

### 6.6 IncomeTracker Agent (`money.income.sources`)
Tracks all income sources: Social Security (monthly, taxability), LLC distributions (from llcRentalTracker events), investment income, RMD withdrawals. Projects annual MAGI for IRMAA and tax planning.

### 6.7 InsurancePremiums Agent (`money.insurance.premiums`)
Tracks Medicare A/B/D premiums, Medigap supplement, long-term care insurance — premium amounts, coverage details, and review dates. Feeds medicalAgent with coverage context.

---

## 7. Records Structure — UANS

```
money.*
└── records/agents/
    ├── accounts/
    │   ├── registry/           ← money.accounts.registry
    │   │   ├── account_registry.json
    │   │   └── action_items.json
    │   ├── transactions/       ← money.accounts.transactions
    │   │   ├── log.json        (rolling 13 months; annual archives)
    │   │   └── action_items.json
    │   └── balances/           ← money.accounts.balances
    │       ├── history.json    (monthly snapshots; append-only)
    │       └── action_items.json
    ├── rmd/
    │   └── calendar/           ← money.rmd.calendar
    │       ├── schedule.json
    │       └── action_items.json
    ├── finance/
    │   └── runway/             ← money.finance.runway
    │       ├── model_output.json
    │       └── action_items.json
    ├── income/
    │   └── sources/            ← money.income.sources
    │       ├── sources.json
    │       ├── events.json     (income received events)
    │       └── action_items.json
    └── insurance/
        └── premiums/           ← money.insurance.premiums
            ├── policies.json
            └── action_items.json
```

### Key JSON Schemas

```json
// money.accounts.registry
{
  "accounts": [
    {
      "account_id":    "ira_schwab_001",
      "type":          "traditional_ira",
      "institution":   "Schwab",
      "tax_status":    "tax_deferred",
      "owner":         "primary",
      "beneficiary_primary":    "trust",
      "beneficiary_contingent": "daughter",
      "rmd_eligible":  true,
      "last_updated":  "2026-06-01"
    },
    {
      "account_id":  "roth_schwab_001",
      "type":        "roth_ira",
      "institution": "Schwab",
      "tax_status":  "tax_free",
      "rmd_eligible": false
    }
  ]
}

// money.rmd.calendar
{
  "rmd_schedule": [
    {
      "year":                   2026,
      "account_id":             "ira_schwab_001",
      "prior_year_end_balance": 485000,
      "age_at_year_end":        74,
      "uniform_divisor":        25.5,
      "rmd_required":           19020,
      "distributed_ytd":        10000,
      "remaining":              9020,
      "deadline":               "2026-12-31"
    }
  ]
}

// money.income.sources
{
  "sources": [
    {
      "source_id":     "ss_primary",
      "type":          "social_security",
      "monthly_gross": 2340,
      "taxable_pct":   0.85,
      "cola_annual":   0.025
    },
    {
      "source_id":  "llc_distribution",
      "type":       "business_distribution",
      "source":     "llcRentalTracker",
      "annual_est": 24000
    }
  ]
}
```

---

## 8. Cross-Agent Integration

| Agent | What moneyAgent Sends | What It Receives |
|---|---|---|
| **estateAgent** | Monthly account balance snapshot; net worth; cost basis per account | None (estateAgent reads) |
| **houseAgent** | HELOC balance; available cash reserves for project approval | Project cost estimates (for budget check) |
| **medicalAgent** | HSA balance; insurance premium schedule | Care cost events; HSA-eligible expenses |
| **llcRentalTracker** | None | K-1 distribution events (income received → `money.income.sources`) |
| **PersonalAssistant** | Monthly spending summary; MAGI projection; runway P50/P90 | Monthly review request |

**Integration event bus**: llcRentalTracker writes a distribution event to a shared events directory; moneyAgent reads and records it as income.

---

## 9. Open-Source Reference Projects

| Project | Role |
|---|---|
| [Beancount](https://beancount.io) | Double-entry accounting core; pip-installable; Fava web UI |
| [mdlacasse/Owl](https://github.com/mdlacasse/Owl) | Retirement runway optimizer; RMDs, Roth conversion, Monte Carlo |
| [jbms/finance-dl](https://github.com/jbms/finance-dl) | Auto-downloads from Schwab, Vanguard, Chase via Selenium |
| [mbafford/plaid-sync](https://github.com/mbafford/plaid-sync) | Plaid → SQLite CLI for live balance sync |
| [ofxparse](https://pypi.org/project/ofxparse/) | Python OFX/QFX parser for bank/brokerage file imports |

---

## 10. Design Principles

1. **Sequencing over accumulation.** The primary goal is tax-efficient withdrawal over the owner's lifetime — not growing the portfolio. Every agent output should frame decisions in terms of sequencing impact.

2. **RMD is the spine.** The RMD calendar drives income, IRMAA, and estate tax exposure. It must be visible and current at all times.

3. **Roth is the most valuable underused asset.** Most seniors with Roth IRAs are too conservative about conversion timing. The RunwayModel agent surfaces every Roth conversion opportunity — a missed conversion window is a real cost to heirs.

4. **moneyAgent never writes into other trackers.** It is a source of truth for financial data. Other trackers pull from it; it does not push.

5. **OFX import before Plaid.** Manual monthly OFX downloads are zero-cost, institution-agnostic, and require no ongoing API authentication. Start there. Add Plaid only when live balance queries provide clear value.

---

## 11. Implementation Plan

| Phase | Milestone |
|---|---|
| 0 | Records scaffold; account registry manually populated |
| 1 | OFX/QFX import pipeline; TransactionLog running; monthly spending visible |
| 2 | BalanceHistory — monthly snapshots; net worth calculable |
| 3 | RMDCalendar — all RMD-eligible accounts registered; 2026 RMD calculated and tracked |
| 4 | IncomeTracker — Social Security and LLC distributions captured; MAGI projection available |
| 5 | RunwayModel — Owl integrated; P50/P90 survival; Roth conversion recommendation |
| 6 | estateAgent integration — balance snapshots and net worth fed on schedule |
| 7 | PersonalAssistant integration — monthly financial summary in life review |
