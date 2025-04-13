from pydantic import BaseModel
from datetime import date
from typing import Optional

class ProjectBase(BaseModel):
    name: Optional[str]
    description: Optional[str] = None
    target_amount: Optional[float]
    collected_amount: Optional[float] = None
    location: Optional[str] = None
    category: Optional[str] = None
    participants_count: Optional[int] = 0
    end_date: Optional[date]
    status: Optional[str] = 'moderation'
    co2: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    description: Optional[str] = None
    target_amount: Optional[float] = None
    collected_amount: Optional[float] = None
    location: Optional[str] = None
    category: Optional[str] = None
    participants_count: Optional[int] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    co2: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True
