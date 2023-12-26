import datetime
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "post"
    """
    Database Model for a post
    """
    id = Column(
        UUID(as_uuid=True), primary_key=True, index=True, default=uuid4
    )
    title = Column(String(255), index=True)
    content = Column(String(255), index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
    )