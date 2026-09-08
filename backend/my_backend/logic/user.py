"""What the application does with an independent user of the system.

Its own unit, so that a rule belonging to system alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import User

from .base import ModelLogic


class UserLogic(ModelLogic):
    """The behaviour of an independent user of the system."""

    definition = User
