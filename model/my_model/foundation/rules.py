"""Domain rules, and the difference between declaring one and enforcing it.

Every rule is declared with the entity it constrains. Where it is enforced
depends on what evaluating it needs: a rule that only reads the entity's own
values is enforced here, a rule that needs stored records or an operation's
context is declared here and enforced by the layer that has them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class RuleScope(str, Enum):
    """What evaluating a rule requires."""

    OWN_DATA = "own_data"
    STORED_STATE = "stored_state"
    APPLICATION_CONTEXT = "application_context"


@dataclass(frozen=True, slots=True)
class DomainRule:
    """One constraint on an entity's valid state."""

    statement: str
    scope: RuleScope
    fields: tuple[str, ...] = ()
    check: Callable[[Any], str | None] | None = field(default=None, compare=False)

    def __post_init__(self) -> None:
        if self.check is not None and self.scope is not RuleScope.OWN_DATA:
            raise ValueError(
                f"rule {self.statement!r} carries a check but needs "
                f"{self.scope.value}, which this entity cannot read"
            )

    def is_enforceable_here(self) -> bool:
        """Whether the entity can evaluate this rule from its own values alone."""

        return self.scope is RuleScope.OWN_DATA and self.check is not None

    def __str__(self) -> str:
        return self.statement
