"""Credential Fields the Entity Group never returns.

The Target designates the credential Fields of three Entities. Logic stores them protected and
returns their stored form on reads, and no response of API carries a credential value in any form,
so a response schema leaves these Fields out. They can still be supplied on input.
"""

from typing import Any

CREDENTIAL_FIELDS = {
    "User": ("password", "api_key"),
    "Instance": ("password", "api_key"),
    "Account": ("password",),
}


def withheld(entity: type[Any]) -> tuple[str, ...]:
    """Return the credential Fields of an Entity.

    Args:
        entity (type[Any]): Entity a Child Service is bound to.

    Returns:
        (tuple[str, ...]): Fields its responses never carry.

    Raises:
        ValueError: When a designated Field is not a Field of the Entity; the message names it.
    """
    fields = CREDENTIAL_FIELDS.get(entity.__name__, ())
    for field in fields:
        if field not in entity.model_fields:
            raise ValueError(f"{entity.__name__} has no credential Field {field}")
    return fields
