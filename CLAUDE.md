# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. What This Project Is

`houseTracker` is a new sub-project within the **pyTrackers** ecosystem (`~/GDrive/dev/pyTrackers/`). It is currently in the bootstrapping phase — no source files exist yet.

Sibling projects for reference:
- `../llcRentalTracker` — most mature; follow its conventions for Flask apps, ledger patterns, and project structure
- `../medicalTracker` — domain-specific tracker, early stage

---

## 2. pyTrackers Ecosystem Conventions

These conventions are shared across all pyTrackers sub-projects.

### Coding Style

- No docstrings or multi-line comment blocks. One short inline comment only when the WHY is non-obvious.
- Prefer editing existing files over creating new ones.
- No backwards-compatibility shims for removed code.
- No trailing summaries in responses — the diff speaks for itself.

### Design Workflow

- For enhancements or major refactoring: discuss goals first, produce a multi-task plan, wait for **GO** before making changes.
- After GO is given, make all changes with no prompts.
- **FIXME convention:** The user marks open action items in docs with the prefix `FIXME:`. When Claude encounters a FIXME, resolve it — research, fill in the content, and remove the FIXME tag. Do not leave FIXMEs in place.

### No Shortcuts / No Silent Fallbacks

- Implement the correct solution. No workarounds or silent fallbacks that hide real errors.
- If a required artifact (config file, data file) is missing, fail with a clear error or generate it explicitly at the start of the pipeline with a log warning — never silently substitute defaults mid-pipeline.

### Git Workflow

- Development is on `main` — this is the dev branch.
- When a minor/major release is tested, push to `release/vMajor.Minor`.
- At session end, commit all changed source files (Python, JSON, Markdown — NOT `.DS_Store` or binary PDFs).
- After every commit, `git push origin main` — pushing is required, not optional.
- `.claude/sessionLogs/` is gitignored — do not commit session log files.
- Remote: `git@github.com-fxr:frankrojas6591/houseTracker.git` (uses `~/.ssh/id_ed25519_fxr` via SSH alias `github.com-fxr`)

---

## 3. Project Structure (to be established)

When source files are added, follow the llcRentalTracker package layout as a model:

```
houseTracker/
├── ledger/       # Core data engine
├── ui/           # Flask views + Jinja2 templates (if web UI is needed)
├── util/         # Session management, working DB helpers
├── tests/        # Test suite
├── docs/         # Architecture and design docs
├── wsCmd.py      # CLI entry point
└── requirements.txt
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
