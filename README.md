# lifeTracker

*My Personal Assistant Ecosystem — One Trusted Advisor/Advocate backed by Expert Agents*

A personal AI system that sits above every domain of life — home, health, money, estate, relationships, and faith — and keeps nothing dark.

---

## Design Principle

**One Trusted Advisor/Advocate backed by six expert agents.**

You have one voice number, one web app, one trusted point of contact: the **Personal Assistant (PA)**. The PA knows your whole life, not just one domain. All six agents report up to it.

```
               Personal Assistant (PA)
                      life.pa.*
          ┌─────┬─────┬─────┬─────┬─────┐
       house  medical money estate emotion faith
       Agent   Agent  Agent  Agent  Agent  Agent
```

---

## Agents

| Agent | Domain | Namespace |
|---|---|---|
| **houseAgent** | Systems, maintenance, financing, aging-in-place | `house.*` |
| **medicalAgent** | Clinical history, medications, FHIR, CPAP, labs | `medical.*` |
| **moneyAgent** | Accounts, RMDs, retirement runway, Beancount | `money.*` |
| **estateAgent** | Assets, trusts, succession, step-up basis | `estate.*` |
| **emotionalAgent** | Relationships, human connection, emotional health | `emotional.*` |
| **faithAgent** | Catholic practice, Ignatian Examen, community | `faith.*` |
| **RecordAgent** | Common records service — all agents write through it | `life.core.records` |

> **llcRentalTracker** is a separate repo on the work account (`wbgroupmgr`). It is not part of this codebase.

---

## Repository Layout

```
lifeTracker/
├── docs/
│   ├── lifeTrackerVision.md      ← START HERE — full ecosystem design
│   ├── lifeTrackerDiagram.svg    ← architecture diagram
│   └── gitStrategy.md
├── houseAgent/
│   └── docs/
│       ├── HouseManagerVision.md
│       └── design/
│           ├── houseMgrAgent.md
│           ├── houseRecords/
│           └── *.md
├── medicalAgent/docs/
├── moneyAgent/docs/
├── estateAgent/docs/
├── emotionalAgent/docs/
├── faithAgent/docs/
└── recordAgent/
    └── docs/
        └── recordAgentDesign.md  ← common records service design
```

---

## Start Here

**Full ecosystem vision:** [`docs/lifeTrackerVision.md`](docs/lifeTrackerVision.md)

Covers: system architecture, all six agents, Universal Agent Naming Schema (UANS), shared communication layer, cross-agent scenarios, design principles, and build order.

**Architecture diagram:** [`docs/lifeTrackerDiagram.svg`](docs/lifeTrackerDiagram.svg)

---

## Infrastructure

| Component | Detail |
|---|---|
| **Language** | Python |
| **Framework** | CrewAI / LangGraph (multi-agent orchestration) |
| **Shared package** | `Communication Agent (pytracker.core)` — comm · auth · records · llm · models |
| **Records store** | `lifeTracker-data` — private Git repo, JSON, `auto_push=true` |
| **LLM** | IntentParser: Claude Haiku · ResponseSynthesizer: Claude Sonnet |
| **Voice** | Twilio (one number for all agents) |
| **Web UI** | Flask + Jinja2 blueprints (one app, all agents) |
| **Git remote** | `git@github.com-fxr:frankrojas6591/lifeTracker.git` |
| **SSH** | `~/.ssh/id_ed25519_fxr` via alias `github.com-fxr` |

---

*pyTrackers ecosystem · Frank Rojas · June 2026*
