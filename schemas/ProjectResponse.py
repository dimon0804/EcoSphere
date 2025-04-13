from pydantic import BaseModel

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True