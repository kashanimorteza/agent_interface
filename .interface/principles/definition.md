# Definition Principles

Definition is the Component that expresses a project through five distinct subjects: the project itself, its conceptual Models, its conceptual Structure, its expected Behaviours, and its ordered phases. It describes the project independently of any particular implementation, execution capability, or example project.

Every statement here is mandatory.

<br>

## 1. Project explains what the project is and why it exists

Project contains the project's name, concise description, broader overview, central concept, general information, and independent Goals. It also records project Scope and project-wide Constraints when they are defined.

Description summarizes the project. Overview provides broader context. Concept explains the core idea. Information supplies open-ended context and classification. Goals describe the outcomes the project is intended to achieve. Scope identifies what is included and excluded. Constraints state limitations that apply to the project as a whole.

Goals remain independent from Behaviours and phases: they define intended outcomes without organizing capabilities or delivery work.

<br>

## 2. Models describe the project's concepts

Models identify the concepts and entities that make up the project. Each Model contains only its name and description.

Fields, relationships, data rules, initial data, persistence, API behaviour, and presentation are not part of Definition.

<br>

## 3. Structure describes conceptual organization

Project Structure explains at a high level how the project is conceptually organized. It describes the project as a system without defining source directories, technologies, packages, runtime composition, deployment, or implementation details.

<br>

## 4. Behaviours describe what the project must do

Project Behaviours identify the capabilities the resulting system must provide. Each Behaviour contains only its name and a description of the expected action or capability, never its implementation mechanism.

<br>

## 5. Phases organize project delivery

Phases are ordered units of project work. Each phase has a stable identity, title, order, target, and description of the work it is intended to accomplish.

A phase target identifies the Component addressed by that phase. It does not define the Component, select its technology, or describe how its work is implemented. Any number of phases may address the same Component.

<br>

## 6. Missing project information remains missing

Definition preserves stated project meaning without silently adding project information, Goals, Models, Structure, Behaviours, Scope, Constraints, phases, or other project intent. A structurally present subject or field remains empty when no information exists for it.

<br>

## 7. Project versioning and lifecycle are not modeled

Definition contains no project version, release lifecycle, or communication lifecycle. Technical metadata used elsewhere in the Interface does not create project-level versioning or lifecycle meaning in Definition.
