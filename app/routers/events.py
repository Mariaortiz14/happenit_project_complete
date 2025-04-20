from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import get_db
from models.event import Event
from models.user import User
from schemas.event import EventCreate, EventResponse, EventUpdate
from schemas.user import UserResponse
from auth.auth import get_current_user
from datetime import datetime
from typing import List
from sqlalchemy import desc

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.post("/", response_model=EventResponse)
def create_event(
    user_id: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    event_date: datetime = Form(...),
    location: str = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db)
):
    if category not in ["gastronomía", "conferencias", "deportes", "festival", "conciertos", "teatros", "otro"]:
        raise HTTPException(status_code=400, detail="Categoría no válida")

    event = Event(
        user_id=user_id,
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        category=category
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("/", response_model=List[EventResponse])
def list_events(category: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    today = datetime.utcnow()
    query = db.query(Event).filter(Event.event_date >= today)

    if category:
        query = query.filter(Event.category.ilike(f"%{category}%"))

    return query.order_by(desc(Event.created_at)).offset(skip).limit(limit).all()

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    
    for key, value in event_data.dict(exclude_unset=True).items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event

from datetime import datetime

@router.get("/user/{user_id}", response_model=List[EventResponse])
def get_future_events_by_user(user_id: int, db: Session = Depends(get_db)):
    today = datetime.utcnow()
    events = (
        db.query(Event)
        .filter(Event.user_id == user_id, Event.event_date >= today)
        .order_by(desc(Event.created_at))
        .all()
    )
    return events


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    if event.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este evento")
    db.delete(event)
    db.commit()
    return {"message": "Evento eliminado correctamente"}
