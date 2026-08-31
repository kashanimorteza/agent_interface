---

name: my-interface-interpreter

description: Generate or update `.interface/config/` from Phase 1 of `.interface/project.md` and the shapes defined in `.interface/schema/` — the agent-oriented representation of the project that the my-interface-tasker and my-interface-developer work from. Use when the project definition changes, or when config files are missing, outdated, or inconsistent with Phase 1.

allowed-tools: Read, Write, Edit, Grep, Glob

---

# My Interface Interpreter

The Interpreter is the transformation layer between the human's project definition and the agent-oriented configuration:

`README.md + root.yaml + project.md + schema/` → **Project Understanding** → `.interface/config/`

It understands the target project and represents that understanding as structured configuration under `.interface/config/`, in exactly the shapes the Schema defines. It does not copy text from `project.md` into config files — it interprets the project and restructures it according to the meaning and format each Schema assigns.

## The understanding sequence

Perform these four readings **in order**, before writing anything. Each answers one question, and the later readings depend on the earlier ones.

### 1. `README.md` — what Agent Interface is

Read the repository's `README.md` first. It establishes what Agent Interface is, the problem it solves, the overall workflow (define → configure → plan → develop → review), and the Interpreter's own place in that workflow: reading `project.md` and producing Config according to the Schema. This is the high-level purpose everything below serves.

### 2. `.interface/root.yaml` — how the Interface is structured

Read `.interface/root.yaml`, the entry point of the Interface. It maps the folders and files of `.interface/`, names each config file and its responsibility, defines the working modes and what each may write, and indexes the Skills. Use it to know which config files exist, how they relate, and where the Interpreter sits: it **runs outside the modes** (transitions S0, S7, S8) and enters none.

### 3. `.interface/project.md` — the target project

Read `.interface/project.md` in full. It is the human-managed source of truth for the target project — what the product is, its parts, its technology decisions, and what each phase must deliver.

Build an agent-oriented understanding of the project from it, under these constraints:

* **Phase 1 only.** The project is defined incrementally in phases; configure only what Phase 1 states. Any later phase, if present, contributes nothing — not a concept, not a parameter, not a requirement.
* **No invention.** Do not invent requirements, architecture, behavior, models, parameters, or any other project information that `project.md` does not support. What Phase 1 leaves undefined is written as `"to be defined"` and raised as an open question in `state.yaml` — never filled with a plausible value. The one exception is a field for which a Schema supplies a `default` (see step 4): a default is an answer, not a guess.

### 4. `.interface/schema/` — how the understanding is represented

Read **every** file in `.interface/schema/`. The Schema is the authoritative definition of the output: which config files exist, what each represents, the structure and required format of each, and how the files relate. Never invent a configuration structure of your own, and never copy a Schema verbatim into a config file — populate its structure with the Phase 1 understanding.

What the schemas give you:

* `file.schema.yaml` — the outer shape **every** config file follows: `meta`, `policy`, `read_order`, `content_map`, `content`. Each `<name>.schema.yaml` gives the shape of that file's `content`. `root.yaml` has no schema of its own — outer shape only.
* `definition.schema.yaml` → `config/definition.yaml`. The item index is `content.architecture.parts` — every other file's notion of an "item" resolves against it.
* `rules.schema.yaml` → `config/rules.yaml`. Each group after `precedence` is a list of single-sentence imperative rules derived from the project and its stated constraints.
* `backend.schema.yaml` / `frontend.schema.yaml` → the per-item files. Honor each schema's `defaults` rule where it declares one: a field carrying a `default` is always written — the project's stated value when the project states one, the schema's default when it does not; such a field is never `"to be defined"` and never becomes an open question. A field with **no** default and no stated value stays `"to be defined"` and is raised as a question.
* `task.schema.yaml` → `config/task.yaml` — frame and empty plans only; see "State and carry-through" below.
* `state.schema.yaml` → `config/state.yaml` — the State contract; see below.

## Generating `.interface/config/`

With the four readings done, update the existing files under `.interface/config/` or generate them where missing, so that they represent the current Phase 1 understanding and strictly follow the Schema. If existing config files are incomplete, outdated, or inconsistent with the current Phase 1 content of `project.md`, modify or regenerate them accordingly — and change nothing that is already correct and current.

* `definition.yaml` and `rules.yaml` carry `agent_may_edit: false`. Regenerating them from `project.md` is the one time they are touched, and only inside this job.
* Apply the Skill Rules below, and — on a run where `config/rules.yaml` already exists — stay consistent with the rules it carries.

## State and carry-through

This job runs **outside the modes** and does not enter one. Its state writes are limited to transitions **S0**, **S7**, and **S8** as the State contract defines them (`config/state.yaml` under `content.state_authority`; for a file being created, the default in `schema/state.schema.yaml` governs its own seeding).

* **S0 — only when `state.yaml` does not exist:** create it with `active.mode: "not set"`, `active.item: "none"`, `set_by: "my-interface-interpreter, generating state.yaml"`, `set_at` today, and a `mode_reason` saying the next Skill the human invokes will set the mode. Seed `content.state_authority` **verbatim** from the `default` in `schema/state.schema.yaml` — no `state.yaml` is ever created without it. Never write `set_by: "the human"` for a value the human did not type.
* **Regeneration carries runtime state through untouched:** `content.active` and the live `content.state_authority` in `state.yaml`, and every plan's `phase_titles` with its `phase_titles_lifecycle` and `phase_titles_derived_from` in `task.yaml`, stay exactly as found. A regeneration never resets state and never rewrites the live authority.
* **S7 / S8:** you may raise blockers and open questions, and record the human's own answer under `answered_so_far` — dated and in the human's terms. You never answer a question yourself, and never close one by supplying its answer.
* **No tasks, no build stages:** this job produces configuration, not a plan. Plans stay under `content.plans.<item>` in `task.yaml`, one per indexed item, with `phases` empty. `phase_titles` are derived by `my-interface-tasker`, not here — write an empty list with lifecycle `empty` only where the plan is new.

## What this job is not

The Interpreter understands the project, structures that understanding, and generates configuration. It does **not** plan tasks, implement code, modify the target project's implementation, test, refactor, or perform any other development work — and it does not invent project requirements.

Its inputs are read-only: `README.md`, `.interface/root.yaml`, `.interface/project.md`, and `.interface/schema/` are never modified, renamed, or deleted by this job — as `root.yaml`'s policy and the State contract's `human_only_decisions` already establish.

## Skill Rules

Rules provide additional constraints for specific responsibilities when generating Config files. They do not replace the Schema and do not change its structure. Apply only the rules explicitly defined here.

#### Backend

* API routes do not need to be defined in detailed, route-by-route form inside `backend.yaml`.

## Completion

Once the Config files correctly represent Phase 1 according to the Schema and the applicable rules — and the runtime state survived (`content.active` and `content.state_authority` as they were unless this run created the file, and where it created the file, `content.state_authority` equal to the schema's default verbatim; every existing plan's `phase_titles` and lifecycle unchanged) — stop. The task is complete.

Report which files changed, and which open questions in `state.yaml` are new or now closed.
