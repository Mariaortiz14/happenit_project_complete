from sqlalchemy.orm import Session
from models.event import Event
from schemas.event import EventCreate, EventUpdate
from datetime import datetime
from typing import List

def create_event(db: Session, event_data: EventCreate) -> Event:
    event = Event(
        user_id=event_data.user_id,
        title=event_data.title,
        description=event_data.description,
        event_date=event_data.event_date,
        location=event_data.location,
        category=event_data.category,
        created_at=datetime.utcnow()
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_event_by_id(db: Session, event_id: int) -> Event:
    return db.query(Event).filter(Event.id == event_id).first()

def get_all_events(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
    return db.query(Event).offset(skip).limit(limit).all()

def update_event(db: Session, db_event: Event, update_data: EventUpdate) -> Event:
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event: Event):
    db.delete(event)
    db.commit()
