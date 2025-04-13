from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ESGRating(Base):
    __tablename__ = 'esg_ratings'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float)  # Оценка от 1 до 10
    category = Column(String)  # Экология, социальная ответственность, управление
    project_id = Column(Integer, ForeignKey('projects.id'))

    # Связь с проектом
    # project = relationship("Project", back_populates="esg_ratings")
