from sqlalchemy.orm import Session, joinedload
from models.comment import Comment
from models.event import Event
from models.user import User
from schemas.comment import CommentCreate

def create_comment(db: Session, comment: CommentCreate, current_user: User):
    event = db.query(Event).filter(Event.id == comment.event_id).first()
    if not event:
        raise ValueError("Evento no encontrado.")
    if event.user_id == current_user.id:
        raise PermissionError("No puedes comentar tu propio evento.")

    db_comment = Comment(
        user_id=current_user.id,
        event_id=comment.event_id,
        content=comment.content
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_for_event(db: Session, event_id: int):
    return (
        db.query(Comment)
        .options(joinedload(Comment.user)) 
        .filter(Comment.event_id == event_id)
        .order_by(Comment.created_at.desc())
        .all()
    )

def update_comment(db: Session, comment_id: int, content: str, user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise ValueError("Comentario no encontrado")
    if comment.user_id != user_id:
        raise PermissionError("No puedes editar este comentario")
    comment.content = content
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int, user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise ValueError("Comentario no encontrado")
    if comment.user_id != user_id:
        raise PermissionError("No puedes eliminar este comentario")
    db.delete(comment)
    db.commit()
    return {"message": "Comentario eliminado correctamente"}

def report_comment(db: Session, comment_id: int, user_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise ValueError("Comentario no encontrado")
    if comment.user_id == user_id:
        raise PermissionError("No puedes reportar tu propio comentario")
    comment.reported = True
    db.commit()
    return {"message": "Comentario reportado"}
