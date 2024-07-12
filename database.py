from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin:root@localhost:9876/fastapi_database"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
