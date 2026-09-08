"""An independent set of rules for closing portions of an open trade."""

from ..foundation import FieldSpec, InitialRecord, define_entity

PartialGroup = define_entity(
    name="PartialGroup",
    purpose=(
        "An independent group of rules for managing portions of an open trade. Its "
        "rules decide how much of the volume is closed when profit or loss reaches "
        "the thresholds they state."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The partial group's display name."),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the partial group."),
    },
    initial_records=[InitialRecord({"name": "Default"})],
)
