# Plan Definition

Plan is the Operation Component that turns a Target phase into bounded, understandable, and verifiable work.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
7. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Plan is the Operation Component that turns each selected and plannable project phase into a bounded Plan of Groups and Tasks. It defines how work is organized, understood, ordered, and shown complete.

### Purpose

Work must be precise enough to execute, order, and verify. Plan provides that standard by expressing work as bounded Tasks, organizing shared context through Groups, and making dependencies and completion observable.

### How It Works

A Planning invocation establishes current Interface Understanding and Target Understanding. A selected value is a Target phase identifier. Planning considers selected phases, or every active and plannable Target phase when none is selected, in Target order. It does not proceed to a later phase until Planning of every earlier applicable phase has concluded without an open Blocker. Each applicable phase becomes a Plan, the Plan becomes Groups, and each Group becomes atomic Tasks. Context is stated once at the highest applicable level and inherited downward.

Each Planning invocation produces or reconciles the applicable Plans once against the current Understanding, then records its outcome, unresolved conditions, and the Skills actually used in one State Log Entry. Planning uses any suitable available Skill, but does not invoke another Core Operation. It stops when required Config records or prerequisites are unavailable, coverage is contradictory, ownership is unresolved, or a required decision remains open.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Plan** — the work required by one project phase, holding the context that applies to the whole phase and decomposing its outcome into Groups.
- **Group** — one coherent implementation area within a Plan, holding the context its Tasks share.
- **Task** — one small, concrete activity with one independently observable result.
- **Phase** — the project stage a Plan represents, identified by its stable identifier and carrying its order and target.
- **Plannable Phase** — an active Target phase whose Target-defined prerequisites permit Planning to begin.
- **Dependency** — another Task whose completed result this Task requires before it can begin.
- **Acceptance** — the observable criterion that determines whether a Task's result is correct.
- **Verification** — the condition that must be observed to prove acceptance, stated as behaviour rather than as a command.
- **Task Skills** — the Skills Planning identifies as useful for completing one Task, distinct from that Task's Source ID.
- **Status** — the current progress value of a Task, updated by Develop and distinct from the aggregate Workflow State.
- **State Log** — the append-only State record of a Skill execution and its result.
- **Task Log** — the append-only history of progress, evidence, and verified transitions for one Task, distinct from the State Log.
- **Task Source ID** — the State Log Entry identifier of the Planning invocation that last created or materially changed a Task.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Interface and Target** — establishes the current authorities and intended outcome from which phase work is derived.
- **Consumes State** — Log Entries containing prior Planning results, Blockers, Open Questions, and aggregate phase progress without duplicating Task records.
- **Consumed by Develop** — the planned outcomes, acceptance criteria, dependencies, and execution conditions used to perform the work.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Plan owns decomposition and completion conditions. Target owns intent, Development owns realization, Develop owns execution, and State owns aggregate progress.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Principles in this Definition govern Plan. Plan Preferences, when present, cannot add technical or project meaning.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

The generated Plan record follows the Plan Schema. Preferences can never override a Principle; a project may only add stricter rules.

<br>

### Every phase has its own Plan

**Rule:** Planning accepts one or more Target phase identifiers, or considers every active and plannable Target phase when none is selected. It processes them in Target order. A Plan represents the work required by one applicable project phase. It preserves the phase's identity, order, target, and intended outcome, then decomposes that outcome into Groups and Tasks. The Plan holds the planning context shared by the whole phase: the Component it targets and work-specific constraints that apply throughout and are not already defined by another source. Language and technology choices are resolved from their owning sources and are not copied into the Plan.

**Why:** Stated once in the Plan, that context is inherited by every Group and Task beneath it, so the phase is described in one place rather than restated by everything it contains.

**Boundary:** Planning does not invent a new project phase or silently change the meaning of an existing one. A selected inactive or unplannable phase is recorded as skipped with its reason as a Blocker in the State Log. An open Blocker for an earlier applicable phase stops Planning before a later phase begins. The phase remains the unit selected for planning and development.

<br>

### Groups organize related work

**Rule:** Every Task belongs to one Group. A Group collects Tasks that contribute to one coherent implementation area and explains what that area is, what it accomplishes, and where within the phase's target Component its work belongs. A Group holds the work area and work-specific constraints shared by its Tasks that apply neither to the whole phase nor through another source. Technology choices remain in their owning sources.

