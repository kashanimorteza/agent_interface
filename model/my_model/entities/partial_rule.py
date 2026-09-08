"""One rule for closing part of an open position."""

from ..foundation import (
    Cardinality,
    FieldSpec,
    FieldType,
    Relationship,
    define_entity,
)

PartialRule = define_entity(
    name="PartialRule",
    purpose=(
        "One partial-close rule, stating the condition under which part of an open "
        "position is closed and how much of its volume that is."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The partial rule's display name."),
        "partial_group_id": FieldSpec(purpose="The partial group that contains the rule."),
        "profit_percentage": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose="The profit percentage that activates the rule.",
        ),
        "close_percentage": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose="The percentage of the position closed when the rule activates.",
        ),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the partial rule."),
    },
    relationships=[
        Relationship(
            target="PartialGroup",
            cardinality=Cardinality.MANY_TO_ONE,
            role="partial_group",
            field="partial_group_id",
        ),
    ],
)
