from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from packages.configuration.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.db.url,
    # Enable SQLite specific args if needed, e.g. connect_args={"check_same_thread": False} for FastAPI
    connect_args={"check_same_thread": False} if "sqlite" in settings.db.url else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
