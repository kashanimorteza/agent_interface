---
name: my-interface-skill-installer
description: Discover and install compatible AI Agent Skills for technologies present in the configured target project. Use for explicit install, synchronization, or refresh requests without changing application dependencies or code.
disable-model-invocation: true
---

# Install technology Skills

Install compatible AI Agent Skills for technologies found in the configured target project. A technology's presence in the project makes it eligible; do not dismiss a compatible Skill merely because the technology is common or Claude Code can work with it without one.

## Load the live Interface and detect

Read `README.md`, then use `.interface/root.yaml` as the sole entry point for discovering the current Interface. Follow its live map and read order to locate the human project definition, generated Understanding, configured target-project locations, current authorities, and read and write boundaries.

Re-read required sources on every invocation. Do not rely on remembered paths, file shapes, technologies, versions, permissions, or installation state. Use the human project definition for context only; detect eligible technologies from the current generated configuration and from dependency manifests, lockfiles, runtime-version files, and framework configuration inside authorized target-project locations.

Check project and personal Skills currently visible to Claude Code, then inspect installed plugins with `claude plugin list --json` so compatible existing capabilities are not duplicated.

Detection is read-only. A part's inactive phase does not make a technology absent and is not a reason to skip matching it.

## Match and install

For each detected technology:

1. Skip installation when a compatible Skill is already available in the current Claude Code environment.
2. Treat the Bash-accessible Claude Code CLI as a supported discovery and installation capability; do not decide it is unavailable merely because no dedicated marketplace tool appears in the model's tool list. Verify it with `command -v claude` and `claude plugin --help`.
3. List configured marketplaces with `claude plugin marketplace list` and query their catalogs with `claude plugin list --available --json`. This is the primary supported discovery mechanism. Plugin marketplaces are valid Skill distribution: a plugin may bundle one or more Skills.
4. Match candidates by their declared purpose, source, and component inventory, not by name alone. Inspect the catalog metadata and the candidate's marketplace or upstream manifest at its declared source, or use the interactive `/plugin` details pane. Do not claim a candidate supplies a relevant Skill until its components confirm that; a name match or an LSP/MCP component alone is not a Skill match.
5. Prefer a matching candidate from `claude-plugins-official`, then a technology-maintained candidate from another configured marketplace, then a trusted third-party candidate. If discovery identifies an unconfigured marketplace, adding it is a separate external change that requires approval.
6. Verify major-version compatibility before proposing installation.
7. Present the selected plugin and Skill, marketplace and upstream source, installation scope, all bundled components or permissions, and compatibility evidence to the Developer before any external installation or update. Recommend `local` scope for a project-specific match unless the Developer chooses `project` or `user` scope.
8. After approval, install with `claude plugin install <plugin@marketplace> --scope <local|project|user>`. Do not pass `--yes` for a command-based source unless the Developer explicitly approved that command. Verify the result with `claude plugin list --json`; use `claude plugin details <plugin>` after installation when component verification is useful, and report when `/reload-plugins` is needed for activation.

Do not replace discovery with an assessment that a dedicated Skill is unnecessary. General-purpose Claude Code support, library popularity, or a technology being standard are not reasons to reject an available compatible Skill.

If the Claude CLI is present and `claude plugin list --available --json` succeeds, discovery is available even when there is no dedicated marketplace API tool. If supported discovery finds no compatible candidate, report the marketplaces and candidate fields checked and mark that technology as skipped; do not make a broader claim that technology-specific Skills do not exist. Mark technologies as blocked for missing discovery only after both the Claude CLI commands above and any documented interactive `/plugin` capability available in the session have been checked. Do not work around a genuine limitation by modifying project files or downloading unverified content.

## Boundaries

Determine all write boundaries and responses to missing or conflicting information from the current authorities. Do not change Interface data, application code, architecture, manifests, lockfiles, or runtime dependencies. Do not install for a technology that was not detected inside a configured target-project location, remove a compatible Skill, or install duplicates.

The operation must be idempotent: a second run against unchanged Config, dependencies, and installed Skills makes no changes.

## Completion

Report each detected technology as installed, updated, skipped, or blocked. Include the project file that established its presence, its detected version or `unresolved`, the selected Skill and source where applicable, and the reason for the status.
