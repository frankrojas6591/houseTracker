# lifeTracker — Email Channel Design

**Version:** 1.0
**Date:** June 2026
**Parent:** [Design Index](./lifeTracker_design.md)

---

## 1. Purpose

Email is both an **ingestion channel** (statements, appointment confirmations, contractor quotes, legal notices all arrive by email) and a **communication channel** (Javier sends summaries, action item reminders, and alerts to the principal).

Phase 0c goal: connect Gmail so agents can learn from what's already there — years of house, medical, financial, and legal correspondence that exists right now, before any agent is built.

---

## 2. Two Roles Email Plays

```
ROLE 1 — INGESTION (Gmail → agents)
  Email arrives → classified by agent → stored as RecordAgent record
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

## 4. Email Ingestion Pipeline

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

### Email Classifier System Prompt (Haiku)

```
You are Javier's email classifier. Given an email thread, identify:
1. Which lifeTracker agent owns this: house, medical, money, estate, emotional, faith, or ignore
2. UANS category and record name (e.g. "finance.tax.appraisal_2026")
3. A 1-sentence summary of the key fact or action needed
4. Whether this requires immediate action (bool)

If the email is personal/social/spam with no life-management relevance, return agent: "ignore".

Respond as JSON only: {agent, uans, summary, action_required}
```

---

## 5. Outbound Email

### When PA Sends Email

| Trigger | Content | Timing |
|---|---|---|
| Monthly check-in complete | Full life review summary (all 6 agents) | 1st of month |
| Urgent action item | One-line alert + link to web UI | Immediately on detection |
| `wsCmd.py --email` import complete | "Classified N emails → X agents" digest | After batch import |
| Principal request via chat | "Email me a summary of my HVAC history" | On demand |

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

lifeTracker Email Import
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
| Email classifier | `core/email/classifier.py` | Haiku IntentParser variant |
| Batch import | `wsCmd.py --email` | Dry run + write modes |
| Outbound draft | `core/email/sender.py` | Draft or send via MCP |
| Web UI | `ui/email.py` | Inbox review + draft approval |
| Milestone test | — | `--dry-run` on 12 months Gmail; review classification accuracy |
