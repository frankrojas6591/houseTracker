# lifeTracker — commMemory Design

**Version:** 1.1
**Date:** June 2026
**Parent:** [Design Index](./lifeTracker_design.md)

---

## 1. Purpose

**commMemory** is the universal communication memory layer for the entire lifeTracker ecosystem. It is a core common service — not a discipline agent — that sits between all inbound channels (web UI, iOS voice, email, Twilio) and the PA.

Two responsibilities:

1. **Universal thread store** — every conversation, email, and voice interaction is captured as a thread, regardless of channel. One place to see all communication history.
2. **STM/LTM priority management** — threads are classified by ownership and priority. High-priority agent-owned threads flow to their owning agent. Lower-priority threads are retained in commMemory's own store with a 12-month LTM horizon.

```
All channels → commMemory → classify + prioritize
                              │
                 80–100 (agent threads) → owning agent (house, medical, money…)
                 0–79  (memory threads) → commMemory STM/LTM store → monthly PA review
```

**commEmail** is commMemory's primary sub-agent for the email channel — responsible for Gmail ingestion and outbound PA drafts.

### Phase 0c Goals

1. Configure and seed commMemory with commEmail
2. Connect Gmail: classify 12 months of existing email across agent namespaces
3. Seed commMemory STM/LTM store with the initial classified thread set
4. Deliver to PA a narrative summary of the email seed moment

---

## 2. Two Roles commEmail Plays

```
ROLE 1 — INGESTION (Gmail → agents)
  commEmail arrives → classified by agent → stored as RecordAgent record
  "Tax appraisal letter scanned from email → house.finance.tax.appraisal_2026"
  "Lab results confirmation → medical.health.labs.arc_2026_06"
  "Contractor quote → house.systems.hvac.quotes"

ROLE 2 — OUTBOUND (agents → Gmail)
  Agent action item → PA drafts summary → sent to principal's Gmail
  Monthly check-in report → delivered to inbox
  Urgent alert → immediate email ("your HVAC warranty expires in 7 days")
```

---

## 3. Gmail Integration

The Gmail MCP server (`mcp__claude_ai_Gmail__*`) provides direct access to the principal's Gmail account. No separate OAuth setup needed for development — the MCP server handles auth.

### Available Operations

| Operation | MCP Tool | Use |
|---|---|---|
| Search email | `search_threads` | Find emails by subject, sender, date range |
| Read thread | `get_thread` | Get full email content for classification |
| Draft reply/send | `create_draft` | PA sends summary or alert |
| Label management | `label_thread` | Tag email as processed by lifeTracker |
| List labels | `list_labels` | Discover existing Gmail label structure |

---

## 4. commEmail Ingestion Pipeline

```
Gmail Inbox
    │
    ▼  search_threads(query="is:unread after:2026/01/01")
    │
    ▼  get_thread(thread_id) → full email text
    │
    ▼  IntentParser (Haiku)
    │    → {agent: "house", category: "finance.tax",
    │        record: "appraisal_2026", action: "record", summary: "..."}
    │
    ▼  RecordAgent.write(uans, data)
    │    → <userData>/agents/house/kingsway_dr/finance/tax/appraisal_2026.json
    │
    ▼  label_thread(thread_id, label="lifeTracker/house/processed")
```

### commEmail Classifier System Prompt (Haiku)

```
You are Javier's email classifier. Given an email thread, identify:
1. Which lifeTracker agent owns this: house, medical, money, estate, emotional, faith, or memory
2. UANS category and record name (e.g. "finance.tax.appraisal_2026")
3. A 1-sentence summary of the key fact or action needed
4. Whether this requires immediate action (bool)

If the email is personal/social/spam with no life-management relevance, return agent: "ignore".

Respond as JSON only: {agent, uans, summary, action_required}
```

### 4.1 commMemory Agent 

The commMemory Agent has 2 tasks:
1. Classify any incoming thread (email, IOS voice, UI) that are not owned by an existing lifeTracker Agent.
    - threads are classified as agentThread
