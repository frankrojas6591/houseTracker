# HouseMgr — Agent Catalog & Build Priority

**Version:** 0.3
**Date:** June 2026
**Parent:** [Design Index](./houseMgrAgent.md)

---

## 1. Agent Interface Contract

Every discipline agent implements the same four methods. The HouseMgr only calls these — it never accesses agent internals.

```python
class DisciplineAgent:
    def brief(self) -> str:
        """2-3 sentence summary of current domain status."""

    def query(self, question: str, context: dict) -> AgentResponse:
        """Answer a domain question given house context."""

    def audit(self) -> list[ActionItem]:
        """Proactive scan — return items needing owner attention."""

    def record(self, event: dict) -> None:
        """Log a domain event (repair, install, inspection, etc.)."""
```

`AgentResponse` and `ActionItem` are shared dataclasses in `houseMgr/models.py` — the only shared contract between HouseMgr and agents. No agent imports from another agent.

### Voice Response Constraint

When the HouseMgr synthesizes a response destined for the phone (TTS), it instructs the Synthesizer to produce **≤ 3 sentences** of spoken prose — no markdown, no lists, no headers. The full structured response is always written to HouseRecords and available via the web view.

---

## 2. LLM Usage Pattern

The HouseMgr uses Claude in two places only:

| Step | Input | Output | Model |
|---|---|---|---|
| **IntentParser** | Owner speech transcript | `{agents: [...], question: str, mode: query/record/plan}` | Haiku (fast, cheap) |
| **ResponseSynthesizer** | Collected agent responses + mode (voice/web) | Spoken prose (voice) or structured HTML (web) | Sonnet |

Individual agents call the LLM internally for domain reasoning using domain-specific system prompts + house context from HouseRecords. Each agent manages its own LLM calls.

---

## 3. Dependency Map

```
HouseRecords ◄─── ALL agents (every agent reads/writes here)
House Profile ◄─── ALL agents (every agent reads for house context)
Communication ◄─── ALL agents (all push action items for check-in)

Architecture ◄─── Plumbing, Electrical, HVAC, Roofing, Landscaping, Decoration
                  (all need floor plan / structural knowledge)

Financing ◄─── Architecture, HVAC, Electrical, Plumbing, Roofing
               (all project agents need budget framing)

Tax ◄─── Financing (capital improvement categorization)
Investment ◄─── Tax (basis), Financing (equity)

Accessibility ◄─── Architecture (structural mods), Security (safety lighting)
Landscaping ◄─── Architecture (site map), Plumbing (irrigation zones)
Decoration ◄─── Architecture (floor plan, room dimensions)
HVAC ◄─── Electrical (panel capacity for heat pump conversion)
```

---

## 4. Build Tiers

Agents within a tier can be built in parallel. Each tier depends on the tier above it being stable.

### Tier 1 — Infrastructure

*Build first — nothing else runs without these.*

| Priority | Component | Why First |
|---|---|---|
| 1 | **Setup WebServer** | `wsCmd.py --setup` on PA console: creates config, bootstraps records tree, registers first user. Nothing else starts without this. |
| 2 | **Configurator (Owner, House)** | Web UI to register and edit houses/owners in config.json. Must exist before agents are configured for a specific house. |
| 3 | **HouseRecords** | All agents store and retrieve through here; must exist before any agent is built. |
| 4 | **House Profile** | Briefs every agent with house context; onboarding starts here. |
| 5 | **Communication** | Owner interaction layer; monthly check-in and alert routing. |

### Tier 2 — House Knowledge

*Understand the physical asset before advising on it.*

| Priority | Agent | Why This Tier |
|---|---|---|
| 6 | **Architecture** | Floor plan and structural knowledge is a prerequisite for Plumbing, Electrical, HVAC, Landscaping, Decoration, and Roofing. |

### Tier 3 — Safety & Life Stage

*Immediate value; senior owner priority.*

| Priority | Agent | Why This Tier |
|---|---|---|
| 7 | **Security & Safety** | Smoke/CO detectors, fall lighting, emergency plan — actionable today with no dependencies. |
| 8 | **Accessibility & Aging-in-Place** | Critical for a 70-year-old owner; depends on Architecture for structural mods. |
| 9 | **HVAC** | Comfort, indoor air quality, health impact; seasonal maintenance calendar has immediate ROI. |

### Tier 4 — Critical Systems

*High failure cost; proactive monitoring value.*

| Priority | Agent | Why This Tier |
|---|---|---|
| 10 | **Electrical** | Safety-critical; panel age and GFCI coverage audit; needed by HVAC (heat pump). |
| 11 | **Plumbing** | High failure risk (water damage); water heater lifespan tracking. |
| 12 | **Roofing & Building Envelope** | Most expensive deferred maintenance failure; annual inspection calendar. |

### Tier 5 — Financial Intelligence

*Required before any major project is approved.*

| Priority | Agent | Why This Tier |
|---|---|---|
| 13 | **Financing** | Budget framing and ROI for every Tier 3–4 project recommendation. |
| 14 | **Tax** | Capital improvements tracking should start at first project; basis matters at sale. |
| 15 | **Investment & Value** | Home value model and project ROI; depends on Tax (basis) and Financing (equity). |

### Tier 6 — Quality of Life

*Valuable but not safety-critical.*

| Priority | Agent | Why This Tier |
|---|---|---|
| 16 | **Appliances** | Lifecycle tracking; lower urgency than systems. |
| 17 | **Landscaping** | Outdoor living, curb appeal, low-maintenance conversion. |
| 18 | **Decoration & Interior Design** | Aesthetics and finish selection; primarily needed for remodel projects. |

---

## 5. Interdependency Summary Table

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

## 6. Implementation Plan (Agents Scope)

### Phase 1 — Tier 1 Agents (after PA scaffold)

Build and test in sequence: HouseRecords → House Profile → Communication. Milestone: monthly check-in loop runs end-to-end with stub data, spoken via Twilio voice.

- [ ] `agents/house_records.py` — JSON read/write; path helpers
- [ ] `agents/house_profile.py` — onboarding intake; briefing output
- [ ] `agents/communication.py` — action item queue; check-in report generator
- [ ] Voice check-in: call Twilio number → hear monthly summary spoken back

### Phase 2 — Tier 2 (Architecture)

Architecture is the gateway for all system agents. Floor plan intake, room tagging, site map — full onboarding via voice Q&A and optional photo upload via web.

- [ ] `agents/architecture.py` — floor plan intake; structural note recording
- [ ] Web UI: photo/document upload for floor plan scans

### Phase 3 — Tiers 3–6

Follow priority order in §4. Each agent follows the `DisciplineAgent` interface from day one — no exceptions — so the HouseMgr router never changes as agents are added.
