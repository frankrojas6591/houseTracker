# emotionalAgent Vision

*My Personal Assistant Ecosystem — One Trusted Advisor/Advocate backed by Expert Agents*

**Version:** 0.2 (Design Draft)
**Author:** Frank Rojas
**Date:** June 2026
**Parent:** [lifeTracker Vision](../../docs/lifeTrackerVision.md)
**UANS namespace:** `emotional.*`

---

## 1. Why an emotionalAgent?

The emotional life of a person in their 70s is not simpler than it was at 40 — it is more complex. Cumulative grief accumulates. Identity shifts as productive roles give way to elder roles. Fear of cognitive decline runs as background noise. Social networks thin naturally. And underneath all of it runs the deepest developmental task of late life: building integrity — the honest acceptance of one's life as it was lived — or sliding toward despair.

Most people in this life stage have no structured support for this inner work. A therapist sees you 50 minutes a week. A doctor may ask "how are you feeling?" in a two-minute check. Family means well but cannot be objective. The **emotionalAgent** fills this gap — not as a therapist or a companion, but as a *structured witness* that knows your emotional history deeply and helps you see patterns you cannot see yourself.

> The goal is not to make you feel better in the moment. It is to help you understand where you are emotionally — and to surface that understanding to you, to your medical team, and to the PersonalAssistant that coordinates your life.

---

## 2. Clinical Foundation

The emotionalAgent is grounded in three evidence-based frameworks with the strongest support for adults in their 70s:

### 2.1 Unified Protocol (Transdiagnostic CBT)

The Unified Protocol (Barlow et al.) applies a single CBT-based framework across depression, anxiety, grief, and worry — the four most common emotional challenges in late life. Rather than separate modules for each condition, it tracks a unified set of primitives:

- **Automatic thoughts** — the first thought that arises in response to an event
- **Cognitive patterns** — the style of thinking (catastrophizing, rumination, black-and-white, gratitude, acceptance)
- **Behavioral activation** — what the person is doing, avoiding, or withdrawing from
- **Emotional regulation** — what strategies are being used to cope

### 2.2 PERMA Model (Positive Psychology)

Seligman's PERMA model provides a proactive health lens — not just tracking distress but tracking flourishing. Daily check-in scores five domains:

| Domain | What It Measures |
|---|---|
| **P** — Positive Emotion | Overall emotional tone; ratio of positive to negative affect |
| **E** — Engagement | Flow states; feeling absorbed and purposeful in daily activity |
| **R** — Relationships | Quality and frequency of meaningful social contact |
| **M** — Meaning | Sense that one's life and actions matter; legacy orientation |
| **A** — Accomplishment | Progress on things that matter; sense of capability |

### 2.3 Erikson Stage 8 — Integrity vs. Despair

The organizing life-stage lens for the 70s. Every session has a background signal:

- **Integrity pathway**: life review that reaches acceptance, wisdom, gratitude for what was. Legacy work — stories, values transmission, relationships. Presence with what is rather than grief over what is not.
- **Despair pathway**: inability to accept the life lived; bitterness, regret, isolation, hopelessness. Untreated complicated grief often fuels despair.

The emotionalAgent tracks movement along this axis as a slow-moving signal across months, not a daily score.

### 2.4 Grief — Worden's Tasks of Mourning

Stage-based grief models are passive and poorly predictive. Worden's *Tasks of Mourning* are active and trackable:

1. **Accept the reality of the loss**
2. **Process the pain of grief**
3. **Adjust to a world without the deceased**
4. **Find an enduring connection while embarking on a new life**

When a loss is logged, the tracker records which tasks are in progress and flags prolonged grief indicators (grief exceeding 12 months with persistent impairment).

---

## 3. Key Life-Stage Considerations (70s)

