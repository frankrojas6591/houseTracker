# HouseMgr — Architecture & Deployment

**Version:** 0.3
**Date:** June 2026
**Parent:** [Design Index](./houseMgrAgent.md)

---

## 1. Design Goals

### 1.1 Lightweight Orchestrator

The HouseMgr is a **thin router and response synthesizer** — it holds no domain knowledge. Every piece of expertise lives in a discipline agent. The HouseMgr's only jobs are:

1. Parse owner intent from speech (via LLM)
2. Identify which agents are relevant
3. Query those agents with current house context
4. Synthesize a unified spoken or written response
5. Route stored outcomes back to HouseRecords

**Anti-pattern to avoid:** A "fat" HouseMgr that accumulates logic for specific domains (e.g., knows HVAC rules, knows tax codes). That logic belongs in the agent. The HouseMgr knows only the *agent registry* — never what the agents know.

### 1.2 Design Principles

- **Owner never tracks details** — agents do. HouseMgr surfaces; agents collect.
- **Proactive over reactive** — agents push action items to the monthly check-in queue; HouseMgr presents them.
- **Recommendation, not menu** — synthesized output is "here's what to do," not a list of options.
- **Voice-first** — every response is designed to be heard, not just read.
- **DIY-first, frugal** — cost framing defaults to quality-for-budget, not premium-fastest.
- **Aging-in-place thread** — every agent response considers the owner's current life stage.

---

## 2. Deployment Architecture

HouseMgr is a **hosted microservice** on PythonAnywhere (PA). There is no local installation. The phone is a dumb voice client; the PA server is everything.

```
┌─────────────────────────────────────────────────────────────┐
│  OWNER DEVICES                                              │
│                                                             │
│  Phone (voice only)          Browser (any device)           │
│  ────────────────            ──────────────────────         │
│  • Calls Twilio number       • Opens https://<app>.pa.com   │
│  • Speaks → STT              • Views records, reports       │
│  • Hears response ← TTS      • Monthly check-in dashboard   │
│  • No record display         • Configurator (admin)         │
└────────────┬────────────────────────────┬───────────────────┘
             │ Twilio webhook (HTTPS POST) │ HTTPS GET/POST
             ▼                            ▼
┌─────────────────────────────────────────────────────────────┐
│  PythonAnywhere — Flask WSGI App                            │
│                                                             │
│  /voice    ← Twilio TwiML webhook (STT input, TTS reply)   │
│  /chat     ← Browser text chat (fallback to voice flow)    │
│  /checkin  ← Monthly check-in dashboard                    │
│  /records  ← Record viewer (browse / search HouseRecords)  │
│  /config   ← Configurator (houses, owners, agents)         │
│  /login    ← Auth (GPG user DB)                            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  HouseMgr Orchestrator                              │   │
│  │  IntentParser (Haiku) → AgentRouter → Synthesizer   │   │
│  │                          (Sonnet)                   │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────────┐   │
│  │  Discipline Agents (16 agents across 6 tiers)       │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────▼────────────────────────────┐   │
│  │  HouseRecords  /home/<pa_user>/houseTracker/        │   │
│  │  ← Git backup → private GitHub repo (JSON data)    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Why PythonAnywhere

| Factor | Rationale |
|---|---|
| **Managed Python WSGI** | No server ops; PA handles gunicorn, SSL, process restart |
| **Persistent filesystem** | HouseRecords live on PA disk; no ephemeral container risk |
| **Always-on tasks** | Paid tier supports always-on background tasks for scheduled check-ins |
| **SSH console** | Admin tasks (`wsCmd.py --setup`, GPG key management) via PA bash console |
| **Cost** | $5–12/mo for a personal always-on app |

### 2.2 Why Twilio for Voice

| Factor | Rationale |
|---|---|
| **Phone number ownership** | Owner calls a real phone number — no app install required |
| **STT/TTS managed** | Twilio Gather (STT) + Say (TTS) — no audio processing on PA |
| **Webhook model** | Each phone interaction is a POST to `/voice`; stateless on PA side |
| **Recording support** | Optional: Twilio can record calls for audit / training |

The voice flow: owner calls Twilio number → Twilio records speech → sends transcript to `PA/voice` → HouseMgr processes → returns TwiML with TTS reply → Twilio speaks it back.

---

## 3. Component Map

```
Owner phone call
      │ Twilio STT (transcript)
      ▼
