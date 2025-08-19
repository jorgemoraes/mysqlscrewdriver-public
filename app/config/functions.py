from config.models import Config
from tools.sqllite import SessionLocal, init_db
from sqlalchemy.orm import Session
# Inicializa o banco de dados
init_db()

session = SessionLocal()


def read_host(session: Session):
    return session.query(Config).filter(Config.name.in_(["host"])).all()


def read_role(session: Session):
    return session.query(Config).filter(Config.name.in_(["role"])).all()


def read_msg(session: Session):
    return session.query(Config).filter(Config.name.in_(["msg"])).all()


def read_buckets3(session: Session):
    return session.query(Config).filter(Config.name.in_(["bucketS3"])).all()
