# lifeTracker — User Profile Service Design

**Version:** 1.0
**Date:** June 2026
**Parent:** [Design Index](./lifeTracker_design.md)

---

## 1. Why User Profile Is a Separate Service

lifeTracker is designed to operate for **U users, each with H houses, M medical team members, and F faith advisors**. This demands that what a user *is* (auth: identity + passphrase) be separated from what a user *has* (profile: their houses, practitioners, advisors).

| Service | Knows | Stored |
|---|---|---|
| **Auth** (`core/auth/`) | who you are — `user_id` + passphrase hash | `~/.lifeTracker/users.json.gpg` — never in git |
| **User Profile** (`core/profile/`) | everything about you — houses, medical team, faith advisors, active agents | `lifeTracker-data/records/users/<user_id>/profile.json` — in data repo |

This split lets the same deployment instance serve multiple users without any agent needing to know about individual user data. Every discipline agent receives a `UserContext` at query time; it never reads user data directly.

---

## 2. User Profile Schema

`records/users/<user_id>/profile.json`

```json
{
  "user_id": "frankr6591",
  "display_name": "Frank Rojas",
  "email": "frankr6591@gmail.com",
  "dob": "1957-09-15",
  "phone": "+15125550100",
  "active_agents": ["house", "medical", "money", "estate", "emotional", "faith"],

  "houses": [
    {
      "house_id": "kingsway_dr",
      "label": "Wimberley Home",
      "address": "177 Kingsway Dr, Wimberley TX 78676",
      "county": "Hays",
      "parcel_id": "R33204",
      "purchase_date": "2022-12-31",
      "purchase_price": 335000,
      "is_primary": true,
      "active": true
    }
  ],

  "medical_team": [
    {
      "practitioner_id": "arc_primary",
      "role": "primary_care",
      "name": "",
      "practice": "Austin Regional Clinic",
      "system": "Epic",
      "fhir_endpoint": "",
      "active": true
    },
    {
      "practitioner_id": "arc_urology",
      "role": "urologist",
      "name": "",
      "practice": "Austin Regional Clinic",
      "system": "Epic",
      "fhir_endpoint": "",
      "active": true
    },
    {
      "practitioner_id": "cpap_resmed",
      "role": "sleep_specialist",
      "name": "",
      "practice": "ResMed myAir",
      "system": "myAir",
      "fhir_endpoint": "",
      "active": true
    }
  ],

  "faith_advisors": [
    {
      "advisor_id": "parish_priest",
      "role": "parish_priest",
      "name": "",
      "parish": "",
      "diocese": "Austin",
      "denomination": "Roman Catholic",
      "active": true
    }
  ],

  "created_at": "2026-06-29T00:00:00Z",
  "updated_at": "2026-06-29T00:00:00Z"
}
```

---

## 3. UserContext — The Runtime Object

After login, the system loads the user's profile and constructs a `UserContext`. This object travels with every request and is passed to all discipline agents.

```python
from dataclasses import dataclass, field

@dataclass
class HouseEntry:
    house_id: str
    label: str
    address: str
    is_primary: bool
    active: bool

@dataclass
class PractitionerEntry:
    practitioner_id: str
    role: str
    name: str
    practice: str
    system: str
    active: bool

@dataclass
class FaithAdvisorEntry:
    advisor_id: str
    role: str
    name: str
    parish: str
    diocese: str
    active: bool

@dataclass
class UserContext:
    user_id: str
    display_name: str
    email: str
    dob: str
    active_agents: list[str]
    houses: list[HouseEntry] = field(default_factory=list)
    medical_team: list[PractitionerEntry] = field(default_factory=list)
    faith_advisors: list[FaithAdvisorEntry] = field(default_factory=list)

    @property
    def primary_house(self) -> HouseEntry | None:
        return next((h for h in self.houses if h.is_primary and h.active), None)

    @property
    def active_houses(self) -> list[HouseEntry]:
        return [h for h in self.houses if h.active]

    @property
    def active_practitioners(self) -> list[PractitionerEntry]:
        return [p for p in self.medical_team if p.active]

    @property
    def active_faith_advisors(self) -> list[FaithAdvisorEntry]:
        return [a for a in self.faith_advisors if a.active]
```

---

## 4. UserProfile Service — `core/profile/user_profile.py`

```python
from core.records.git_store import read_json, write_json
from core.profile.models import UserContext, HouseEntry, PractitionerEntry, FaithAdvisorEntry
from datetime import datetime

class UserProfileService:
    def __init__(self, config: dict):
        self._config = config

    def load(self, user_id: str) -> UserContext | None:
        """Load and hydrate UserContext from profile.json. Returns None if not found."""
        data = read_json(f"users.{user_id}.profile", self._config)
        if not data:
            return None
        return self._hydrate(data)

    def save(self, ctx: UserContext) -> None:
        """Persist UserContext back to profile.json via RecordAgent (commits to data repo)."""
        write_json(
            f"users.{ctx.user_id}.profile",
            self._serialize(ctx),
            self._config,
            message=f"profile: update {ctx.user_id}"
        )

    def add_house(self, user_id: str, house: HouseEntry) -> UserContext:
        ctx = self.load(user_id)
        ctx.houses.append(house)
        ctx.updated_at = datetime.utcnow().isoformat() + "Z"
        self.save(ctx)
        return ctx

    def add_practitioner(self, user_id: str, practitioner: PractitionerEntry) -> UserContext:
        ctx = self.load(user_id)
        ctx.medical_team.append(practitioner)
        self.save(ctx)
        return ctx

    def add_faith_advisor(self, user_id: str, advisor: FaithAdvisorEntry) -> UserContext:
        ctx = self.load(user_id)
        ctx.faith_advisors.append(advisor)
        self.save(ctx)
        return ctx

    def _hydrate(self, data: dict) -> UserContext:
        return UserContext(
            user_id=data["user_id"],
            display_name=data["display_name"],
            email=data["email"],
            dob=data["dob"],
            active_agents=data["active_agents"],
            houses=[HouseEntry(**h) for h in data.get("houses", [])],
            medical_team=[PractitionerEntry(**p) for p in data.get("medical_team", [])],
            faith_advisors=[FaithAdvisorEntry(**a) for a in data.get("faith_advisors", [])],
        )

    def _serialize(self, ctx: UserContext) -> dict:
        return {
            "user_id": ctx.user_id,
            "display_name": ctx.display_name,
            "email": ctx.email,
            "dob": ctx.dob,
            "active_agents": ctx.active_agents,
            "houses": [h.__dict__ for h in ctx.houses],
            "medical_team": [p.__dict__ for p in ctx.medical_team],
            "faith_advisors": [a.__dict__ for a in ctx.faith_advisors],
            "updated_at": datetime.utcnow().isoformat() + "Z",
        }
```

