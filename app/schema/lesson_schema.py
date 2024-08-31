from pydantic import BaseModel
from datetime import datetime

class LearningResourceBase(BaseModel):
    title: str
    description: str
    video_url: str

class LearningResourceCreate(LearningResourceBase):
    pass

class LearningResourceUpdate(LearningResourceBase):
    pass

class LearningResourceResponse(LearningResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True