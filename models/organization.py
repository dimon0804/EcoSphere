from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    user_id = Column(Integer, index=True)
    
    # Связь с проектами
    projects = relationship("Project", back_populates="organization")
    # users = relationship('User', back_populates='organization')
