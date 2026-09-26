"""Instance Entity."""

from typing import ClassVar

from sqlmodel import Field, UniqueConstraint

from my_model.model_declaration import (
    AtRest,
    FieldDeclaration,
    LogicalType,
    ModelDeclaration,
    Reference,
    RelationshipKind,
    Sensitivity,
    UniquenessConstraint,
    ValueGeneration,
)
from my_model.model_foundation import ModelFoundation


class Instance(ModelFoundation, table=True):
    """Defines a user-owned connection instance through which the system accesses a supported Trading Platform."""

    declaration: ClassVar[ModelDeclaration] = ModelDeclaration(
        entity="Instance",
        purpose="Defines a user-owned connection instance through which the system accesses a supported Trading Platform.",
        fields=(
            FieldDeclaration(
                "id",
                LogicalType.INTEGER,
                generation=ValueGeneration.AUTO_INCREMENT,
                purpose="",
            ),
            FieldDeclaration(
                "user_id",
                LogicalType.INTEGER,
                purpose="Identifies the user who owns this instance",
            ),
            FieldDeclaration(
                "trading_platform_id",
                LogicalType.INTEGER,
                purpose="Identifies the trading platform used by this instance",
            ),
            FieldDeclaration(
                "name", LogicalType.STRING, purpose="The instance's display name"
            ),
            FieldDeclaration(
                "ip",
                LogicalType.STRING,
                nullable=True,
                purpose="Identifies the technical network address used to reach the Trading Platform when required",
            ),
            FieldDeclaration(
                "username",
                LogicalType.STRING,
                nullable=True,
                purpose="Defines the technical username used to establish the Instance connection when required",
            ),
            FieldDeclaration(
                "password",
                LogicalType.STRING,
                nullable=True,
                sensitivity=Sensitivity.CREDENTIAL,
                at_rest=AtRest.ENCRYPTED,
                purpose="Defines the technical password used to establish the Instance connection when required",
            ),
            FieldDeclaration(
                "api_key",
                LogicalType.STRING,
                nullable=True,
                sensitivity=Sensitivity.CREDENTIAL,
                at_rest=AtRest.ENCRYPTED,
                purpose="Defines the technical API credential used to establish the Instance connection when required",
            ),
            FieldDeclaration(
                "is_active",
                LogicalType.BOOLEAN,
                has_default=True,
                default=True,
                purpose="Indicates whether the instance is active",
            ),
            FieldDeclaration(
                "description",
                LogicalType.STRING,
                nullable=True,
                purpose="Describes the instance",
            ),
        ),
        references=(
            Reference("user_id", "User", "id", RelationshipKind.BELONGS_TO),
            Reference(
                "trading_platform_id", "TradingPlatform", "id", RelationshipKind.USES
            ),
        ),
        unique_constraints=(
            UniquenessConstraint(
                (
                    "user_id",
                    "name",
                )
            ),
        ),
    )
    __table_args__ = (UniqueConstraint("user_id", "name"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    trading_platform_id: int = Field(foreign_key="tradingplatform.id")
    name: str
    ip: str | None = None
    username: str | None = None
    password: str | None = None
    api_key: str | None = None
    is_active: bool = True
    description: str | None = None
