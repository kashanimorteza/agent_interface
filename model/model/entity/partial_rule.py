"""Partial Rule Entity."""

from decimal import Decimal
from typing import ClassVar

from model.core import _storage as storage
from model.core.declaration import (
    Declaration,
    FieldDeclaration,
    FieldType,
    Relation,
    ValueGeneration,
)
from model.core.foundation import Foundation


class PartialRule(Foundation, table=True):
    declaration: ClassVar[Declaration] = Declaration(
        name="Partial Rule",
        description="Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.",
        primary_key="id",
        fields=(
            FieldDeclaration(
                name="id",
                type=FieldType.integer,
                nullable=False,
                immutable=True,
                value_generation=ValueGeneration.auto_increment,
            ),
            FieldDeclaration(
                name="name",
                type=FieldType.string,
                nullable=False,
                description="The partial rule's display name.",
            ),
            FieldDeclaration(
                name="partial_group_id",
                type=FieldType.integer,
                nullable=False,
                description="Identifies the partial group that contains the rule.",
            ),
            FieldDeclaration(
                name="profit_percentage",
                type=FieldType.decimal,
                nullable=False,
                description="Defines the profit percentage that activates the rule.",
            ),
            FieldDeclaration(
                name="close_percentage",
                type=FieldType.decimal,
                nullable=False,
                description="Defines the percentage of the position closed when the rule is activated.",
            ),
            FieldDeclaration(
                name="is_active",
                type=FieldType.boolean,
                nullable=False,
                description="Indicates whether the partial rule is active.",
                default=True,
            ),
            FieldDeclaration(
                name="description",
                type=FieldType.string,
                nullable=True,
                description="Describes the partial rule.",
            ),
        ),
        relations=(
            Relation(
                local_field="partial_group_id",
                target_entity="Partial Group",
                target_field="id",
            ),
        ),
        unique_constraints=(
            ("name",),
            ("partial_group_id", "profit_percentage"),
        ),
    )
    __tablename__ = "PartialRule"
    __table_args__ = storage.table_args(declaration)

    id: int | None = storage.field(declaration, "id")
    name: str = storage.field(declaration, "name")
    partial_group_id: int = storage.field(declaration, "partial_group_id")
    profit_percentage: Decimal = storage.field(declaration, "profit_percentage")
    close_percentage: Decimal = storage.field(declaration, "close_percentage")
    is_active: bool = storage.field(declaration, "is_active")
    description: str | None = storage.field(declaration, "description")
