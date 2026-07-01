# lifeTracker — Project Roadmap

**Version:** 1.0
**Date:** June 2026
**Status:** BirthPlan — Phase 0 starting

---

## The Journey in One Picture

```
YEAR 1 — BirthPlan                   YEAR 2 — Cert/Year2       YEAR 3+ — Trusted
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━   ━━━━━━━━━━━━━━━━━━━━━━   ━━━━━━━━━━━━━━━━
[Foundation]──[Comm]──[6 Agents]──[YTD Review]  [+RAG]──[Steady State]  [+Graph]──[External]

Phase 0  1  2  3  | 4  5a 5b 5c 5d 5e | 6         Cert → Year2        TrustedPlan
```

---

## Knowledge Growth Arc

Each phase adds a layer of what Javier knows. The test at each level:

| Level | Javier Can… | Knowledge Layer |
|---|---|---|
| **L0 — Identity** | Answer "who is Frank?" | Profile: houses, medical team, faith advisors |
| **L1 — History** | Answer "what has happened?" | Structured JSON records per agent |
| **L2 — Story** | Narrate "tell me about my house" | Episodic logs — every interaction captured |
| **L3 — Patterns** | Surface "I notice you always…" | Vector RAG over growing record corpus |
| **L4 — Synthesis** | Connect "your health is affecting your estate" | Cross-agent signals + lightweight graph |

BirthPlan (Phases 0–6) reaches L1→L2. CertificationPlan validates L2. Year2Plan adds L3. TrustedPlan achieves L4.

---

## BirthPlan — Phases 0–6

### Phase 0a — Flask Scaffold + Auth Identity
**Duration:** 1 session
**Knowledge level reached:** L0 (partial) — system exists, one user can log in

**Deliverables:**
- [ ] `wsCmd.py --setup` wizard → writes `config.json`, creates `users.json.gpg`
- [ ] Flask app factory (`wsgi.py`) + auth routes (`/login`, `/logout`)
- [ ] JWT session; `@login_required` decorator
- [ ] `setup_paths.py` reads config; all modules use it

**Milestone test:**
> Browser → PA URL → `/login` → passphrase → session established. Done.

---

### Phase 0b — User Profile
**Duration:** 1 session
**Knowledge level reached:** L0 (complete) — Javier knows who Frank is

**Deliverables:**
- [ ] `UserContext`, `HouseEntry`, `PractitionerEntry`, `FaithAdvisorEntry` dataclasses
- [ ] `UserProfileService.load()` / `save()` / `add_*()` methods
- [ ] `wsCmd.py --setup` extension: prompted for houses, medical team, faith advisors
- [ ] `/profile` web route: view + edit

**Milestone test:**
> After setup: `request.user.primary_house.address == "177 Kingsway Dr…"` ✓
> Ask Javier: *"Who am I?"* → displays full profile: Frank Rojas, Wimberley TX, ARC/Epic, 3 practitioners.

---

### Phase 0c — commMemory + commEmail Seed
**Duration:** 1–2 sessions
**Knowledge level reached:** L1 (partial) — 12 months of email classified into agent records

**Deliverables:**
- [ ] `core/comm/gmail_client.py` — wraps Gmail MCP tools
- [ ] `core/comm/classifier.py` — Haiku: thread → `{agent, uans, summary, priority, action_required}`
- [ ] `core/comm/commMemory.py` — STM/LTM store; priority weighting (0–100)
- [ ] `wsCmd.py --email --dry-run` and `--email` batch import
- [ ] commEmail outbound draft (`core/comm/sender.py`)
- [ ] Web UI: `/email/inbox`, `/email/drafts`, `/email/import`

**Milestone test:**
> `wsCmd.py --email --dry-run` → classifies 50+ Gmail threads across ≥4 agent namespaces.
> Javier delivers: *"Frank, here's what your inbox tells me about your life right now…"* — one narrative summary.

---

### Phase 1 — RecordAgent + Data Store
**Duration:** 1 session
**Knowledge level reached:** L1 (infrastructure ready) — agents can now store and read records

