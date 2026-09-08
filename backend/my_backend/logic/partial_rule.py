"""What the application does with one rule for closing part of a position.

Its own unit, so that a rule belonging to position alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import PartialRule

from .base import ModelLogic


class PartialRuleLogic(ModelLogic):
    """The behaviour of one rule for closing part of a position."""

    definition = PartialRule
