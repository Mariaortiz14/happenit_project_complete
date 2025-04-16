from pydantic import BaseModel, EmailStr, root_validator, ConfigDict
from typing import Optional
import re
from pydantic import ConfigDict
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserUpdate(BaseModel):
    name: str
    surname: str
    phone: str
    email: EmailStr
    currentPassword: str  

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    name: str
    surname: Optional[str] = None
    phone: str
    email: EmailStr
    password: str
    confirm_password: str

    @root_validator(pre=True)
    def check_password(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if password != confirm_password:
            raise ValueError("Las contraseñas no coinciden")

        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValueError("La contraseña debe contener al menos un carácter especial.")

        return values


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str

    model_config = ConfigDict(from_attributes=True) 



class LoginRequest(BaseModel):
    username: str
    password: str
