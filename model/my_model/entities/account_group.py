"""An independent grouping of trading accounts."""

from ..foundation import FieldSpec, InitialRecord, define_entity

AccountGroup = define_entity(
    name="AccountGroup",
    purpose="An independent group that organizes trading accounts.",
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The account group's display name."),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the account group."),
    },
    initial_records=[InitialRecord({"name": "Default"})],
)
