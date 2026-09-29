"""Entity Child Service bound to Model's Instance Entity."""

from model.interface import Instance

from logic.services.entity.credential_protection import ProtectedCredentials


class InstanceService(ProtectedCredentials):
    """Selects Instance once and offers every shared Entity Action for it; credentials are encrypted at rest."""

    entity = Instance
    credential_fields = ("password", "api_key")
    treatment = "encrypt"
