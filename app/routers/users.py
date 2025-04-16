from fastapi import APIRouter, Depends, HTTPException, Form, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, LoginRequest,UserUpdate
from app.auth.auth import create_access_token
import bcrypt
from datetime import datetime, timedelta
from typing import List
from app.models.event import Event
from app.schemas.event import EventResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

ACCESS_TOKEN_EXPIRE_MINUTES = 60

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        email=user.email,
        hashed_password=hashed_password.decode('utf-8'),
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login")
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login.username).first()
    if not user or not bcrypt.checkpw(login.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Usuario o contraseña inválidos")

    token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": str(user.id)}, expires_delta=token_expires)

    return {
        "message": "Inicio de sesión exitoso",
        "user_id": user.id,
        "name": user.name,
        "token": token
    }

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "firstName": user.name,
        "lastName": user.surname,
        "email": user.email,
        "phone": user.phone
    }
@router.get("/{user_id}/events/", response_model=List[EventResponse])
def get_user_events(user_id: int, db: Session = Depends(get_db)):
    events = db.query(Event).filter(Event.user_id == user_id).all()
    if not events:
        return []
    return events



@router.put("/{user_id}/profile")
def update_user_profile(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not bcrypt.checkpw(update_data.currentPassword.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta")
    
    user.name = update_data.name
    user.surname = update_data.surname
    user.phone = update_data.phone
    user.email = update_data.email

    db.commit()
    db.refresh(user)
    return {
        "message": "Perfil actualizado correctamente",
        "user_id": user.id
    }