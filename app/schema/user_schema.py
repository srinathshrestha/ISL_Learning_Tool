from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3,max_length=100)  # Enforces string length constraints
    email: EmailStr = Field(...) # Validates email format
    password: str = Field(..., min_length=5,max_length=250)  # Enforces a minimum length for passwords
    full_name: Optional[str] = Field(None, max_length=100)  # Optional field with a max length constraint
    role: Optional[Literal['user', 'admin']] = Field('user') 

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    is_active: bool
    role: str  # role is included in response but not in creation
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    password: str


class TokenRespose(BaseModel):
    access_token: str
    token_type: str


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