# lifeTracker — Git & User Configuration Strategy

**Version:** 1.1
**Date:** June 2026
**Status:** Decided and implemented

---

## Decision: Monorepo within `lifeTracker`

| Option | Synopsis |
|---|---|
| A — one repo per tracker | Clean isolation, but 7+ repos + versioned shared package — solo-developer overhead |
| **B — monorepo (chosen)** | `core/` is literally shared; one push covers all agents; maps naturally to one Flask deployment |
| C — hybrid | New trackers monorepo, houseTracker separate — splits the shared layer |

Migration complete. All discipline agents live under `lifeTracker/` as `<name>Agent/` subdirectories.

---

## Code Repos

```
pyTrackers/
├── lifeTracker/            ← monorepo (frankrojas6591, SSH: github.com-fxr)
│   ├── core/               ← auth · profile · records
│   ├── life/               ← PersonalAssistant orchestrator
│   ├── ui/                 ← Flask web UI + iOS + email API routes
│   ├── houseAgent/
│   ├── medicalAgent/
│   ├── moneyAgent/
│   ├── estateAgent/
│   ├── emotionalAgent/
│   ├── faithAgent/
│   ├── recordAgent/        ← docs only; code lives in core/records/
│   ├── wsCmd.py            ← CLI: --setup, --start, --check, --backup, --email
│   └── wsgi.py             ← Flask WSGI for PythonAnywhere
│
├── mobileAudioIO/          ← iOS voice client (frankrojas6591, Swift/Xcode)
└── llcRentalTracker/       ← LLC/rental business (wbgroupmgr — NEVER touched here)
```

---

## User Configuration — `~/.lifeTracker/config.json`

One `config.json` per host (local Mac, PythonAnywhere). **Never committed.** Per-environment secret store and user anchor.

```json
{
  "userID"      : "frank",
  "userData"    : "~/GDrive/Family/PersonalAssistant",
  "paName"      : "javier",
  "passphrase"  : "...",
  "flaskSecret" : "...",
  "anthropicKey": "sk-ant-...",
  "twilioSID"   : "AC...",
  "twilioToken" : "...",
  "twilioPhone" : "+1...",
  "userPhone"   : "+1...",
  "gpgKeyID"    : "",
  "jwtDays"     : 30
}
```

| Field | Purpose |
|---|---|
| `userID` | Short login name — used as the data folder key |
| `userData` | Absolute path to the user's Google Drive data folder |
| `paName` | PA's spoken name — **Javier** (hah-vee-ay) for Frank |
| `passphrase` | Master passphrase for GPG identity DB |
| `flaskSecret` | Flask signed session key |
| `anthropicKey` | Claude API key |
| `twilio*` | Voice channel credentials |
| `userPhone` | Owner's mobile (Twilio caller-ID login) |
| `gpgKeyID` | GPG key fingerprint; blank = symmetric encryption |
| `jwtDays` | JWT expiry in days (default 30) |

`wsCmd.py --setup` prompts for every field and writes this file. Full design: `docs/design/lifeTracker_auth.md`.

### PA Audio Naming Convention

The `paName` is the wake word and conversational name for the PA. Each discipline agent also has an audio alias: **"my \<agent\>"**.

> *"Javier, let **my house** know I received a county tax appraisal letter — make sure **my house** contacts the appraisal protest company to handle this year's protest. I'll upload the letter to the infile."*

| Spoken | Maps to |
|---|---|
| "Javier" | PersonalAssistant |
| "my house" | houseAgent |
| "my health" / "my medical" | medicalAgent |
| "my money" / "my finances" | moneyAgent |
| "my estate" | estateAgent |
| "my feelings" / "my heart" | emotionalAgent |
| "my faith" / "my spiritual" | faithAgent |

---

## Agent Data Storage — `<userData>/`

Each user's records live in the **Google Drive folder** pointed to by `userData`. Google Drive (desktop app or API) provides cross-device sync — no separate data git repo.

