from sqlalchemy import Column, Integer, String, Text, Float, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship between Project and User
project_user_association = Table(
    'project_user_association',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    target_amount = Column(Float)
    collected_amount = Column(Float, default=0)
    location = Column(String)
    category = Column(String)
    participants_count = Column(Integer, default=0)
    end_date = Column(Date)
    status = Column(String)  # Статус проекта (активен, завершен и т.д.)
    co2 = Column(String)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    
    # # Связь с организацией
    organization = relationship("Organization", back_populates="projects")
    
    # # Связь с пожертвованиями
    # donations = relationship("Donation", back_populates="project")
    
    # # Связь с ESG-оценками
    # esg_ratings = relationship("ESGRating", back_populates="project")
    # user = relationship("User", secondary=project_user_association, back_populates="projects")
    # participants = relationship("ProjectParticipant", back_populates="project")
