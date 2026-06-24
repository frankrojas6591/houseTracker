# HouseMgr Agent — Top-Level Design

**Version:** 0.1
**Date:** June 2026
**Status:** Design — pre-implementation

---

## 1. Design Goals

### 1.1 Lightweight Orchestrator

The HouseMgr is a **thin router and response synthesizer** — it holds no domain knowledge itself. Every piece of expertise lives in a discipline agent. The HouseMgr's job is:

1. Parse owner intent from natural language (via LLM)
2. Identify which agents are relevant
3. Query those agents with the current house context
4. Synthesize a unified response
5. Route any stored outcomes back to HouseRecords

**Anti-pattern to avoid:** A "fat" HouseMgr that accumulates logic for specific domains (e.g., knows HVAC rules, knows tax codes). That logic belongs in the agent. The HouseMgr only knows the *agent registry* — not what the agents know.

### 1.2 Design Principles (from Vision)

- **Owner never tracks details** — agents do. HouseMgr surfaces, not collects.
- **Proactive over reactive** — agents push action items to the monthly check-in queue; HouseMgr presents them.
- **Recommendation, not menu** — synthesized output is a clear "here's what to do," not a list of options.
- **DIY-first, frugal** — cost framing defaults to quality-for-budget, not premium-fastest.
- **Aging-in-place thread** — every agent response considers the owner's current life stage.

---

## 2. Position Within pyTrackers

```
pyTrackers/
├── llcRentalTracker/   ← LLC accounting & IRS (Flask, ledger engine, MCP)
├── medicalTracker/     ← Personalized health management (early stage)
├── houseTracker/       ← THIS PROJECT
│   ├── houseMgr/       ← Orchestrator (lightweight router)
│   ├── agents/         ← Discipline agents (one module per agent)
│   ├── records/        ← HouseRecords DB (JSON, local)
│   ├── ui/             ← Flask web interface (monthly check-in, chat)
│   └── wsCmd.py        ← CLI entry point (start, onboard, check-in)
└── financialTracker/   ← TBD — will integrate with Financing agent
```

**No shared infrastructure with sibling trackers.** Any future cross-tracker integration (e.g., houseTracker ↔ medicalTracker for Accessibility agent, houseTracker ↔ financialTracker for utility bills) will be explicitly designed as narrow API contracts, not shared code.

### 2.1 pyTrackers Conventions Followed

- Python 3, Flask for web UI
- `wsCmd.py` as the CLI entry point
- `setup_paths.py` anchors all paths — no hardcoded absolutes
- JSON files as the persistent data store (no external DB)
- No docstrings; one-line inline comments only when WHY is non-obvious
- Tests under `tests/` using `python -m tests.test_<module>`

---

## 3. Architecture

### 3.1 Component Map

```
Owner (voice / chat / monthly check-in)
        │
        ▼
┌─────────────────────────────────────────┐
│            HouseMgr (Orchestrator)       │
│                                          │
│  IntentParser  ──►  AgentRouter          │
│       │                  │               │
│  (Claude API)     AgentRegistry          │
│                          │               │
│               ResponseSynthesizer        │
│                   (Claude API)           │
└──────────┬──────────────────────────────┘
           │  queries / receives action items
           ▼
┌──────────────────────────────────────────┐
│           Discipline Agents              │
│  Architecture │ HVAC │ Plumbing │ ...    │
│  (each agent: query / audit / record)    │
└──────────┬───────────────────────────────┘
           │  all reads/writes
           ▼
┌──────────────────────────────────────────┐
│           HouseRecords (DB)              │
│  house_profile.json                      │
│  agents/<agent_name>/records.json        │
│  agents/<agent_name>/action_items.json   │
│  documents/ (photos, PDFs, invoices)     │
└──────────────────────────────────────────┘
```

### 3.2 HouseMgr Core Loop

Two operating modes:

**Interactive mode** — owner sends a message, HouseMgr responds immediately:

```
owner_input → IntentParser → [relevant agents] → ResponseSynthesizer → reply
```

**Monthly check-in mode** — scheduled review of all agents:

```
for each agent:
    agent.audit() → list of action items
HouseMgr collects, ranks, presents as check-in report
Owner dismisses / defers / acts on items
```

### 3.3 Agent Interface Contract

Every discipline agent implements the same four methods. The HouseMgr only calls these — it never accesses agent internals.

```python
class DisciplineAgent:
    def brief(self) -> str:
        """Return a 2-3 sentence summary of current domain status."""

    def query(self, question: str, context: dict) -> AgentResponse:
        """Answer a domain-specific question given house context."""

    def audit(self) -> list[ActionItem]:
        """Proactive scan — return items needing owner attention."""

    def record(self, event: dict) -> None:
        """Log a domain event (repair done, system installed, etc.)."""
```

