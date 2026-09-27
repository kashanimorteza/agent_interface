"""Model_Declaration: the shared declarative base every Domain Entity extends, combining SQLModel's table declaration with Model_Foundation's shared conversion behaviour."""

from sqlmodel import SQLModel

from my_model.model_foundation import Model_Foundation


class Model_Declaration(SQLModel, Model_Foundation):
    pass
