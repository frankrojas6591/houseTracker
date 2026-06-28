# lifeTracker — System Vision

**Version:** 1.0 (Design Draft)
**Author:** Frank Rojas
**Date:** June 2026

---

## 1. What lifeTracker Is

**lifeTracker** is the repository for Frank Rojas's personal life management ecosystem. It contains a **Personal Assistant (PA)** orchestrator and six **discipline agents**, each an expert in one domain of life. A single voice call, a single web app, a single shared communication layer.

Design principle: **One tracker, six discipline agents.**

```
lifeTracker/
├── docs/                ← this document, architecture diagrams
├── houseAgent/          ← home manager — systems, maintenance, aging-in-place
├── medicalAgent/        ← health advocate — history, medications, care navigation
├── moneyAgent/          ← financial advisor — accounts, retirement, RMDs
├── estateAgent/         ← estate manager — assets, trusts, succession
├── emotionalAgent/      ← counselor — emotional health, grief, life transitions
├── faithAgent/          ← spiritual advisor — Catholic practice, Examen, community
└── recordAgent/         ← common records service — all agents write through it
```

**What it is NOT:**
- llcRentalTracker — the LLC/rental business manager is a separate repo on the work account (`wbgroupmgr`). It integrates only via narrow API signal.

---

## 2. Why a Personal Assistant at 70

Life in the 70s creates a specific management challenge: the cognitive and logistical load of managing a full life does not decrease with age — it increases. Systems age. Health changes. Estate decisions become urgent. Emotional resilience is tested by loss and transition. Financial complexity grows.

The cost of managing these domains in silos compounds:
- A doctor doesn't know the house is a financial drain.
- The financial planner doesn't know health is declining.
- The home manager doesn't know the estate plan is outdated.
- Missed connections become missed decisions. Missed decisions become crises.

The Personal Assistant fixes this by sitting above every life domain, knowing the full picture, and surfacing what matters — without being asked.

> The goal is not to replace your advisors. It is to be the one person in the room who knows what every advisor is saying — and who synthesizes it into a clear picture of where you stand and what to do next.
>
> *A mix of a CEO's chief of staff and a wise grandma counseling a grandchild: clear-eyed about priorities, warm in delivery, unhurried in wisdom.*

---

## 3. System Architecture

See `docs/lifeTrackerDiagram.svg` for the full visual.

```
╔══════════════════════════════════════════════════════════════════════════╗
║  COMMUNICATION CHANNELS (shared across all agents)                       ║
║                                                                          ║
║  (A) iPhone Voice          (B) PA Web UI          (C) Local Mac UI      ║
║  ─────────────────          ────────────────        ──────────────────   ║
║  Call Twilio number         Browser → PA URL        Browser → :5000      ║
║  Speak / listen             Full web UI             Same web UI          ║
╚══════════════════════════════════════════════════════════════════════════╝
                    │ Twilio webhook  │ HTTPS  │ HTTP
                    ▼                 ▼        ▼
╔══════════════════════════════════════════════════════════════════════════╗
║  pytracker.core  (shared Python package)                                 ║
║                                                                          ║
║  Auth (GPG user DB + caller-ID)   │  IntentParser (Haiku)               ║
║  VoiceResponder (TwiML)           │  ResponseSynthesizer (Sonnet)        ║
║  SessionManager (agent, owner)    │  ActionItemQueue (cross-agent)       ║
╚══════════════════════════════════════════════════════════════════════════╝
                                   │
                    ┌──────────────▼──────────────┐
                    │  Personal Assistant (PA)      │
                    │  life.pa.*                   │
                    │                              │
                    │  – Route intent → agent      │
                    │  – Monthly life review       │
                    │  – Cross-agent synthesis     │
                    │  – Priority arbitration      │
                    └──┬──┬──┬──┬──┬──┬───────────┘
                       │  │  │  │  │  │
           ┌───────────┘  │  │  │  │  └──────────────┐
           │    ┌─────────┘  │  │  └──────────┐      │
           │    │    ┌───────┘  └──────┐       │      │
           ▼    ▼    ▼                 ▼       ▼      ▼
        ┌──────────────────────────────────────────────────────┐
        │ house  │ medical │  money │ estate │emotional│ faith │
        │Agent   │Agent    │Agent   │Agent   │Agent    │Agent  │
        │house.* │medical.*│money.* │estate.*│emotion.*│faith.*│
        └────┬───┴────┬────┴────┬───┴────┬───┴────┬───┴───┬───┘
             │        │         │         │        │       │
             └────────┴─────────┴─────────┴────────┴───────┘
                                      │
                    ╔═════════════════▼═══════════════════╗
                    ║  RecordAgent (common records service) ║
                    ║  life.core.records                    ║
                    ║  lifeTracker-data (private Git repo)  ║
                    ║  records/**/*.json  auto_push=true    ║
                    ╚══════════════════════════════════════╝
```

