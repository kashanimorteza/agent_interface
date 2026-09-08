"""What the application does with a risk-based grouping of actions.

Its own unit, so that a rule belonging to actions alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import ActionGroup

from .base import ModelLogic


class ActionGroupLogic(ModelLogic):
    """The behaviour of a risk-based grouping of actions."""

    definition = ActionGroup
