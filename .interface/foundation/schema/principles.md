# Principles File Structure

This document is the common structure every Principles file follows. It defines the shape of a Principles file, not the content of any Component. Each Component describes itself inside this shape so that every Principles file is written, read, and reasoned about the same way.

One Principles file exists per Component, at `.interface/developer/<component>/principles.md`. The file is human-owned: Interface operations read it and never write to it.


<!--------------------------------------------------------------------------------- Purpose --->
<br>

## Purpose

A Principles file exists to raise understanding of the project. It answers what a Component is, what responsibility it holds, and under which mandatory rules it operates, so that any reader — human or Agent — can reason about the Component without inspecting an implementation.

A Component describes its own responsibilities, boundaries, and relationships with other Components, including what it consumes and provides. It does not assign roles to Skills or Agents, prescribe their Workflows, or decide which Skill reads it and when. Those decisions belong to the Agent layer that consumes these files.


<!--------------------------------------------------------------------------------- Scope --->
<br>

## Scope

A Principles file contains only mandatory philosophy, responsibilities, and boundaries. It is independent of specific tools, versions, third-party packages, providers, and any particular project. Architectural concepts such as packages, modules, layers, and their ownership and public interfaces are permitted.

A Principles file never contains:

- a specific tool, library, framework, engine, third-party package, or version selection, or a concrete filename, folder name, path, or implementation layout; these choices belong to Preferences;
- a technical default or a resolved technical choice, which belong to the Component's Preferences;
- the shape of a generated file, which belongs to the Component's Schema when one exists; or
- instructions assigning roles to Skills or Agents, prescribing their Workflows, or deciding which Skill reads the Component and when.

Relationships between Components are permitted and belong in Relationships. They describe what each Component consumes or provides without directing a Skill's execution.

A Principle is portable: the same file can be handed unchanged to another project or another Agent.


<!--------------------------------------------------------------------------------- Structure --->
<br>

## Structure

Every Principles file contains these parts, in this order:

1. **Title** — the file's single first-level heading.
2. **Introduction** — what the Component is and what it contributes.
3. **Terms** — the vocabulary the Component owns.
4. **Relationships** — what it consumes and what consumes it.
5. **Layering** — where the Component's technical choices live instead.
6. **Authority** — the binding force of the file and its precedence.
7. **Principles** — the numbered mandatory rules.
8. **At a Glance** — the derived list of every obligation in the file.

Introduction, Layering, and Authority are unheaded prose. Terms, Relationships, and At a Glance carry their own second-level heading. Every numbered second-level heading in the file is a Principle. A `<br>` separates each part from the next and each Principle from the next.


<!--------------------------------------------------------------------------------- Title --->
<br>

## Title

The file opens with one first-level heading naming the Component:

```markdown
# <Component> Principles
```

No other first-level heading appears in the file.


<!--------------------------------------------------------------------------------- Introduction --->
<br>

## Introduction

One or two paragraphs in which the Component introduces itself: what it is, the responsibility it holds, what it contributes to the project, and what it is independent of.

It is written about the Component, never about the document: it begins by defining the Component, not by describing what the file contains. It states what the Component *is* and *does*. Relationships with other Components belong in Relationships; instructions about Skill roles, execution order, or when a Skill should read the Component do not belong in this file.

The Component's own boundary — what it does not own — is stated explicitly, either as the closing sentences of Introduction or as one dedicated Principle. It is never left implicit and never stated in both places.


<!--------------------------------------------------------------------------------- Terms --->
<br>

## Terms

A short definition list of the terms this Component owns — the capitalized concepts its Principles use and that a reader would otherwise have to infer from the prose.

```markdown
## Terms

- **<Term>** — <one sentence defining it within this Component>
```

A term is listed only when this Component owns it. A term owned by another Component is used as that Component defines it and is not redefined here. Terms defined by the Interface itself, such as Component, Principle, and Preference, are not repeated in any Component's list.


<!--------------------------------------------------------------------------------- Relationships --->
<br>

## Relationships

A short list naming the other Components this Component consumes and the other Components that consume it, each with the reason for the connection.

```markdown
## Relationships

- **Consumes <Component>** — <what it takes and why>
- **Consumed by <Component>** — <what it provides and why>
```

