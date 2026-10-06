# Agent Native Implement

This Foundation File instructs an Agent Native to create or update its Agent Native Implement Skill and defines what that Skill does. The Skill is the only reader of the Executor Module and transfers the Human's Agent concepts into the selected Agent Native. The Native's registered Skill name and invocation are authoritative; in this project the invocation is `/my-interface-native-implement`. The selected Agent Native is the Agent that runs this Skill; the Executor Module never names one.

## How to start

To create or update the Agent Native Implement Skill, the Human tells the Agent:

```text
Read `.interface/foundation/create-agent-native-implement.md` completely and execute every instruction in it.

Use the selected Agent Native's official Agent Native Implement entry point. In this project, invoke `/my-interface-native-implement` according to the Foundation File. Preserve the authority and boundaries defined there. Do not read Target sources and do not modify `.interface/executor/`.

Report exactly what was done and whether realization completed successfully.
```

## Instruction

According to the selected Agent Native's Skill-creation policy, create or update its Agent Native Implement Skill from this Foundation File. The Skill must be self-contained after creation and must not require a later read of the Executor Module to understand its own realization procedure. In this project, the Human invokes the resulting Skill only through `/my-interface-native-implement`, without a mode or numeric argument.

Creating or updating the Agent Native Implement Skill is a preparation step only. The creation process must not invoke, schedule, chain, or simulate the resulting Skill, and must not begin Executor Module realization in the same run. Realization starts only after a separate explicit Human invocation of `/my-interface-native-implement`.

When the Skill is explicitly invoked, it must read and understand the complete Executor Module, then realize that understanding in the selected Agent Native. It must update an existing Native realization or create one when it is missing.

Every explicit invocation is a full realization against the current Executor Module and the current instructions in this Foundation File. The existence of the Agent Native Implement Skill or any previously generated Native artifact never satisfies the invocation and never permits the Skill to skip creation, reconciliation, or verification under the current mechanism.

## Purpose

The Skill transfers the Executor Module's portable definition of the Agent into the selected Agent Native. It makes the Agent Native understand and apply the Human's declared Components, Skills, Rules, Permissions, Commands, Tools, Connections, Context, Runtime choices, Personalities, and Agent Instances wherever the Native provides a corresponding mechanism.

## Source Understanding

The Skill reads these sources in full:

- `.interface/executor/agent.md` for the Executor Module's structure and shared meaning;
- the applicable `.interface/executor/<component>/<component>.md` files for portable meaning and Principles;
- the applicable `.interface/executor/<component>/<component>.yaml` files for current declarations and selections; and
- any file explicitly referenced by those Agent sources.

The Skill discovers the current Components and referenced sources from the Executor Module itself. It does not rely on a hardcoded component list or on an earlier run.

Interface Understanding is not required for realization. When navigation is necessary, the Skill may consult `.interface/interface.md` as a map of the Interface. It never needs Target Understanding and must not read Target sources to perform this work.

The Skill must then enumerate every Contract in `.interface/executor/skill/contracts/` before realizing any Skill. Each Contract is one required realization item: its named Operation Component Definition and Preferences are the source of its meaning, and the Contract is the source of its invocation and Native boundary. No declared Skill may be skipped because it is unfamiliar, already present, or not selected as the coordinating Skill. An Operation Component that has no Contract — such as State when it is not declared as a Skill — must not be turned into a Skill merely because it exists in the Implementation Module. It must also enumerate every folder in `.interface/executor/skill/providers/`. Each folder is one required realization item, copied byte-for-byte into the Native's Skill location; it has no Contract or Source and is never reconstructed.

## Realization Procedure

The Skill establishes an Understanding of the complete Executor Module before changing any Native artifact. It preserves the meaning, scope, ownership, boundaries, and mandatory Principles declared by the Human.

For each declared Component or capability, the Skill:

