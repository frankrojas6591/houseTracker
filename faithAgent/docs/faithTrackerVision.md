# faithAgent Vision

*My Personal Assistant Ecosystem — One Trusted Advisor/Advocate backed by Expert Agents*

**Version:** 0.2 (Design Draft)
**Author:** Frank Rojas
**Date:** June 2026
**Parent:** [lifeTracker Vision](../../docs/lifeTrackerVision.md)
**UANS namespace:** `faith.*`

---

## 1. Why a Faith Tracker?

Faith is not a weekend activity — it is a practice. And like any practice, it has structure, rhythm, and seasons. A Catholic life is shaped by daily prayer, the Eucharist, the liturgical calendar, the sacraments, the examination of conscience, and works of service. These practices compound. They build spiritual resilience that shows up everywhere else in life — in how grief is processed, in how uncertainty is held, in how legacy is understood.

The **faithAgent** is not a piety meter or a sin ledger. It is a *practice companion* — a structured witness to your spiritual life that helps you see where you are in the rhythms of faith, notice when the practice drops, and prepare thoughtfully for the end of life in a way that is spiritually grounded.

> The Ignatian tradition calls it the Examen — a daily review of where God was present and where you moved toward or away from that presence. The faithAgent makes this practice habitual and cumulative, so that over months and years, you can see the arc of your spiritual life, not just today's mood.

In the 70s, the spiritual tasks are specific and urgent: building an integrated sense of life meaning (legacy), preparing for death in the full Catholic tradition, maintaining the community ties that sustain faith as mobility decreases, and giving the next generation what only you can give — the transmission of values, faith, and story.

---

## 2. Catholic Spiritual Practice Framework

### 2.1 Practice Tiers

**Daily:**
- Morning offering
- Mental prayer / rosary (partial or full)
- Scripture reading (even one verse)
- Examination of conscience (Examen) at day's end

**Weekly:**
- Sunday Mass (obligatory)
- Daily Mass (aspirational; track when achieved)
- Eucharistic adoration (aspirational)

**Monthly:**
- Confession (recommended 1–2× for serious practitioners; annually is the minimum)
- Review of personal spiritual goals and intentions

**Seasonal / Liturgical:**
- Lenten practices: Stations of the Cross, fasting, almsgiving, additional confession
- Advent practices: Advent wreath, daily reflection
- Feast days: patron saints, major solemnities — log attendance and observance

**Sacramental milestones (lifetime log):**
- Confession dates (note: date and optional brief note — no content)
- Anointing of the Sick (date, circumstances, priest — end-of-life critical data)

**Service / Community:**
- Corporal Works of Mercy (feeding, visiting the sick, sheltering)
- Parish roles (lector, Eucharistic minister, committee, council)
- Charitable giving (time and treasure)

---

### 2.2 Liturgical Calendar

The Catholic year has five seasons. Every practice log entry is tagged with the current liturgical season and feast, giving the practice its proper context.

| Season | Approximate Dates (2026) | Character |
|---|---|---|
| **Advent** | Nov 29 – Dec 24 | Waiting, preparation, hope |
| **Christmas** | Dec 25 – Jan 11 | Incarnation, joy, light |
| **Ordinary Time (winter)** | Jan 12 – Mar 3 | Daily discipleship |
| **Lent** | Mar 4 – Apr 18 | Penance, conversion, fasting |
| **Easter** | Apr 19 – Jun 7 | Resurrection, joy, mission |
| **Ordinary Time (summer/fall)** | Jun 8 – Nov 28 | Growth, stewardship |

**2026:** Sunday Cycle Year A; Weekday Cycle Year II.

