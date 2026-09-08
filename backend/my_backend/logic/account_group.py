"""What the application does with a grouping of trading accounts.

Its own unit, so that a rule belonging to accounts alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import AccountGroup

from .base import ModelLogic


class AccountGroupLogic(ModelLogic):
    """The behaviour of a grouping of trading accounts."""

    definition = AccountGroup
