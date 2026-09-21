# Understanding

This section defines how an Agent establishes Interface Understanding and Target Understanding before acting.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Interface Understanding](#interface-understanding)**
2. **[Target Understanding](#target-understanding)**

<br>

<!--------------------------------------------------------------------------------- Interface Understanding --->
## Interface Understanding

Interface Understanding is the understanding of Agent Interface that an Agent establishes before performing an ordinary Skill's role. It starts from `.interface/interface.md` and follows only the routes provided for the active role. Agent Native Sync is the sole explicit exception: it reads the Agent Module directly after explicit Human invocation and does not require Target Understanding.

→ [Read more about Interface](../interface.md)

<br>

<!--------------------------------------------------------------------------------- Target Understanding --->
## Target Understanding

Target Understanding is the understanding of the project's Target that an Agent establishes when the role needs Target meaning. Human Definition provides the Human's stated intent and context; Technical Definition is the primary Target authority and takes precedence wherever they conflict. Configure uses only the phase identities and Platform selections required for its role. Reset establishes the minimum Target Understanding needed for a phase scope, omits it for Config scope, and uses only phase identity and ownership for Complete scope.

An empty Human Definition contributes no information. Understanding is reconstructed from the current sources under their declared precedence when required and is never copied into Config as a second project definition.

→ [Read more about the Non-Technical Definition](../target/non-technical.md)

→ [Read more about the Technical Definition](../target/technical.md)

<br>
