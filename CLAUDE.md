# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. What This Project Is

`lifeTracker` is the single git repo for all personal discipline agents within the **pyTrackers** ecosystem (`~/GDrive/dev/pyTrackers/`). It is currently in the design phase — vision docs exist for all agents; source files are being established.

**Design principle:** One tracker, N discipline agents. Each agent lives under `<agentName>/` at the repo root.

Sibling project (separate repo, do NOT touch):
- `../llcRentalTracker` — LLC rental business tracker on the work GitHub account (`wbgroupmgr`)

---

## 2. pyTrackers Ecosystem Conventions

These conventions are shared across all pyTrackers sub-projects.

### Coding Style

- No docstrings or multi-line comment blocks. One short inline comment only when the WHY is non-obvious.
- Prefer editing existing files over creating new ones.
- No backwards-compatibility shims for removed code.
- No trailing summaries in responses — the diff speaks for itself.

### Documentation/Markdown Style

- No long winded text descriptions.
- prefer pictures over words (within limits and a balanced approach). 
- prefer bullets (short) to break down a long description.
- Emphasize real scenarios vs technical prose
- Make it fun, make it a story. 

### Session/Design/Dev Workflow

- For enhancements or major refactoring: discuss goals first, produce a multi-task plan, wait for **GO** before making changes.
- After GO is given, make all changes with no prompts.
- **FIXME convention:** The user marks open action items in docs, code and other files with the prefix `FIXME:`. When Claude encounters a FIXME, resolve it — research, fill in the content, and remove the FIXME tag. Do not leave FIXMEs in place.

### No Shortcuts / No Silent Fallbacks

- Implement the correct solution. No workarounds or silent fallbacks that hide real errors.
- If a required artifact (config file, data file) is missing, fail with a clear error or generate it explicitly at the start of the pipeline with a log warning — never silently substitute defaults mid-pipeline.

### Git Workflow

- Development is on `main` — this is the dev branch.
- When a minor/major release is tested, push to `release/vMajor.Minor`.
- At session end, commit all changed source files (Python, JSON, Markdown — NOT `.DS_Store` or binary PDFs).
- After every commit, `git push origin main` — pushing is required, not optional.
- `.claude/sessionLogs/` is gitignored — do not commit session log files.
- Remote: `git@github.com-fxr:frankrojas6591/lifeTracker.git` (uses `~/.ssh/id_ed25519_fxr` via SSH alias `github.com-fxr`)

---

## 3. Project Structure

```
lifeTracker/                  ← this repo (was: houseTracker)
├── docs/                     ← top-level tracker docs (personalAssistanceVision, gitStrategy)
├── houseAgent/               ← House Manager discipline agent
│   └── docs/
│       ├── HouseManagerVision.md
│       └── design/
├── emotionalAgent/           ← Emotional Health discipline agent
│   └── docs/
├── estateAgent/              ← Estate Planning discipline agent
│   └── docs/
├── faithAgent/               ← Faith Practice discipline agent
│   └── docs/
├── medicalAgent/             ← Medical / Health Records discipline agent
│   └── docs/
├── moneyAgent/               ← Personal Finance discipline agent
│   └── docs/
├── CLAUDE.md
└── README.md
```

All Python source should use a `setup_paths.py` module at the package root to anchor all paths relative to the repo — no hardcoded absolute paths.

---

## 4. Running the Application

> Commands will be added here once the project is bootstrapped.

---

## 5. Running Tests

> Test commands will be added here once a test suite is established. Follow the llcRentalTracker pattern:
> ```bash
> python -m tests.test_<module>
> ```
