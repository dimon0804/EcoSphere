from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Badge(Base):
    __tablename__ = 'badges'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    co2_saved_required = Column(Float)  # Сколько CO2 нужно сэкономить для получения


    # user_id = Column(Integer, ForeignKey('users.id'))
    # user = relationship("User", back_populates="user_badges")
