# HouseMgr Agent — Design Index

**Version:** 0.3
**Date:** June 2026
**Status:** Design — pre-implementation

---

## System Overview

HouseMgr is a voice-first home management assistant hosted on **PythonAnywhere (PA)**. The owner interacts by **phone only — voice**; records, reports, and check-in summaries are viewed in a browser at the PA-hosted web URL. The phone never displays records — it speaks them or routes the owner to the web view.

```
Phone (voice only)
     │
     ▼  Twilio STT/TTS (webhook)
PythonAnywhere — Hosted Flask App
     ├── HouseMgr Orchestrator  ← routes intent to agents
     ├── Discipline Agents      ← domain expertise
     ├── HouseRecords           ← PA filesystem
     │       └── Git backup     ← private repo (JSON records)
     └── Web UI                 ← browser: records, reports, check-in
          ↑
     Browser (any device — phone, tablet, desktop)
```

**Microservice boundary:** The phone is a dumb voice terminal. All logic, all records, and all intelligence live on PA. The only thing the phone does is carry speech in and speech out.

---

## Design Documents

| Document | Scope |
|---|---|
| [Architecture & Deployment](./houseMgrAgent_arch.md) | PA hosting, Twilio voice, component map, H×O model, config profile |
| [Agent Catalog](./houseMgrAgent_agents.md) | Agent interface contract, LLM usage, build tiers, dependency graph |
| [Data & Auth](./houseMgrAgent_data.md) | HouseRecords layout on PA, config.json schema, GPG auth, Git backup |
| [Implementation Plan](./houseMgrAgent_impl.md) | Phase-by-phase build from PA scaffold through full agent suite |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| **Hosting** | PythonAnywhere (PA) | Managed Python WSGI; persistent filesystem; no ops burden |
| **Voice interface** | Phone → Twilio → PA `/voice` route | Owner never types; voice is the primary interaction channel |
| **Visual interface** | Browser → PA web URL | Records/reports read on screen, not dictated; separates read vs. speak |
| **Records storage** | PA filesystem; private Git backup | Persistent on PA; Git provides version history and off-host redundancy |
| **Orchestrator** | Thin router — zero domain logic in HouseMgr | Domain bugs stay in agents; HouseMgr stays stable as agents are added |
| **LLM** | Haiku for intent parsing; Sonnet for synthesis | Cost-efficient routing; quality response generation |
| **Auth** | GPG-encrypted user DB; Flask session `(house_id, owner_id)` | Sensitive data never on disk as plaintext; follows llcRentalTracker pattern |
| **Multi-house** | H × O — any number of homes × owners per PA instance | Config-driven; no code change to add a new house or owner |