**Deliverables:**
- [ ] `core/records/uans.py` — `uans_to_path()` with UserContext + Google Drive root
- [ ] `core/records/file_store.py` — `write_json()` / `read_json()`
- [ ] `RecordAgent.provision()` — creates full `<userData>/agents/` tree
- [ ] `wsCmd.py --setup` extension: calls `RecordAgent.provision()` after profile

**Milestone test:**
> `ls ~/GDrive/Family/PersonalAssistant/agents/` → 8 namespace directories exist.
> `ra.write("house.core.profile.house_profile", {...})` → file written, visible in Google Drive.

---

### Phase 2 — Web UI Communication Layer
**Duration:** 1–2 sessions
**Knowledge level reached:** L1 — Frank can talk to Javier via browser; conversations logged

**Deliverables:**
- [ ] PA orchestrator (`life/pa.py`): `register()`, `query()`, `monthly_briefing()`
- [ ] IntentParser (`life/router.py`): Haiku → `{agents, question, mode}`
- [ ] ResponseSynthesizer (`life/synthesizer.py`): web mode (full) + voice mode (≤3 sentences)
- [ ] Chat route (`/chat`), check-in route (`/checkin`)
- [ ] `AgentResponse`, `ActionItem`, `AgentBriefing` dataclasses (`life/models.py`)
- [ ] Conversation logged to commMemory on every query

**Milestone test:**
> Browser → `/chat` → *"What's the status of my house?"* → PA returns stub response ≤3 seconds.

---

### Phase 3 — iOS Voice API
**Duration:** 1 session
**Knowledge level reached:** L1 — Frank can talk to Javier by voice from iPhone

**Deliverables:**
- [ ] `/api/auth/token`, `/api/query`, `/api/notifications` (iOS API routes)
- [ ] `@api_auth_required` Bearer token decorator
- [ ] Channel detection: `"ios_voice"` → ≤3 sentence constraint
- [ ] mobileAudioIO app pointed at local dev server

**Milestone test:**
> iPhone → speak → text sent → Javier responds in voice ≤3 sentences.
> *"Javier, what do I need to handle this week?"* → spoken action items.

---

### Phase 4 — houseAgent (Tier 1)
**Duration:** 2–3 sessions (per `houseMgrAgent_impl.md`)
**Knowledge level reached:** L1→L2 — Javier knows Kingsway Drive

**Knowledge milestone:**
> *"Javier, tell me about my house."*
> → Systems installed, last service dates, open items, what's coming due. Not a list — a story.

**Deliverables:**
- [ ] `HouseMgr` registers with PA — implements `DisciplineAgent` 4-method contract
- [ ] HouseRecords agent (`house.core.records`)
- [ ] House Profile agent (`house.core.profile`) — onboarding Q&A
- [ ] Communication agent (`house.core.comm`) — action item queue
- [ ] Monthly house briefing surfaces in `/checkin`

**Episodic log start:** Every house interaction logged to `<userData>/agents/house/kingsway_dr/core/comm/interaction_log.json`

**Phase 4b–4d:** Build Tiers 2–6 per `houseMgrAgent_impl.md` (Architecture → Systems → Finance → Life)

---

### Phase 5 — Remaining Discipline Agents

Build order follows value + dependency priority. Each agent follows the same pattern: scaffold → onboarding intake → PA registration → briefing visible in `/checkin`.

#### Phase 5a — medicalAgent
**Duration:** 2–3 sessions
**Knowledge milestone:**
> *"Javier, prepare me for my ARC appointment Thursday."*
> → Recent labs, medication changes, open questions, conditions summary, upcoming follow-ups. Appointment prep in 60 seconds.

