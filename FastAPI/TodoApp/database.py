# Connection to DB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create engine (SQLite needs check_same_thread=False for multithreading)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base class for ORM models
Base = declarative_base()