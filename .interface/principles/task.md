# Task Principles

Task is the Component that turns project phases into precise, executable work. It organizes that work as Plans, Groups, and Tasks while preserving enough context for either a human or an Agent to understand and execute every Task reliably.

Every statement here is mandatory. Technical defaults, when any are defined, belong to Task Preferences. The exact shape of the generated Task configuration belongs to the Task Schema.

<br>

## 1. Every phase has its own Plan

A Plan represents the implementation of one project phase. It preserves the phase's identity, order, target, and intended outcome, then decomposes that outcome into Groups and Tasks.

Planning does not invent a new project phase or silently change the meaning of an existing one. The phase remains the unit selected for planning and development.

<br>

## 2. Groups organize related work

Every Task belongs to one Group. A Group collects Tasks that contribute to one coherent implementation area and explains what that area is, what it accomplishes, which Component it targets, and where within that Component its work belongs.

Grouping supplies useful shared context, but it never replaces the information carried by an individual Task.

<br>

## 3. A Task is one atomic action

Each Task describes one small, concrete implementation action that can be completed and verified independently. A Task never combines unrelated changes or hides several broad outcomes behind one title.

Large work is divided into as many precise Tasks as necessary. Clarity and executability take precedence over minimizing the number of Tasks.

<br>

## 4. Every Task is independently understandable

A Task remains understandable when viewed outside its Plan, Group, or project. It carries enough information to explain:

- what must be done;
- why the work is necessary;
- what result it must produce;
- which Component and specific work area it targets;
- which language, technologies, and execution context apply;
- which inputs, dependencies, constraints, and existing resources matter;
- which files or resources it may touch; and
- how completion is accepted and verified.

The Task does not need to repeat the identity or general description of the project. It does need all context required to understand and perform its own work without reconstructing that context from unrelated documents.

<br>

## 5. Task context is resolved from authoritative project Understanding

The target, language, technologies, paths, interfaces, constraints, and other implementation context written into a Task are resolved from the applicable generated Component configurations. A Task does not create a competing technical decision.

The Task records the resolved context it needs so its executor does not have to rediscover that context before work can begin.

<br>

## 6. Dependencies are explicit

A Task names every other Task whose completed result it requires. Readiness is derived from those dependencies rather than guessed from file order or proximity inside a Group.

Dependencies express execution order only where a real dependency exists. Unrelated Tasks remain independently executable.

<br>

## 7. Completion must be demonstrable

Every Task has a concrete acceptance criterion and a runnable verification method. Writing code or changing a file is not sufficient evidence of completion; the verification must pass before the Task is considered done.

<br>

## 8. Task progress and workflow authority remain separate

The Task Component owns Plans, Groups, Task content, Task status, blockers, and Task-local history. The State Component owns the workflow authority that decides when and under which conditions those values may change.

An executor claims eligible work before modifying it, records meaningful progress transitions, and preserves an append-only Task log while that Task exists. Planning, development, reconciliation, and reset operations may change only the portions authorized by the current State.

<br>

## 9. Existing work is never silently destroyed

Replanning or regeneration reconciles unchanged work and adds newly required work without silently overwriting completed, active, or otherwise meaningful Task content. Removing or invalidating such work requires an explicit authorized operation or a surfaced critical conflict.
