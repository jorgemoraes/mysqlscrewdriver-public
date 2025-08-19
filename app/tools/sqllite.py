import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.models import Base

# Banco SQLite local
DATABASE_URL = "sqlite:///./config/database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Cria tabelas se não existirem


def init_db():
    Base.metadata.create_all(bind=engine)
