from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
import enum
import datetime
import uuid

Base = declarative_base()

class StatusEnum(enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class DocumentMetadata(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    filename = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
