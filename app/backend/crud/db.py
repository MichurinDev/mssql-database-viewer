from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.backend.config import config as cfg

DATABASE_URL = f"mssql+pymssql://{cfg.MSSQL_USER}:{cfg.MSSQL_PASSWORD}@{cfg.MSSQL_IP}:{cfg.MSSQL_PORT}/{cfg.MSSQL_DATABASE}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()
