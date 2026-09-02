---
name: my-interface-reset
description: Reset Agent Interface by deleting the currently mapped generated Config files and the exact project code_path directories resolved from them when the Developer explicitly invokes this Skill; no second confirmation is required.
disable-model-invocation: true
---

# Reset generated project state

Return the repository to a clean Agent Interface state by removing only the current generated Config and its configured project code directories.

## Developer guidance

- At the start of every invocation, read the repository `README.md` completely to understand Agent Interface and this Skill's role.
- Then read `.interface/root.yaml` as the live entry point and map, followed only by the existing mapped files under `.interface/config/` needed to resolve the reset.
- Re-read those files from disk on every invocation. Do not use remembered paths, state, configuration, or conclusions from an earlier run.
- Do not read the human project-definition file, other Skill files, or target-project contents. This reset needs only the Interface map and generated Config metadata.
- Perform only the reset role. Do not interpret, plan, develop, review, or invoke another Skill.

## Resolve and validate

1. Resolve the repository root and every exact generated Config file currently mapped by the live Interface.
2. Before deleting any Config file, read the mapped item Config files and collect each exact `code_path`. Resolve each path relative to the repository root as its current Config specifies, then deduplicate the targets.
3. Require every code-directory target to be a non-empty relative path without `..`, to resolve as a strict descendant of the repository root, and to remain outside `.interface/`, `.claude/`, and `.git/`. Refuse symlinks, files where a directory is expected, unresolved paths, and any protected or unmapped target.
4. Validate the complete deletion set before deleting anything. Missing mapped Config files or absent validated code directories require no deletion and are not errors; an unsafe or ambiguous target stops the entire reset.

The explicit invocation of this Skill authorizes the validated deletion set. Proceed without requesting another confirmation.

## Reset

Delete each existing validated `code_path` directory recursively by its explicit resolved path, then delete each existing mapped generated Config file by its explicit path. Preserve the Config directory itself.

Do not use wildcards, unresolved variables, inferred folder names, or broad recursive targets. Never delete `README.md`, `.interface/root.yaml`, the human project definition, `.interface/schema/`, `.claude/`, `.git/`, or anything outside the validated deletion set.

## Completion

Verify that every existing target selected for deletion is absent. Return one brief result listing the Config files and project directories removed. Do not invoke another Skill automatically.
