# strategy — Web 3.0 & My Personal Assistant

**Version:** 1.0
**Date:** July 2026
**Status:** Research / Strategic Horizon

---

## The Two Web 3.0s — Which One Matters Here?

Two movements share the "Web 3.0" name. They are not the same thing.

| | **Crypto Web3** | **Semantic/Agent Web3** |
|---|---|---|
| **Core idea** | Decentralized finance, NFTs, token economies | AI agents acting autonomously; machine-readable world; user-owned data |
| **Stack** | Ethereum, Solana, IPFS, DeFi protocols | DIDs, Verifiable Credentials, SOLID pods, Agent2Agent, MCP |
| **For Javier?** | Peripheral — estate smart contracts, maybe | **Central — this IS the future of personal AI** |
| **Maturity** | Boom/bust cycles; speculative | Steady W3C standards; production in 2025–2026 |
| **Our bet** | 10% (estate smart contracts, Year 3+) | 90% (identity, data sovereignty, agent mesh) |

**lifeTracker's Web 3.0 story is not about crypto. It is about Javier becoming a sovereign agent — owning Frank's data, speaking to the world on Frank's behalf, without middlemen.**

---

## What Web 2.0 Javier Looks Like (BirthPlan)

```
Frank ──► Browser/iPhone ──► Flask (Javier) ──► Anthropic API
                                    │
                         Google Drive (data)
                         Gmail (commEmail)
                         Twilio (SMS)
```

**Every layer has a platform in the middle:**
- Identity: Frank logs in with a password Javier hashes. Platform = lifeTracker's own DB.
- Data: Google owns the Drive. Google can read it. Google can go down.
- AI: Anthropic processes every prompt. Anthropic sees the context.
- Communication: Gmail reads Frank's email. Twilio owns the phone channel.

This is Web 2.0. Frank is a user of platforms. Javier is an app inside those platforms.

---

## What Web 3.0 Javier Looks Like (TrustedPlan+)

```
Frank ──► DID (did:key:frankrojas) ──► Javier (sovereign agent)
                                            │
                        ┌───────────────────┼────────────────────┐
                        │                   │                    │
                  SOLID Pod            Agent Mesh           ZK Proofs
               (Frank's data)     (doctor, attorney,       (share proof,
              encrypted, local    contractor agents)        not data)
```

**Every layer is Frank's:**
- Identity: Frank IS his DID. No password file. No platform. Cryptographic proof.
- Data: Frank's SOLID pod. Apps request access. Frank approves. Data never leaves.
- AI: Javier is a named agent. Talks to other agents via open protocols.
- Communication: Agent-to-agent messaging. No Gmail middleman required.

---

## The Relevant Web 3.0 Technologies

### 1. Self-Sovereign Identity (SSI) — W3C DIDs + Verifiable Credentials

**What it is:**
- **DID** (Decentralized Identifier): `did:key:z6Mk...` — cryptographic ID Frank generates and owns. Like a passport no government issued.
- **VC** (Verifiable Credential): A signed claim. ARC signs: *"Frank is a patient, DOB 1959."* Frank holds it. Shows it without exposing raw EHR data.

**Scenario:**
> Javier needs to book a specialist referral. Today: Frank has to call, give his name, DOB, insurance — to a receptionist who types it into Epic.
>
> Web 3.0: Javier presents Frank's VC from ARC. Specialist's agent verifies it cryptographically in 2 seconds. No phone call. No data entry. No fax.

**Maturity:** W3C standard (2022). Production SDKs exist (`did-resolver`, `@veramo/core`). **Ready now for design; Year 2 for implementation.**

---

### 2. SOLID Pods — Personal Data Sovereignty

**What it is:** Sir Tim Berners-Lee's answer to Big Tech owning your data. A **SOLID pod** is your personal data store — a server you control (or self-host). Apps don't store your data; they request read/write access to your pod with your permission.

**The lifeTracker parallel:** `<userData>/agents/` on Google Drive IS a proto-pod. Swapping Google Drive for a SOLID pod is a storage layer change, not an architecture change — because RecordAgent already abstracts all I/O.

**Scenario:**
> Frank's cardiologist's app wants to see his BP history. Today: Frank downloads a CSV from myAir, emails it.
>
> Web 3.0: Cardiologist's app requests read on `did:frank/agents/medical/vitals/bp/`. Javier approves. Cardiologist reads live data. Frank revokes access after the appointment.