**Why:** Grouping supplies this shared context so that an individual Task does not have to carry it.

**Boundary:** The Group does not absorb the activity, expected result, or verification that belong to one Task.

<br>

### A Task is one atomic action

**Rule:** Each Task describes one small, concrete activity with one independently observable result. Large work is divided into as many precise Tasks as necessary.

**Why:** Clarity and executability take precedence over minimizing the number of Tasks.

**Boundary:** A Task never combines unrelated changes or hides several broad outcomes behind one title.

<br>

### Context is written once and inherited

**Rule:** A Plan, its Groups, and their Tasks form one nested structure, and that nesting is the Task's context. A Task's phase is the Plan that contains it and its Group is the Group that contains it; neither is repeated inside the Task. Every piece of context the record does hold — the targeted Component, the work area, and any constraint specific to the work — is recorded exactly once, at the highest level where it holds: in the Plan when it holds for the whole phase, in the Group when it holds for one work area, in the Task only when it is specific to that one activity. Lower levels inherit what higher levels state.

**Why:** The Task identifier carries the Plan and Group identifiers, so a Task can be named unambiguously outside the file while the nesting answers everything else. Context repeated in every Task makes the record large and turns one correction into many edits that can disagree with each other.

**Boundary:** A Task or Group may add to inherited context or make it stricter; it never repeats it and never contradicts it. The same statement never appears in more than one Task of a Plan: when the same statement is being written into several Tasks, it belongs to their common Group or Plan and is moved there.

<br>

### Planning requires the operational Config records

**Rule:** Planning starts only when the Plan Config and State Config exist and are structurally valid. If either required record is missing or invalid, Plan stops and records the unmet prerequisite.

**Why:** Planning needs a place to preserve the Plan and to record aggregate progress and the planning event before it can safely produce work.

**Boundary:** A missing Config prerequisite stops Plan; it does not authorize Plan to create, repair, initialize, or replace that record.

<br>

### Planning establishes current understanding and reconciles existing work

**Rule:** Every invocation establishes current Interface Understanding and Target Understanding, then produces or reconciles the existing Plan against them once. The invocation records its outcome, unresolved conditions, and Skills actually used in one State Log Entry.

**Why:** A later Target, Interface, Principle, or Preference change can change what the phase requires, while an unchanged understanding makes wholesale Task regeneration unnecessary.

**Boundary:** Plan reads State as an execution record and never performs another Core Operation's responsibility. It may use any other suitable available Skill.

<br>

### Every Task is understandable in its context

**Rule:** A Task is read together with its Group and Plan. Read that way, the Task and its inherited context together explain:

- what must be done;
- why the work is necessary;
- what result it must produce;
- which phase and Group provide its planning context;
- which Component and specific work area it targets;
- which applicable authorities and constraints govern it;
- which inputs, dependencies, constraints, and Task Skills matter; and
- how completion is accepted and verified.

The Task itself carries only what is its own: the activity, its reason, its inputs and dependencies, its Task Skills, its expected result, its acceptance and verification, its progress, and any constraint that applies to it alone. Planning records every Skill it identifies as useful for completing the Task in Task Skills. That guidance helps Develop choose a suitable Skill but does not limit Develop to that list.

**Why:** Understanding is a property of the Task together with its place in the Plan, so completeness is measured across the three levels rather than inside one record.

**Boundary:** A Task does not repeat the identity or general description of the project, of its phase, or of its Group. Task Skills are execution guidance, not a record of the Skill that created or changed the Task.

<br>

### A Task is independent of the implementation structure

**Rule:** Planning content in Plans, Groups, and Tasks is expressed in terms of responsibilities, behaviour, and observable results. It never states where anything lives: no file, folder, path, module, package layout, class, function, symbol, or command appears in that planning content, and it never asserts that a particular artifact already exists at a particular location. The target and work area identify a Component and a responsibility inside it, not a directory. Planning content carries no list of sources to consult. Execution history is distinct: a Task's log records the concrete check actually performed, relevant locations, and the observed outcome, with secret values excluded.

**Why:** The shared understanding a Task depends on is produced by the Interface itself — the human project definition together with the applicable Principles and Preferences. That understanding is established from those current sources at the moment the Task is executed, so a Task remains valid when the implementation is rearranged and is never invalidated by a path that has moved.

