# lifeTracker — RecordAgent Design

**Version:** 1.1
**Date:** June 2026
**Parent:** [Design Index](./lifeTracker_design.md)

---

## 1. Purpose

RecordAgent is the **sole read/write interface** between every discipline agent and the filesystem. No agent touches the filesystem directly. No agent accesses git directly. All I/O flows through RecordAgent.

Three responsibilities:

1. **Path derivation** — translate a UANS identifier into its filesystem path
2. **Read/write/git-push** — atomic write → git commit → git push, so git history IS the audit trail
3. **Provisioning** — create the full `records/agents/` directory tree for all namespaces on first run

Full ecosystem background: `recordAgent/docs/recordAgentDesign.md`
This doc focuses on implementation design for the Phase 1 build.

---

## 2. The UANS → Path Contract

Every record is identified by a 4-segment dot-notation UANS. The root is `<userData>` from `config.json` (user-specific Google Drive folder). `UserContext` supplies the namespace-specific scope IDs.

```
<namespace>.<category>.<agent>.<record>  +  config.userData + UserContext
```

Maps to:

```
<userData>/agents/<namespace>/[<scope_id>/]<category>/<agent>/<record>.json
```

| Namespace | Scope ID source | Example path (userData = `~/GDrive/Family/PersonalAssistant`) |
|---|---|---|
| `house` | `UserContext.primary_house.house_id` | `<userData>/agents/house/kingsway_dr/systems/hvac/maintenance_log.json` |
| `medical` | `practitioner_id` passed at query time | `<userData>/agents/medical/arc_primary/health/medications/current.json` |
| `money` `estate` `emotional` `faith` | none | `<userData>/agents/money/planning/rmd/schedule.json` |
| `life` | none | `<userData>/agents/life/pa/action_items/open.json` |

The `<record>` segment is optional in directory-level operations. When omitted, the UANS identifies a directory.

---

## 3. Data Store — `<userData>/`

The data root is the Google Drive folder in `config.json["userData"]`. Google Drive desktop app syncs it across Mac and PythonAnywhere. Path is per-host.

For Frank: `~/GDrive/Family/PersonalAssistant/`, house `kingsway_dr`:

```
<userData>/
├── profile.json                   ← UserProfile (core/profile/ service)
└── agents/
    ├── house/
    │   └── kingsway_dr/           ← house_id from UserContext
    │       ├── core/records/
    │       ├── core/profile/
    │       ├── core/comm/
    │       ├── systems/hvac/
    │       ├── systems/electrical/
    │       ├── systems/plumbing/
    │       ├── systems/roofing/
    │       ├── systems/security/
    │       ├── systems/appliances/
    │       ├── designs/architecture/
    │       ├── designs/landscaping/
    │       ├── designs/interior/
    │       ├── finance/budget/
    │       ├── finance/tax/
    │       ├── finance/investment/
    │       └── life/accessibility/
    ├── medical/
    │   ├── arc_primary/           ← practitioner_id from UserContext
    │   │   ├── health/profile/
    │   │   ├── health/conditions/
    │   │   ├── health/medications/
    │   │   ├── vitals/labs/
    │   │   ├── vitals/bp/
    │   │   ├── vitals/cpap/
    │   │   ├── care/appointments/
    │   │   └── care/directives/
    │   └── arc_urology/
    │       └── care/appointments/
    ├── money/
    │   ├── accounts/registry/
    │   ├── transactions/log/
    │   └── planning/rmd/ runway/ income/
    ├── estate/
    │   ├── assets/registry/ net_worth/
    │   ├── legal/documents/ beneficiaries/
    │   └── planning/runway/
    ├── emotional/
    │   ├── core/checkin/
    │   ├── relationships/
    │   ├── grief/companion/
    │   ├── legacy/review/
    │   └── stress/monitor/
    ├── faith/
    │   ├── core/practice/
    │   ├── examen/reflection/
    │   ├── sacraments/history/
    │   ├── community/life/
    │   └── legacy/ethical_will/
    └── life/
        └── pa/
            ├── briefings/
            └── action_items/
```

---

## 4. Implementation

### 4.1 UANS Path Derivation — `core/records/uans.py`

```python
from pathlib import Path
from core.profile.models import UserContext

def uans_to_path(uans: str, data_root: Path, user_ctx: UserContext,
                 scope_id: str = None) -> Path:
    """
    Translate UANS + config.userData + UserContext → filesystem path.

    house.systems.hvac.maintenance_log  (house kingsway_dr)
      → <userData>/agents/house/kingsway_dr/systems/hvac/maintenance_log.json

    medical.health.medications.current  (practitioner arc_primary)
      → <userData>/agents/medical/arc_primary/health/medications/current.json

    money.planning.rmd.schedule
      → <userData>/agents/money/planning/rmd/schedule.json
    """
    parts = uans.split(".")
    if len(parts) < 3:
        raise ValueError(f"UANS must have at least 3 segments: {uans}")

    namespace = parts[0]
    base = data_root / "agents" / namespace

    if namespace == "house":
        hid = scope_id or (user_ctx.primary_house.house_id if user_ctx.primary_house else "default")
        base = base / hid
    elif namespace == "medical" and scope_id:
        base = base / scope_id

    category_agent = "/".join(parts[1:-1])
    record = parts[-1] + ".json" if len(parts) >= 4 else ""
    path = base / category_agent
    return path / record if record else path

def uans_to_dir(uans: str, data_root: Path, user_ctx: UserContext,
                scope_id: str = None) -> Path:
    """Return directory path (strips record segment if present)."""
    parts = uans.split(".")
    return uans_to_path(".".join(parts[:3]), data_root, user_ctx, scope_id)
```

