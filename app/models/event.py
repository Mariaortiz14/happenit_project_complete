from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(999), nullable=False)
    event_date = Column(DateTime, nullable=False)
    location = Column(String(255), nullable=False)
    category = Column(Enum("gastronomía", "conferencias", "deportes", "festival", "conciertos", "teatros", "otro"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    comments = relationship("app.models.comment.Comment", back_populates="event")
    user = relationship("User", back_populates="events")