### Cross-Agent Dependencies

```
PersonalAssistant ◄── ALL agents (monthly briefings, action items, alerts)

estateAgent ◄── houseAgent (home value, equity, deferred maintenance cost)
            ◄── moneyAgent (account balances, retirement projections)
            ◄── llcRentalTracker (business income, depreciation, K-1)
            ◄── medicalAgent (longevity projection, care cost modeling)

moneyAgent  ◄── houseAgent (HELOC, home projects budget)
            ◄── llcRentalTracker (rental income, business distributions)
            ◄── medicalAgent (health insurance, HSA, out-of-pocket)

medicalAgent ◄── emotionalAgent (mental health ↔ physical health)
             ◄── houseAgent.accessibility (health needs → home mods)
             ◄── moneyAgent (HSA balance, insurance coverage)

emotionalAgent ◄── ALL agents (stress events from any domain affect emotional state)
               ◄── faithAgent (consolation/desolation ↔ emotional wellbeing)

houseAgent.finance ◄── moneyAgent (liquidity check before project approval)
houseAgent.accessibility ◄── medicalAgent (mobility needs → home adaptations)
```

---

## 4. Discipline Agents

### 4.1 Personal Assistant — `life.pa`

**Role:** Chief of staff. Routes. Synthesizes. Prioritizes. Advocates for simplicity.

The PA knows the full priority stack across all agents. What is overdue. What is in conflict between domains. What the owner most values right now.

**Key scenarios:**
- *Monthly life review:* Pull briefings from all active agents → produce a unified view
- *Cross-domain question:* "Can I afford to replace the HVAC this year?" → coordinate moneyAgent (liquidity), houseAgent (HVAC cost), estateAgent (retirement runway)
- *Priority arbitration:* When four agents surface urgent items simultaneously, the PA makes the call
- *Burden reduction:* Identify items that can be deferred, eliminated, or automated

---

### 4.2 houseAgent — `house.*`

**Role:** Home manager — systems, maintenance, financing, aesthetics, aging-in-place.

**Property:** 177 Kingsway Dr, Wimberley TX 78676 (Hays County, R33204) — purchased 2022-12-31, $335K cash.

**16 discipline sub-agents in 5 UANS categories:** `core.*` · `systems.*` · `designs.*` · `finance.*` · `life.*`

**Key cross-agent signals:**
- Sends equity and deferred maintenance cost to estateAgent
- Requests liquidity check from moneyAgent before approving major projects
- Sends accessibility gaps to medicalAgent for aging-in-place coordination

Full design: `houseAgent/docs/HouseManagerVision.md`

---

### 4.3 medicalAgent — `medical.*`

**Role:** Health advocate — clinical history, medication management, test tracking, care navigation, insurance.

**Owner profile:** Frank Rojas, 68yo male, 6'0" / 299 lbs. ARC / Epic (primary), IBM Post-Retirement UHC Advantage Medicare.

**Active conditions:** venous insufficiency (bilateral, 2025), bilateral hearing loss, sleep apnea (CPAP), thyroid, urology (2026), hypertension.

**Domain expertise:** FHIR R4 schema, Geriatric 5M's (Mind, Mobility, Medications, Multi-complexity, Matters Most), Epic SMART on FHIR OAuth.

**Key cross-agent signals:**
- Sends longevity and care-cost projections to estateAgent
- Sends HSA and medical spending to moneyAgent
- Sends mobility/cognition assessment to houseAgent.accessibility
- Receives emotional state from emotionalAgent (mind-body link)

