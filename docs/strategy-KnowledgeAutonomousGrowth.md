# Strategy: Knowledge & Autonomous Growth

**Version:** 1.0
**Date:** June 2026

---

## The Goal

Five years from now, Javier should be able to tell the story of your life — not just the facts, but the texture:

> *"Frank, remember 2026 when the Kingsway HVAC died the week after you replaced the water heater? You were convinced your house had it in for you. We ended up getting a heat pump — which turned out to cut your summer electric bill by 40%. That's why we set the 10-year HVAC replacement budget at $18K."*

That is the test: **can the agent narrate your life in its discipline?** Not just data retrieval. Story. Humor. Pattern. Wisdom earned from your specific decisions over time.

---

## How Agents Learn — In Plain English

Think of each agent like a new specialist you hire. On day one, they know their profession. By year two, they know *you* — your quirks, your history, your preferences.

There are three layers of what they know:

```
Layer 1 — Facts          (your records: dates, costs, decisions)
Layer 2 — Your Story     (what happened, why you decided, what you were feeling)
Layer 3 — Your Patterns  (your habits, your risk tolerance, your blind spots)
```

All three layers grow over time. RecordAgent stores Layer 1. Layers 2 and 3 accumulate through conversation and reflection.

---

## The Memory Architecture

### What an LLM Actually Is

An LLM (like Claude) has no memory between conversations. Every time you talk to Javier, it's like the first day on the job — **unless you give it context**. That context is the memory system.

lifeTracker's memory system has three components:

```
┌─────────────────────────────────────────────────┐
│  LONG-TERM MEMORY  (Google Drive — always there) │
│  Records, profile, decisions, logs               │
│  Format: structured JSON in <userData>/agents/   │
└─────────────────────────────────────────────────┘
                        │
                        │  (loaded at query time)
                        ▼
┌─────────────────────────────────────────────────┐
│  WORKING CONTEXT  (injected into each request)  │
│  Recent conversations, relevant records,         │
│  UserContext (who you are, what you have)        │
│  Format: text injected into the LLM prompt       │
└─────────────────────────────────────────────────┘
                        │
                        │  (agent generates response)
                        ▼
┌─────────────────────────────────────────────────┐
│  NEW MEMORY  (written back to Google Drive)     │
│  Agent writes insights, patterns, follow-ups     │
│  via RecordAgent → persists for next session     │
└─────────────────────────────────────────────────┘
```

---

## DAG vs. No DAG — The Honest Answer

**What's a DAG?** A Directed Acyclic Graph — a way to link knowledge nodes with relationships:

```
"HVAC failure" ──causes──► "Financial stress"
                                    │
                              affects
                                    ▼
                          "Emotional tension in June 2026"
                                    │
                              noted by
                                    ▼
                          "faithAgent: consolation in difficulty"
```

**Should lifeTracker use a DAG?** Not yet. Here's why:

| Approach | What it does | Verdict |
|---|---|---|
| **Structured JSON** (Phase 0–2) | Stores facts reliably; LLM reads them as context | ✅ Start here |
| **Episodic log** (Phase 2–3) | Timestamped conversation & event history; agent can "remember last time" | ✅ Add in Year 1 |
| **Vector RAG** (Phase 3–4) | Semantic search over years of records; "anything like this before?" | ✅ Add in Year 2 |
| **Knowledge graph / DAG** (Phase 4+) | Cross-agent relationship reasoning | 🔜 Year 2–3 only if needed |

**The practical rule:** Start with structured records + good context injection. Add a knowledge graph only when you have enough history that semantic search alone isn't capturing the cross-domain connections. That's a Year 2 problem.

---

## Phase-by-Phase Knowledge Growth

### BirthPlan (Year 1, Phases 0–6) — *Structured Records + Episodic Log*

Each agent starts with a blank slate and grows by:

1. **Intake questionnaire** (`wsCmd.py --setup`) — structured onboarding captures baseline knowledge per agent
2. **Conversation logging** — every interaction is recorded in `<userData>/agents/<namespace>/life/log.json`
3. **Record writing** — every event the principal reports is stored via RecordAgent
4. **Monthly briefing** — agent synthesizes its records into a 3-sentence current status

**What the agent "knows" at end of Year 1:**
- Full baseline profile (house, medical, finances, estate, emotional, faith)
- Every event reported through the year
- 12 monthly briefings — a year's worth of narrated history
- Open action items carried forward

---

### CertificationPlan (Year 1 → Year 2) — *Value Assessment*

**The question:** Is the agent adding value? Can it tell your story?

Test: ask each agent to narrate the year. If the narrative is accurate, personal, and catches things you forgot — the agent has earned its certification.

Certification is measured in:
- How often you consult the agent (frequency)
- Tasks the agent surfaced that you acted on (burden reduction)
- Connections the agent made you weren't aware of (synthesis value)

---

### Year2Plan (Year 2) — *Vector Search + Steady State*

Add **vector embeddings** over the growing record store:

- Every significant event is embedded (converted to a semantic fingerprint)
- When you ask a question, the agent retrieves the most relevant past events automatically
- This is how the agent starts to catch patterns: "This feels like the Q3 2026 HVAC situation..."

Tools at this stage: ChromaDB or FAISS running locally alongside RecordAgent.

---

### TrustedPlan (Year 3+) — *Cross-Agent Signals*

The PA begins to synthesize cross-agent patterns:

> *"Frank, I notice a pattern: every time a major house expense hits, your emotional check-ins drop off for 2–3 weeks. We should build a financial buffer trigger that prompts a check-in when a project goes over $5K."*

This is lightweight graph reasoning — not a full DAG, but the PA tracking relationship signals between agents and surfacing them proactively.

---

## Quick Response + Deep Thinking

The agent serves two modes simultaneously:

```
QUICK (synchronous — you wait)
  Haiku model + cached recent context
  Responds in ~1 second
  "What's the HVAC filter status?" → immediate answer

DEEP (asynchronous — background)
  Opus/Sonnet model + full record analysis
  Runs after the quick response is sent
  Stored back in RecordAgent when complete
  Surfaces at next check-in or via notification
  "Is this house on track for aging-in-place by 2030?" → deep analysis
```

**Implementation pattern (Phase 2+):**

```python
def handle_query(question, user_ctx, agent):
    quick = agent.query(question, context=recent_context(user_ctx))
    respond_immediately(quick)

    if requires_deep_analysis(question):
        enqueue_background_task(agent.deep_analysis, question, user_ctx)
```

Background tasks write their findings to `<userData>/agents/<namespace>/life/insights.json`. The PA surfaces them at the next monthly check-in.

**Cost rule:**
- Haiku for quick response: ~$0.001/query
- Opus for deep analysis: ~$0.05/analysis, triggered only when the question warrants it
- Monthly deep review: one Opus call per agent per month (~$0.30/month total)

---

## The Knowledge Test

At any point, ask an agent: *"Tell me the story of my house since January."*

A passing answer:
> *"The year started well — January inspection found no issues. Then March hit hard: you discovered the water heater was 17 years old and replaced it proactively for $1,400. Two months later the HVAC compressor failed on the hottest week of June. You almost patched it, but we ran the numbers and the heat pump made more sense at $12,800. You used the HELOC. The rest of the year was quiet — no major systems events. October: you finally got the gutter guards installed. Smart call before winter."*

A failing answer:
> *"I have records of a water heater replacement in March 2026 and an HVAC system replacement in June 2026."*

The difference is **narrative synthesis** — agents earn this through accumulated episodic logs, not just structured records. This is why every conversation is logged from Day 1.
