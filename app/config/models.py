from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Config(Base):
    __tablename__ = "configs"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