**Key deliverables:**
- [ ] PersonProfile + ConditionsLog + MedicationsManager (FHIR R4 schema)
- [ ] LabsTracker seed from `frankrojas_labHistory.json`
- [ ] VitalsMonitor seed from `BloodPressure.xlsx`
- [ ] FiveMsAssessment — initial structured assessment
- [ ] Epic FHIR API pull (once; quarterly refresh)
- [ ] CPAPMonitor via ResMed myAir or OSCAR export
- [ ] DirectivesKeeper — advance directive status
- [ ] Cross-agent: mobility flag → houseAgent; health events → emotionalAgent

---

#### Phase 5b — moneyAgent
**Duration:** 2 sessions
**Knowledge milestone:**
> *"Can I afford to replace the HVAC this year?"*
> → Liquid savings, RMD obligations, bucket status, IRMAA risk — PA coordinates with houseAgent to give a 3-sentence answer.

**Key deliverables:**
- [ ] Account registry (Schwab, Vanguard, IRA, HSA)
- [ ] RMD calendar for current year (SECURE 2.0, Uniform Lifetime Table)
- [ ] Bucket strategy model (cash/conservative/growth)
- [ ] OFX/QFX import from Schwab/Vanguard
- [ ] IRMAA risk tracker
- [ ] Cross-agent: liquidity signal → houseAgent, estateAgent; HSA balance → medicalAgent

---

#### Phase 5c — estateAgent
**Duration:** 2 sessions
**Knowledge milestone:**
> *"What's my net worth and what's missing from my estate plan?"*
> → Asset registry aggregated from all agents, 7 legal pillars status, gaps called out.

**Key deliverables:**
- [ ] Asset registry (aggregates from houseAgent, moneyAgent, llcRentalTracker)
- [ ] 7 legal pillars status tracker
- [ ] Net worth history (monthly snapshot)
- [ ] Step-up basis and §121 exclusion tracking
- [ ] DirectivesKeeper cross-reference (POLST currency → medicalAgent)

---

#### Phase 5d — emotionalAgent
**Duration:** 2 sessions
**Knowledge milestone:**
> *"How have I been doing emotionally this year?"*
> → Mood trend, grief threads active, relationship cadence, stress correlation with life events. Honest, not sugar-coated.

**Key deliverables:**
- [ ] DailyCheckIn — voice-optimized 5-field + free text; CBT/PERMA lens
- [ ] GriefCompanion — Worden task tracking
- [ ] RelationshipTracker — contacts log, isolation detection
- [ ] StressMonitor — subscribes to cross-agent stress events
- [ ] LifeReview — monthly Erikson framing
- [ ] Ethical guardrails: crisis protocol, referral logging, context rotation

---

#### Phase 5e — faithAgent
**Duration:** 1–2 sessions
**Knowledge milestone:**
> *"How is my spiritual life this Lent?"*
> → Practice consistency, Examen trend, consolation/desolation arc, sacramental history.

**Key deliverables:**
- [ ] Daily Examen logger (consolation/desolation score −3 to +3)
- [ ] Practice tracker (Mass, prayer, rosary, confession) with liturgical calendar tagging
- [ ] LiturgicalCalendarAPI integration (diocese-aware season/feast tagging)
- [ ] Sacramental history log (confession dates, Anointing of the Sick)
- [ ] Ethical will — first draft prompted annually
- [ ] Cross-agent: consolation score → emotionalAgent; end-of-life spiritual prep → estateAgent + medicalAgent

---

### Phase 6 — YTD Life Review (BirthPlan MILESTONE)
**Duration:** 1 session
**Knowledge level reached:** L2 complete — Javier can narrate the story of Frank's life

**The test:**
> *"Javier, give me my year in review."*

Expected output per agent (Phase 6 deliverable):
1. **Start of year**: Where each agent began
2. **YTD Accomplishments**: Positive events, decisions made, progress
3. **What needs focus**: Current year gaps and open items
4. **5-year outlook**: What each agent sees coming — good, bad, and urgent

**Not Frank's self-assessment. The agents' independent view from their domain expertise.**