**Implementation:** Pull from [LiturgicalCalendarAPI](https://github.com/Liturgical-Calendar/LiturgicalCalendarAPI) — a PHP REST endpoint that returns diocese-aware JSON/ICS for any year, sourced from official Roman Missal decrees. Cache daily as `faith.liturgical.cache/<year>.json`. Each practice log entry is auto-tagged with `season`, `liturgical_color`, `feast_name`, `feast_rank`.

---

## 3. Ignatian Spiritual Direction

The faithAgent's reflection layer is grounded in **Ignatian Spirituality** — specifically the Daily Examen and the framework of consolation/desolation.

### 3.1 The Daily Examen (5 Steps)

The Examen is a 10–15 minute daily prayer of review. The faithAgent LLM agent guides this interactively or accepts a free-form reflection and structures it into five sections:

1. **Presence** — Become aware of God's presence in this moment
2. **Gratitude** — Review the day; identify gifts received
3. **Emotions** — Pay attention to feelings during the day — what moved you?
4. **Focal moment** — Choose one moment and pray from it
5. **Tomorrow** — Look forward; what intention do you carry into tomorrow?

### 3.2 Consolation / Desolation

Ignatius defined the spiritual temperature of the soul in two states:

| State | Characteristics | Daily Score |
|---|---|---|
| **Consolation** | Peace, faith, hope, generosity, movement toward God | +1 to +3 |
| **Neutral** | Ordinary — neither pulled toward nor away | 0 |
| **Desolation** | Spiritual heaviness, isolation, distraction, diminished prayer, movement away from God | -1 to -3 |

The `consolation_score` is the primary cross-agent signal to emotionalAgent. A sustained desolation trend (score ≤ −1 for 7+ days) triggers an alert and suggests a deeper reflection prompt.

### 3.3 Discernment Framework

For major life decisions with a faith dimension (estate choices, end-of-life preferences, major service commitments), the faithAgent logs the discernment process: the question, the period of prayer and reflection, the movements felt (consolation / desolation), and the resolution. This becomes part of the ethical will.

---

## 4. Senior Life-Stage Considerations

| Challenge | Tracking Approach |
|---|---|
| **Legacy and generativity** | Ethical will journal — structured prompts each month for values, stories, and blessings to pass on |
| **Grief of peers and community thinning** | Grief entries with prayer intention; rosary offered for the deceased; grief log linked to emotionalAgent |
| **Anticipatory death preparation** | Advance spiritual care directive (see §7); spiritual preparation for death is a first-class record, not an afterthought |
| **Anointing of the Sick** | Each celebration logged with date, priest, and circumstances — this record becomes essential at end of life |
| **Community continuity** | Parish role and engagement tracking; alert when engagement drops significantly (mobility-related isolation risk) |
| **Cumulative gratitude** | Life review prompts monthly; gratitude practice as antidote to despair (Erikson's integrity vs. despair) |

---

## 5. Agent Catalog

### 5.1 DailyPractice Agent (`faith.practice.log`)
Records daily practice checklist — what was completed, liturgical context, location for Mass. Simple, low-friction, voice-friendly: "Did you pray this morning? Did you attend Mass?"

### 5.2 ExamenReflection Agent (`faith.reflection.journal`)
The reflection companion. Guides the five-step Examen or accepts free-form reflection and structures it. Extracts consolation score, gratitude items, and tomorrow's intention. The LLM prompt is encoded with Ignatian framing — not as a director, but as a structured guide.

### 5.3 SacramentalHistory Agent (`faith.sacramental.history`)
Logs confession dates (date only — never content), Anointing of the Sick events (full record: date, priest, church, circumstances), and other sacramental milestones. At end of life, this record tells the care team what spiritual sacraments have been received and what remains.

### 5.4 CommunityLife Agent (`faith.community.commitments`)
Tracks parish roles, volunteer commitments, service hours, and charitable giving. Surfaces to PersonalAssistant's monthly check-in for calendar awareness. Flags when community engagement drops.

### 5.5 LiturgicalCalendar Agent (`faith.liturgical.cache`)
Pulls from LiturgicalCalendarAPI and caches the full year. Serves as a lookup for all other agents — every practice entry is auto-enriched with season, feast, and liturgical color.

### 5.6 EthicalWill Agent (`faith.legacy.ethical_will`)
Scaffolds the ethical will — a written document passing on values, faith, stories, and blessings to the next generation. Monthly structured prompts; drafts saved and refined over time. Separate from the legal will (which handles possessions); this handles meaning.

### 5.7 CharitableGiving Agent (`faith.charitable.giving`)
Tracks donations, tithing, legacy gift pledges (to parish, diocese, or Catholic charities), and Corporal Works of Mercy hours. Feeds estateAgent's beneficiary and bequest records.

---

## 6. Records Structure — UANS

```
faith.*
└── records/agents/
    ├── practice/
    │   ├── log/               ← faith.practice.log
    │   │   ├── log.json       (rolling 90-day active entries, annual archives)
    │   │   └── action_items.json
    │   └── calendar/          ← faith.liturgical.cache
    │       └── 2026.json      (full year cached from LiturgicalCalendarAPI)
    ├── reflection/
    │   └── journal/           ← faith.reflection.journal
    │       ├── examen_log.json
    │       └── discernment_log.json
    ├── sacramental/
    │   └── history/           ← faith.sacramental.history
    │       ├── confessions.json
    │       ├── anointing.json
    │       └── action_items.json
    ├── community/
    │   └── commitments/       ← faith.community.commitments
    │       ├── parish_roles.json
    │       ├── service_log.json
    │       └── action_items.json
    ├── legacy/
    │   └── ethical_will/      ← faith.legacy.ethical_will
    │       ├── drafts.json
    │       ├── prompts_completed.json
    │       └── action_items.json
    └── charitable/
        └── giving/            ← faith.charitable.giving
            ├── donations.json
            ├── bequests.json
            └── action_items.json
```

### Key JSON Schema: `faith.reflection.journal`

```json
{
  "examen_entries": [
    {
      "entry_id":         "uuid",
      "date":             "2026-06-27",
      "liturgical_season":"Ordinary Time",
      "feast":            "Our Lady of Perpetual Help",
      "examen": {
        "presence":     "Felt close during Mass, distracted at work",
        "gratitude":    ["Good health today", "Phone call with Maria"],
        "emotions":     "Peace in the morning; mild anxiety mid-afternoon",
        "focal_moment": "Offered the anxiety during Communion",
        "tomorrow":     "Morning prayer before doctor appointment"
      },
      "consolation_score": 2,
      "petitions":        ["healing for Maria", "guidance on estate decision"],
      "practices_today":  ["mass", "rosary", "examen"]
    }
  ]
}
```

---

## 7. Advance Spiritual Care Directive

A first-class record that lives in faithAgent and is referenced by medicalAgent and estateAgent:

```json
{
  "priest_present_at_death": true,
  "last_rites_requested":    true,
  "anointing_preferences":   "Call Fr. [Name] at [Parish] first",
  "funeral_preferences":     "Traditional Latin Mass if possible; burial, not cremation",
  "music_preferences":       ["Ave Maria", "Salve Regina"],
  "readings_preferences":    ["Psalm 23", "John 14:1-6"],
  "obituary_wishes":         "Emphasize faith, family, and service",
  "last_reviewed":           "2026-06-27"
}
```

---

## 8. Cross-Agent Integration

| Agent | What faithAgent Sends | What It Receives |
|---|---|---|
| **emotionalAgent** | `consolation_score` (daily); grief event when peer/family dies | Major life events that may need spiritual response |
| **medicalAgent** | Advance spiritual care directive; anointing history | Health events that suggest spiritual preparation |
| **estateAgent** | Charitable bequest intentions; ethical will draft | Estate events that may need faith-informed discernment |
| **PersonalAssistant** | Community commitments (for calendar); consolation trend (for emotional load calibration) | Monthly life event stream (enables prayer intention logging for major events across domains) |

---

## 9. AI Layer

### 9.1 ExamenReflection LLM

The LLM's role in faithAgent is the most carefully constrained of all agents:

- **Persona**: structured Examen guide — asks the five questions, listens, reflects back what it heard
- **NOT**: spiritual director, confessor, or theological advisor
- **Framework**: encode the Ignatian Examen steps as a structured system prompt with JSON output fields
- **Doctrine layer**: for catechetical or doctrinal questions, use [Magisterium AI](https://www.magisterium.com/) API as a secondary retrieval source (30,000+ Catholic texts, Church-aligned)

### 9.2 Ethical Will Prompts

Monthly rotating prompts for the ethical will — generated by the LLM based on the current liturgical season and recent life events:
- *Advent*: "What are you hoping for, and what hope do you want to leave your children?"
- *Lent*: "What do you want to ask forgiveness for, and what forgiveness do you want to extend?"
- *Easter*: "What has been resurrected in your life — returned after loss?"
- *Ordinary Time*: "What does faithfulness look like in your daily life right now?"

---

## 10. Design Principles

1. **Structure is a gift, not a burden.** The Catholic spiritual life has centuries of tested structure — the Examen, the liturgical calendar, the sacraments. The faithAgent does not invent a new framework; it makes the existing framework habitual and visible.

2. **The consolation score is the primary signal.** One number, tracked daily, tells more about the spiritual life than any other metric. It is also the most important cross-agent signal to emotionalAgent.

3. **End-of-life preparation is not morbid — it is faithful.** The advance spiritual care directive, the sacramental history, the ethical will — these are gifts faithAgent helps the owner prepare while they have the clarity and the time.

4. **No replacement of human community.** The faithAgent does not substitute for a confessor, a spiritual director, or a parish community. It supports and strengthens the practice that connects to those human relationships.

5. **Voice-friendly, never burdensome.** The daily check-in is three questions. The Examen is five. The monthly ethical will prompt is one. The faithAgent must never feel like homework.

---

## 11. Implementation Plan

| Phase | Milestone |
|---|---|
| 0 | Records scaffold; liturgical calendar cache populated for current year |
| 1 | DailyPractice agent — voice check-in; practice log written; liturgical context auto-tagged |
| 2 | ExamenReflection agent — guided Examen via voice; consolation score logged; cross-posted to emotionalAgent |
| 3 | SacramentalHistory — back-fill known confession/anointing dates; advance spiritual care directive drafted |
| 4 | EthicalWill agent — first ethical will session; monthly prompts active |
| 5 | CommunityLife + CharitableGiving — parish roles and giving tracked; bequest intentions fed to estateAgent |
| 6 | PersonalAssistant integration — consolation trend and community commitments surface in monthly check-in |