Full design: `medicalAgent/docs/medicalTrackerVision.md`

---

### 4.4 moneyAgent — `money.*`

**Role:** Financial advisor — personal accounts (checking, savings, investment, retirement IRA/401k, HSA), debt management, retirement income planning.

**Not a business agent** — llcRentalTracker handles the LLC. moneyAgent is personal wealth management.

**Domain expertise:** RMDs (mandatory at 73, SECURE 2.0 Uniform Lifetime Table), IRMAA surcharge tracking, Roth conversion sequencing, Beancount double-entry core, Owl retirement runway model.

**Key cross-agent signals:**
- Sends account balances and liquidity to estateAgent and houseAgent
- Receives rental distributions from llcRentalTracker
- Sends HSA balance to medicalAgent
- Reports retirement runway to PersonalAssistant for life-stage planning

Full design: `moneyAgent/docs/moneyTrackerVision.md`

---

### 4.5 estateAgent — `estate.*`

**Role:** Estate manager — comprehensive view of all assets and their disposition. Trust management, succession planning, retirement wealth trajectory.

**Domain expertise:** 7 legal pillars (RLT, Pour-Over Will, DPOA, POLST/AHD, TODD, Beneficiary Designations, Letter of Instruction). §121 exclusion, step-up in basis, $15M estate tax exemption (2026, One Big Beautiful Bill Act). Owl retirement model, Ghostfolio/Wealthfolio for asset tracking.

**Key cross-agent signals:**
- Aggregates home value from houseAgent, accounts from moneyAgent, business value from llcRentalTracker
- Receives longevity/care projections from medicalAgent
- Sends estate tax exposure and succession priorities to PersonalAssistant

Full design: `estateAgent/docs/estateTrackerVision.md`

---

### 4.6 emotionalAgent — `emotional.*`

**Role:** Counselor and emotional health advisor — life stage transitions, stress, grief, relationship dynamics, cognitive resilience.

**Domain expertise:** CBT (Unified Protocol), PERMA (Positive Emotion, Engagement, Relationships, Meaning, Accomplishment), Erikson Stage 8 (Integrity vs. Despair), Worden's Tasks of Mourning (4-task active grief model).

**Key cross-agent signals:**
- Receives stress events from all agents (financial stress, health events, house crises)
- Informs medicalAgent about mental health status (mind-body link)
- Informs PersonalAssistant about owner's current emotional load (calibrates how much to surface at once)
- Receives consolation/desolation signal from faithAgent

Full design: `emotionalAgent/docs/emotionalTrackerVision.md`

---

### 4.7 faithAgent — `faith.*`

**Role:** Spiritual advisor — Catholic faith practice tracking, Ignatian Examen, prayer and reflection calendars, liturgical calendar context, community connection.

**Domain expertise:** Ignatian Examen (5 steps: Presence, Gratitude, Emotions, Focal moment, Tomorrow), consolation/desolation (-3 to +3), LiturgicalCalendarAPI, Magisterium AI for doctrinal knowledge retrieval.

**Key cross-agent signals:**
- Receives major life events from all agents (illness, loss, financial change) to suggest spiritual response
- Informs emotionalAgent (spiritual resilience and emotional health are linked — consolation/desolation is a primary cross-agent signal)
- Informs PersonalAssistant about community and service commitments

Full design: `faithAgent/docs/faithTrackerVision.md`

---

### 4.8 RecordAgent — `life.core.records`

**Role:** Common records infrastructure — owns and manages the `records/agents/` directory tree for all six discipline agent namespaces. Every discipline agent reads and writes through RecordAgent. No agent accesses the filesystem directly.

**Key capabilities:** read/write/append interface; git-as-master records (auto_push=true on every write); documents index; cross-agent action items API; full directory tree provisioning on first run.

Full design: `recordAgent/docs/recordAgentDesign.md`

---

## 5. Universal Agent Naming Schema (UANS)

The UANS is the connective tissue that ties the agent catalog, records directory, and data schemas into one coherent system. Every agent, every record, and every file path shares the same four-segment dot-notation identifier:

```
<namespace>.<category>.<agent>.<record>
```

