import os
from dataclasses import dataclass, field

@dataclass
class SystemConfig:
    environment: str = field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    debug: bool = field(default_factory=lambda: os.getenv("APP_DEBUG", "True").lower() in ("true", "1", "yes"))

@dataclass
class APIConfig:
    host: str = field(default_factory=lambda: os.getenv("API_HOST", "0.0.0.0"))
    port: int = field(default_factory=lambda: int(os.getenv("API_PORT", "8000")))

@dataclass
class DBConfig:
    url: str = field(default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///./local_prototype.db"))

@dataclass
class Settings:
    system: SystemConfig = field(default_factory=SystemConfig)
    api: APIConfig = field(default_factory=APIConfig)
    db: DBConfig = field(default_factory=DBConfig)

def get_settings() -> Settings:
    """Returns a new instance of Settings, pulling current env vars."""
    return Settings()
