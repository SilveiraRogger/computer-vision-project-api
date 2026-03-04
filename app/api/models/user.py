import uuid
from sqlalchemy.orm import relationship
from app.api.db.base import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = "users"

    id = Column("id", UUID, primary_key=True, default=uuid.uuid4)
    name = Column("name", String, nullable=False)
    email = Column("email", String, nullable=False)
    password = Column("password", String, nullable=False)
    detections = relationship("Detection", back_populates="user")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
