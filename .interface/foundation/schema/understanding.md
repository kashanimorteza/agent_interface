# Understanding File Structure

This document is the common structure every Understanding file follows. One Understanding file may exist per Implementation Component at `.interface/implementation/<component>/understanding.md` and per Agent Component at `.interface/agent/<component>/understanding.md`, beside that Component's `principles.md` and `preferences.yaml`.

It is optional: a Component whose Understanding has not been recorded has no such file. It is human-owned and never written by an Interface operation.


<!--------------------------------------------------------------------------------- Purpose --->
<br>

## Purpose

How the Human explained this Component, in their own words, and what was decided along the way.

The Principles state what holds. This part preserves how the Human arrived there, so that a later session — human or Agent — does not have to rediscover the reasoning, and so that a question already settled is not reopened as if it were new. Each entry names its subject under a fourth-level heading, gives the Human's explanation close to the words they used, and lists the decisions it produced, including the proposals that were not accepted and why:

```markdown
# <Component> Understanding

## <Subject>

**<The question the Human is answering>** <Their explanation, in their own words.>

**Decisions:**

1. <what holds, and what it replaces>
2. <a proposal that was not accepted, and why — so it is not proposed again>
```

It is written close to how the Human said it, not translated into the file's formal voice, because the wording is part of what is being preserved. A proposal that was not accepted is recorded with its reason; without that, the same suggestion returns in the next session.

It carries no dates, and it is written in the present tense. It states what holds now and what it replaces, and is rewritten when the Human's understanding changes — the file is the current picture, not a log of when each part of it arrived.

This part is a record, never an authority. Where the record and a Principle disagree, the Principle is correct and the record is out of date. A Component whose Understanding has not been recorded omits it.


<!--------------------------------------------------------------------------------- Structure --->
<br>

## Structure

The file opens with one first-level heading naming the Component — `# <Component> Understanding` — and carries one second-level heading per subject, in the order the subjects were settled. Each subject carries the Human's explanation and then its numbered **Decisions:** list. A `<br>` separates each subject from the next.

The Principles file links to it from its Introduction and does not repeat what it holds.


<!--------------------------------------------------------------------------------- Template --->
<br>

## Template

```markdown
# <Component> Understanding

## <Subject>

**<The question the Human is answering>** <Their explanation, in their own words.>

**Decisions:**

1. <what holds, and what it replaces>
2. <a proposal that was not accepted, and why — so it is not proposed again>

<br>

## <Subject>

...
```
