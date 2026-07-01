# strategy — Web 3.0 & My Personal Assistant

**Version:** 1.0
**Date:** July 2026
**Status:** Research / Strategic Horizon

---

## Contents

- [1. lifeTracker's Web 3.0 Story](#1-lifetrackers-web-30-story)
  - [1.2 Web 2.0 Javier — Trapped in Platforms](#12-what-web-20-javier-looks-like-birthplan)
  - [1.3 Web 3.0 Javier — Sovereign Agent](#13-what-web-30-javier-looks-like-trustedplan)
- [2. The Relevant Web 3.0 Technologies](#2-the-relevant-web-30-technologies)
- [3. Web 2.0 → Web 3.0 Evolution Map](#3-web-20--web-30-evolution-map)
- [4. Technology Readiness Matrix](#4-technology-readiness-matrix)
- [5. Migration Timetable](#5-migration-timetable)

---

## 1. lifeTracker's Web 3.0 story

### 1.1 Understanding Web 3.0

It is 2026 and most of the world lives in "Web 2.0" - a complex set of platforms that hold data and systems of the world.

The term "Web 3.0" refers to the next generation where there are no platforms and data/systems are personal and AI enabled - "Agentic".  Specifically, the table below shows key areas of the Web 3.0 world:

| | **Semantic/Agent Web3** |
|---|---|
| **Core idea** | AI agents acting autonomously; machine-readable world; user-owned data |
| **Stack** | DIDs, Verifiable Credentials, SOLID pods, Agent2Agent, MCP |
| **For Javier?** | **Central — this IS the future of personal AI** |
| **Maturity** | Steady W3C standards; production in 2025–2026 |
| **Our bet** | 90% (identity, data sovereignty, agent mesh) |

In short, this aligns very nicely with key design principles for the concept of my personal assistant `Javier` (hah-vee-ay), ie. my trusted agent, my **lifeTracker**. 

**lifeTracker's Web 3.0 story is about Javier becoming a sovereign agent — owning principal's data, speaking to the world on the principal's behalf, without middlemen.**

## 1.1a The Roadmap:

> **Today, build a clean Web 2.0 assistant now. Every abstraction layer created today (RecordAgent, UANS, UserContext, MCP tools) is a Web 3.0 swap point later — and Javier (lifeTracker Assistant) evolves from an app into a sovereign agent who holds the principal's keys, owns their data, and speaks to the world on their behalf.**


---

### 1.2 What Web 2.0 Javier Looks Like (BirthPlan)

![Web 2.0 Architecture — Javier trapped in platforms](./web3-arch-web20.svg)

**Every layer has a platform in the middle:**
- Identity: principal logs in with a password Javier hashes. Platform = lifeTracker's own DB.
- Data: Google owns the Drive. Google can read it. Google can go down.
- AI: Anthropic processes every prompt. Anthropic sees the context.
- Communication: Gmail reads principal's email. Twilio owns the phone channel.

This is Web 2.0. principal is a user of platforms. Javier is an app inside those platforms.

---

### 1.3 What Web 3.0 Javier Looks Like (TrustedPlan+)

![Web 3.0 Architecture — Javier as sovereign agent](./web3-arch-web30.svg)

**Every layer is principal's:**
- Identity: principal IS his DID. No password file. No platform. Cryptographic proof.
- Data: principal's SOLID pod. Apps request access. principal approves. Data never leaves.
- AI: Javier is a named agent. Talks to other agents via open protocols.
- Communication: Agent-to-agent messaging. No Gmail middleman required.

---

## 2. The Relevant Web 3.0 Technologies

### 2.1. Self-Sovereign Identity (SSI) — W3C DIDs + Verifiable Credentials

**What it is:**
- **DID** (Decentralized Identifier): `did:key:z6Mk...` — cryptographic ID principal generates and owns. Like a passport no government issued.
- **VC** (Verifiable Credential): A signed claim. ARC signs: *"principal is a patient, DOB 1959."* principal holds it. Shows it without exposing raw EHR data.

**Scenario:**
> Javier needs to book a specialist referral. Today: principal has to call, give his name, DOB, insurance — to a receptionist who types it into Epic.
>
> Web 3.0: Javier presents principal's VC from ARC (doctor). Specialist's agent verifies it cryptographically in 2 seconds. No phone call. No data entry. No fax.

**Maturity:** W3C standard (2022). Production SDKs exist (`did-resolver`, `@veramo/core`). **Ready now for design; Year 2 for implementation.**

---

### 2.2. SOLID Pods — Personal Data Sovereignty

**What it is:** Sir Tim Berners-Lee's answer to Big Tech owning your data. A **SOLID pod** is your personal data store — a server you control (or self-host). Apps don't store your data; they request read/write access to your pod with your permission.

**The lifeTracker parallel:** `<userData>/agents/` on Google Drive IS a proto-pod. Swapping Google Drive for a SOLID pod is a storage layer change, not an architecture change — because RecordAgent already abstracts all I/O.

**Scenario:**
> principal's cardiologist's app wants to see his BP history. Today: principal downloads a CSV from myAir, emails it.
>
> Web 3.0: Cardiologist's app requests read on `did:principal/agents/medical/vitals/bp/`. Javier approves. Cardiologist reads live data. principal revokes access after the appointment.

**Maturity:** SOLID protocol spec is final. CSS (Community Solid Server) is production-grade. **Year 2–3 for lifeTracker adoption.**

---

### 2.3. Agent-to-Agent Protocols (MCP + A2A)

**What it is:** The infrastructure for agents talking to other agents, not just to humans.

| Protocol | Origin | What It Does |
|---|---|---|
| **MCP** (Model Context Protocol) | Anthropic (2024) | Tool/resource exposure standard — Javier already uses this (Gmail MCP, Google Calendar MCP) |
| **A2A** (Agent2Agent) | Google (2025) | Agent discovery + task delegation — agents find each other and hand off work |
| **ANP** (Agent Network Protocol) | Open standard (2025) | Peer-to-peer agent communication with DID-based authentication |

**Scenario:**
> principal's HVAC needs replacing. Today: principal calls 3 contractors, gets quotes by email, enters them in a spreadsheet.
>
> Web 3.0: Javier (houseAgent) sends an A2A task to a contractor registry. 3 licensed contractor agents respond with structured quotes (UANS-compatible JSON). Javier compares, checks principal's moneyAgent for liquidity, makes a recommendation. principal says yes. Javier books.

**Maturity:** MCP — production now. A2A — emerging (2025 spec). ANP — early draft. **MCP: already in use. A2A: Year 2 horizon.**

---

### 2.4. Zero-Knowledge Proofs (ZKPs) — Share Proof, Not Data

**What it is:** Cryptographic technique that proves a statement is true without revealing the underlying data.

**Why it matters for health + estate:**
- Prove *"principal's A1C is below 7.5"* without sharing the lab value → insurance pricing
- Prove *"principal is over 65"* without showing DOB → pharmacy discount
- Prove *"principal has a valid advance directive on file"* without sharing the document → hospital system

**Scenario:**
> principal applies for long-term care insurance. Today: 6-month underwriting process; 40-page medical questionnaire; full EHR release to insurer.
>
> Web 3.0: Javier generates a ZK proof bundle: conditions controlled (✓), no hospitalization in 3 years (✓), medications list within acceptable range (✓). Insurer's agent verifies the proofs. Policy issued in 48 hours. Insurer never sees a single lab value.

**Maturity:** ZK circuits (Circom, snarkjs) are production. Health-specific ZK toolkits are early (2025–2026). **Year 3+ for lifeTracker.**

---

### 2.5. Smart Contracts — Estate Execution (Crypto Web3 Intersection)

**What it is:** Self-executing code on a blockchain. When conditions are met, actions fire automatically.

**The narrow use case for principal:** Estate execution — not speculation.

**Scenario:**
> principal's estate plan has a TODD (Transfer on Death Deed) for Wimberley house. Today: it requires probate, an attorney, 6–18 months.
>
> Web 3.0: A death certificate VC is issued (county → DID registry). Javier's estate agent detects the VC. Smart contract fires: property title transfers to named beneficiary on-chain. Attorney involvement: zero for the transfer itself.

**Maturity:** Ethereum smart contracts — production. Legal recognition of blockchain estate execution: Texas has digital asset laws (HB 4474, 2023). Court precedent: thin but growing. **Year 4+ — legal maturity is the constraint, not tech.**

---

## 3. Web 2.0 → Web 3.0 Evolution Map

```
TODAY                        YEAR 2              YEAR 3+
(BirthPlan)                  (Year2Plan)         (TrustedPlan+)
─────────────────────────────────────────────────────────────────
IDENTITY
  Passphrase + JWT         → DID created       → DID-based sessions
  users.json.gpg           → DID keystore      → VC wallet (principal's credentials)
  user_id = "principal"        → did:key:z6Mk...   → SSI everywhere

DATA STORE
  Google Drive             → Encrypted GDrive  → SOLID pod (self-hosted)
  file_store.py            → file_store.py     → solid_store.py (same interface)
  No access control        → GPG encryption    → WebACL per resource

AI
  Single Claude instance   → Claude + local    → Agent mesh: Javier +
  All context to Anthropic   model option        specialist micro-agents;
                                                  context stays local

COMMUNICATION
  Gmail MCP                → Gmail + A2A seed  → A2A: agent-to-agent tasks
  Twilio SMS               → same              → ANP: peer agent messaging
  commMemory (local)       → commMemory + STM  → commMemory + federated

KNOWLEDGE
  Structured JSON (L1)     → Episodic log (L2) → Vector RAG (L3) → Graph (L4)
  Local only               → Local + cloud     → Local + agent mesh sharing

ESTATE
  Documents on Drive       → VCs for directives → Smart contract triggers
  Manual execution         → Javier drafts      → Autonomous execution (limited)
```

---

## 4. Technology Readiness Matrix

| Technology | Standard Body | Maturity | Adoption Risk | lifeTracker Target |
|---|---|---|---|---|
| **MCP** | Anthropic | ✅ Production | Low | Now (already in use) |
| **W3C DIDs** | W3C | ✅ Production | Low | Year 2 |
| **Verifiable Credentials** | W3C | ✅ Production | Low | Year 2 |
| **SOLID pods** | W3C/Inrupt | 🟡 Stable | Medium (hosting) | Year 2–3 |
| **A2A Protocol** | Google/Open | 🟡 Emerging | Medium | Year 2–3 |
| **ANP** | Open spec | 🔴 Draft | High | Year 3+ |
| **ZK health proofs** | Open research | 🔴 Early | High | Year 3–4 |
| **Smart contract estate** | Ethereum + legal | 🟡 Tech ready / 🔴 Legal lagging | High | Year 4+ |

---

## 5. Migration Timetable

### Now — BirthPlan (Year 1): Build Web 2.0 Right

The smartest Web 3.0 prep is **clean abstraction now**. Every interface that hides a Web 2.0 detail becomes a swap point.

| Decision | Why It Preserves Web 3.0 Optionality |
|---|---|
| `RecordAgent` abstracts all I/O | Swap `file_store.py` → `solid_store.py` — zero agent changes |
| `user_id` as the identity anchor | Replace with DID string — same field, new format |
| `UserContext` carries identity | Add `did`, `vc_wallet_path` fields without breaking existing code |
| UANS dot-notation | Maps directly to SOLID pod path hierarchy |
| `config.json` `userData` field | Replace Google Drive path with pod URL |
| MCP already in use for Gmail | A2A is built on same tool-exposure paradigm |

**Nothing to build for Web 3.0 in Year 1. Just build Web 2.0 cleanly.**

---

### 5.1 Year 2 — Web 2.5: Identity + Agent Protocols

**Trigger:** CertificationPlan complete. Javier is trusted. Time to give principal a digital identity.

| Task | Module | Effort |
|---|---|---|
| Generate principal's DID (`did:key`) | `core/identity/did_manager.py` | 1 session |
| DID-based JWT replacement | `core/auth/did_auth.py` | 1 session |
| VC wallet for principal's health credentials | `core/identity/vc_wallet.py` | 2 sessions |
| Request ARC to issue patient VC (Epic SMART on FHIR) | `medicalAgent/fhir_vc.py` | 2 sessions |
| A2A task endpoint (Javier accepts inbound tasks) | `core/agent/a2a_server.py` | 2 sessions |
| A2A client (Javier delegates to external agents) | `core/agent/a2a_client.py` | 1 session |
| Encrypt Google Drive data at rest (GPG per-file) | `core/records/encrypted_store.py` | 1 session |

**Year 2 milestone test:**
> Javier presents principal's ARC patient VC to a specialist's scheduling agent. Appointment booked without a phone call.

---

### 5.2 Year 3 — Web 3.0 Foundation: SOLID + Agent Mesh

**Trigger:** principal is comfortable with agent-assisted decisions. Time to own his data.

| Task | Module | Effort |
|---|---|---|
| Spin up SOLID pod (Community Solid Server on home server or VPS) | Infra | 1 session |
| `solid_store.py` — SOLID-compliant RecordAgent store | `core/records/solid_store.py` | 2 sessions |
| Migrate Google Drive data → SOLID pod | `wsCmd.py --migrate-to-pod` | 1 session |
| WebACL per agent namespace — scoped access control | `core/records/access_control.py` | 2 sessions |
| commMemory → federated threads (ANP or ActivityPub) | `core/comm/federated.py` | 3 sessions |
| Knowledge graph: agent-mesh cross-agent signals | `core/knowledge/graph.py` | 3 sessions |

**Year 3 milestone test:**
> principal's cardiologist's app requests read access to `medical/vitals/bp/`. Javier approves. Access auto-revoked after 30 days. principal never types his BP data again.

---

### 5.3 Year 4+ — Full Autonomy: ZK + Smart Contracts

**Trigger:** principal's estate plan is in order. Legal frameworks have caught up.

| Task | Effort | Notes |
|---|---|---|
| ZK proof generator for health disclosures | 3–5 sessions | Use `snarkjs` + health circuit libraries |
| Smart contract for TODD execution (Ethereum) | 3 sessions | Requires Texas legal validation |
| Death certificate VC receiver | 1 session | Watch county registrar DID issuance |
| Autonomous estate agent | 4 sessions | High stakes — human-in-the-loop for all actions |

**Year 4 milestone test:**
> principal's long-term care insurer's agent receives a ZK proof bundle from Javier. Policy approved. Zero raw health data exchanged.

---

## 5.4 What This Means for Javier's Identity

Today Javier is **principal's app**.

Web 3.0 Javier is **principal's agent** — a named, cryptographically-identified actor in the world with:

- A **DID** (`did:key:z6MkJavier...`) — Javier's own identity, separate from principal's, but authorized by principal
- An **A2A endpoint** — other agents can find Javier and send tasks
- A **VC authority** — Javier can issue credentials on principal's behalf ("principal authorized this contractor to bill $X")
- A **pod ACL role** — Javier manages who sees what in principal's SOLID pod

This is the **agentic internet** — not agents as chatbots, but agents as actors with keys, permissions, and persistent relationships.

---

## 5.5 What NOT to Build (Web 3.0 Traps)

| Trap | Why to Avoid |
|---|---|
| **Blockchain data storage** (Filecoin, Arweave) for health records | HIPAA + GDPR require right-to-delete; immutable ledgers conflict; SOLID is better |
| **Crypto wallets for estate assets** | Texas probate law + family complexity; smart contracts are enforcement layer, not asset layer |
| **Decentralize AI compute** (federated learning, blockchain ML) | Premature; Anthropic quality gap is enormous; revisit Year 4+ |
| **Token incentive economics** | No user community here; it's one principal's PA — tokens solve multi-stakeholder problems |
| **Build ANP from scratch** | Wait for the open standard to stabilize (2026–2027 window) |

---