`AgentResponse` and `ActionItem` are shared dataclasses in `houseMgr/models.py` — the only shared contract between HouseMgr and agents.

### 3.4 LLM Usage Pattern

The HouseMgr uses Claude in two places only:

| Step | Input | Output | Model |
|---|---|---|---|
| **IntentParser** | Raw owner text | Intent JSON: `{agents: [...], question: str, mode: query/record/plan}` | Haiku (fast, cheap) |
| **ResponseSynthesizer** | Collected agent responses | Single coherent reply to owner | Sonnet |

Individual agents also call the LLM internally for domain reasoning — each agent manages its own LLM calls using its domain knowledge base (system prompt) + house-specific context from HouseRecords.

### 3.5 HouseRecords DB Structure

```
records/
├── house_profile.json          ← House Profile agent output
├── systems_registry.json       ← All systems/appliances (HVAC, water heater, etc.)
├── documents/                  ← PDFs, photos, invoices
│   ├── permits/
│   ├── invoices/
│   └── photos/
└── agents/
    ├── architecture/
    │   ├── knowledge.json      ← Floor plan, structural notes
    │   └── action_items.json   ← Pending items from last audit
    ├── hvac/
    ├── plumbing/
    └── ...                     ← One directory per agent
```

All JSON. All local. No cloud dependency.

---

## 4. Agent Build Priority & Interdependencies

### 4.1 Dependency Map

```
HouseRecords ◄─── ALL agents (every agent reads/writes here)
House Profile ◄─── ALL agents (every agent reads for house context)
Communication ◄─── ALL agents (all push action items here for check-in)

Architecture ◄─── Plumbing, Electrical, HVAC, Roofing, Landscaping, Decoration
                  (all need floor plan / structural knowledge)

Financing ◄─── Architecture, HVAC, Electrical, Plumbing, Roofing
               (all project agents need budget framing)

Tax ◄─── Financing (capital improvement categorization)
Investment ◄─── Tax (basis), Financing (equity)

Accessibility ◄─── Architecture (structural mods), Security (lighting/safety)
Landscaping ◄─── Architecture (site map), Plumbing (irrigation zones)
Decoration ◄─── Architecture (floor plan, room dimensions)
HVAC ◄─── Electrical (panel capacity for heat pump conversion)
```

### 4.2 Build Tiers

Agents within a tier can be built in parallel. Each tier depends on the tier above it being stable.

---

**Tier 1 — Infrastructure** *(build first; nothing else works without these)*

| Priority | Agent | Why First |
|---|---|---|
| 1 | **HouseRecords** | All agents store and retrieve through here; must exist before any agent is built |
| 2 | **House Profile** | Briefs every agent with house context; onboarding starts here |
| 3 | **Communication** | Owner interaction layer; monthly check-in and alert routing |

---

**Tier 2 — House Knowledge** *(understand the physical asset before advising on it)*

| Priority | Agent | Why This Tier |
|---|---|---|
| 4 | **Architecture** | Floor plan and structural knowledge is a prerequisite for Plumbing, Electrical, HVAC, Landscaping, Decoration, and Roofing agents |

---

**Tier 3 — Safety & Life Stage** *(immediate value; senior owner priority)*

| Priority | Agent | Why This Tier |
|---|---|---|
| 5 | **Security & Safety** | Smoke/CO detectors, fall lighting, emergency plan — actionable today with no dependencies |
| 6 | **Accessibility & Aging-in-Place** | Critical for a 70-year-old owner; depends on Architecture for structural mods |
| 7 | **HVAC** | Comfort, indoor air quality, health impact; seasonal maintenance calendar has immediate ROI |

---

**Tier 4 — Critical Systems** *(high failure cost; proactive monitoring value)*

| Priority | Agent | Why This Tier |
|---|---|---|
| 8 | **Electrical** | Safety-critical; panel age and GFCI coverage audit is high-value; needed by HVAC (heat pump) |
| 9 | **Plumbing** | High failure risk (water damage); water heater lifespan tracking |
| 10 | **Roofing & Building Envelope** | Most expensive deferred maintenance failure; annual inspection calendar |

---

**Tier 5 — Financial Intelligence** *(needed before any major project is approved)*

| Priority | Agent | Why This Tier |
|---|---|---|
| 11 | **Financing** | Budget framing and ROI for every Tier 3–4 project recommendation |
| 12 | **Tax** | Capital improvements tracking should start at first project; basis matters at sale |
| 13 | **Investment & Value** | Home value model and project ROI; depends on Tax (basis) and Financing (equity) |

---

**Tier 6 — Quality of Life** *(valuable but not safety-critical)*

| Priority | Agent | Why This Tier |
|---|---|---|
| 14 | **Appliances** | Lifecycle tracking; lower urgency than systems |
| 15 | **Landscaping** | Outdoor living, curb appeal, low-maintenance conversion |
| 16 | **Decoration & Interior Design** | Aesthetics and finish selection; primarily needed for remodel projects |

