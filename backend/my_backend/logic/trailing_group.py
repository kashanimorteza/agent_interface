"""What the application does with a set of rules for moving protective and target levels.

Its own unit, so that a rule belonging to levels alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import TrailingGroup

from .base import ModelLogic


class TrailingGroupLogic(ModelLogic):
    """The behaviour of a set of rules for moving protective and target levels."""

    definition = TrailingGroup
