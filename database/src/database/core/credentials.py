"""Generation of the credential values that Initial Data requires."""

import secrets


class Credentials:
    """Issue secure credential values that are distinct from one another.

    Attributes:
        issued: Values already issued by this generator.
    """

    def __init__(self) -> None:
        self.issued: set[str] = set()

    def next(self) -> str:
        """Return a new secure credential value never issued before by this generator."""
        while (value := secrets.token_urlsafe(32)) in self.issued:
            pass
        self.issued.add(value)
        return value
