# Task Principles

Task is the Component that turns project phases into precise, bounded activities and organizes them as Plans, Groups, and Tasks. It is the standard by which work is broken down: it decides what an activity must contain to be understood and executed, how activities are organized so that shared context is stated once, and what counts as proof that one is finished. Every Plan, Group, and Task in the project is produced and read under this standard.

## Terms

- **Plan** — the work required by one project phase, holding the context that applies to the whole phase and decomposing its outcome into Groups.
- **Group** — one coherent implementation area within a Plan, holding the context its Tasks share.
- **Task** — one small, concrete activity with one independently observable result.
- **Phase** — the project stage a Plan represents, identified by its order and target.
- **Dependency** — another Task whose completed result this Task requires before it can begin.
- **Acceptance** — the observable criterion that determines whether a Task's result is correct.
- **Verification** — the condition that must be observed to prove acceptance, stated as behaviour rather than as a command.
- **Status** — the current progress value of a Task.
- **Log** — the append-only record of a Task's meaningful transitions and the evidence of its completion.

## Relationships

- **Consumes State** — the shared Blocker records a Task refers to when it cannot proceed.
- **Consumed by no other Component** — Task records the work; no Component depends on its contents.

Technical choices and defaults belong to Task Preferences, which currently define none. The exact shape of the generated Task configuration belongs to the Task Schema.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every phase has its own Plan

**Rule:** A Plan represents the work required by one project phase. It preserves the phase's identity, order, target, and intended outcome, then decomposes that outcome into Groups and Tasks. The Plan is also the home of everything that holds for the whole phase: the Component it targets, the resolved language and technologies, and the constraints every Task of the phase must respect.

**Why:** Stated once in the Plan, that context is inherited by every Group and Task beneath it, so the phase is described in one place rather than restated by everything it contains.

**Boundary:** Planning does not invent a new project phase or silently change the meaning of an existing one. The phase remains the unit selected for planning and development.

<br>

## 2. Groups organize related work

**Rule:** Every Task belongs to one Group. A Group collects Tasks that contribute to one coherent implementation area and explains what that area is, what it accomplishes, and where within the phase's target Component its work belongs. A Group is the home of the context its Tasks share: the work area, the constraints that apply to that area but not to the whole phase, and any technology that only that area uses.

**Why:** Grouping supplies this shared context so that an individual Task does not have to carry it.

**Boundary:** The Group does not absorb the activity, expected result, or verification that belong to one Task.

<br>

## 3. A Task is one atomic action

**Rule:** Each Task describes one small, concrete activity with one independently observable result. Large work is divided into as many precise Tasks as necessary.

**Why:** Clarity and executability take precedence over minimizing the number of Tasks.

**Boundary:** A Task never combines unrelated changes or hides several broad outcomes behind one title.

<br>

## 4. Context is written once and inherited

**Rule:** A Plan, its Groups, and their Tasks form one nested structure, and that nesting is the Task's context. A Task's phase is the Plan that contains it and its Group is the Group that contains it; neither is repeated inside the Task. Every piece of context the record does hold — the targeted Component, the work area, and any constraint specific to the work — is recorded exactly once, at the highest level where it holds: in the Plan when it holds for the whole phase, in the Group when it holds for one work area, in the Task only when it is specific to that one activity. Lower levels inherit what higher levels state.

**Why:** The Task identifier carries the Plan and Group identifiers, so a Task can be named unambiguously outside the file while the nesting answers everything else. Context repeated in every Task makes the record large and turns one correction into many edits that can disagree with each other.

**Boundary:** A Task or Group may add to inherited context or make it stricter; it never repeats it and never contradicts it. The same statement never appears in more than one Task of a Plan: when the same statement is being written into several Tasks, it belongs to their common Group or Plan and is moved there.

<br>

## 5. Every Task is understandable in its context

**Rule:** A Task is read together with its Group and Plan. Read that way, the Task and its inherited context together explain:

- what must be done;
- why the work is necessary;
- what result it must produce;
- which phase and Group provide its planning context;
- which Component and specific work area it targets;
- which resolved language and technologies apply, as the applicable Preferences state them;
- which inputs, dependencies, and constraints matter; and
- how completion is accepted and verified.

The Task itself carries only what is its own: the activity, its reason, its inputs and dependencies, its expected result, its acceptance and verification, its progress, and any constraint that applies to it alone.

**Why:** Understanding is a property of the Task together with its place in the Plan, so completeness is measured across the three levels rather than inside one record.

**Boundary:** A Task does not repeat the identity or general description of the project, of its phase, or of its Group.

<br>

## 6. A Task is independent of the implementation structure

**Rule:** A Task is expressed in terms of responsibilities, behaviour, and observable results. It never states where anything lives: no file, folder, path, module, package layout, class, function, symbol, or command appears in a Task, and a Task never asserts that a particular artifact already exists at a particular location. The Task's target and work area identify a Component and a responsibility inside it, not a directory. A Task carries no list of sources to consult.

**Why:** The shared understanding a Task depends on is produced by the Interface itself — the human project definition together with the applicable Principles and Preferences. That understanding is established from those current sources at the moment the Task is executed, so a Task remains valid when the implementation is rearranged and is never invalidated by a path that has moved.

**Boundary:** Language and technology metadata identify what has been resolved, not how the source is arranged. When a Task must constrain the result, it constrains observable behaviour and the boundaries the result must respect, not the shape of the code that produces it.

<br>

## 7. Task defines the activity and Development defines the implementation

**Rule:** A Task defines what must be achieved, why it is needed, where its responsibility belongs, and what evidence demonstrates completion. The targeted Component and the work area are recorded at the level where they hold and inherited by the Task.

**Why:** The implementation method and the arrangement of the source belong to whoever implements the Task, working from the current project sources and the existing implementation.

