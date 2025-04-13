from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Donation(Base):
    __tablename__ = 'donations'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    timestamp = Column(DateTime)
    project_id = Column(Integer, ForeignKey('projects.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    # # Связи с проектом и пользователем
    # project = relationship("Project", back_populates="donations")
    # user = relationship("User", back_populates="donations")
