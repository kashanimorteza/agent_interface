"""Tables: the Create Tables Setup Operation over the Entities of Model."""

import model

from .data import Selected


def create(selected: Selected) -> tuple[int, int]:
    """Create the Table of every Entity of the Model Entity Collection that is missing on the selected Instance.

    Returns how many Tables were created and how many already matched their Declaration.
    """
    with selected.unit.scope(selected.connection) as session:
        return selected.unit.create_tables(session, tuple(model.entities))