| Segment | Values | Purpose |
|---|---|---|
| `<namespace>` | `life` · `house` · `medical` · `money` · `estate` · `emotional` · `faith` · `llc` | top-level discipline boundary |
| `<category>` | functional grouping within a discipline | `systems` · `health` · `accounts` · `assets` · `core` · etc. |
| `<agent>` | short name of the discipline sub-agent | `hvac` · `medications` · `rmd` · `records` · `checkin` · etc. |
| `<record>` | specific record file (stem only) | `log` · `current` · `schedule` · `history` · etc. |

**Why UANS matters:** A named agent is also a named path. There is no ambiguity about who owns a file or where it lives. The name alone identifies expertise domain, ownership, and storage location. Adding an agent means adding a name; the directory path, registry entry, and data schema all derive from it automatically.

**Path derivation (via RecordAgent):**
```
<namespace>.<category>.<agent>.<record>
       ↓          ↓        ↓        ↓
records/agents/<namespace>/<category>/<agent>/<record>.json
```

---

### 5.1 UANS Namespace Table

| Agent | Namespace | Categories |
|---|---|---|
| PersonalAssistant | `life` | `pa` |
| houseAgent | `house` | `core` · `systems` · `designs` · `finance` · `life` |
| medicalAgent | `medical` | `health` · `vitals` · `care` |
| moneyAgent | `money` | `accounts` · `transactions` · `planning` |
| estateAgent | `estate` | `assets` · `legal` · `planning` |
| emotionalAgent | `emotional` | `core` · `grief` · `legacy` · `stress` |
| faithAgent | `faith` | `core` · `examen` · `sacraments` · `community` · `legacy` |
| RecordAgent | `life` | `core.records` (infrastructure — not a discipline namespace) |
| llcRentalTracker | `llc` | (separate repo — work account) |

---

### 5.2 UANS Reference — All Discipline Agents

#### lifeTracker / PersonalAssistant

| UANS | Agent | File Path |
|---|---|---|
| `life.pa.briefings.monthly` | PA monthly review | `records/pa/briefings/monthly.json` |
| `life.pa.action_items.open` | PA action item queue | `records/pa/action_items/open.json` |
| `life.core.records` | RecordAgent | `records/agents/` (root — managed by RecordAgent) |

---

#### houseAgent — `house.*`

| UANS | Agent | File Path |
|---|---|---|
| `house.core.records` | HouseRecords | `records/agents/house/core/records/` |
| `house.core.profile` | House Profile | `records/agents/house/core/profile/` |
| `house.core.comm` | Communication | `records/agents/house/core/comm/` |
| `house.systems.hvac` | HVAC | `records/agents/house/systems/hvac/` |
| `house.systems.hvac.maintenance_log` | HVAC log | `records/agents/house/systems/hvac/maintenance_log.json` |
| `house.systems.electrical` | Electrical | `records/agents/house/systems/electrical/` |
| `house.systems.plumbing` | Plumbing | `records/agents/house/systems/plumbing/` |
| `house.systems.plumbing.sewer_diagram` | Sewer layout | `records/agents/house/systems/plumbing/sewer_diagram.json` |
| `house.systems.roofing` | Roofing | `records/agents/house/systems/roofing/` |
| `house.systems.security` | Security & Safety | `records/agents/house/systems/security/` |
| `house.systems.appliances` | Appliances | `records/agents/house/systems/appliances/` |
| `house.designs.architecture` | Architecture | `records/agents/house/designs/architecture/` |
| `house.designs.architecture.structural_notes` | Structural notes | `records/agents/house/designs/architecture/structural_notes.json` |
| `house.designs.landscaping` | Landscaping | `records/agents/house/designs/landscaping/` |
| `house.designs.interior` | Interior Design | `records/agents/house/designs/interior/` |
| `house.finance.budget` | Financing | `records/agents/house/finance/budget/` |
| `house.finance.budget.capital_improvements` | Capital improvements | `records/agents/house/finance/budget/capital_improvements.json` |
| `house.finance.tax` | Tax | `records/agents/house/finance/tax/` |
| `house.finance.investment` | Investment & Value | `records/agents/house/finance/investment/` |
| `house.life.accessibility` | Accessibility | `records/agents/house/life/accessibility/` |

---

#### medicalAgent — `medical.*`

