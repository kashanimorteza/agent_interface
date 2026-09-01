---
name: my-interface-clear
description: Clear the generated Agent Interface Config so the Interpreter can regenerate it from scratch. Use only when the Developer explicitly asks to clear or reset generated Config and confirms the exact deletion list.
disable-model-invocation: true
---

# Clear generated Config safely

Remove only the generated Config authorized by the current Interface.

## Resolve the clear operation

1. Read `README.md` to understand Agent Interface, its workflow, and the Clear Skill's role. README content is system context only.
2. Read `.interface/root.yaml` to locate generated Config and the authority governing a reset. Do not rely on a deletion path or file list embedded in this Skill.
3. Read the live State contract and the policies of the files that would be removed.
4. Enumerate the exact existing files the authorized clear operation would delete.

Show that exact list to the Developer and request confirmation in the current run. Do not delete anything before the Developer confirms the list. The original request to invoke this Skill does not substitute for confirmation of an unresolved or newly discovered deletion scope.

## Delete

After confirmation, delete exactly the confirmed generated files and nothing else. Keep any directory the Interface map says must remain. Do not use an unresolved variable, wildcard, broad recursive target, or remembered path to determine deletion scope.

Do not modify or delete `README.md`, `.interface/root.yaml`, `.interface/project.md`, Schemas, Skills, target-project code, or anything outside the confirmed generated Config set.

## Completion

Report the files removed, whether the generated Config directory remains ready for regeneration, and whether recovery is available through version control. Stop without invoking the Interpreter automatically.
