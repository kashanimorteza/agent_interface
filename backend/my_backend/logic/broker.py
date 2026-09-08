"""What the application does with a broker the system works with.

Its own unit, so that a rule belonging to with alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import Broker

from .base import ModelLogic


class BrokerLogic(ModelLogic):
    """The behaviour of a broker the system works with."""

    definition = Broker
