import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres@localhost:5432/postgres"

engine = create_engine(
    DATABASE_URL,
    echo=True,   # leave True for now so we see SQL (CREATE TABLE, etc.)
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()