### 4.2 File Store — `core/records/file_store.py`

Writes to the local `<userData>` path. Google Drive desktop app syncs automatically. No git required for data.

```python
import json
from pathlib import Path

def write_json(path: Path, data: dict) -> None:
    """Write data dict to path. Raises on failure — no silent fallback."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))

def read_json(path: Path) -> dict | None:
    """Return parsed JSON or None if file does not exist."""
    if not path.exists():
        return None
    return json.loads(path.read_text())
```

### 4.3 RecordAgent — `core/records/record_agent.py`

```python
from pathlib import Path
from core.records.file_store import write_json, read_json
from core.records.uans import uans_to_path, uans_to_dir

AGENT_DIRECTORIES = [
    "house.core.records", "house.core.profile", "house.core.comm",
    "house.systems.hvac", "house.systems.electrical", "house.systems.plumbing",
    "house.systems.roofing", "house.systems.security", "house.systems.appliances",
    "house.designs.architecture", "house.designs.landscaping", "house.designs.interior",
    "house.finance.budget", "house.finance.tax", "house.finance.investment",
    "house.life.accessibility",
    "medical.health.profile", "medical.health.conditions", "medical.health.medications",
    "medical.vitals.labs", "medical.vitals.bp", "medical.vitals.cpap",
    "medical.care.appointments", "medical.care.directives",
    "money.accounts.registry", "money.transactions.log",
    "money.planning.rmd", "money.planning.runway", "money.planning.income",
    "estate.assets.registry", "estate.assets.net_worth",
    "estate.legal.documents", "estate.legal.beneficiaries", "estate.planning.runway",
    "emotional.core.checkin", "emotional.relationships",
    "emotional.grief.companion", "emotional.legacy.review", "emotional.stress.monitor",
    "faith.core.practice", "faith.examen.reflection",
    "faith.sacraments.history", "faith.community.life", "faith.legacy.ethical_will",
    "life.pa.briefings", "life.pa.action_items",
]

class RecordAgent:
    def __init__(self, config: dict, user_ctx: "UserContext"):
        self._root = Path(config["userData"]).expanduser()
        self._user = user_ctx

    def provision(self) -> None:
        """Create <userData>/agents/ directory tree. Safe to re-run."""
        for uans in AGENT_DIRECTORIES:
            uans_to_dir(uans, self._root, self._user).mkdir(parents=True, exist_ok=True)

    def write(self, uans: str, data: dict, scope_id: str = None) -> None:
        path = uans_to_path(uans, self._root, self._user, scope_id)
        write_json(path, data)

    def read(self, uans: str, scope_id: str = None) -> dict | None:
        path = uans_to_path(uans, self._root, self._user, scope_id)
        return read_json(path)

    def append_action_item(self, uans: str, item: dict, scope_id: str = None) -> None:
        existing = self.read(uans, scope_id) or {"action_items": []}
        existing["action_items"].append(item)
        self.write(uans, existing, scope_id)
```

---

## 5. Who Owns What

Each JSON file belongs to exactly one agent — its sole writer. RecordAgent enforces this by design: agents request reads and writes through the RecordAgent API; they never touch the filesystem directly. Cross-agent reads go through RecordAgent too — one agent never imports from another.

| UANS prefix | Owning agent | Record types |
|---|---|---|
| `house.*` | houseAgent sub-agents | systems, profiles, maintenance logs, budgets |
| `medical.*` | medicalAgent sub-agents | health records, vitals, care history |
| `money.*` | moneyAgent sub-agents | account registry, transactions, planning |
| `estate.*` | estateAgent sub-agents | asset registry, legal documents, runway |
| `emotional.*` | emotionalAgent sub-agents | check-ins, relationships, grief, stress |
| `faith.*` | faithAgent sub-agents | practice log, examen, community |
| `life.pa.*` | PersonalAssistant | monthly briefings, action items queue |

---

## 6. Milestone Tests

```bash
# Phase 1 milestone: verify provisioning
python wsCmd.py --setup
ls ~/GDrive/Family/PersonalAssistant/agents/
# Should show: house/ medical/ money/ estate/ emotional/ faith/ life/

# Verify write
python -c "
from core.records.record_agent import RecordAgent
from core.profile.models import UserContext
import json

config = json.load(open(Path.home() / '.lifeTracker/config.json'))
user_ctx = ...  # loaded from profile.json after setup
ra = RecordAgent(config, user_ctx)
ra.provision()
ra.write('house.core.profile.house_profile', {'address': '177 Kingsway Dr', 'year_built': 2006})
"

ls ~/GDrive/Family/PersonalAssistant/agents/house/kingsway_dr/core/profile/
# Should show: house_profile.json
```