Relationships are stated between Components only. No Skill, operation, Mode, or Workflow step appears here. A Component that consumes nothing, or that nothing consumes, records that fact rather than inventing a connection.


<!--------------------------------------------------------------------------------- Layering --->
<br>

## Layering

One paragraph placing the Component's technical choices outside this file, and naming what holds them:

- technical choices and defaults belong to the Component's Preferences;
- implementation applies those choices to the current project definition; and
- when the Component owns a generated file, the shape of that file belongs to its Schema.

A Component whose Preferences currently define nothing still states where its technical choices would belong. The absence of defaults is a fact about today's Preferences, not a reason to omit the layering statement.


<!--------------------------------------------------------------------------------- Authority --->
<br>

## Authority

One paragraph, stating all three of:

- every statement in the file is mandatory;
- a Preference can never override a Principle; and
- a project may only add stricter rules, never looser ones.

No Principles file omits or weakens any of the three.


<!--------------------------------------------------------------------------------- Principles --->
<br>

## Principles

Each Principle is a second-level heading carrying its number and a title, followed by three labelled subsections:

```markdown
## <N>. <Title>

**Rule:** <the mandatory statement>

**Why:** <the reason the rule exists>

**Boundary:** <the limit of the rule>
```

### Title

The title states the rule as a claim, not as a topic: `Data Access is the only Backend route to Database`, not `Data Access`. It is read alone in a list of Principles and still communicates the rule.

### Rule

The mandatory statement itself, written in the present tense as something that holds rather than something to do. It uses the binding words — *is*, *must*, *only*, *never* — and remains free of tools, versions, and locations.

The Rule may be one sentence or several, and may carry a list when the rule enumerates parts, such as the layers a Component is formed from or the values a field accepts. It states the rule completely; a reader who reads only the Rule subsections of a file has read every obligation the file imposes.

### Why

The reason the rule exists: what it protects, what it makes possible, or what breaks without it. It never introduces a new obligation. A statement that a reader would have to obey belongs in Rule.

### Boundary

The limit of the rule: what it does not authorize, the adjacent responsibility it must not absorb, the case it does not reach, or the decision it leaves to another authority.

Every Principle has one, because a rule with no stated limit is read as unlimited. When the limit is that no exception exists, Boundary says so.

### Numbering

Principles are numbered from 1 in a single sequence. A number is permanent once assigned: a new Principle is appended after the highest existing number, and removing a Principle never renumbers the ones that follow it. This keeps a Principle citable as `<Component> Principle <N>` across versions of the file.

### Order

Principles are ordered so that the ones establishing the Component's own shape come before the ones governing its relationships with other Components. Within that, order follows the reading path a newcomer needs rather than importance.


<!--------------------------------------------------------------------------------- At a Glance --->
<br>

## At a Glance

The closing section: every obligation in the file, one line each, in Principle order.

```markdown
## At a Glance

- **Must** — <the obligation in one line> *(1)*
- **Never** — <the prohibition in one line> *(1)*
- **Must** — <the obligation in one line> *(2)*
```

Each line is labelled **Must** or **Never** and carries the number of the Principle it comes from. A Principle contributes as many lines as it has distinct obligations, and every obligation in the file appears exactly once in this list.

This section is derived, never authoritative. It introduces no rule that its Principle does not already state, and it is rewritten whenever a Principle changes. When the list and a Principle disagree, the Principle is correct.


<!--------------------------------------------------------------------------------- Template --->
<br>

## Template

```markdown
# <Component> Principles

<Introduction: what the Component is, the responsibility it holds, what it contributes,
what it is independent of, and what it does not own.>

## Terms

- **<Term>** — <definition within this Component>

## Relationships

- **Consumes <Component>** — <what it takes and why>
- **Consumed by <Component>** — <what it provides and why>

<Layering: technical choices and defaults belong to <Component> Preferences; implementation
applies them to the current project definition.>

Every statement here is mandatory. A Preference can never override a Principle, and a project
may only add stricter rules, never looser ones.

<br>

## 1. <Title stating the rule as a claim>

**Rule:** <the mandatory statement>

**Why:** <the reason it exists>

**Boundary:** <the limit of the rule>

<br>

## 2. <Title>

**Rule:** ...

**Why:** ...

**Boundary:** ...

<br>

## At a Glance

- **Must** — <obligation> *(1)*
- **Never** — <prohibition> *(2)*
```
