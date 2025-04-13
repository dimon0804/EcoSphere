from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class UserBadge(Base):
    __tablename__ = 'user_badges'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    badge_id = Column(Integer, ForeignKey('badges.id'), primary_key=True)
    date_earned = Column(DateTime, default=datetime.utcnow)  # Когда был получен бейдж

    # user = relationship("User", back_populates="user_badges")
    # badge = relationship("Badge", back_populates="user_badges")

    def __repr__(self):
        return f"UserBadge(user_id={self.user_id}, badge_id={self.badge_id}, date_earned={self.date_earned})"