| UANS | Agent | File Path |
|---|---|---|
| `medical.health.profile` | Person Profile | `records/agents/medical/health/profile/` |
| `medical.health.profile.current` | Current profile | `records/agents/medical/health/profile/current.json` |
| `medical.health.conditions` | Conditions Log | `records/agents/medical/health/conditions/` |
| `medical.health.conditions.current` | Active conditions | `records/agents/medical/health/conditions/current.json` |
| `medical.health.medications` | Medications Manager | `records/agents/medical/health/medications/` |
| `medical.health.medications.current` | Current meds | `records/agents/medical/health/medications/current.json` |
| `medical.vitals.labs` | Labs Tracker | `records/agents/medical/vitals/labs/` |
| `medical.vitals.labs.history` | Lab history | `records/agents/medical/vitals/labs/history.json` |
| `medical.vitals.bp` | Vitals Monitor (BP) | `records/agents/medical/vitals/bp/` |
| `medical.vitals.cpap` | CPAP Monitor | `records/agents/medical/vitals/cpap/` |
| `medical.care.appointments` | Appointment Log | `records/agents/medical/care/appointments/` |
| `medical.care.directives` | Directives Keeper | `records/agents/medical/care/directives/` |

---

#### moneyAgent — `money.*`

| UANS | Agent | File Path |
|---|---|---|
| `money.accounts.registry` | Account Registry | `records/agents/money/accounts/registry/` |
| `money.accounts.registry.current` | Account list | `records/agents/money/accounts/registry/current.json` |
| `money.transactions.log` | Transaction Log | `records/agents/money/transactions/log/` |
| `money.planning.rmd.schedule` | RMD Calendar | `records/agents/money/planning/rmd/schedule.json` |
| `money.planning.runway` | Runway Model | `records/agents/money/planning/runway/` |
| `money.planning.income` | Income Tracker | `records/agents/money/planning/income/` |

---

#### estateAgent — `estate.*`

| UANS | Agent | File Path |
|---|---|---|
| `estate.assets.registry` | Asset Registry | `records/agents/estate/assets/registry/` |
| `estate.assets.registry.current` | Current assets | `records/agents/estate/assets/registry/current.json` |
| `estate.legal.documents` | Document Vault | `records/agents/estate/legal/documents/` |
| `estate.legal.beneficiaries` | Beneficiary Manager | `records/agents/estate/legal/beneficiaries/` |
| `estate.planning.runway` | Runway Model | `records/agents/estate/planning/runway/` |
| `estate.planning.tax` | Tax Planner | `records/agents/estate/planning/tax/` |
| `estate.assets.net_worth` | Net Worth History | `records/agents/estate/assets/net_worth/` |

---

#### emotionalAgent — `emotional.*`

| UANS | Agent | File Path |
|---|---|---|
| `emotional.core.checkin` | Daily Check-In | `records/agents/emotional/core/checkin/` |
| `emotional.core.checkin.log` | Check-in log | `records/agents/emotional/core/checkin/log.json` |
| `emotional.grief.companion` | Grief Companion | `records/agents/emotional/grief/companion/` |
| `emotional.legacy.review` | Life Review | `records/agents/emotional/legacy/review/` |
| `emotional.stress.monitor` | Stress Monitor | `records/agents/emotional/stress/monitor/` |

---

#### faithAgent — `faith.*`

| UANS | Agent | File Path |
|---|---|---|
| `faith.core.practice` | Daily Practice | `records/agents/faith/core/practice/` |
| `faith.core.practice.log` | Practice log | `records/agents/faith/core/practice/log.json` |
| `faith.examen.reflection` | Examen Reflection | `records/agents/faith/examen/reflection/` |
| `faith.examen.reflection.log` | Examen log | `records/agents/faith/examen/reflection/log.json` |
| `faith.sacraments.history` | Sacramental History | `records/agents/faith/sacraments/history/` |
| `faith.community.life` | Community Life | `records/agents/faith/community/life/` |
| `faith.legacy.ethical_will` | Ethical Will | `records/agents/faith/legacy/ethical_will/` |

---

### 5.3 Key Cross-Agent UANS Signals

These are the cross-namespace reads that the PersonalAssistant and discipline agents make to synthesize across domains:

