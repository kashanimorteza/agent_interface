"""Public interface of the my_backend package.

    import my_backend
    app = my_backend.create_app()

`create_app()` is the package's documented public startup boundary. Every
other module (`_model_interface`, `_database_interface`, `_app`, `_schemas`,
`logic`, `api`) is an internal implementation detail.
"""

from my_backend._app import create_app

__all__ = ["create_app"]
