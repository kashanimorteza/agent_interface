# Developer Guide

This guide defines the Developer's shared defaults for `my-interface-skill-installer`. The Skill's live authorities and safety boundaries remain controlling.

## Understand the Interface

- At the start of every invocation, read the repository `README.md` completely to understand Agent Interface, its workflow, and this Skill's supporting role. Treat it as Interface context, not as a source of target-project technologies.
- Then read `.interface/root.yaml` as the Interface entry point and current map. Resolve every other path, read order, policy, authority, and boundary from the files currently named by that map.
- Resolve the human-managed project-definition file from the live map and read it completely for current project context.
- Re-read every required source from disk on every invocation. Do not rely on remembered paths, technologies, versions, installation state, configuration, or conclusions from an earlier run.

## Project Knowledge Boundary

- Use `project.md` only to understand the project as a whole. Only `my-interface-interpreter` may interpret it into generated Understanding.
- Use the current generated Understanding to locate authorized target-project areas and determine eligible configured technologies. Do not install from information found only in `project.md`; a mismatch with generated sources requires interpretation first. Within authorized areas, dependency and project files may establish installed technologies and versions as this Skill permits; they do not authorize reinterpretation or expansion of project intent.

## Role Discipline

- Perform only this Skill's technology-Skill discovery and installation responsibility. Do not silently change application dependencies, code, Interface data, or another Skill's work.
- Treat the Developer's invocation as authority only for discovery. Obtain the separate approval required by the Skill before an external installation, update, marketplace addition, or other mutation.
- Apply this guide as discovery and selection guidance, never as permission to widen installation scope, write boundaries, or authority.
- If this guide conflicts with a live policy, authority, permission boundary, or safety requirement, stop and report the conflict instead of guessing.

## Working Defaults

- Prefer current project and catalog evidence over memory or general assumptions.
- Prefer official library-bundled Skills when the installed library provides them, then official or technology-maintained distributions, then trusted third-party candidates.
- Do not equate general Claude capability with the absence or irrelevance of a compatible Skill.

## Reporting

- Ground each technology and candidate in current project, catalog, manifest, and compatibility evidence.
- Distinguish installed, updated, skipped, blocked, and unresolved items, and identify any approval or decision that remains with the Developer.