| Challenge | Tracking Approach |
|---|---|
| **Cumulative grief** — loss of peers, siblings, spouse compounds | Each loss logged independently with task stage; a running grief load score surfaces when multiple active grief threads exist |
| **Identity transition** — loss of productive role (career, parenting) | Values-alignment score; legacy work entries; role description field that evolves over time |
| **Anticipatory grief** — preparation for one's own death | Explicit tracking mode: "forward grief" entries separate from loss grief; ties to faithAgent's end-of-life preparation |
| **Cognitive anxiety** — fear of dementia (distinct from clinical assessment) | Dedicated field; does NOT attempt to assess cognition — surfaces to medicalAgent for clinical evaluation |
| **Social thinning** — natural shrinkage of network | Social contact frequency and quality; isolation flag triggers PersonalAssistant alert when social contact drops below baseline for 2+ weeks |
| **Legacy and meaning** — primary protective factor against despair | Legacy work journal entries; values transmission notes; prompted monthly |

---

## 4. Agent Catalog

### 4.1 DailyCheckIn Agent (`emotional.core.checkin`)

Daily structured intake. 5 scored fields + one free-text reflection prompt. Takes 2–3 minutes. Voice-optimized.

**Scored fields:**
- Overall mood (1–10)
- Dominant emotion (from a curated list)
- Social contact quality today (1–5)
- Values alignment (did today match what matters most?) (1–5)
- Faith engagement (prayer / Mass / community — boolean flags)

**Free-text prompt (rotating weekly theme):**
- Week A: "What is weighing on you this week?"
- Week B: "What are you grateful for right now?"
- Week C: "Who matters most to you, and when did you last connect with them?"
- Week D: "What would you like to leave behind — a value, a story, a lesson?"

The LLM layer applies CBT/ACT lenses to the free text, extracts cognitive patterns, and writes the structured JSON record.

---

### 4.2 GriefCompanion Agent (`emotional.grief.companion`)

Activated when a loss is logged. Tracks progress through Worden's four tasks. Prompts gently on the natural timeline. Flags complicated grief indicators to medicalAgent.

---

### 4.3 LifeReview Agent (`emotional.legacy.review`)

Monthly. Draws from journal entries and cross-agent events to surface the emotional arc of the month. Frames it in Erikson Stage 8 terms: what moved toward integrity, what needs attention.

---

### 4.4 StressMonitor Agent (`emotional.stress.monitor`)

Subscribes to stress-flagged events from all other agents. Correlates domain stress (financial, home, health) with mood scores. Surfaces pattern: "Your mood scores drop significantly in the 2 weeks after a major house expense."

---

## 5. Records Structure — UANS

```
emotional.*
└── records/agents/
    ├── core/
    │   ├── checkin/          ← emotional.core.checkin
    │   │   ├── log.json      ← daily check-in entries (rolling 90 days active)
    │   │   └── action_items.json
    │   └── profile/          ← emotional.core.profile
    │       └── profile.json  ← emotional baseline, dominant patterns, Erikson stage assessment
    ├── grief/
    │   └── companion/        ← emotional.grief.companion
    │       ├── losses.json   ← loss registry with Worden task tracking
    │       └── action_items.json
    ├── legacy/
    │   └── review/           ← emotional.legacy.review
    │       ├── monthly.json  ← monthly life review summaries
    │       ├── journal.json  ← legacy work entries
    │       └── action_items.json
    └── stress/
        └── monitor/          ← emotional.stress.monitor
            ├── events.json   ← cross-domain stress events
            └── action_items.json
```

### Key JSON Schema: `emotional.core.checkin.log`

```json
{
  "entries": [
    {
      "entry_id":             "uuid",
      "date":                 "2026-06-27",
      "mood_score":           7,
      "mood_valence":         "positive",
      "dominant_emotion":     "gratitude",
      "social_contact":       { "count": 2, "quality": 4, "isolation_flag": false },
      "values_alignment":     4,
      "faith":                { "prayer": true, "mass": false, "community": false },
      "cognitive_patterns":   ["gratitude", "acceptance"],
      "stress_events":        [],
      "free_text":            "Called Maria today — good conversation.",
      "llm_reflection":       "Strong values alignment and social connection today...",
      "perma":                { "P": 7, "E": 6, "R": 8, "M": 7, "A": 5 },
      "crisis_flag":          false,
      "referral_suggested":   false
    }
  ]
}
```

