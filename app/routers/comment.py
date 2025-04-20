from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from schemas.comment import CommentUpdate, CommentCreate, Comment
from crud import comment as crud_comment
from database import get_db
from auth.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=Comment)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return crud_comment.create_comment(db, comment, current_user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/event/{event_id}", response_model=List[Comment])
def get_comments_for_event(event_id: int, db: Session = Depends(get_db)):
    return crud_comment.get_comments_for_event(db, event_id)

@router.put("/{comment_id}", response_model=Comment)
def update_comment(
    comment_id: int,
    update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return crud_comment.update_comment(db, comment_id, update.content, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return crud_comment.delete_comment(db, comment_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.post("/{comment_id}/report")
def report_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return crud_comment.report_comment(db, comment_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
