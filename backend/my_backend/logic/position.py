"""What the application does with a position the system created.

Its own unit, so that a rule belonging to created alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import Position

from .base import ModelLogic


class PositionLogic(ModelLogic):
    """The behaviour of a position the system created."""

    definition = Position
