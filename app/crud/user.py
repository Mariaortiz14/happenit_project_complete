from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
import bcrypt
from datetime import datetime

def create_user(db: Session, user_data: UserCreate) -> User:
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
    db_user = User(
        name=user_data.name,
        surname=user_data.surname,
        phone=user_data.phone,
        email=user_data.email,
        hashed_password=hashed_password.decode('utf-8'),
        created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()
