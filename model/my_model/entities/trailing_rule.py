"""One rule for moving protective and target levels during a trade."""

from ..foundation import (
    Cardinality,
    FieldSpec,
    FieldType,
    Relationship,
    define_entity,
)

TrailingRule = define_entity(
    name="TrailingRule",
    purpose=(
        "One rule inside a trailing group, stating when the system adjusts take "
        "profit and stop loss and what those adjustments are."
    ),
    fields={
        "id": FieldSpec(),
        "name": FieldSpec(purpose="The trailing rule's display name."),
        "trailing_group_id": FieldSpec(purpose="The trailing group that contains the rule."),
        "trigger_percentage": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=False,
            purpose=(
                "The percentage of the take-profit target that, once reached, "
                "activates the rule."
            ),
        ),
        "take_profit_adjustment": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=True,
            purpose="The take-profit adjustment applied when the rule activates.",
        ),
        "stop_loss_adjustment": FieldSpec(
            type=FieldType.DECIMAL,
            nullable=True,
            purpose="The stop-loss adjustment applied when the rule activates.",
        ),
        "status": FieldSpec(),
        "description": FieldSpec(purpose="Describes the trailing rule."),
    },
    relationships=[
        Relationship(
            target="TrailingGroup",
            cardinality=Cardinality.MANY_TO_ONE,
            role="trailing_group",
            field="trailing_group_id",
        ),
    ],
)
