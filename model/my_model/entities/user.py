"""An independent user of the system."""

from ..foundation import (
    CredentialStorage,
    FieldSpec,
    FieldType,
    GENERATE_SECURELY,
    InitialRecord,
    define_entity,
)

User = define_entity(
    name="User",
    purpose=(
        "An independent user of the system. Each user carries a separate set of "
        "settings, so a new user is added without disturbing the existing ones."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The user's display name."),
        "username": FieldSpec(
            type=FieldType.STRING,
            nullable=False,
            purpose="The username used to identify the user.",
        ),
        "password": FieldSpec(
            type=FieldType.STRING,
            nullable=False,
            credential_storage=CredentialStorage.HASH,
            purpose="The password credential used by the user.",
        ),
        "api_key": FieldSpec(
            credential_storage=CredentialStorage.HASH,
            purpose="The API key assigned to the user.",
        ),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the user."),
    },
    initial_records=[
        InitialRecord(
            {
                "name": "Admin",
                "username": "admin",
                "password": GENERATE_SECURELY,
                "api_key": GENERATE_SECURELY,
            }
        ),
    ],
)
