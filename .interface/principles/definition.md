# Definition Principles

Definition is the Component that expresses what a project is, what it is intended to achieve, the concepts and behaviours that define it, its scope and constraints, and the ordered phases through which it is developed. It describes the project independently of any particular implementation, execution capability, or example project.

Every statement here is mandatory.

<br>

## 1. Definition describes the project, not its implementation

Definition is the semantic overview of a project. It describes project identity, general information, intended outcomes, conceptual Models, expected project Behaviours, scope, project-wide constraints, and ordered phases.

It never defines technologies, packages, runtime composition, deployment, source layout, executable Tasks, workflow State, or implementation details owned by another Component.

<br>

## 2. Definition subjects remain distinct

Identity names and describes the project. Information provides open-ended context and classification. Goals describe the independent outcomes the project is intended to achieve.

Models identify the concepts and entities that make up the project. A Model entry contains only its name and description; fields, relationships, data rules, initial data, persistence, API behaviour, and presentation belong outside Definition.

Project Behaviours identify what the resulting system must be able to do. A Behaviour entry contains only its name and description and states no implementation mechanism.

Scope identifies what is included and excluded. Constraints state project-wide limitations that do not belong to one implementation Component. These subjects may remain empty when the project defines no information for them.

Goals, Behaviours, and phases are independent: Goals state desired outcomes, Behaviours state required capabilities, and phases organize delivery. None is a grouping mechanism for another.

<br>

## 3. Phases organize project delivery

Phases are ordered units of project work. Each phase has a stable identity, title, order, target, and description of the work it is intended to accomplish.

A phase target identifies the Component addressed by that phase. It does not define the Component, select its technology, or describe how its work is implemented. Any number of phases may address the same Component.

<br>

## 4. Missing project information remains missing

Definition preserves stated project meaning without silently adding goals, Models, Behaviours, scope, constraints, phases, or other project intent. A structurally present subject remains empty when no information exists for it.

<br>

## 5. Project versioning and lifecycle are not modeled

Definition contains no project version, release lifecycle, or communication lifecycle. Technical metadata used elsewhere in the Interface does not create project-level versioning or lifecycle meaning in Definition.
