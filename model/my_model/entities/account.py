"""A funded trading account trades are sent to."""

from ..foundation import (
    Cardinality,
    CredentialStorage,
    FieldSpec,
    FieldType,
    GENERATE_SECURELY,
    InitialRecord,
    Relationship,
    define_entity,
)

Account = define_entity(
    name="Account",
    purpose=(
        "A funded trading account through which positions are launched. It states "
        "which broker holds it, which currency it is denominated in, how it is "
        "accessed and on what terms it trades, so the system knows where an order "
        "goes and how to get there."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The account's display name."),
        "group_id": FieldSpec(purpose="The account group that contains the account."),
        "broker_id": FieldSpec(purpose="The broker that holds the account."),
        "base_currency_id": FieldSpec(purpose="The base currency the account is held in."),
        "username": FieldSpec(
            type=FieldType.STRING,
            nullable=False,
            purpose="The username used to access the trading account.",
        ),
        "password": FieldSpec(
            type=FieldType.STRING,
            nullable=False,
            credential_storage=CredentialStorage.ENCRYPTED,
            purpose="The credential used to access the trading account.",
        ),
        "leverage": FieldSpec(
            type=FieldType.INTEGER,
            nullable=False,
            purpose="The account's leverage multiplier.",
        ),
        "balance": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            default=0,
            purpose="The account's current balance.",
        ),
        "account_type": FieldSpec(
            type=FieldType.STRING,
            nullable=False,
            purpose="The account model, such as cfd or spread_betting.",
        ),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the account."),
    },
    relationships=[
        Relationship(
            target="AccountGroup",
            cardinality=Cardinality.MANY_TO_ONE,
            role="group",
            field="group_id",
        ),
        Relationship(
            target="Broker",
            cardinality=Cardinality.MANY_TO_ONE,
            role="broker",
            field="broker_id",
        ),
        Relationship(
            target="Currency",
            cardinality=Cardinality.MANY_TO_ONE,
            role="base_currency",
            field="base_currency_id",
        ),
    ],
    initial_records=[
        InitialRecord(
            {
                "name": "Acc-1",
                "group_id": 1,
                "broker_id": 1,
                "base_currency_id": 1,
                "username": "test",
                "password": GENERATE_SECURELY,
                "leverage": 100,
                "account_type": "CFD",
            }
        ),
    ],
)
