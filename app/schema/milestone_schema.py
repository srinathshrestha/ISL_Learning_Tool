from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MilestoneCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="The name of the milestone.")
    description: Optional[str] = Field(None, description="A brief description of the milestone.")

class MilestoneUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="The updated name of the milestone.")
    description: Optional[str] = Field(None, description="The updated description of the milestone.")

class MilestoneResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
