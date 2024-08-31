from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BadgeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="The name of the badge.")
    description: Optional[str] = Field(None, description="A brief description of the badge.")
    milestone_id: int = Field(..., description="The ID of the associated milestone.")

class BadgeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="The updated name of the badge.")
    description: Optional[str] = Field(None, description="The updated description of the badge.")
    milestone_id: Optional[int] = Field(None, description="The updated ID of the associated milestone.")

class BadgeResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    milestone_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
