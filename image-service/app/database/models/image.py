from sqlalchemy import Column, Integer, String, UUID, DateTime, Boolean

from app.database.config import Base
from uuid import uuid4


class Image(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid4)
    name = Column(String(100), nullable=False)
    extension = Column(String(5), nullable=False)
    resolution = Column(String(10), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    size = Column(Integer, nullable=False)
    bits = Column(Integer, nullable=False)
