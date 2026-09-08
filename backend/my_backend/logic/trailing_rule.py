"""What the application does with one rule for moving protective and target levels.

Its own unit, so that a rule belonging to levels alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import TrailingRule

from .base import ModelLogic


class TrailingRuleLogic(ModelLogic):
    """The behaviour of one rule for moving protective and target levels."""

    definition = TrailingRule