```
<userData>/                        ← ~/GDrive/Family/PersonalAssistant/
├── profile.json                   ← UserProfile: houses, medical team, faith advisors
└── agents/
    ├── house/
    │   └── kingsway_dr/           ← house_id (from profile.json)
    │       ├── systems/hvac/
    │       ├── finance/budget/
    │       └── ...
    ├── medical/
    │   ├── arc_primary/           ← practitioner_id (from profile.json)
    │   └── arc_urology/
    ├── money/
    ├── estate/
    ├── emotional/
    ├── faith/
    └── life/
        └── pa/
            ├── briefings/
            └── action_items/
```

- **Local Mac:** `userData` = `~/GDrive/Family/PersonalAssistant` → synced automatically via Google Drive desktop app.
- **PythonAnywhere:** `userData` = `/home/frank/paData` → synced via Google Drive API (`wsCmd.py --sync`) or manual rsync.
- Data is **not** in the code repo. Path is per-host in `config.json`.

RecordAgent uses `userData` as its root path. All reads and writes go to `<userData>/agents/<namespace>/...`. Full design: `docs/design/lifeTracker_records.md`.

---

## Common Services Architecture

One-paragraph summaries; full design in `docs/design/`.

| Service | Module | Design Doc |
|---|---|---|
| **Auth** — identity only | `core/auth/` | `lifeTracker_auth.md` |
| **User Profile** — U users × H houses × M medical × F faith | `core/profile/` | `lifeTracker_userProfile.md` |
| **RecordAgent** — sole filesystem I/O | `core/records/` | `lifeTracker_records.md` |
| **Web UI** — chat, check-in, Twilio voice | `ui/chat.py`, `ui/checkin.py` | `lifeTracker_commWeb.md` |
| **iOS API** — `/api/*` for mobileAudioIO | `ui/api.py` | `lifeTracker_commIOS.md` |
| **Email** — Gmail ingestion + PA send | `ui/email.py` | `lifeTracker_email.md` |

---

## Branch & Commit Rules

### Monorepo Branch Strategy

| Rule | Detail |
|---|---|
| Primary branch | `main` — active development, always deployable |
| Release branch | `release/vMajor.Minor` — cut when a BirthPlan milestone is tested |
| Push policy | After every commit: `git push origin main` |
| Commit scope | Python, Markdown — NOT `.DS_Store`, `__pycache__`, `*.pyc`, PDFs |
| Session logs | `.claude/sessionLogs/` — gitignored, never commit |

Remote: `git@github.com-fxr:frankrojas6591/lifeTracker.git`

### Per-Agent Session Rules

lifeTracker is a **living, learning ecosystem** — each agent matures on its own cadence. Sessions follow these rules:

**One session = one agent focus.**

> If you're working on houseAgent, that session is entirely houseAgent. Don't drift into medicalAgent unless a specific inter-agent goal requires it.

| Scenario | Rule |
|---|---|
| Single-agent work | Session tagged to that agent. Commits prefixed `[house]`, `[medical]`, etc. |
| Inter-agent project | Define the cross-agent goal first. Then break into per-agent sessions. Each session owns one agent's side of the work. |
| Common services | Tag `[core]`. Can span agent design docs if warranted. |
| PA orchestrator | Tag `[pa]`. |

**Commit prefix convention:**

```
[house]   Add HvacAgent audit() — overdue filter detection
[medical] Wire medicalAgent to PA registration
[core]    Update UserProfileService.add_house()
[pa]      Monthly check-in loop — stub all 6 agents
[inter:house+estate]  Cross-agent home equity signal
```

**GitHub Issues:** One issue per agent per BirthPlan phase. Close when milestone passes.

```
[house] Phase 4b — Tier 1 agents (HouseRecords, HouseProfile, Communication)
[medical] Phase 5a — medicalAgent scaffold + PA registration
```
