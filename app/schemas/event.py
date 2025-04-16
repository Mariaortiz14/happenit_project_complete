from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserResponse  

class EventCreate(BaseModel):
    user_id: int
    title: str
    description: str
    event_date: datetime
    location: str
    category: str

class EventResponse(BaseModel):
    id: int
    title: str
    description: str
    event_date: datetime
    user_id: int
    location: str
    category: str
    user: Optional[UserResponse] 

    model_config = ConfigDict(from_attributes=True) 

class EventUpdate(BaseModel):
    title: str
    description: str
    event_date: datetime

    class Config:
        orm_mode = True
