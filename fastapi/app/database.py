from sqlmodel import Session, create_engine
import os
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_db():
    with Session(engine) as session:
        yield session

Base = declarative_base()