3. Prioritize the importantance of memory threads.
    - the priorities of memory threads is expected to constantly shift.
    - Priorities are weighted 0-100
        - 80-100 : these are reserved for lifeTracker agents
        - 50-79  : these are threads that the principle user has interests in
        - 25-49  : these are threads the principle has no interest but need some level of attention within a period of 3 months
        - 0-24.  : these are junk, ignore, advertisements/promotions of no interest to the principal user.

### commMemory Management

|  Ownership   |  Prio  |          STM                 |          LTM               |
|--------------|--------|------------------------------|----------------------------|
|agentThreads  | 80-100 | passed to agent (traced)     |  NA: stored in agent store |
|memoryThreads |  0-79  | stored in commMemory store   |  retained for 12 months.   |

The commEmail Memory Agent should schedue a monthly check-in with the PA to provide a summary of activities (memory threads 0-79), and top items needing possible attention.    Over time, the commEmail Memory Agent with the PA learn what is important and what is not important.   Mistakes are bound to happen - learn and move forward. 

---

## 5. Outbound commEmail

### When PA Sends commEmail

| Trigger | Content | Timing |
|---|---|---|
| Monthly check-in complete | Full life review summary (all 6 agents) | 1st of month |
| Urgent action item | One-line alert + link to web UI | Immediately on detection |
| `wsCmd.py --email` import complete | "Classified N emails → X agents" digest | After batch import |
| Principal request via chat | "commEmail me a summary of my HVAC history" | On demand |

### Draft Format

PA composes email using the Sonnet synthesizer in `web_mode` (full structured text, not the 3-sentence voice cap):

```python
def send_summary(subject: str, body: str, config: dict) -> None:
    """Create Gmail draft for principal review, or send directly if auto_send=True."""
    # create_draft returns draft_id; principal reviews in Gmail or approves via web UI
```

Default: **draft mode** — PA creates a draft, principal reviews and sends. Auto-send enabled only for urgent alerts (opt-in in config).

---

## 6. `wsCmd.py --email` — Batch Import

The batch import is run once (or periodically) to pull historical email into agent records.

```
$ python wsCmd.py --email

lifeTracker commEmail Import
========================
Gmail search window [last 365 days]: 
Dry run (preview without writing)? [Y/n]: Y

Scanning Gmail... found 847 threads
Classifying...
  house:   142 threads (tax letters, contractor quotes, HOA, utilities)
  medical:  89 threads (appointment confirmations, lab results, insurance)
  money:    201 threads (statements, tax forms, investment notices)
  estate:   23 threads (attorney, insurance, deed)
  faith:    12 threads
  ignore:  380 threads (personal, news, shopping)

Dry run complete. Write 467 records? [y/N]: y
Writing... done.
Labels applied: lifeTracker/<agent>/processed
```

---

## 7. Flask Routes — `ui/email.py`

| Route | Method | Description |
|---|---|---|
| `GET /email/inbox` | GET | Show unclassified lifeTracker emails in web UI |
| `POST /email/classify` | POST | Manually reclassify a thread to a different agent |
| `POST /email/import` | POST | Trigger batch import (same as `wsCmd.py --email`) |
| `GET /email/drafts` | GET | Review pending outbound PA email drafts |
| `POST /email/send/<draft_id>` | POST | Approve and send a PA draft |

---

## 8. Config Fields

Add to `~/.lifeTracker/config.json`:

```json
{
  "email": {
    "auto_send_alerts": false,
    "import_days_back": 365,
    "processed_label": "lifeTracker",
    "summary_recipient": "frankr6591@gmail.com"
  }
}
```

---

## 9. Phase 0c Milestone

**Milestone:** `wsCmd.py --email --dry-run` classifies 50+ Gmail threads correctly. At least one record written to each active agent namespace. PA can draft a summary email.

| Task | Module | Notes |
|---|---|---|
| Gmail search + fetch | `core/email/gmail_client.py` | Wraps MCP Gmail tools |
| commEmail classifier | `core/email/classifier.py` | Haiku IntentParser variant |
| Batch import | `wsCmd.py --email` | Dry run + write modes |
| Outbound draft | `core/email/sender.py` | Draft or send via MCP |
| Web UI | `ui/email.py` | Inbox review + draft approval |
| Milestone test | — | `--dry-run` on 12 months Gmail; review classification accuracy |
