"""Backend-targeted project Behaviour.

The project's one Behaviour — enable users to enter and manage all defined project data — is fulfilled
entirely by the standard operations (create, get, list, update, delete) of every Model Logic unit; no
Behaviour beyond those operations is required (.interface/config/backend.yaml layers.logic.project_behaviours).
"""

from trading_backend.logic.model_specs import MODEL_KEYS

PROJECT_BEHAVIOURS: dict[str, tuple[str, ...]] = {
    "enable_users_to_enter_and_manage_all_defined_project_data": MODEL_KEYS,
}
