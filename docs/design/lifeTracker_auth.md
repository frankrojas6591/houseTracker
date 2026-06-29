# lifeTracker — Auth Service Design

**Version:** 1.1
**Date:** June 2026
**Parent:** [Design Index](./lifeTracker_design.md)

---

## 1. Overview

Auth is the first thing built in Phase 0. Nothing else runs without it. The lifeTracker auth service handles:

- **User identity** — who is allowed to use this system (identity only — not profile)
- **Login** — passphrase verification against GPG-encrypted user DB
- **Session** — JWT issued on login; verified on every request
- **Decorators** — `@login_required` gates all non-public routes
- **Setup wizard** — `wsCmd.py --setup` creates the user DB on first run

**Auth is identity-only.** Who a user *is* (auth) is separate from what they *have* (User Profile Service). Auth stores only `user_id` + `passphrase_hash`. Everything else — houses, medical team, faith advisors — lives in the User Profile. See `lifeTracker_userProfile.md`.

---

## 2. User DB — `users.json.gpg`

The user database is a GPG-encrypted JSON file stored at `~/.lifeTracker/users.json.gpg`. It never touches git.

### Schema

```json
{
  "users": [
    {
      "user_id": "frankr6591",
      "passphrase_hash": "<bcrypt hash>",
      "phone": "+15125550100",
      "created_at": "2026-06-29T00:00:00Z"
    }
  ]
}
```

- `passphrase_hash` — bcrypt-hashed passphrase. Never stored in plaintext. Never sent over the network.
- `phone` — stored here for Twilio caller-ID login (voice channel). Not duplicated in the profile.
- `active_agents`, `display_name`, `email`, houses, medical team — all in User Profile, not here.
- GPG symmetric encryption wraps the entire JSON file. The GPG key ID is in `config.json`.

### File: `core/auth/gpg_users.py`

```python
def load_users(config: dict) -> list[dict]:
    """Decrypt users.json.gpg and return parsed list."""

def verify_user(user_id: str, passphrase: str, config: dict) -> bool:
    """Load users; find user_id; bcrypt verify passphrase."""

def add_user(user_id: str, passphrase: str, phone: str, config: dict) -> None:
    """Add new user to DB; re-encrypt and write. Does NOT create profile."""

def list_users(config: dict) -> list[str]:
    """Return list of user_ids."""
```

---

## 3. JWT Session

### Token Design

On successful login, the server issues a JWT. The JWT is stored:
- **Browser sessions:** in a `Secure; HttpOnly; SameSite=Strict` cookie named `lt_session`
- **iOS app:** in the Keychain (via `mobileAudioIO`'s `AuthManager`)

JWT payload:
```json
{
  "user_id": "frankr6591",
  "iat": 1719532800,
  "exp": 1722124800
}
```

The JWT carries only `user_id`. `active_agents` and all other profile data are loaded from the User Profile service after token verification — not embedded in the token.

- Expiry: 30 days for browser sessions, 30 days for iOS (silent refresh before expiry)
- Signed with `flask_secret` from `config.json` using `HS256`

### File: `core/auth/session.py`

```python
def issue_token(user_id: str, config: dict) -> str:
    """Create signed JWT with user_id only; return token string."""

def verify_token(token: str, config: dict) -> dict | None:
    """Verify signature and expiry; return payload dict or None."""

def token_from_request(request) -> str | None:
    """Extract token from cookie (web) or Authorization header (iOS API)."""
```

---

## 4. Route Protection

### File: `core/auth/decorators.py`

```python
from functools import wraps
from flask import redirect, url_for, request, jsonify
from core.auth.session import token_from_request, verify_token

def login_required(f):
    """For web routes: redirect to /login if no valid session."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = token_from_request(request)
        payload = verify_token(token, current_app.config) if token else None
        if not payload:
            return redirect(url_for('auth.login'))
        request.owner = payload
        return f(*args, **kwargs)
    return decorated

def api_auth_required(f):
    """For /api/* routes: return 401 JSON if no valid Bearer token."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = token_from_request(request)
        payload = verify_token(token, current_app.config) if token else None
        if not payload:
            return jsonify({"error": "unauthorized"}), 401
        request.owner = payload
        return f(*args, **kwargs)
    return decorated
```

All web routes use `@login_required`. All `/api/*` routes use `@api_auth_required`.

---

## 5. Login Routes

### File: `ui/auth.py`

| Route | Method | Description |
|---|---|---|
| `/login` | GET | Render login form |
| `/login` | POST | Verify passphrase → issue JWT cookie → redirect to `/chat` |
| `/logout` | GET | Clear session cookie → redirect to `/login` |
| `/register` | GET/POST | Add new owner (admin only; guarded by existing session) |

### Login Flow

```
Browser → GET /login
         ← login.html (user_id + passphrase fields)

Browser → POST /login {user_id, passphrase}
         → verify_user() against users.json.gpg     ← auth: identity check
         → profile_service.load(user_id)            ← profile: load full context
         → issue_token(user_id) → set lt_session cookie
         → store UserContext in signed session
         ← redirect /chat

All subsequent requests:
         → @login_required reads cookie
         → verify_token() → hydrates request.user (UserContext)
         → handler runs with full user context available
```

### Twilio Caller-ID Login (voice channel)

When a call arrives on the Twilio voice webhook, the caller's phone number is used as a soft authentication signal. The `config.json` stores `owner_phone_numbers` — a list of known owner numbers. If the incoming call matches, the session is auto-established for the call duration. This is supplementary, not a replacement for full auth on the web channel.

```json
"owner_phone_numbers": ["+15125550100"]
```

---

## 6. `wsCmd.py --setup` Wizard

The setup wizard runs once per environment (PythonAnywhere and local Mac each run it separately). It is the only way to create the `config.json` and `users.json.gpg`.

```
$ python wsCmd.py --setup

lifeTracker Setup Wizard
========================
PA name (your assistant's name) [javier]:
User ID [frank]:
Google Drive data folder [~/GDrive/Family/PersonalAssistant]:
Your mobile number (for Twilio caller-ID): +1...
Flask secret key: [generated randomly if blank]
Anthropic API key: sk-ant-...
Twilio Account SID: AC...
Twilio Auth Token: ...
Twilio phone number: +1...
GPG key ID (or press Enter to use symmetric encryption):

Creating identity entry...
  Passphrase: [hidden input]
  Confirm passphrase: [hidden input]

Writing ~/.lifeTracker/config.json ... done
Encrypting ~/.lifeTracker/users.json.gpg ... done
Profile creation continues in Phase 0b.

Setup complete. Run: python wsCmd.py --start
```

### `wsCmd.py` commands

| Command | Description |
|---|---|
| `--setup` | First-run wizard: config.json, GPG identity DB, data folder provisioning |
| `--start` | Start Flask dev server at `localhost:5000` |
| `--check` | Verify config, GPG DB, data folder, and all agent registrations |
| `--add-user` | Add a new user to the GPG DB (identity only; profile created separately) |
| `--email` | Batch Gmail ingestion — classify threads and write to agent records |
| `--sync` | Sync data folder to/from PythonAnywhere via Google Drive API |

---

## 7. Config Schema

`~/.lifeTracker/config.json` — **never committed to git**.

Full schema with all fields: `docs/strategy-Git_UserConfig.md`.

`config.json.example` in the repo is a committed schema template with placeholder values.

`setup_paths.py` reads this file at import time and exposes all path constants to every module. No other module reads `config.json` directly.