---

## 6. Cross-Agent Integration

| Agent | What emotionalAgent Receives | What It Sends |
|---|---|---|
| **medicalAgent** | Diagnosis events, chronic pain scores, medication changes — all elevate depression/anxiety risk | Mood trend and distress scores; complicated grief flags; cognitive anxiety entries |
| **moneyAgent** | Financial stress events (unexpected expenses, market losses, estate decisions) | Emotional load level (informs how much moneyAgent should surface at once) |
| **houseAgent** | Home crises (major repairs, relocation risk) — identity threat for seniors | None directly |
| **faithAgent** | Mass attendance, prayer consistency, community engagement (resilience factors) | Life-stage emotional context; grief entries that may need spiritual support |
| **PersonalAssistant** | Priority arbitration context; overall life event stream | Current emotional load level; crisis flags (immediate escalation); weekly trend summary |

---

## 7. Ethical Guardrails

This is a personal tool — not a clinical service. The following guardrails are hard-coded:

1. **Non-clinical disclaimer** injected at every session start and when distress scores exceed threshold
2. **Crisis protocol**: any mention of hopelessness, suicidal ideation, or self-harm halts the session immediately and outputs crisis resources (988 Suicide & Crisis Lifeline, local emergency contact on file)
3. **No relationship simulation**: the agent is a tracker and reflector — never a companion or friend substitute
4. **Referral suggestion logging**: every time the agent suggests professional support, the suggestion is timestamped and logged
5. **Trusted contact alert**: if crisis flag is raised or mood score averages below 3 for 7+ days, a summary is flagged for a designated trusted contact (family member, physician)
6. **Session context rotation**: journal entries older than 90 days are summarized and archived — preventing context drift that could erode safety guardrails

---

## 8. Design Principles

1. **Structured witness, not therapist.** The tracker observes, patterns, and reflects. It does not treat, counsel, or advise clinically. It creates the conditions for self-understanding.

2. **Integrity as the north star.** Every feature asks: does this help the person move toward integrity — honest acceptance and meaning-making — or does it reinforce avoidance and rumination?

3. **Brevity is kindness.** A 70-year-old with emotional weight does not need a 20-question daily survey. Five scored fields and one open prompt. The LLM does the synthesis work.

4. **Grief deserves its own architecture.** Grief is not "low mood." It gets its own agent, its own tracking model, and its own patient timeline.

5. **The emotional load informs everything else.** The PersonalAssistant should know the owner's current emotional load before routing any other tracker's output. A person in active grief should receive fewer action items, simpler language, and more frequent check-ins.

---

## 9. Open-Source Reference Projects

| Project | Relevance |
|---|---|
| [neuhai/Mental-LLM](https://github.com/neuhai/Mental-LLM) | LLM-based mental health prediction from text; distress pattern research |
| [EmocareAI/ChatPsychiatrist](https://github.com/emocareai/chatpsychiatrist) | Instruct-tuned LLaMA on counseling domain data; system prompt architecture reference |
| Barlow Unified Protocol (Oxford UP) | Transdiagnostic CBT framework; freely documented; basis for the cognitive pattern taxonomy |
| Seligman PERMA | Positive psychology measurement; 5-item daily scoring widely validated |

---

## 10. Implementation Plan

| Phase | Milestone |
|---|---|
| 0 | Records scaffold — UANS directory tree, stub JSON files |
| 1 | DailyCheckIn agent — voice check-in via Twilio; JSON record written; mood trend visible in web UI |
| 2 | GriefCompanion agent — loss logging, Worden task tracking, complicated grief flag |
| 3 | StressMonitor — subscribe to cross-agent stress events; correlation surfacing |
| 4 | LifeReview agent — monthly summary, Erikson framing, legacy journal |
| 5 | PersonalAssistant integration — emotional load informs PA routing and communication style |
