---
name: my-interface-Install-skills
description: Detect the technologies actually installed in this project (FastAPI, Next.js, React, Node.js — extensible) and install the matching AI Agent Skills for each, at the detected version. Skips anything the project does not use, never adds dependencies, and is idempotent — safe to run repeatedly. Use when the human asks to install, sync, or refresh the project's technology skills.
allowed-tools: Bash, Read, Grep, Glob, ListSkills, SearchSkills, SuggestSkills, ListPlugins, SearchPlugins, SuggestPluginInstall, ToolSearch
---

# Install technology Skills for this project

Detect what the project is actually built with, then install the AI Agent Skill that matches each detected technology and version. Nothing else: this command installs skills — it never touches application code, dependencies, or configuration.

## 1. Resolve where the project's code lives

Prefer the Agent Interface when present: read `.interface/config/` item files (`backend.yaml`, `frontend.yaml`, and any other indexed item) and take each item's `code_path` — that is where its technology lives. An item with `enabled: false` is still inspected: its code may exist, and a skill for it still helps.

Where no interface config exists, fall back to scanning: `pyproject.toml`, `requirements.txt`, or `setup.py` mark a Python project root; `package.json` marks a Node project root. Search the repository root and one level of subdirectories. Read-only — never create or modify these files.

## 2. The technology registry

One entry per supported technology. **To add a technology later, add a row here** — detection command, version source, and skill search terms — and nothing else changes.

| Technology | Present when | Version from |
|---|---|---|
| FastAPI | `fastapi` appears in the Python project's declared dependencies AND resolves in its existing environment | `uv pip show fastapi` (or `<venv>/bin/pip show fastapi`) run against the project's own virtual environment |
| Next.js | `next` appears in `package.json` dependencies/devDependencies AND `node_modules/next` exists | `node_modules/next/package.json` → `version`; fall back to the `package.json` range if `node_modules` is absent, noting it as declared-not-installed |
| React | `react` appears in `package.json` dependencies AND `node_modules/react` exists | `node_modules/react/package.json` → `version` |
| Node.js | a `package.json` exists (Node is the runtime of that item) | `.nvmrc` / `package.json` `engines.node` when declared; otherwise `node --version` of the runtime actually on PATH, noted as "environment version, not pinned by the project" |

Future rows follow the same shape — e.g. Python (`pyproject.toml` `requires-python` + the venv's `python --version`), SQLAlchemy / Alembic (`uv pip show`), PostgreSQL (connection URL in project config), Flutter (`pubspec.yaml` + `flutter --version`), Docker (`Dockerfile` / `compose.yaml` + `docker --version`).

**Detection rules — strict:**
- A technology counts as present only if it is *actually installed in the project* — declared **and** resolvable in the project's own environment. A name merely mentioned in a doc or config does not count.
- Run detection commands read-only, inside the project's existing environment. Never let detection install anything: with uv use `uv pip show` (not `uv run`, which may sync), with npm inspect `node_modules` directly (never `npm install`).
- If a technology is absent, **skip it completely** — no skill install, no dependency added to make it installable.

## 3. Find and install the matching skill

For each detected technology, in registry order:

1. **Idempotency check first**: call `ListSkills` (and `ListPlugins`) and look for an already-installed skill covering this technology. If one exists and is compatible with the detected version, leave it exactly as it is and record it under *Skipped — already installed and compatible*. Never install a duplicate.
2. **Search**: use `SearchSkills` and `SearchPlugins` with the technology name and its major version (e.g. `fastapi 0.141`, `next.js 15`, `react 19`, `node 22`). Prefer, in order: the framework's official skill → a framework-maintained or Anthropic-published skill → a well-matched community skill. Reject anything unrelated to the technology or explicitly incompatible with the detected major version.
3. **Install**: install through the mechanism the match offers — `SuggestPluginInstall` for marketplace plugins (the human approves the rendered install card; that approval is part of the flow, not an error), or the skill's own documented installation mechanism when it has one (e.g. an official FastAPI skill installer). Install only the one matching skill per technology.
4. **Version mismatch**: if the only available skill targets a different major version, do not install it — record the mismatch under *Errors* with both versions, and leave the decision to the human.
5. **No suitable skill** (React and Node.js in particular may have none): record under *Skipped — no suitable skill exists*. That is a valid outcome, not a failure.
6. **Outdated existing skill**: if an installed skill targets an older major version than the project now uses, update it through the same mechanism it was installed by; only then does an existing skill change.

## 4. Hard boundaries

Do not:
- modify application source code, project architecture, or any file outside skill installation,
- upgrade, downgrade, or add project dependencies — not even to make a skill installable,
- install skills for technologies the project does not contain,
- remove or rewrite an existing compatible skill.

## 5. Report

End every run with exactly this summary, listing every registry technology once:

```
Installed:
- <technology> — detected <version> — installed <skill name + source>

Skipped:
- <technology> — <reason: not present in project | already installed and compatible | no suitable skill exists>

Errors:
- <technology> — <failed installation or version-compatibility issue, with both versions named>
```

An empty section is written as `- none`. Running the command again immediately after a successful run must land everything in *Skipped*.