**Boundary:** Execution evidence describes what happened and does not prescribe future implementation. Language and technology choices remain in their authoritative sources. A work-specific constraint limits observable results or activity scope without defining the code or a new technical requirement.

<br>

### Task defines the activity and Development defines the implementation

**Rule:** A Task defines what must be achieved, why it is needed, where its responsibility belongs, and what evidence demonstrates completion. The targeted Component and the work area are recorded at the level where they hold and inherited by the Task.

**Why:** The implementation method and the arrangement of the source belong to whoever implements the Task, working from the current project sources and the existing implementation.

**Boundary:** Task does not take ownership of its implementation or make a new technical decision.

<br>

### Dependencies are explicit

**Rule:** A Task names every other Task whose completed result it requires. Readiness is derived from those dependencies rather than guessed from file order or proximity inside a Group.

**Why:** Stated prerequisites are what make execution order reliable and let unrelated Tasks proceed at the same time.

**Boundary:** Dependencies express execution order only where a real dependency exists. Unrelated Tasks remain independently executable.

<br>

### Completion must be demonstrable

**Rule:** Every Task states an acceptance criterion and a verification condition, both expressed as observable behaviour. Acceptance states what makes the result correct. Verification states what must be observed to prove it, in terms of the interfaces and behaviour the result publishes, without naming the command, tool, path, or code that observes it. The concrete executable check that satisfies the verification condition is constructed and run at implementation time, and the check used and its outcome are recorded in the Task's log. A Task is complete only when that check has passed. The applicable testing authority determines whether the evidence is persisted or transient; Plan never widens that scope.

**Why:** Writing code or changing a file is never sufficient evidence of completion, and a proof expressed as behaviour survives every rearrangement of the implementation that produces it.

**Boundary:** Verification describes how to prove the expected result after implementation. It never doubles as a hidden implementation procedure.

<br>

### Task progress and Workflow State remain separate

**Rule:** Plan owns Plans, Groups, and Task planning content. It provides the Task status, Blocker reference, and Task Log fields but does not update execution progress. Develop claims eligible work before modifying it, records meaningful progress transitions, and preserves an append-only Task Log while that Task exists.

When a blocking condition is verified as resolved, Develop records the resolution evidence and transition in the Task Log, clears the obsolete Blocker reference, and returns unfinished blocked work to its initial pending status. Dependencies and any remaining blocking conditions are checked again before the Task can be claimed; resolving a Blocker never marks work complete. If another condition still blocks the Task, its reference identifies that current condition. Removal of the State Blocker is coordinated with these updates. A missing Blocker record alone is not evidence of resolution; the underlying condition must be verified before progress is changed.

**Why:** Progress belongs with the work it describes, while the question of where the Workflow stands is shared by everything that touches the project and belongs to one small record.

**Boundary:** State owns active Workflow position, aggregate phase progress, and the Log Entries containing Blockers and Open Questions. Aggregate Planning progress summarizes the phase and never replaces or duplicates Task status and Task log. Each Operation acts only within the authority of the Component that owns the content it changes.

<br>

### Existing work is never silently destroyed

**Rule:** When current Understanding requires replanning, Planning preserves still-valid work and adds newly required work. A Task that Develop has not begun may be removed and replaced. A Task that Develop has begun or completed is never removed or rewritten: Planning creates a new Task with `replaces` pointing to the earlier Task, and Develop marks the earlier Task as `replaced` when that relationship takes effect. Every created or materially changed Task records the State Log Entry identifier of the Planning invocation in `source_id`. Every addition, change, removal, preservation, or replacement is recorded with its reason in that invocation's State Log Entry.

**Why:** Planning runs many times over the life of a phase, and work already done or already underway is the most expensive thing the record holds.

**Boundary:** Planning never silently overwrites meaningful Task content. A Task with a `replaces` reference keeps its earlier Task visible and does not itself change that earlier Task's execution status.

<br>

### The record holds work and progress, not project meaning

**Rule:** Plans, Groups, and Tasks record which work exists, what each activity must produce, what it depends on, where it stands, and what has happened to it. Planning content does not store the project's concepts, its resolved technical choices, the rules of any Component, or an explanation of anything the human project definition, the Principles, and the Preferences already state. Execution history may identify concrete technologies and locations when needed as evidence of an action actually performed; it does not become the authority for choosing them.

