---
name: my-interface-skill-installer
description: Discover and install compatible AI Agent Skills for technologies represented in the current generated Understanding. Use for explicit install, synchronization, or refresh requests without changing application dependencies or code.
disable-model-invocation: true
---

# Install technology Skills

Install compatible AI Agent Skills for verified technologies in the configured target project.

## Refresh context and detect

1. Re-read the repository `README.md` to understand Agent Interface and this Skill's supporting role. It is Interface context, not a source of target-project technologies.
2. Re-read `.interface/root.yaml` as the Interface entry point and resolve all other paths and authorities from its current map.
3. Follow the live map to read the generated Understanding that owns project parts, technologies, code locations, and enabled state.
4. Inspect dependency manifests and existing Skill installations only where the current Understanding permits, and only to verify configured technologies and their installed versions.

Re-read every required file from disk on every invocation. Do not rely on remembered technologies, versions, locations, settings, or installation state, and do not copy them into this Skill.

Do not read the human project-definition file. The generated Understanding is the source of configured technology facts; target code may verify them but cannot expand them. Detection is read-only.

## Match and install

For each verified technology:

1. Check the Skills already available to the current Claude Code environment and skip a compatible existing match.
2. Use only discovery and installation capabilities actually available in the current environment. Do not assume undocumented tool names or invent an installation mechanism.
3. Prefer an official or technology-maintained Skill, then a well-matched compatible Skill from a trusted source.
4. Verify major-version compatibility before proposing installation.
5. Present the selected Skill, source, requested permissions, and compatibility evidence to the Developer before any external installation or update.
6. Install or update only after the required user approval is granted through the supported mechanism.

If no supported discovery or installation mechanism is available, report that limitation and the evidence collected; do not work around it by modifying project files or downloading unverified content.

## Boundaries

Determine all write boundaries from the current authorities. Do not change Interface data, application code, architecture, manifests, lockfiles, or runtime dependencies. Do not install for an absent or unverified technology, remove a compatible Skill, or install duplicates.

The operation must be idempotent: a second run against unchanged Config, dependencies, and installed Skills makes no changes.

## Completion

Report each configured technology as installed, updated, skipped, or blocked, including its detected version, selected Skill and source where applicable, and the reason.
