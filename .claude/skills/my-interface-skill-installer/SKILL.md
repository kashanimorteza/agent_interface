---
name: my-interface-skill-installer
description: Discover and install compatible AI Agent Skills for the technologies present in the current target project. Use for an explicit install, synchronization, or refresh request; never changes application dependencies or code.
disable-model-invocation: true
---

# Install technology Skills

## Role

Support the target project by discovering and, after approval, installing compatible AI Agent Skills for the technologies it actually uses.

A technology's presence in the project makes it eligible. Do not dismiss a compatible Skill because the technology is common, popular, or something the agent can already work with unaided: a Skill carries current practice for that technology, which general capability does not.

This operation equips the agent with Skills. Determine the actual installation scope and location from the environment's supported mechanism, and report whether the installed resources are stored in the repository or depend on machine-local setup. Do not assume that an installation travels with a checkout. Skill installation does not add application dependencies; installing what the project needs in order to run is Development's work.

Detection reads what the project actually uses, which is not always what it chose. A technology found in the implementation but absent from the Preferences is still eligible, and the mismatch itself is worth reporting: it means the project is running on something its own choices do not describe.

## Workflow

### Detect

First establish Agent Interface Understanding by reading the canonical Interface document and the shared Skill rules it catalogues. Use it to understand the Interface organization, Skill Installer's supporting role, and the current locations of the relevant project sources.

Then establish Target Project Understanding by reading the human project definition and the applicable Principles and Preferences. Detect the eligible technologies from those current sources, and inspect dependency manifests, lockfiles, runtime-version files, framework configuration, and the existing implementation as compatibility and installation evidence. The operational Config records do not define project technologies.

The set of technologies is derived on every run, never remembered. A project gains and loses technologies over its life, and a remembered list would keep matching the project it was written for rather than the one in front of you.

Detection is read-only. A Component whose phase has not started yet is still a Component whose technology is present, so an inactive phase is not a reason to skip matching it.

Then determine what is already available, so that nothing compatible is duplicated: the Skills currently visible in this environment, and the capabilities already supplied by installed plugins.

### Match and install

Establish the current way to discover and install a Skill in this environment before relying on any particular mechanism. Verify that the environment's own Skill and plugin management capability is present and ask it what it supports, rather than assuming a command, an option, a scope name, or a catalog name that an earlier version offered. When a documented interactive capability exists alongside the command-line one, treat it as an equally valid route.

For each detected technology:

1. On an ordinary installation run, skip installation when a compatible Skill is already available. When the human explicitly requests Refresh or Update, inspect the installed version and source and check for a compatible update through the supported mechanism. Do not skip that check merely because the Skill is installed. If an update is available, follow the compatibility checks and approval process below before applying it; otherwise, preserve the installation and report why no update was made.
2. Discover candidates through the environment's supported discovery mechanism, starting with the most authoritative available sources. A catalog may distribute a Skill inside a larger bundle, so a bundle is a valid candidate. Once a candidate's relevance, source, and compatibility have been verified, further catalog searches are optional unless the human requested a comparison of alternatives.
3. Match candidates by their declared purpose, source, and component inventory, not by name alone. Inspect the candidate's own metadata and manifest at its declared source. Do not claim a candidate supplies a relevant Skill until its components confirm that; a name match, or a component of a different kind, is not a Skill match.
4. Prefer the most authoritative source the environment reports for that candidate: an official catalog first, then a catalog maintained by the technology itself, then a trusted third party. Adding a catalog the environment does not already have is an external change and requires its own approval.
5. Verify major-version compatibility before proposing installation.
6. Present the candidate, its source, the installation scope, every bundled component or permission it carries, and the compatibility evidence to the human before any external installation or update. Prefer the narrowest scope that serves the project unless the human chooses a wider one.
7. Install only after approval, using the environment's supported installation route, and never accept an unattended installation from a command-based source unless the human approved that source explicitly. Verify the result afterwards, and report any activation step the environment says is still required.

Do not replace discovery with a judgment that a dedicated Skill is unnecessary. If supported discovery finds no compatible candidate, report which catalogs and candidate fields were checked and mark that technology as skipped; that is a narrower and truer claim than saying no such Skill exists.

Mark a technology as blocked for missing discovery only after every discovery route the environment offers has been tried. Never work around a genuine limitation by modifying project files or downloading unverified content.

## Boundaries

Do not initialize Config, plan implementation, or develop the application. Do not change Interface data, application code, architecture, manifests, lockfiles, or runtime dependencies. Do not install for a technology that was not detected in the current target-project sources or implementation, remove a compatible Skill, or install duplicates.

The operation is idempotent: repeating the same request against unchanged project sources, dependencies, installed Skills, and available compatible releases makes no changes.

## Report

Report one entry per detected technology, each stating:

1. **Technology** — its name, and the project file that established its presence.
2. **Version** — the detected version, or `unresolved`.
3. **Status** — installed, updated, skipped, or blocked.
4. **Skill and source** — the selected Skill and where it came from, when one applies, together with its actual installation scope and location and whether it travels with the repository or requires machine-local setup.
5. **Reason** — why that status was reached, including the catalogs checked when the status is skipped or blocked.
6. **Not in Preferences** — mark the entry when the technology was found in the implementation but the applicable Preferences do not offer it, and say where it was found.

Close with any activation step the environment reported as still required.
