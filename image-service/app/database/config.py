from sqlalchemy import create_engine, Column, DateTime
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.core.config import settings
from app.utils.generic import camel_to_snake

if settings.TESTING:
    engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True, isolation_level="AUTOCOMMIT")
else:
    engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True, pool_recycle=60)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
