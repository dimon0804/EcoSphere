from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ProjectParticipant(Base):
    __tablename__ = 'project_participants'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)

    # user = relationship("User", back_populates="project_participants")
    # project = relationship("Project", back_populates="participants")