---

## 5. Session Integration

After login succeeds in `ui/auth.py`, the User Profile is loaded and injected into the request context alongside the JWT:

```python
# ui/auth.py  — POST /login success path
user_ctx = profile_service.load(owner_id)
token = issue_token(owner_id, user_ctx.active_agents, config)
# Store serialized user_ctx in session (signed by flask_secret)
session["user_context"] = profile_service._serialize(user_ctx)
```

The `@login_required` decorator hydrates `UserContext` from the session and sets `request.user`:

```python
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = token_from_request(request)
        payload = verify_token(token, current_app.config) if token else None
        if not payload:
            return redirect(url_for('auth.login'))
        request.user = profile_service.load(payload["user_id"])
        return f(*args, **kwargs)
    return decorated
```

Every route handler accesses the full `UserContext` via `request.user`. No route reads the profile JSON directly.

---

## 6. Record Path Structure — User-Scoped

All agent records are scoped under `records/users/<user_id>/`. House records are further scoped by `house_id`. This lets the same RecordAgent instance serve multiple users and multiple houses without path collision.

```
lifeTracker-data/
└── records/
    └── users/
        └── frankr6591/
            ├── profile.json                          ← UserProfile (this service)
            └── agents/
                ├── house/
                │   └── kingsway_dr/                  ← house_id from UserContext
                │       ├── core/records/
                │       ├── core/profile/
                │       ├── systems/hvac/
                │       ├── systems/electrical/
                │       └── ...
                ├── medical/
                │   ├── arc_primary/                  ← practitioner_id
                │   │   ├── health/conditions/
                │   │   └── care/appointments/
                │   └── arc_urology/
                │       └── care/appointments/
                ├── money/
                │   ├── accounts/registry/
                │   └── planning/rmd/
                ├── estate/
                │   └── assets/registry/
                ├── emotional/
                │   └── core/checkin/
                ├── faith/
                │   └── examen/reflection/
                └── life/
                    └── pa/
                        ├── briefings/
                        └── action_items/
```

RecordAgent path derivation receives `UserContext` at construction and uses `user_id` (and `house_id` for house namespace) as the path prefix. UANS segments remain unchanged — only the base path changes.

```python
def uans_to_path(uans: str, user_ctx: UserContext, data_root: Path, house_id: str = None) -> Path:
    parts = uans.split(".")
    namespace = parts[0]
    base = data_root / "records" / "users" / user_ctx.user_id / "agents" / namespace

    if namespace == "house":
        hid = house_id or (user_ctx.primary_house.house_id if user_ctx.primary_house else "default")
        base = base / hid

    remainder = "/".join(parts[1:-1])   # category/agent
    record = parts[-1] + ".json" if len(parts) >= 4 else ""
    return base / remainder / record if record else base / remainder
```

---

## 7. `ltCmd.py --setup` — Profile Creation Step

After auth setup, the wizard creates the initial user profile:

```
Creating user profile...
  Houses: Add a house? [Y/n]: Y
    House ID [kingsway_dr]:
    Label [Wimberley Home]:
    Address: 177 Kingsway Dr, Wimberley TX 78676
    Is this the primary residence? [Y/n]: Y
    Add another house? [y/N]: N

  Medical team: Add a practitioner? [Y/n]: Y
    Practitioner ID [arc_primary]:
    Role [primary_care]:
    Practice: Austin Regional Clinic
    System [Epic]:
    Add another? [y/N]: N

  Faith advisors: Add an advisor? [Y/n]: Y
    Advisor ID [parish_priest]:
    Role [parish_priest]:
    Parish: ...
    Diocese [Austin]:
    Add another? [y/N]: N

Writing records/users/frankr6591/profile.json ... done
```

Profile is also editable at runtime via `/profile` web route (Phase 0b).

---

## 8. Files

```
core/
└── profile/
    ├── __init__.py
    ├── models.py           ← UserContext, HouseEntry, PractitionerEntry, FaithAdvisorEntry
    └── user_profile.py     ← UserProfileService: load, save, add_house, add_practitioner, add_faith_advisor
```

Routes (added to `ui/auth.py` blueprint or a new `ui/profile.py`):

| Route | Description |
|---|---|
| `GET /profile` | View current user profile |
| `POST /profile/houses` | Add a house |
| `POST /profile/medical` | Add a practitioner |
| `POST /profile/faith` | Add a faith advisor |
