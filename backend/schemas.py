from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    name: str
    bio: Optional[str] = None
    role: str  # 'mentor' 또는 'mentee'
    image: Optional[str] = None
    skills: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    class Config:
        orm_mode = True

class MatchBase(BaseModel):
    mentor_id: int
    mentee_id: int
    message: Optional[str] = None

class MatchCreate(MatchBase):
    pass

class MatchOut(MatchBase):
    id: int
    status: str
    class Config:
        orm_mode = True
