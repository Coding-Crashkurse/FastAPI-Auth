from sqlalchemy import create_engine
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")

engine = create_engine("postgresql://admin:test@localhost:5432/fast_api_test")

def get_db():
    with DBContext() as db:
        yield db

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

class DBContext:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, et, ev, traceback):
        self.db.close()