**Why:** Those sources are living and authoritative, and a copy of them inside the record goes stale the moment one of them changes, leaving two answers to the same question. Keeping the record to work and progress also keeps it small enough to stay readable as a project grows.

**Boundary:** A constraint is recorded only when it is specific to the work itself and derivable from no other source; anything derivable is resolved from its own source at the moment the work is implemented. This limits what the record stores, never what an implementation must respect.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Every phase has its own Plan**

- **Must** — every planned phase has one Plan holding its identity, order, target, outcome, and phase-wide context
- **Must** — plan selected active and plannable phases in Target order, or every active and plannable phase when none is selected
- **Must** — stop before a later phase when an earlier applicable phase has an open Blocker
- **Never** — planning invents a new phase or silently changes the meaning of an existing one

**Planning requires the operational Config records**

- **Must** — require structurally valid Plan Config and State Config before planning
- **Never** — create, repair, or replace a missing Config record

**Planning establishes current understanding and reconciles existing work**

- **Must** — establish current Interface and Target Understanding, then produce or reconcile the existing Plan once
- **Must** — record the Planning invocation and its outcome in State
- **Must** — record the Planning outcome, unresolved conditions, and Skills actually used in its State Log Entry
- **Never** — treat a previous Plan as current without comparing its Understanding

**Groups organize related work**

- **Must** — every Task belongs to one Group that holds the context its Tasks share
- **Never** — a Group absorbs the activity, expected result, or verification of one Task

**A Task is one atomic action**

- **Must** — each Task is one atomic activity with one independently observable result
- **Never** — a Task combines unrelated changes or hides several outcomes behind one title

**Context is written once and inherited**

- **Must** — every piece of context the record holds is recorded exactly once, at the highest level where it holds
- **Never** — a Task stores its phase or Group, repeats inherited context, or contradicts it
- **Never** — the same statement appears in more than one Task of a Plan

**Every Task is understandable in its context**

- **Must** — a Task carries only what is its own, and is read together with its Group and Plan
- **Must** — record every Skill Planning identifies as useful for completing a Task as Task Skills
- **Never** — a Task repeats the identity or general description of the project, its phase, or its Group

**A Task is independent of the implementation structure**

- **Must** — a Task is expressed in responsibilities, behaviour, and observable results
- **Never** — planning content names a file, folder, path, module, layout, class, function, symbol, or command, asserts an artifact's location, or carries a list of sources to consult
- **Must** — execution history records actual checks, relevant locations, and observed results without secret values or prescriptions for future implementation

**Task defines the activity and Development defines the implementation**

- **Must** — a Task states what must be achieved, why, where the responsibility belongs, and what proves completion
- **Never** — a Task takes ownership of its implementation or makes a technical decision

**Dependencies are explicit**

- **Must** — a Task names every other Task whose completed result it requires
- **Never** — readiness is guessed from file order or proximity inside a Group

**Completion must be demonstrable**

- **Must** — every Task states acceptance and a verification condition, both as observable behaviour
- **Must** — the executable check used and its outcome are recorded in the Task's log, and the Task is complete only once it passes
- **Never** — verification names the command, tool, path, or code that observes it, or doubles as an implementation procedure
- **Must** — let the applicable testing authority determine whether verification evidence is persisted or transient
- **Never** — widen the declared testing scope merely to demonstrate a Task

**Task progress and Workflow State remain separate**

- **Must** — Develop claims eligible work before modifying it and preserves an append-only Task log
- **Must** — authorized Task progress updates record verified Blocker resolution, reconcile its reference and pending status, and recheck dependencies and remaining conditions before claiming work
- **Never** — Blocker removal alone proves resolution, or resolution marks a Task complete
- **Never** — Task duplicates the active Workflow position or the shared Blocker and Open Question records

**Existing work is never silently destroyed**

- **Must** — replanning preserves valid work, adds what is newly required, and records the Planning State Log Entry for every created or materially changed Task
- **Must** — replace a developed Task through a new Task that references it; Develop marks the prior Task as replaced
- **Never** — a developed Task is removed or rewritten by Planning

**The record holds work and progress, not project meaning**

- **Must** — the record holds which work exists, what it must produce, what it depends on, where it stands, and its history
- **Never** — planning content stores project concepts, resolved technical choices, Component rules, or explanations its sources already hold, or execution history becomes the authority for technical choices
- **Never** — a constraint is recorded when it is derivable from the project definition, the Principles, or the Preferences
