"""Storage Adapter layer.

Owns the connection to the SQLite engine, the SQLAlchemy mappings that realize
the storage schema, credential at-rest transformations, and physical
persistence. Nothing in this package is published to consumers directly.
"""
