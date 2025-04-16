from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    event_id: int

class CommentUpdate(BaseModel):
    content: str

class UserInfo(BaseModel):
    id: int
    name: str
    surname: str

    class Config:
        from_attributes = True

class Comment(CommentBase):
    id: int
    user_id: int
    event_id: int
    created_at: datetime
    user: UserInfo

    class Config:
        from_attributes = True
