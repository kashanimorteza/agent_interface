"""Verifies the Model Foundation imposes no Field or relationship of its own."""

from model import DomainModel


def test_foundation_declares_no_domain_fields():
    assert DomainModel.model_fields == {}


def test_foundation_declares_no_foreign_keys():
    assert DomainModel.__foreign_keys__ == {}


def test_foundation_persistence_metadata_has_no_declared_fields():
    metadata = DomainModel.persistence_metadata()
    assert metadata["fields"] == {}
    assert metadata["foreign_keys"] == {}