| Consumer | Source UANS | Signal |
|---|---|---|
| estateAgent | `house.finance.investment` | home value, equity |
| estateAgent | `money.accounts.registry.current` | account balances |
| estateAgent | `medical.health.profile.current` | longevity/care projection |
| moneyAgent | `medical.health.conditions.current` | HSA-eligible expenses |
| houseAgent.life.accessibility | `medical.health.conditions.current` | mobility constraints |
| emotionalAgent | `faith.examen.reflection.log` | consolation/desolation score |
| medicalAgent | `emotional.core.checkin.log` | mood/stress state |
| PersonalAssistant | ALL `*.action_items` | monthly briefing aggregation |

---

## 6. Shared Communication Layer

One voice channel, one web app, one user identity — all agents surface through the PersonalAssistant.

### 6.1 What Is Shared

| Component | Shared? | Notes |
|---|---|---|
| Twilio voice number | Yes — one number | PersonalAssistant answers; routes to agent |
| PA Flask deployment | Yes — one app | All agents registered as Flask blueprints |
| Auth (GPG user DB) | Yes — one user DB | Session carries `(owner_id, active_agent)` |
| IntentParser (Haiku) | Yes — one model call | Parses intent + identifies which agent handles it |
| ResponseSynthesizer (Sonnet) | Yes — one model call | Synthesizes across one or more agent responses |
| Monthly check-in loop | Yes — PA aggregates | Pulls briefings from all registered agents |
| Local Mac web UI | Yes — one Flask app | All agent UIs under one server |

### 6.2 Communication Flow

```
Owner speaks: "How are my finances and can I afford a new roof?"

Step 1 — IntentParser (Haiku):
  → agents: ["money", "house"]
  → question: "current financial position and cost of roof replacement"
  → mode: query

Step 2 — PersonalAssistant routes:
  → moneyAgent.query("current liquidity and available funds")
  → houseAgent.systems.roofing.query("replacement cost and urgency")

Step 3 — ResponseSynthesizer (Sonnet):
  → mode: voice → ≤ 3 sentences
  "Your current liquid savings are $42K. Roof replacement is estimated at $18–22K
   and the inspector flagged it as needed within 2 years. You have the funds, and
   the timing is good — do you want me to get contractor bids?"
```

### 6.3 pytracker.core Package

```
pytracker-core/
├── comm/
│   ├── voice.py          ← Twilio TwiML builder, Gather loop
│   ├── web.py            ← shared Flask route helpers
│   └── local.py          ← localhost config helpers
├── auth/
│   ├── gpg_users.py      ← GPG-encrypted user DB
│   └── session.py        ← session management (owner_id, agent, channel)
├── records/
│   ├── uans.py           ← UANS path derivation
│   └── git_store.py      ← read_json / write_json / git commit+push
├── llm/
│   ├── intent_parser.py  ← Haiku IntentParser; identifies agents + question
│   └── synthesizer.py    ← Sonnet ResponseSynthesizer; voice vs. web mode
└── models/
    └── models.py         ← AgentResponse, ActionItem, AgentBriefing dataclasses
```

---

## 7. Cross-Agent Scenarios

### 7.1 The Annual Life Review (January)

**Agents:** ALL

PersonalAssistant runs the annual review:
- Medical: key health events, upcoming screenings, medication changes
- Money: account performance, retirement runway update, RMD status
- Estate: net worth snapshot, trust review flag, beneficiary currency
- House: deferred maintenance list, systems approaching end-of-life, accessibility gaps
- LLC: business net income, distributions received, tax prep status
- Emotional: major life events and how they were processed; stress level trending
- Faith: practice consistency, community engagement, spiritual goals for the year

Output: a 2-page annual life summary — what happened, what it means, what to do next.

---

### 7.2 Health Crisis Response

**Agents:** medical · emotional · money · house · estate

1. medicalAgent logs the event and assesses care plan impact
2. emotionalAgent records the stress event and offers a coping framework
3. moneyAgent checks insurance coverage and out-of-pocket exposure
4. houseAgent.accessibility flags modifications that support recovery
5. estateAgent flags whether advance directive or care proxy documents need updating
6. PersonalAssistant presents a unified "here's what this means and what to do" response

