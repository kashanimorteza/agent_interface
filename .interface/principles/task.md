# Task Principles

Task is the Component that turns project phases into precise, bounded activities. It organizes those activities as Plans, Groups, and Tasks while preserving enough context for either a human or an Agent to understand what each Task requires and how its result is evaluated.

Every statement here is mandatory. Technical defaults, when any are defined, belong to Task Preferences. The exact shape of the generated Task configuration belongs to the Task Schema.

<br>

## 1. Every phase has its own Plan

A Plan represents the work required by one project phase. It preserves the phase's identity, order, target, and intended outcome, then decomposes that outcome into Groups and Tasks.

Planning does not invent a new project phase or silently change the meaning of an existing one. The phase remains the unit selected for planning and development.

<br>

## 2. Groups organize related work

Every Task belongs to one Group. A Group collects Tasks that contribute to one coherent implementation area and explains what that area is, what it accomplishes, which Component it targets, and where within that Component its work belongs.

Grouping supplies useful shared context, but it never replaces the information carried by an individual Task.

<br>

## 3. A Task is one atomic action

Each Task describes one small, concrete activity with one independently observable result. A Task never combines unrelated changes or hides several broad outcomes behind one title.

Large work is divided into as many precise Tasks as necessary. Clarity and executability take precedence over minimizing the number of Tasks.

<br>

## 4. Every Task is independently understandable

A Task remains understandable when viewed outside its Plan, Group, or project. It carries enough information to explain:

- what must be done;
- why the work is necessary;
- what result it must produce;
- which phase and Group provide its planning context;
- which Component and specific work area it targets;
- which resolved language and technology metadata apply, when relevant;
- which inputs, dependencies, constraints, and existing resources matter; and
- how completion is accepted and verified.

The Task does not need to repeat the identity or general description of the project. Its metadata identifies its phase and Group without requiring its nesting location to be known. It carries the context required to understand its activity and expected result, while Development reads the applicable generated configuration before deciding how to implement it.

<br>

## 5. Task defines the activity and Development defines the implementation

A Task defines what must be achieved, why it is needed, where its responsibility belongs, which resolved constraints apply, and what evidence demonstrates completion. It may record descriptive context already resolved by Planning or generated configuration, such as its phase, Group, target, language, relevant technologies, and interface references.

Task does not prescribe implementation steps, algorithms, source layout, classes, functions, code, commands for performing the work, or new technical decisions. It does not guess the files that Development should change. Development owns the implementation method and reads the referenced generated configuration and current implementation when executing the Task.

Verification describes how to prove the expected result after implementation. It never doubles as a hidden implementation procedure.

<br>

## 6. Dependencies are explicit

A Task names every other Task whose completed result it requires. Readiness is derived from those dependencies rather than guessed from file order or proximity inside a Group.

Dependencies express execution order only where a real dependency exists. Unrelated Tasks remain independently executable.

<br>

## 7. Completion must be demonstrable

Every Task has a concrete acceptance criterion and a runnable verification method. Writing code or changing a file is not sufficient evidence of completion; the verification must pass before the Task is considered done.

<br>

## 8. Task progress and Workflow State remain separate

The Task Component owns Plans, Groups, Task content, Task status, a Task's reference to any Blocker, and Task-local history. The State Component records the active Workflow position and owns the shared records for critical Blockers and Open Questions.

An executor claims eligible work before modifying it, records meaningful progress transitions, and preserves an append-only Task log while that Task exists. Each operation may change only the portions owned by its own contract; the current State mode records the operation but does not grant or deny that permission.

<br>

## 9. Existing work is never silently destroyed

Replanning or regeneration reconciles unchanged work and adds newly required work without silently overwriting completed, active, or otherwise meaningful Task content. Removing or invalidating such work requires an explicit authorized operation or a surfaced critical conflict.
