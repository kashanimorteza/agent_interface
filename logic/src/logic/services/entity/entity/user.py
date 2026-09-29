"""Entity Child Service bound to Model's User Entity."""

from model.interface import User

from logic.services.entity.credential_protection import ProtectedCredentials


class UserService(ProtectedCredentials):
    """Selects User once and offers every shared Entity Action for it; credentials are hashed at rest."""

    entity = User
    credential_fields = ("password", "api_key")
    treatment = "hash"