**Maturity:** SOLID protocol spec is final. CSS (Community Solid Server) is production-grade. **Year 2–3 for lifeTracker adoption.**

---

### 3. Agent-to-Agent Protocols (MCP + A2A)

**What it is:** The infrastructure for agents talking to other agents, not just to humans.

| Protocol | Origin | What It Does |
|---|---|---|
| **MCP** (Model Context Protocol) | Anthropic (2024) | Tool/resource exposure standard — Javier already uses this (Gmail MCP, Google Calendar MCP) |
| **A2A** (Agent2Agent) | Google (2025) | Agent discovery + task delegation — agents find each other and hand off work |
| **ANP** (Agent Network Protocol) | Open standard (2025) | Peer-to-peer agent communication with DID-based authentication |

**Scenario:**
> Frank's HVAC needs replacing. Today: Frank calls 3 contractors, gets quotes by email, enters them in a spreadsheet.
>
> Web 3.0: Javier (houseAgent) sends an A2A task to a contractor registry. 3 licensed contractor agents respond with structured quotes (UANS-compatible JSON). Javier compares, checks Frank's moneyAgent for liquidity, makes a recommendation. Frank says yes. Javier books.

**Maturity:** MCP — production now. A2A — emerging (2025 spec). ANP — early draft. **MCP: already in use. A2A: Year 2 horizon.**

---

### 4. Zero-Knowledge Proofs (ZKPs) — Share Proof, Not Data

**What it is:** Cryptographic technique that proves a statement is true without revealing the underlying data.

**Why it matters for health + estate:**
- Prove *"Frank's A1C is below 7.5"* without sharing the lab value → insurance pricing
- Prove *"Frank is over 65"* without showing DOB → pharmacy discount
- Prove *"Frank has a valid advance directive on file"* without sharing the document → hospital system

**Scenario:**
> Frank applies for long-term care insurance. Today: 6-month underwriting process; 40-page medical questionnaire; full EHR release to insurer.
>
> Web 3.0: Javier generates a ZK proof bundle: conditions controlled (✓), no hospitalization in 3 years (✓), medications list within acceptable range (✓). Insurer's agent verifies the proofs. Policy issued in 48 hours. Insurer never sees a single lab value.

**Maturity:** ZK circuits (Circom, snarkjs) are production. Health-specific ZK toolkits are early (2025–2026). **Year 3+ for lifeTracker.**

---

### 5. Smart Contracts — Estate Execution (Crypto Web3 Intersection)

**What it is:** Self-executing code on a blockchain. When conditions are met, actions fire automatically.

**The narrow use case for Frank:** Estate execution — not speculation.

**Scenario:**
> Frank's estate plan has a TODD (Transfer on Death Deed) for Wimberley house. Today: it requires probate, an attorney, 6–18 months.
>
> Web 3.0: A death certificate VC is issued (county → DID registry). Javier's estate agent detects the VC. Smart contract fires: property title transfers to named beneficiary on-chain. Attorney involvement: zero for the transfer itself.

**Maturity:** Ethereum smart contracts — production. Legal recognition of blockchain estate execution: Texas has digital asset laws (HB 4474, 2023). Court precedent: thin but growing. **Year 4+ — legal maturity is the constraint, not tech.**

---

## Web 2.0 → Web 3.0 Evolution Map

