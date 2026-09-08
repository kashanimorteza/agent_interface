"""An independent set of rules for managing protective and target levels."""

from ..foundation import FieldSpec, InitialRecord, define_entity

TrailingGroup = define_entity(
    name="TrailingGroup",
    purpose=(
        "An independent group organizing the rules that manage stop loss and take "
        "profit during a trade. The group identifies the rule set; each rule "
        "states its own activation condition and the changes it applies."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The trailing group's display name."),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the trailing group."),
    },
    initial_records=[InitialRecord({"name": "Default"})],
)
