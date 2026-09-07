"""The ActionGroup Model."""

from pydantic import Field

from ._base import Model


class ActionGroup(Model):
    """Defines an independent grouping for trading actions based on their risk profile, such as high
    risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized
    and selected by their intended risk level.
    """

    id: int | None = Field(default=None, description="Assigned by persistence on create; absent until then.")
    name: str = Field(description="The action group's display name. Unique.")
    status: bool = Field(default=True, description="Indicates whether the action group is active.")
    description: str | None = Field(default=None, description="Describes the action group.")