┌─────────────────────────────────────────┐
│  ConfigLoader + AuthLayer               │
│  /home/<pa_user>/.houseTracker/         │
│  config.json · users.json.gpg           │
│  session: (house_id, owner_id, role)    │
└──────────┬──────────────────────────────┘
           │ house context on every request
           ▼
┌─────────────────────────────────────────┐
│  HouseMgr Orchestrator (Flask WSGI)     │
│                                         │
│  IntentParser ──► AgentRouter           │
│       │                │                │
│  (Haiku API)     AgentRegistry          │
│                        │                │
│               ResponseSynthesizer       │
│                  (Sonnet API)           │
│                        │                │
│         ┌──────────────┴──────────┐    │
│         │ VoiceResponder          │    │
│         │ (TwiML TTS → Twilio)    │    │
│         │ WebResponder            │    │
│         │ (HTML → browser)        │    │
│         └─────────────────────────┘    │
└──────────┬──────────────────────────────┘
           │ queries / action items
           ▼
┌─────────────────────────────────────────┐
│  Discipline Agents (16 agents)          │
│  Architecture │ HVAC │ Plumbing │ ...   │
│  (each: query / audit / record)         │
└──────────┬──────────────────────────────┘
           │ all reads/writes
           ▼
┌─────────────────────────────────────────┐
│  HouseRecords (PA filesystem)           │
│  /home/<pa_user>/houseTracker/          │
│  <house_id>/records/                    │
│  ← periodic git push → private repo    │
└─────────────────────────────────────────┘
```

---

## 4. H × O Service Model

The app supports **H homes × O owners** per PA instance:

- **H (homes):** One PA instance manages any number of houses. Each house has its own records directory on PA.
- **O (owners):** Multiple owners can be registered. Each authenticates separately and accesses only their associated houses.

Active session context is `(house_id, owner_id)`. Multi-house owners select the active house at login or via the house-switcher in the nav bar.

Voice sessions: Twilio caller ID is mapped to `owner_id` in the user DB, so a known phone number auto-selects the owner without a spoken login. Unknown callers hear a PIN challenge.

---

## 5. Position Within pyTrackers

```
pyTrackers/
├── llcRentalTracker/   ← LLC accounting & IRS (Flask, ledger engine, MCP)
├── medicalTracker/     ← Personalized health (early stage)
├── houseTracker/       ← THIS PROJECT (hosted on PA)
│   ├── houseMgr/       ← Orchestrator (thin router)
│   ├── agents/         ← Discipline agents (one module per agent)
│   ├── ui/             ← Flask views (web + voice routes)
│   └── wsCmd.py        ← CLI admin (run in PA console)
└── financialTracker/   ← TBD
```

No shared infrastructure with sibling trackers. Cross-tracker integration (e.g., houseTracker ↔ medicalTracker for Accessibility) will be narrow API contracts, not shared code.

---

## 6. Implementation Plan (Architecture Scope)

### Phase 0 — PA Scaffold

- [ ] Create PA account; set up always-on WSGI app (`wsgi.py`)
- [ ] `wsCmd.py --setup`: creates `/home/<pa_user>/.houseTracker/config.json`, bootstraps records directories
- [ ] `setup_paths.py`: reads config.json from PA path; sets `TOP`, `RECORDS_DIR`, `DOCUMENTS_DIR`
- [ ] Flask skeleton: `/login`, `/logout`, `/register`, `/select_house`, `/voice`, `/chat`, `/checkin`, `/records`, `/config`
- [ ] Twilio account + phone number; webhook pointed to `https://<app>.pa.com/voice`
- [ ] Smoke test: call Twilio number → Flask logs the transcript → TTS "received" reply

### Phase 1 — Voice Loop

- [ ] `VoiceResponder`: formats HouseMgr response as TwiML `<Say>` with Gather for follow-up
- [ ] Caller ID → owner lookup (auto-login for known numbers; PIN challenge for unknown)
- [ ] `WebResponder`: same response rendered as HTML for browser path

### Phase 2+ — Full Stack

See [Implementation Plan](./houseMgrAgent_impl.md) for phase-by-phase agent build schedule.
