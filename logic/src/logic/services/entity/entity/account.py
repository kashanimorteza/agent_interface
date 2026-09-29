"""Entity Child Service bound to Model's Account Entity."""

from model.interface import Account

from logic.services.entity.credential_protection import ProtectedCredentials


class AccountService(ProtectedCredentials):
    """Selects Account once and offers every shared Entity Action for it; credentials are encrypted at rest."""

    entity = Account
    credential_fields = ("password",)
    treatment = "encrypt"
