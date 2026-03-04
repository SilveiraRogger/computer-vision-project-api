import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from app.api.db.base import Base
from sqlalchemy.dialects.postgresql import UUID, JSONB


class Detection(Base):
    __tablename__ = "detections"

    id = Column("id", UUID, primary_key=True, default=uuid.uuid4)
    image_url = Column("image_url", String, nullable=False)
    image_url_result = Column("image_url_result", String, nullable=False)
    result = Column("result", JSONB, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="detections")

    # def __init__(self, image_url, result, user_id):
    #     self.image_url = image_url
    #     self.result = result
    #     self.image_url_result
    #     self.user_id = user_id
