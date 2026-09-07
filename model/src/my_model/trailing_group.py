"""The TrailingGroup Model."""

from pydantic import Field

from ._base import Model


class TrailingGroup(Model):
    """Defines an independent group for organizing the rules that manage Stop Loss and Take Profit
    during a trade. The group identifies the rule set, while each rule separately defines its
    activation condition and the changes to apply.
    """

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The trailing group's display name. Unique.")
    status: bool = Field(default=True, description="Indicates whether the trailing group is active.")
    description: str | None = Field(default=None, description="Describes the trailing group.")