**Boundary:** Task does not prescribe implementation steps, algorithms, source layout, classes, functions, code, or commands for performing the work, and it makes no new technical decision.

<br>

## 8. Dependencies are explicit

**Rule:** A Task names every other Task whose completed result it requires. Readiness is derived from those dependencies rather than guessed from file order or proximity inside a Group.

**Why:** Stated prerequisites are what make execution order reliable and let unrelated Tasks proceed at the same time.

**Boundary:** Dependencies express execution order only where a real dependency exists. Unrelated Tasks remain independently executable.

<br>

## 9. Completion must be demonstrable

**Rule:** Every Task states an acceptance criterion and a verification condition, both expressed as observable behaviour. Acceptance states what makes the result correct. Verification states what must be observed to prove it, in terms of the interfaces and behaviour the result publishes, without naming the command, tool, path, or code that observes it. The concrete executable check that satisfies the verification condition is constructed and run at implementation time, and the check used and its outcome are recorded in the Task's log. A Task is complete only when that check has passed.

**Why:** Writing code or changing a file is never sufficient evidence of completion, and a proof expressed as behaviour survives every rearrangement of the implementation that produces it.

**Boundary:** Verification describes how to prove the expected result after implementation. It never doubles as a hidden implementation procedure.

<br>

## 10. Task progress and Workflow State remain separate

**Rule:** The Task Component owns Plans, Groups, Task content, Task status, a Task's reference to any Blocker, and Task-local history. An executor claims eligible work before modifying it, records meaningful progress transitions, and preserves an append-only Task log while that Task exists.

**Why:** Progress belongs with the work it describes, while the question of where the Workflow stands is shared by everything that touches the project and belongs to one small record.

**Boundary:** The State Component records the active Workflow position and owns the shared records for critical Blockers and Open Questions. Each operation may change only the portions owned by its own contract; the current State mode records the operation but does not grant or deny that permission.

<br>

## 11. Existing work is never silently destroyed

**Rule:** Replanning or regeneration reconciles unchanged work and adds newly required work without silently overwriting completed, active, or otherwise meaningful Task content.

**Why:** Planning runs many times over the life of a phase, and work already done or already underway is the most expensive thing the record holds.

**Boundary:** Removing or invalidating such work requires an explicit authorized operation or a surfaced critical conflict.

<br>

## 12. The record holds work and progress, not project meaning

**Rule:** Plans, Groups, and Tasks record which work exists, what each activity must produce, what it depends on, where it stands, and what has happened to it. They do not store the project's concepts, its resolved technical choices, the rules of any Component, or an explanation of anything the human project definition, the Principles, and the Preferences already state.

**Why:** Those sources are living and authoritative, and a copy of them inside the record goes stale the moment one of them changes, leaving two answers to the same question. Keeping the record to work and progress also keeps it small enough to stay readable as a project grows.

**Boundary:** A constraint is recorded only when it is specific to the work itself and derivable from no other source; anything derivable is resolved from its own source at the moment the work is implemented. This limits what the record stores, never what an implementation must respect.

<br>

## At a Glance

- **Must** — every phase has one Plan holding its identity, order, target, outcome, and phase-wide context *(1)*
- **Never** — planning invents a new phase or silently changes the meaning of an existing one *(1)*
- **Must** — every Task belongs to one Group that holds the context its Tasks share *(2)*
- **Never** — a Group absorbs the activity, expected result, or verification of one Task *(2)*
- **Must** — each Task is one atomic activity with one independently observable result *(3)*
- **Never** — a Task combines unrelated changes or hides several outcomes behind one title *(3)*
- **Must** — every piece of context the record holds is recorded exactly once, at the highest level where it holds *(4)*
- **Never** — a Task stores its phase or Group, repeats inherited context, or contradicts it *(4)*
- **Never** — the same statement appears in more than one Task of a Plan *(4)*
- **Must** — a Task carries only what is its own, and is read together with its Group and Plan *(5)*
- **Never** — a Task repeats the identity or general description of the project, its phase, or its Group *(5)*
- **Must** — a Task is expressed in responsibilities, behaviour, and observable results *(6)*
- **Never** — a file, folder, path, module, layout, class, function, symbol, or command appears in a Task *(6)*
- **Never** — a Task asserts that an artifact exists at a location, or carries a list of sources to consult *(6)*
- **Must** — a Task states what must be achieved, why, where the responsibility belongs, and what proves completion *(7)*
- **Must** — the record holds which work exists, what it must produce, what it depends on, where it stands, and its history *(12)*
- **Never** — the record stores project concepts, resolved technical choices, Component rules, or explanations its sources already hold *(12)*
- **Never** — a constraint is recorded when it is derivable from the project definition, the Principles, or the Preferences *(12)*
- **Never** — a Task prescribes implementation steps, algorithms, source layout, code, or commands, or makes a technical decision *(7)*
- **Must** — a Task names every other Task whose completed result it requires *(8)*
- **Never** — readiness is guessed from file order or proximity inside a Group *(8)*
- **Must** — every Task states acceptance and a verification condition, both as observable behaviour *(9)*
- **Must** — the executable check used and its outcome are recorded in the Task's log, and the Task is complete only once it passes *(9)*
- **Never** — verification names the command, tool, path, or code that observes it, or doubles as an implementation procedure *(9)*
- **Must** — an executor claims eligible work before modifying it and preserves an append-only Task log *(10)*
- **Never** — Task duplicates the active Workflow position or the shared Blocker and Open Question records *(10)*
- **Must** — replanning reconciles unchanged work and adds what is newly required *(11)*
- **Never** — completed, active, or meaningful Task content is removed without an authorized operation or a surfaced conflict *(11)*