**Deliverables:**
- [ ] PA `monthly_briefing()` evolved into `annual_review()` — calls each agent's `brief()` in depth mode
- [ ] Each agent implements `annual_summary()` → returns structured narrative per the 4 items above
- [ ] PA synthesizes all 6 into one "State of Frank" review document
- [ ] Delivered via email draft + web UI `/checkin/annual`

---

## CertificationPlan (Year 1 → Year 2)

**Trigger:** Phase 6 complete.
**Goal:** Prove agents are adding value — not just storing records.

### Certification Metrics

| Metric | How Measured | Pass |
|---|---|---|
| Consultation frequency | Queries per week | Increasing trend over 6 months |
| Task completion | Actions surfaced → acted on | >50% acted on within 30 days |
| Burden reduction | "I didn't have to think about that" moments | Captured in monthly self-assessment |
| Narrative test | Ask each agent to tell the year | Accurate, personal, catches things Frank forgot |

### Knowledge Upgrades (CertificationPlan)

- [ ] **Episodic memory operational** — every interaction logged; agents can say "last time you mentioned…"
- [ ] **Agent self-assessment** — each agent runs a quarterly self-audit: "What do I know well? What am I missing?"
- [ ] **commMemory LTM review** — monthly digest of memory threads (priority 0–79) surfaced to PA

---

## Year2Plan (Year 2)

**Goal:** Steady state. Frank consults Javier habitually. Agents know the year's rhythm.

### Knowledge Upgrades (Year2Plan)

- [ ] **Vector RAG** over growing records
  - Every significant event embedded (ChromaDB or FAISS, running locally)
  - Semantic retrieval: *"Anything like this before?"* → agent retrieves relevant past events
  - Tool: ChromaDB local instance alongside RecordAgent
- [ ] **YE/YS cadence** — Year-End and Year-Start review sessions built into the system
  - Dec: estate plan currency check, tax optimization window, insurance review
  - Jan: RMD calendar reset, health goals, home maintenance schedule
- [ ] **Monthly check-in steady state** — each agent's `brief()` takes <10 seconds; PA synthesizes in <30 seconds

---

## TrustedPlan (Year 3+)

**Goal:** Javier communicates not just with Frank but *for* Frank — to the people who matter.

### Knowledge Upgrades (TrustedPlan)

- [ ] **Cross-agent pattern signals** — PA detects relationships between domains
  > *"Every time a house expense > $5K hits, your emotional check-ins drop for 2 weeks. Let's build a buffer trigger."*
- [ ] **External communication** — PA drafts outbound for doctor, attorney, family
  - *"Frank, want me to draft a note to your attorney about updating the TODD?"*
  - Auto-draft → Frank reviews → sends
- [ ] **PA-as-advocate** — PA attends (as prepared notes) appointments:
  - Appointment prep summary: conditions, medications, labs, questions
  - Post-appointment log: what was decided, follow-up actions
- [ ] **Lightweight knowledge graph** — cross-agent relationship tracking at the PA level (not full DAG)

---

## Open Design Issues

These conflicts and gaps are tracked in GitHub Issue **"Finalize Core Design Services"**:

| # | Issue | Docs in Conflict |
|---|---|---|
| 1 | **Data store**: Google Drive vs. git-as-master | `recordAgentDesign.md` vs `lifeTracker_records.md` + `strategy-Git_UserConfig.md` |
| 2 | **PA namespace**: `assistant.life.*` vs `life.pa.*` | `lifeTracker_records.md` vs `lifeTrackerVision.md` + `recordAgentDesign.md` |
| 3 | **UANS paths in vision**: `records/agents/` vs `<userData>/agents/` | `lifeTrackerVision.md §6.2` vs `lifeTracker_records.md` |
| 4 | **medicalAgent UANS**: vision categories don't match records design | `medicalTrackerVision.md` vs `lifeTracker_records.md` |
| 5 | **commMemory** missing from code repo structure | `lifeTracker_design.md §2` |
| 6 | **`recordAgentDesign.md`** significantly stale (old paths, old git model) | `recordAgent/docs/recordAgentDesign.md` |
