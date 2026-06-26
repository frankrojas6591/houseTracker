# HouseMgr — Data, Config & Auth

**Version:** 0.3
**Date:** June 2026
**Parent:** [Design Index](./houseMgrAgent.md)

---

## 1. Storage Overview

All HouseMgr data lives on the **PythonAnywhere filesystem** — not the local machine, not a cloud DB. The PA filesystem is the single source of truth. A private GitHub repo provides off-host backup of the JSON records.

| Data Type | Location on PA | In Git? |
|---|---|---|
| App code | `/home/<pa_user>/houseTracker/` (cloned from GitHub) | Yes — code repo |
| Config & secrets | `/home/<pa_user>/.houseTracker/config.json` | No — never committed |
| User auth DB | `/home/<pa_user>/.houseTracker/users.json.gpg` | No — never committed |
| HouseRecords (JSON) | `/home/<pa_user>/houseTracker/<house_id>/records/` | Yes — private data repo (backup) |
| Documents (PDFs, photos) | `/home/<pa_user>/houseTracker/<house_id>/documents/` | No — too large; PA filesystem only |

---

## 2. HouseRecords DB Structure

```
/home/<pa_user>/houseTracker/<house_id>/        ← top_folder from config.json
├── records/
│   ├── house_profile.json                       ← House Profile agent output
│   ├── systems_registry.json                    ← All systems / appliances
│   └── agents/
│       ├── architecture/
│       │   ├── knowledge.json                   ← Floor plan, structural notes
│       │   └── action_items.json                ← Pending items from last audit
│       ├── hvac/
│       │   ├── knowledge.json
│       │   └── action_items.json
│       ├── plumbing/
│       └── ...                                  ← One directory per agent
└── documents/
    ├── permits/
    ├── invoices/
    └── photos/
```

All JSON. No external DB. `setup_paths.py` sets `RECORDS_DIR` and `DOCUMENTS_DIR` at startup from `config.json`.

### Git Backup of Records

The `records/` subtree (JSON only, no documents) is pushed to a **private GitHub repo** on a scheduled basis (PA always-on task, nightly). This gives version history and off-PA redundancy without committing sensitive data to the code repo.

```
Code repo  (public or private):  github.com/<user>/houseTracker
Data repo  (private):            github.com/<user>/houseTracker-data
```

The data repo contains only `<house_id>/records/**/*.json`. Documents (PDFs, photos) are never committed — PA filesystem only.

---

## 3. Configuration Profile

`config.json` lives at `/home/<pa_user>/.houseTracker/config.json` on PA. It is **never committed** to either repo. The code repo contains `config.json.example` with all keys and placeholder values.

### Schema

```json
{
  "default":            "ranch_house",
  "APP_SECRET_KEY":     "<flask signing key>",
  "APP_GPG_PASSPHRASE": "<gpg passphrase — encrypts users.json.gpg>",
  "twilio_account_sid": "<Twilio account SID>",
  "twilio_auth_token":  "<Twilio auth token>",
  "twilio_phone_number": "+15125550100",
  "houses": [
    {
      "house_id":   "ranch_house",
      "house_name": "Westwood Ranch",
      "top_folder": "/home/<pa_user>/houseTracker/ranch_house",
      "address":    "123 Ranch Rd, Austin TX 78701",
      "owner_id":   "frank"
    }
  ],
  "owners": [
    {
      "owner_id":   "frank",
      "full_name":  "Frank Rojas",
      "email":      "frankr6591@gmail.com",
      "phone":      "+15125550101"
    }
  ]
}
```

`owner.phone` is the Twilio caller ID used for auto-login on incoming voice calls. If the inbound number matches a registered owner, the session is established without a spoken PIN.

`setup_paths.py` reads this file and exposes module-level constants (`TOP`, `RECORDS_DIR`, `DOCUMENTS_DIR`, `TWILIO_*`) to all other modules. No other module reads `config.json` directly.

---

## 4. Authentication & Login Layer

Follows the `llcRentalTracker` pattern (`llcLogin_auth.py`), adapted for voice caller-ID auto-login.

### User DB

A single GPG-encrypted file at `/home/<pa_user>/.houseTracker/users.json.gpg`. Decrypted in-memory only; never written to disk as plaintext. Passphrase from `config.json → APP_GPG_PASSPHRASE`.

### Roles

| Role | Access |
|---|---|
| `houseMgr` | Full admin — all houses, user management, configurator |
| `owner` | Full access to their associated house(s) |
| `viewer` | Read-only access to a house (e.g., family member) |

### Routes (`ui/houseLogin_auth.py`)

| Route | Method | Description |
|---|---|---|
| `/login` | GET/POST | Credential check against GPG user DB; sets session context |
| `/logout` | GET | Clears session, redirects to `/login` |
| `/register` | GET/POST | `houseMgr` role only — creates new user |
| `/select_house` | GET/POST | Multi-house owners pick the active house after login |
| `/voice` | POST | Twilio webhook — caller ID lookup → auto-login or PIN challenge |

### Flask Session

```python
session["logged_in"]  = True
session["username"]   = "frank"
session["role"]       = "owner"
session["house_id"]   = "ranch_house"
session["owner_id"]   = "frank"
session["via_voice"]  = True          # set when entry is via Twilio /voice
```

`login_required` decorator (from `ui/houseLogin_auth.py`) protects all routes except `/login`, `/logout`, `/register`, and `/voice` (voice handles its own auth). Flask secret key loaded from `config.json → APP_SECRET_KEY` at startup.

---

## 5. `setup_paths.py` Contract

Every module that needs a path imports from `setup_paths`:

```python
from setup_paths import TOP, RECORDS_DIR, DOCUMENTS_DIR, TWILIO_SID, TWILIO_TOKEN
```

`setup_paths.py` is the only module that reads `config.json`. It fails loudly if the file is missing — no silent fallback to default paths.

---

## 6. Implementation Plan (Data Scope)

### Phase 0 — Config & Auth Scaffold

- [ ] `config.json.example` in repo root — all keys, placeholder values, inline comments
- [ ] `setup_paths.py` — reads `~/.houseTracker/config.json`; fails with clear error if missing
- [ ] `wsCmd.py --setup` — interactive wizard on PA console: writes config.json, creates records tree, initializes GPG user DB with first `houseMgr` user
- [ ] `ui/houseLogin_auth.py` — GPG user DB, `make_auth_routes()`, `login_required`, caller-ID auto-login in `/voice` handler

### Phase 1 — Records Scaffold

- [ ] `agents/house_records.py` — `read_json(path)`, `write_json(path, data)`, `append_action_item(agent, item)`, `get_action_items(agent)`
- [ ] Bootstrap records directories on `wsCmd.py --setup`

### Phase 2 — Git Backup

- [ ] PA always-on task: nightly `git add records/ && git commit && git push` to private data repo
- [ ] `wsCmd.py --backup` — manual trigger for the same push