```
TODAY                        YEAR 2              YEAR 3+
(BirthPlan)                  (Year2Plan)         (TrustedPlan+)
─────────────────────────────────────────────────────────────────
IDENTITY
  Passphrase + JWT         → DID created       → DID-based sessions
  users.json.gpg           → DID keystore      → VC wallet (Frank's credentials)
  user_id = "frank"        → did:key:z6Mk...   → SSI everywhere

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

## Technology Readiness Matrix

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

## Migration Timetable

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

### Year 2 — Web 2.5: Identity + Agent Protocols

**Trigger:** CertificationPlan complete. Javier is trusted. Time to give Frank a digital identity.

| Task | Module | Effort |
|---|---|---|
| Generate Frank's DID (`did:key`) | `core/identity/did_manager.py` | 1 session |
| DID-based JWT replacement | `core/auth/did_auth.py` | 1 session |
| VC wallet for Frank's health credentials | `core/identity/vc_wallet.py` | 2 sessions |
| Request ARC to issue patient VC (Epic SMART on FHIR) | `medicalAgent/fhir_vc.py` | 2 sessions |
| A2A task endpoint (Javier accepts inbound tasks) | `core/agent/a2a_server.py` | 2 sessions |
| A2A client (Javier delegates to external agents) | `core/agent/a2a_client.py` | 1 session |
| Encrypt Google Drive data at rest (GPG per-file) | `core/records/encrypted_store.py` | 1 session |

**Year 2 milestone test:**
> Javier presents Frank's ARC patient VC to a specialist's scheduling agent. Appointment booked without a phone call.

---

### Year 3 — Web 3.0 Foundation: SOLID + Agent Mesh

**Trigger:** Frank is comfortable with agent-assisted decisions. Time to own his data.

| Task | Module | Effort |
|---|---|---|
| Spin up SOLID pod (Community Solid Server on home server or VPS) | Infra | 1 session |
| `solid_store.py` — SOLID-compliant RecordAgent store | `core/records/solid_store.py` | 2 sessions |
| Migrate Google Drive data → SOLID pod | `wsCmd.py --migrate-to-pod` | 1 session |
| WebACL per agent namespace — scoped access control | `core/records/access_control.py` | 2 sessions |
| commMemory → federated threads (ANP or ActivityPub) | `core/comm/federated.py` | 3 sessions |
| Knowledge graph: agent-mesh cross-agent signals | `core/knowledge/graph.py` | 3 sessions |

**Year 3 milestone test:**
> Frank's cardiologist's app requests read access to `medical/vitals/bp/`. Javier approves. Access auto-revoked after 30 days. Frank never types his BP data again.

---

### Year 4+ — Full Autonomy: ZK + Smart Contracts

**Trigger:** Frank's estate plan is in order. Legal frameworks have caught up.

| Task | Effort | Notes |
|---|---|---|
| ZK proof generator for health disclosures | 3–5 sessions | Use `snarkjs` + health circuit libraries |
| Smart contract for TODD execution (Ethereum) | 3 sessions | Requires Texas legal validation |
| Death certificate VC receiver | 1 session | Watch county registrar DID issuance |
| Autonomous estate agent | 4 sessions | High stakes — human-in-the-loop for all actions |

**Year 4 milestone test:**
> Frank's long-term care insurer's agent receives a ZK proof bundle from Javier. Policy approved. Zero raw health data exchanged.

---

## What This Means for Javier's Identity

Today Javier is **Frank's app**.

Web 3.0 Javier is **Frank's agent** — a named, cryptographically-identified actor in the world with:

- A **DID** (`did:key:z6MkJavier...`) — Javier's own identity, separate from Frank's, but authorized by Frank
- An **A2A endpoint** — other agents can find Javier and send tasks
- A **VC authority** — Javier can issue credentials on Frank's behalf ("Frank authorized this contractor to bill $X")
- A **pod ACL role** — Javier manages who sees what in Frank's SOLID pod

This is the **agentic internet** — not agents as chatbots, but agents as actors with keys, permissions, and persistent relationships.

---

## What NOT to Build (Web 3.0 Traps)

| Trap | Why to Avoid |
|---|---|
| **Blockchain data storage** (Filecoin, Arweave) for health records | HIPAA + GDPR require right-to-delete; immutable ledgers conflict; SOLID is better |
| **Crypto wallets for estate assets** | Texas probate law + family complexity; smart contracts are enforcement layer, not asset layer |
| **Decentralize AI compute** (federated learning, blockchain ML) | Premature; Anthropic quality gap is enormous; revisit Year 4+ |
| **Token incentive economics** | No user community here; it's one principal's PA — tokens solve multi-stakeholder problems |
| **Build ANP from scratch** | Wait for the open standard to stabilize (2026–2027 window) |

---

## The One Sentence Summary

> **Build a clean Web 2.0 assistant now. Every abstraction layer you create today (RecordAgent, UANS, UserContext, MCP tools) is a Web 3.0 swap point later — and Javier evolves from an app into a sovereign agent who holds Frank's keys, owns his data, and speaks to the world on his behalf.**
