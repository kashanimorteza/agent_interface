---
description: Answers about this project cite the interface file and section they came from
keep-coding-instructions: true
---

When you state something about this project — a rule, a setting, a contract, where a task stands — name the file and the section it came from, inline, as `file.yaml → section.path`. A claim with no source is an opinion, and this project has files precisely so that opinions are not needed.

Separate the three kinds of statement, and never let one pass as another:

- **Stated** — it is written in an interface file. Cite it.
- **Derived** — it follows from what is written. Show the step. ("ready" is derived: todo, and every `depends_on` done.)
- **Unknown** — Phase 1 does not settle it. Name the open question in `state.yaml` that covers it, or say plainly that no question covers it yet.

Never restate a rule from memory. `rules.yaml` says a rule that is not in that file is not a rule, so if you cannot cite it, you are inventing it.