1. identifies the Native mechanism that corresponds to the declaration;
2. reads the existing Native realization completely when one exists;
3. compares the declaration with that realization;
4. creates or updates the Native artifact when it is missing or stale;
5. preserves Native metadata and compatible Native content that the Executor Module does not own; and
6. re-reads the result, runs every Component's Review checks in the Native, including each Enforced Guarantee's probe and allow_probe, and reports whether the declaration was realized faithfully.

The Skill must realize every current declaration and must not silently skip an unfamiliar or newly added Component. If the Native has no equivalent mechanism, it reports the declaration as unsupported or approximated and states the exact difference. It never invents a declaration, narrows its scope, or silently changes its authority.

## Native Realization

The Agent Native decides where and how each concept is represented. The Skill learns the Native's own documented mechanisms, file conventions, invocation rules, and limitations before choosing a destination. Native-specific paths, formats, commands, and configuration details belong to the Native realization, not to the Executor Module.

Agent Native Implement may restate a declaration in the Native's idiom only when necessary for the Native to apply it. Such restatement must preserve the declaration's meaning, scope, ownership, and authority. A Native artifact is never a second authority.

When a declared Skill is required, the Skill creates or updates that Native Skill according to the Native's Skill policy. When a declared Rule, Permission, Connection, Output Style, or other declared Component has another Native mechanism, it uses that mechanism instead of forcing every concept into a Skill.

For every declared Skill entry, the Skill must create the Native Skill when it is missing and reconstruct its Agent-owned content from the current Contract and every Source it names on every run. It may preserve only Native metadata and compatible content that the Executor Module does not own. It must then verify the reconstructed result against the Contract and every Source. A Native Skill is `already current` only when that verification finds no omitted, weakened, or contradictory requirement; the mere existence of the file, matching name, matching Contract, or a prior run never establishes that result. Any mismatch requires `updated`, even when the Contract itself is unchanged. It must report one result for every declared entry, including entries that are already current, unsupported, approximated, or blocked. The coordinating Skill selection affects invocation and coordination only; it does not make any other declared Skill optional.

## Authority and Boundaries

The Executor Module is Human-owned. Agent Native Implement reads it read-only; it never changes any file or directory under `.interface/executor/`. Only the Human may change Agent Definitions and Preferences.

The Human's direct explicit invocation of Agent Native Implement is standing authorization for every additive, project-scoped Native change within this Foundation File's scope. The Skill must create, update, save, and verify the required Native artifacts without asking whether it may save or whether each individual change is approved. It may pause only for credentials, external trust, authentication, broader authority, an irreversible action, or a Native capability that cannot realize the declaration; ordinary project-scoped Native file changes require no second confirmation.

Agent Native Implement is the only process authorized to read the Executor Module for Native realization. No other Skill, Agent Instance, coordinator, startup routine, Context, or Runtime operation may read, resolve, or depend directly on those sources. Other Native operations use the Native realization.

The Skill does not:

- read or understand Target sources;
- inspect Git status, history, branches, diffs, tracked state, deleted files, or earlier versions;
- restore, compare, or recover anything from Git or from any past project state;
- choose or change Implementation decisions;
- install plugins, packages, or external capabilities;
- change application dependencies, project code, Config, credentials, user settings, or machine settings;
- create new Agent declarations; or
- remove unrelated Native content.

If a required declaration needs Human input, broader authority, external trust, authentication, or a Native capability that does not exist, the Skill stops that item and reports the exact reason. Independent declarations may continue when doing so is safe.

## Output

The Skill reports:

- the Executor Module sources it read;
- the Native mechanism and artifact used for each declaration;
- whether each realization was created, updated, already current, approximated, unsupported, or blocked;
- the exact difference for every approximation or unsupported declaration; and
- whether re-reading the Native artifacts and running every Review check and probe confirmed faithful realization.

The overall result is successful only when the complete current Executor Module has been read and every required declaration has been realized and verified. A successful result never claims that a Native artifact is authoritative over the Executor Module.
