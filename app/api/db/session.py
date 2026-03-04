from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"sslmode": "require"})

SessionLocal = sessionmaker(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
