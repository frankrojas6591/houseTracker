# lifeTracker — Git Repository Strategy

**Version:** 1.0
**Date:** June 2026
**Status:** Decided and implemented

---

## Decision: Monorepo within `lifeTracker`

**Option A (one repo per tracker + shared pip package):** clean isolation, but 7+ repos + versioned shared package for a solo developer.
**Option B (monorepo — chosen):** shared common services (`core/`) are literally shared code; one push commits all agents; natural fit for one Flask deployment.
**Option C (hybrid):** houseTracker separate, new trackers in monorepo — abandoned because it splits the shared layer.

Migration is complete. All discipline agents live under `lifeTracker/` as `<name>Agent/` subdirectories. `houseTracker` repo is archived.

---

## Current State

### Code Repos

```
pyTrackers/
├── lifeTracker/            ← THE monorepo (personal GitHub: frankrojas6591)
│   │                         SSH alias: github.com-fxr
│   ├── core/               ← common services (auth, profile, records)
│   ├── life/               ← PersonalAssistant orchestrator
│   ├── ui/                 ← shared Flask web UI + iOS API routes
│   ├── houseAgent/         ← House Manager discipline agent
│   ├── medicalAgent/       ← Health Advocate discipline agent
│   ├── moneyAgent/         ← Financial Advisor discipline agent
│   ├── estateAgent/        ← Estate Manager discipline agent
│   ├── emotionalAgent/     ← Emotional Health discipline agent
│   ├── faithAgent/         ← Spiritual Advisor discipline agent
│   ├── recordAgent/        ← RecordAgent docs (code lives in core/records/)
│   ├── ltCmd.py            ← CLI: --setup, --start, --check, --backup
│   ├── wsgi.py             ← Flask WSGI entry for PythonAnywhere
│   └── docs/
│       ├── lifeTrackerVision.md
│       └── design/         ← common services design docs
│
├── mobileAudioIO/          ← iOS voice client (separate repo — Swift/Xcode)
│   │                         SSH alias: github.com-fxr
│   └── docs/
│
└── llcRentalTracker/       ← LLC/rental business (SEPARATE — work GitHub: wbgroupmgr)
                              Never touched from this codebase
```

### Data Repo

```
lifeTracker-data/           ← private data repo (frankrojas6591, SSH: github.com-fxr)
└── records/
    └── users/
        └── <user_id>/
            ├── profile.json
            └── agents/
                ├── house/<house_id>/
                ├── medical/<practitioner_id>/
                ├── money/ estate/ emotional/ faith/
                └── life/pa/
```

`lifeTracker-data` is **never** cloned with the code repo. It is checked out separately on each deployment environment (PythonAnywhere, local Mac). Path configured in `~/.lifeTracker/config.json`.

---

## Common Services Architecture

The common services in `core/` are the shared foundation all discipline agents build on. No agent re-implements any of these.

### `core/auth/` — Identity

Responsibility: verify who you are. Nothing else.

| File | Role |
|---|---|
| `gpg_users.py` | GPG-encrypted user DB (`users.json.gpg`): `verify_user`, `add_user` |
| `session.py` | JWT issue/verify — token carries `user_id` only |
| `decorators.py` | `@login_required` (web), `@api_auth_required` (iOS API) |

Identity DB (`users.json.gpg`) lives at `~/.lifeTracker/` — never committed. Holds `user_id` + bcrypt passphrase hash + phone. Nothing else.

Design: `docs/design/lifeTracker_auth.md`

---

### `core/profile/` — User Profile

Responsibility: everything about a user that is not identity. Supports **U users × H houses × M medical practitioners × F faith advisors**.

| File | Role |
|---|---|
| `models.py` | `UserContext`, `HouseEntry`, `PractitionerEntry`, `FaithAdvisorEntry` |
| `user_profile.py` | `UserProfileService`: `load(user_id)` → `UserContext`; `add_house/practitioner/advisor` |

`UserContext` is the runtime object that travels with every request (`request.user`). Every discipline agent receives it at query time — they never read user data directly. Stored at `records/users/<user_id>/profile.json` in the data repo.

Design: `docs/design/lifeTracker_userProfile.md`

---

### `core/records/` — RecordAgent

Responsibility: sole interface between all agents and the filesystem. All agent records are user-scoped.

| File | Role |
|---|---|
| `uans.py` | UANS + `UserContext` → filesystem path |
| `git_store.py` | `write_json` → write file → `git commit` → `git push` |
| `record_agent.py` | `RecordAgent`: `read`, `write`, `append_action_item`, `provision` |

Path pattern: `records/users/<user_id>/agents/<namespace>/[<house_id>/]<category>/<agent>/<record>.json`

Design: `docs/design/lifeTracker_records.md`

---

### `ui/` — Communication Layer

Responsibility: all inbound channels. Channels share the same Flask codebase; channel detection determines response format.

| Channel | Entry | Response |
|---|---|---|
| Browser | `ui/chat.py` `/chat`, `ui/checkin.py` `/checkin` | Full HTML |
| Twilio voice | `ui/chat.py` `/voice` | TwiML `<Say>` ≤ 3 sentences |
| iOS app | `ui/api.py` `/api/query` `/api/auth/token` `/api/notifications` | JSON |

`mobileAudioIO` is the iOS client consuming `/api/*`. It is a separate repo (Swift/Xcode) and handles STT + TTS on-device — only text crosses the network.

Design: `docs/design/lifeTracker_commWeb.md`, `docs/design/lifeTracker_commIOS.md`

---

## Branch and Commit Rules

| Rule | Detail |
|---|---|
| Primary branch | `main` — active development |
| Release branch | `release/vMajor.Minor` — when a milestone is tested |
| Push policy | After every commit: `git push origin main` |
| Commit scope | Python, Markdown — NOT `.DS_Store`, `__pycache__`, `*.pyc`, binary PDFs |
| Session logs | `.claude/sessionLogs/` is gitignored — never commit |

Remote: `git@github.com-fxr:frankrojas6591/lifeTracker.git` (uses `~/.ssh/id_ed25519_fxr`)
