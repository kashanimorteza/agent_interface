---
name: my-interface-skill-installer
description: Discover and install compatible AI Agent Skills for technologies represented in the generated project Config. Use when the Developer explicitly asks to install, synchronize, or refresh technology Skills without changing application dependencies or code.
disable-model-invocation: true
---

# Install technology Skills

Install compatible AI Agent Skills for the technologies used by the configured target project.

## Read and detect

1. Read `README.md` to understand Agent Interface and this Skill's supporting role. README content describes the Interface, not the target project's technologies.
2. Read `.interface/root.yaml` and follow its mappings to the generated Config.
3. Read the Config files that own the target project's parts, technologies, code locations, and enabled state. Do not read `.interface/project.md` and do not hardcode currently known parts or technologies in this Skill.
4. Inspect dependency manifests and existing installations only within the code locations resolved from Config, and only to verify the configured technology and determine its actual installed version.

Config is the source of target-project Understanding. Files in the target code may verify that a configured technology is installed, but they do not authorize adding a technology or expanding the configured project.

Detection must be read-only. Do not install, synchronize, upgrade, or downgrade application dependencies while determining versions.

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

Do not modify Agent Interface Config, application code, architecture, dependency manifests, lockfiles, or runtime dependencies. Do not install a Skill for an absent or unverified technology, remove a compatible Skill, or install duplicates.

The operation must be idempotent: a second run against unchanged Config, dependencies, and installed Skills makes no changes.

## Completion

Report each configured technology as installed, updated, skipped, or blocked, including its detected version, selected Skill and source where applicable, and the reason for the outcome.