---

### 4.3 Interdependency Summary Table

| Agent | Hard Dependencies | Soft Dependencies |
|---|---|---|
| HouseRecords | — | — |
| House Profile | HouseRecords | — |
| Communication | HouseRecords | All agents (receives action items) |
| Architecture | HouseRecords, House Profile | — |
| Security & Safety | HouseRecords | Communication |
| Accessibility | Architecture | Security, HVAC, medicalTracker (external) |
| HVAC | Architecture | Electrical, Financing |
| Electrical | Architecture | Financing |
| Plumbing | Architecture | Financing |
| Roofing | Architecture | Electrical (solar), Financing |
| Financing | HouseRecords | All project agents |
| Tax | Financing | Investment |
| Investment | Tax, Financing | — |
| Appliances | HouseRecords | Financing |
| Landscaping | Architecture, Plumbing | Financing |
| Decoration | Architecture | Financing |

---

## 5. Project File Structure

```
houseTracker/
├── wsCmd.py                    ← CLI: start, onboard, check-in
├── wsgi.py                     ← Flask WSGI entry
├── requirements.txt
├── setup_paths.py              ← Path constants (follows pyTrackers convention)
│
├── houseMgr/                   ← Orchestrator package
│   ├── __init__.py
│   ├── router.py               ← IntentParser + AgentRouter
│   ├── synthesizer.py          ← ResponseSynthesizer
│   ├── registry.py             ← AgentRegistry (maps name → agent instance)
│   ├── checkin.py              ← Monthly check-in workflow
│   └── models.py               ← AgentResponse, ActionItem dataclasses
│
├── agents/                     ← One module per discipline agent
│   ├── base.py                 ← DisciplineAgent base class (interface contract)
│   ├── house_records.py        ← HouseRecords agent (A.14)
│   ├── house_profile.py        ← House Profile agent (A.15)
│   ├── communication.py        ← Communication agent (A.16)
│   ├── architecture.py         ← Architecture agent (A.1)
│   └── ...                     ← One file per remaining agent
│
├── records/                    ← HouseRecords DB (gitignored data)
│   ├── house_profile.json
│   ├── systems_registry.json
│   ├── documents/
│   └── agents/
│
├── ui/                         ← Flask views
│   ├── __init__.py
│   ├── chat.py                 ← Chat / voice interface route
│   ├── checkin.py              ← Monthly check-in UI route
│   └── templates/
│
├── tests/
│   ├── test_router.py
│   ├── test_checkin.py
│   └── test_agents/
│       └── test_house_records.py
│
└── docs/
    ├── HouseManagerVision.md   ← Vision (also README.md)
    └── design/
        └── houseMgrAgent.md    ← THIS FILE
```

---

## 6. Implementation Approach

### Phase 0 — Scaffold (no agents yet)

- `wsCmd.py` with `--onboard` and `--checkin` stubs
- `setup_paths.py` with path constants
- `houseMgr/models.py` with `AgentResponse`, `ActionItem`
- `agents/base.py` with `DisciplineAgent` interface
- `records/` directory structure
- Flask app skeleton with `/chat` and `/checkin` routes

### Phase 1 — Tier 1 Agents (infrastructure)

Build and test HouseRecords → House Profile → Communication in sequence. At the end of Phase 1, the monthly check-in loop runs end-to-end with stub data.

### Phase 2 — Tier 2 Agent (Architecture)

The Architecture agent is the gateway for all subsequent system agents. Onboarding (floor plan intake, room tagging, site map) is the Phase 2 deliverable.

### Phase 3+ — Remaining Tiers

Each tier follows the priority order in §4.2. Every new agent follows the `DisciplineAgent` interface from day one — no exceptions — to keep the HouseMgr router unchanged as agents are added.

---

## 7. Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| **Orchestrator pattern** | Thin router (no domain logic in HouseMgr) | Keeps HouseMgr stable as agents are added; domain bugs stay in agents |
| **LLM for intent parsing** | Haiku (fast/cheap) for routing, Sonnet for synthesis | Intent parsing is a simple classification; synthesis needs quality |
| **Agent LLM calls** | Each agent manages its own | Agents have domain-specific system prompts; centralized LLM would require HouseMgr to know all domains |
| **Storage** | Local JSON via HouseRecords agent | Consistent with pyTrackers; no cloud dependency; sensitive data stays local |
| **Agent interface** | 4-method contract (brief/query/audit/record) | Minimal surface area; new agents drop in without changing router |
| **Monthly check-in as primary UX** | Scheduled pull, not push | Matches owner preference; avoids notification fatigue; agents queue items between check-ins |
| **No shared infrastructure with sibling trackers** | Explicit integration contracts only | Each tracker evolves independently; avoids coupling |
