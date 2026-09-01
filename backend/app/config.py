from pathlib import Path


class Settings:
    base_dir: Path = Path(__file__).resolve().parent.parent
    database_path: Path = base_dir / "data" / "app.db"
    database_url: str = f"sqlite:///{database_path}"


settings = Settings()
