from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PQRCreate(BaseModel):
    user_id: int
    type: str
    subject: str
    message: str

class PQRResponse(BaseModel):
    id: int
    user_id: int
    type: str
    subject: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True
