"""A risk-based grouping of trading actions."""

from ..foundation import FieldSpec, InitialRecord, define_entity

ActionGroup = define_entity(
    name="ActionGroup",
    purpose=(
        "An independent grouping of trading actions by risk profile, such as high, "
        "normal or low risk, so trades can be organized and selected by the risk "
        "level they are intended to carry."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The action group's display name."),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the action group."),
    },
    initial_records=[InitialRecord({"name": "Default"})],
)
