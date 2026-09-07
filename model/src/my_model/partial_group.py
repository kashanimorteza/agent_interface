"""The PartialGroup Model."""

from pydantic import Field

from ._base import Model


class PartialGroup(Model):
    """Defines an independent group of rules for managing portions of an open trade. Its rules
    determine how much of the trade volume must be closed when profit or loss reaches specified
    thresholds.
    """

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The partial group's display name. Unique.")
    status: bool = Field(default=True, description="Indicates whether the partial group is active.")
    description: str | None = Field(default=None, description="Describes the partial group.")
