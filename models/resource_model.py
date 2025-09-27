from sqlalchemy import Column, String
from database import Base
from pydantic import BaseModel
import uuid


class Resource(Base):
    __tablename__ = "resources"

    resource_id = Column(
        String,                      
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    resource_name = Column(String, nullable=False)
    description = Column(String)

class ResourceCreate(BaseModel):
    resource_name: str
    description: str

class ResourceResponse(BaseModel):
    resource_id: str
    resource_name: str
    description: str

    class Config:
        orm_mode = True