---

### 7.3 Major Financial Decision

**Agents:** money · estate · house · llcRentalTracker

"Should I sell the house and move to a smaller place?"

1. houseAgent: current home value, deferred maintenance estimate, selling costs
2. moneyAgent: current liquid position, impact on income if equity is freed
3. estateAgent: tax basis, §121 exclusion, impact on estate plan
4. llcRentalTracker: any business-use allocations to reconcile
5. medicalAgent: accessibility of potential new home given current and projected health
6. PersonalAssistant: synthesizes a recommendation — financially, medically, emotionally sound?

---

### 7.4 Estate Planning Trigger

**Agents:** estate · money · house · llcRentalTracker · medical · faith

Triggered annually or when a major life event occurs (health change, death of spouse, large asset change):
- Full asset inventory (house + accounts + business)
- Updated longevity and care-cost model (from medicalAgent)
- Trust and beneficiary review
- Advance directive currency check
- Faith-informed values clarification for end-of-life decisions

---

## 8. Design Principles

1. **One voice, many domains.** The owner has one relationship — with the PersonalAssistant. All agents surface through it, never directly.

2. **The PA advocates for less cognitive load, not more.** The system's job is to reduce what the owner needs to think about. The default is silence; the exception is action.

3. **Cross-domain synthesis is the highest-value function.** Any single agent can answer domain questions. Only the PersonalAssistant can answer questions that span domains.

4. **Shared comm layer, isolated domain logic.** The communication layer is shared infrastructure. Each agent's domain expertise is fully isolated. No agent knows another agent's internals — they communicate only through the PersonalAssistant.

5. **Life-stage calibration.** Every response is calibrated to the Senior Owner stage: proactive, low-friction, clear recommendation (not a menu of options), with energy and capacity constraints respected.

6. **Trust through consistency.** The system only earns trust if it shows up reliably on the monthly check-in, remembers what was discussed, and follows through on action items.

7. **No domain gets permanently dark.** Even if the owner hasn't interacted with an agent in months, the monthly check-in surfaces it. No domain is allowed to go unreviewed for more than 90 days.

8. **UANS as connective tissue.** Every agent name, every record file, and every data schema path share the same four-segment dot-notation hierarchy. The category is always explicit — `systems.hvac` is distinct from `designs.architecture` is distinct from `finance.budget` — so the name alone identifies ownership, location, and expertise domain without any lookup table.

9. **RecordAgent is the sole filesystem interface.** No discipline agent reads or writes files directly. This concentrates file I/O, path management, and git commits in one place. Adding an agent means adding a UANS entry; the directory path and data schema derive automatically.

10. **Git-as-master records.** All records in `lifeTracker-data/` are private Git repositories. `auto_push=true` on every write. The git history IS the audit trail.

---

## 9. Build Order

Build in dependency order. The communication layer must exist before any agent can register. The PersonalAssistant routes before agents can answer.

| Phase | Component | Milestone |
|---|---|---|
| 0 | `pytracker.core` — shared comm layer | One voice number routes to one PA; auth works |
| 0 | RecordAgent — records infrastructure | Directory tree provisioned; read/write/git-push interface working |
| 1 | PersonalAssistant (lifeTracker) — orchestrator | Monthly check-in loop runs end-to-end with stub responses |
| 2 | houseAgent — Tier 1 agents | First discipline agent integrated; house queries answered by voice |
| 3 | medicalAgent — Tier 1 agents | Health queries answered; health events cross-posted to PA monthly review |
| 4 | moneyAgent — Tier 1 agents | Financial position queryable; monthly review shows account snapshot + RMD status |
| 5 | estateAgent | Full asset view; estate plan currency tracked |
| 6 | emotionalAgent | Stress events tracked; emotional load informs PA's communication style |
| 7 | faithAgent | Practice calendar; liturgical-calendar-aware check-ins |
| 8+ | Cross-agent scenarios | Active routing of multi-domain queries; annual life review automated |

---

*This document is v1.0 — authoritative ecosystem design. Supersedes `personalAssistanceVision.md` §5 (UANS) for all ecosystem-level UANS documentation. See individual agent vision docs for per-discipline detail.*
