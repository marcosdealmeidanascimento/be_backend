import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"
    """
    Database Model for an application user
    """
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean(), default=False)
    last_post = Column(DateTime, nullable=True)
    can_post = Column(Boolean(), default=True, nullable=True)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )
