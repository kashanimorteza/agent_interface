"""What the application does with the instruction for opening a position.

Its own unit, so that a rule belonging to position alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import Action

from .base import ModelLogic


class ActionLogic(ModelLogic):
    """The behaviour of the instruction for opening a position."""

    definition = Action
