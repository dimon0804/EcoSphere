from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from passlib.context import CryptContext 
from database import Base

# Настройка хеширования пароля
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    eco_wallet_balance = Column(Float, default=0)  # Баланс эко-кошелька
    total_donated = Column(Float, default=0)  # Общее пожертвованное
    total_co2_saved = Column(Float, default=0)  # Сэкономлено CO2
    hashed_password = Column(String)  # Хешированный пароль
    created_at = Column(DateTime, default=func.now())  # Дата создания пользователя

    # donations = relationship("Donation", back_populates="user")
    # projects = relationship("Project", secondary="project_participants", back_populates="user")
    # project_participants = relationship("ProjectParticipant", back_populates="user")
    # user_badges = relationship("Badge", back_populates="user")
    # user_organizations = relationship("Organization", back_populates="user")
    # user_esg_ratings = relationship("ESGRating", back_populates="user")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)