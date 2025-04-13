from pydantic import BaseModel
from typing import Optional

class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[int] = None


class OrganizationResponse(OrganizationBase):
    id: int

    class Config:
        from_attributes = True