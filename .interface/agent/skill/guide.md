# Agent Skill

This document explains the Skill directory of the Agent Module: what it holds, how a Skill is defined, and the Human's recorded understanding of the Interface-owned Skills, beginning with Agent Sync. It explains; it does not redefine. `principles.md`, `profile.yaml`, and each Skill Contract are the authorities, and where this document disagrees with them, they are correct.

<br>

## Contents

```text
skill/
├── guide.md
├── principles.md        ← the shared philosophy every Skill follows
├── profile.yaml         ← the declared Skills, their invocation policy, and provider declarations
├── contracts/           ← one portable Contract per Interface-owned Skill
│   ├── configure.md
│   ├── planning.md
│   ├── developing.md
│   ├── reviewing.md
│   ├── launch.md
│   ├── implement.md
│   ├── reset.md
│   ├── skill-installer.md
│   └── agent-sync.md
└── files/               ← optional prepared Skill files, keyed by stable Skill key (declared; currently absent)
```

A Skill has exactly one Capability Realization Kind. An Interface-owned Skill is **Constructed**: its Contract defines it completely and Agent Sync builds the native Skill from it. A Skill with a matching prepared file is **Prepared** and a Skill from an external provider is **Installed**; both belong to the install mode of the Agent Native Skill.

<br>

## How a Skill is defined

Three layers, each with one owner:

- **Principles** (`principles.md`) — rules shared by every Skill: one complete Contract each, proven availability, safe repeatability, fingerprints that prove staleness but never conformance, prepared files.
- **Contract** (`contracts/<skill>.md`) — the Skill's own portable behavior in the thirteen sections of the Skill Contract Schema: purpose, responsibility, trigger, inputs, outputs, required understanding, authority, workflow invariants, verification, idempotency, stopping conditions, runtime realization. Every obligation appears once; nothing vendor-specific.
- **Native adapter** (outside `.interface/`, for example `.claude/skills/<name>/SKILL.md`) — the synchronized, self-contained realization of the Contract in the selected Agent Native. It owns only runtime execution detail and never becomes a second authority.

When a conversation produces a new understanding of a Skill, the *why* is recorded in this guide and the *obligation* it implies is written into that Skill's Contract. The adapter is then brought into line by Agent Sync, never by hand — except for the Agent Sync adapter itself, once, at bootstrap.

<br>

## Understanding record — Agent Sync

The following questions were put to the Human and answered on 2026-09-17.

**What is Agent Sync?**
Agent Sync is the Agent Native configuring itself. It runs inside the selected Native — Claude Code, Codex, Copilot — establishes an Understanding of the complete Agent Module, starting from the Agent Module Guide, and then, following the Native's own principles and standards, shapes the Native to match: the concepts, skills, rules, and limits declared in the Module are carried into the Native's own configuration. The Human does not know, and does not need to know, where a given Native keeps a rule or a skill; what matters is that Sync recognizes "here is a Skill that must exist", "here are rules", and the Native, being the one that runs Sync, knows where those go.

**Does Sync install anything?**
No. Sync gains an Understanding of the declared Skills and does whatever that Understanding requires, which for an Interface-owned Skill is to create it from its Contract. Nothing is installed by Sync; Prepared and Installed Skills remain with the install mode of the Agent Native Skill.

**Why two modes, `self` and `module`?**
Because a Skill that is already running cannot load a new definition of itself. So Sync first realizes its own adapter from its Contract (`self`), the Human restarts the Native, and only then does Sync realize the rest of the Module (`module`). The Human considered collapsing the two modes and updating the adapter by hand every time, and decided against it: the two modes stay, and the adapter is written by hand only once, at bootstrap.

**What happens when the Native cannot realize a declaration exactly?**
Sync reports it, realizes the nearest native equivalent, and continues. Sync does not stop. The report must state exactly how the realization differs from the declaration. Only when no equivalent exists at all, or a genuine stopping condition applies, is the item blocked.

**What about things present in the Native but declared nowhere in the Module?**
Report them, and touch nothing. "These exist in the Native and not here" is all that is needed.

**How should the restart requirement be communicated?**
As a warning that cannot be missed — visually set apart, in a box — placed prominently in the report whenever any native artifact was written.

**How thorough should verification be?**
Sync follows a loop: do the work, check it, and if the check finds a gap, do it again and check again. Whether that takes one pass, two, or three is Sync's own judgment; what is required is the process that ends only when Sync is satisfied that every concept in the Module has reached the Native.

<br>

## Decisions taken — Agent Sync

Recorded on 2026-09-17 and written into `contracts/agent-native.md` the same day:

- Later the same day the Skill was renamed `agent-native` with three numeric modes — `1` sync self, `2` sync component, `3` install — and the separate `skill-installer` Skill was merged into mode `3`; both Contracts were merged into `contracts/agent-native.md` with nothing dropped.

- Module Understanding starts from the Agent Module Guide (`.interface/agent/guide.md`), where the Agent Structure now lives.
- A new result status `approximated`: realized through the nearest native mechanism, with the exact difference stated; Sync continues. `blocked` is reserved for declarations with no native equivalent or a genuine stopping condition.
- The restart notice is visually set apart in the report.
- Kept unchanged, now with the Human's stated reasons: the two modes, the read-only treatment of unmanaged native capabilities, and the Understanding–Reconcile–Verify loop until convergence.

<br>

## Open decisions

- The prepared-file directory `files/` is declared in `profile.yaml` but does not exist; whether to create it empty or leave it absent until a prepared Skill exists.
- Understanding records for the other seven Interface-owned Skills, and for the install mode of Agent Native, are not yet captured.
