# HouseMgr — Implementation Plan

**Version:** 0.3
**Date:** June 2026
**Parent:** [Design Index](./houseMgrAgent.md)

---

## 1. Guiding Rules

- Each phase produces a **runnable, testable milestone** — not just code.
- No agent is started until its hard dependencies (see [Agent Catalog §3](./houseMgrAgent_agents.md#3-dependency-map)) are tested and stable.
- Every agent implements the `DisciplineAgent` interface from day one. No exceptions.
- Voice path and web path are both tested at every phase milestone.
- PA deployment is the target environment. No "run locally first, deploy later."

---

## 2. Project File Structure

**Code repo** (`github.com/<user>/houseTracker` — private):

```
houseTracker/
├── wsCmd.py                    ← CLI admin: --setup, --start, --onboard, --checkin, --backup
├── wsgi.py                     ← Flask WSGI entry for PA
├── requirements.txt
├── config.json.example         ← Schema template (no secrets)
├── setup_paths.py              ← Reads ~/.houseTracker/config.json; sets all path constants
│
├── houseMgr/                   ← Orchestrator package
│   ├── __init__.py
│   ├── router.py               ← IntentParser (Haiku) + AgentRouter
│   ├── synthesizer.py          ← ResponseSynthesizer (Sonnet); voice vs. web mode
│   ├── registry.py             ← AgentRegistry (maps name → agent instance)
│   ├── checkin.py              ← Monthly check-in workflow
│   └── models.py               ← AgentResponse, ActionItem dataclasses
│
├── agents/
│   ├── base.py                 ← DisciplineAgent base class
│   ├── house_records.py        ← Tier 1
│   ├── house_profile.py        ← Tier 1
│   ├── communication.py        ← Tier 1
│   ├── architecture.py         ← Tier 2
│   └── ...                     ← One file per remaining agent
│
├── ui/
│   ├── __init__.py
│   ├── houseLogin_auth.py      ← Auth routes + login_required + Twilio caller-ID login
│   ├── configurator.py         ← Manage houses + owners in config.json (web UI)
│   ├── voice.py                ← /voice Twilio webhook handler (TwiML builder)
│   ├── chat.py                 ← /chat browser text interface
│   ├── checkin.py              ← /checkin monthly dashboard
│   ├── records.py              ← /records browser record viewer
│   └── templates/
│       ├── login.html
│       ├── select_house.html
│       ├── configurator.html
│       ├── checkin.html
│       └── records.html
│
└── tests/
    ├── test_router.py
    ├── test_synthesizer.py
    ├── test_checkin.py
    ├── test_setup_paths.py
    └── test_agents/
        └── test_house_records.py
```

**Outside git (on PA filesystem, never committed):**

```
/home/<pa_user>/.houseTracker/
├── config.json                 ← Profile: houses, owners, Twilio keys, Flask secret
└── users.json.gpg              ← GPG-encrypted user DB

/home/<pa_user>/houseTracker/<house_id>/    ← top_folder per house
├── records/                                 ← Backed up to private data repo
└── documents/                               ← PDFs, photos (PA filesystem only)
```

---

## 3. Phase 0 — PA Scaffold

**Milestone:** Flask app running on PA. Call the Twilio number → hear "HouseMgr ready." Login works in browser.

| Task | Owner Module |
|---|---|
| Create PA account; deploy Flask skeleton via `wsgi.py` | `wsgi.py` |
| `wsCmd.py --setup`: wizard that writes `config.json`, creates records tree, initializes GPG user DB | `wsCmd.py`, `setup_paths.py` |
| Auth routes: `/login`, `/logout`, `/register`, `/select_house` | `ui/houseLogin_auth.py` |
| `/voice` stub: Twilio webhook receives POST, returns TwiML `<Say>HouseMgr ready.</Say>` | `ui/voice.py` |
| Twilio: purchase number, point webhook to `https://<app>.pa.com/voice` | Twilio console |
| `houseMgr/models.py`: `AgentResponse`, `ActionItem` dataclasses | `houseMgr/models.py` |
| `agents/base.py`: `DisciplineAgent` abstract base class | `agents/base.py` |
| Configurator routes: add/edit houses and owners in config.json | `ui/configurator.py` |

---

## 4. Phase 1 — Tier 1 Agents + Voice Loop

**Milestone:** Call in, speak a question about the house → hear a spoken response. Monthly check-in runs end-to-end with stub data and speaks a summary.

| Task | Module |
|---|---|
| `agents/house_records.py` — JSON CRUD; `append_action_item`, `get_action_items` | `agents/house_records.py` |
| `agents/house_profile.py` — onboarding Q&A intake; `brief()` returns house summary | `agents/house_profile.py` |
| `agents/communication.py` — action item queue; monthly check-in report | `agents/communication.py` |
| `houseMgr/router.py` — Haiku IntentParser; AgentRouter maps intent → agent list | `houseMgr/router.py` |
| `houseMgr/synthesizer.py` — Sonnet synthesis; `voice_mode=True` caps output at 3 sentences | `houseMgr/synthesizer.py` |
| `ui/voice.py` — full Twilio Gather loop: STT → HouseMgr → TwiML TTS reply | `ui/voice.py` |
| `houseMgr/checkin.py` — scheduled monthly check-in; collects audits from all active agents | `houseMgr/checkin.py` |
| PA always-on task: monthly check-in trigger | PA console |

---

## 5. Phase 2 — Architecture Agent + Web Record View

**Milestone:** Onboard a house via voice Q&A. Floor plan and structural notes stored in records. Browse records in browser at PA URL.

| Task | Module |
|---|---|
| `agents/architecture.py` — intake: room count, sq ft, year built, structural notes | `agents/architecture.py` |
| Voice onboarding: guided Q&A sequence via Twilio Gather (multi-turn) | `ui/voice.py` |
| Web photo upload: floor plan scans, permit documents | `ui/records.py` |
| `/records` browser view: read-only record browsing by agent/category | `ui/records.py`, `templates/records.html` |

---

## 6. Phase 3+ — Remaining Tiers

Follow priority order from [Agent Catalog §4](./houseMgrAgent_agents.md#4-build-tiers). Tier 3 (Safety, Accessibility, HVAC) is the highest value after Architecture — start there.

Each new agent:
1. Implements `DisciplineAgent` interface (brief / query / audit / record)
2. Gets its own `agents/<name>/knowledge.json` and `action_items.json` under HouseRecords
3. Registers in `houseMgr/registry.py`
4. Is tested with both a voice query and a web check-in pass

No changes to the router, synthesizer, or HouseMgr core are expected as agents are added — that's the point of the interface contract.

---

## 7. Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| **Hosting** | PythonAnywhere — no local install | Managed WSGI; persistent FS; no ops burden; phone can reach it 24/7 |
| **Voice gateway** | Twilio | Phone number ownership; managed STT/TTS; webhook model keeps PA stateless per call |
| **Voice response length** | ≤ 3 sentences (Synthesizer enforces) | Spoken responses must be listenable; detail goes to web view |
| **Records location** | PA filesystem (not local, not S3) | Simple; persistent on paid PA plan; backed up via Git |
| **Records backup** | Private GitHub repo (JSON only, nightly push) | Version history; off-host copy; no documents (too large) |
| **Orchestrator** | Thin router — zero domain logic | HouseMgr stays stable as agents are added; domain bugs isolated in agents |
| **LLM routing** | Haiku for intent, Sonnet for synthesis | Cheap classification; quality response generation |
| **Auth** | GPG user DB + caller-ID auto-login | Sensitive data stays encrypted; voice callers get seamless login |
| **Multi-house** | H × O in config.json; session holds `(house_id, owner_id)` | Add a house by editing config; no code change needed |
| **Agent interface** | 4-method contract (brief/query/audit/record) | Minimal surface area; router never changes; agents are drop-in |
| **No shared infra with sibling trackers** | Explicit API contracts only | Each tracker evolves independently; no coupling |
