import pytest

from database import default_instance, list_instances
from database.adapter import get_engine


def test_registry_lists_configured_instances_with_a_resolvable_default():
    instances = list_instances()
    keys = {i.key for i in instances}
    assert default_instance() in keys
    engine = get_engine(default_instance())
    with engine.connect():
        pass


def test_registry_entries_expose_no_connection_or_secret():
    for info in list_instances():
        assert not hasattr(info, "connection")
        assert not hasattr(info, "password")
        assert not hasattr(info, "secret")


def test_unconfigured_instance_is_rejected():
    with pytest.raises(ValueError):
        get_engine("does-not-exist")
